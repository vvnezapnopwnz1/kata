import sys
import time
import threading
import logging
import numpy as np
import pyaudio
from faster_whisper import WhisperModel
import litellm
import argparse
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal, QObject
from pynput import keyboard
from src.interview_assistant.ui_overlay import OverlayWindow
from src.interview_assistant.audio_buffer import AudioRingBuffer
from src.interview_assistant.llm_pipeline import LLMPipeline

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# LiteLLM Configuration for Vertex AI
# Make sure to set your real GCP Project ID here!
litellm.vertex_project = "project-7d570aed-312f-4939-9a4" 
litellm.vertex_location = "global"

class SignalEmitter(QObject):
    update_ui = pyqtSignal(str, str)
    update_status = pyqtSignal(str)
    update_transcript = pyqtSignal(str)

class Controller:
    def __init__(self, args=None):
        self.args = args if args is not None else argparse.Namespace(
            backend="direct",
            project_id="project-7d570aed-312f-4939-9a4",
            location="eu",
            data_store_id="",
            app_id="289f0946-709f-4a80-b7ff-e863aace6bde",
            version_id="2abf9851-9b93-405d-8420-2f73931def9a",
            deployment_id="17540902-bba7-4693-b05d-52c77970c493",
            session_id="aAOXjF"
        )
        self.is_recording_context = False
        self.emitter = SignalEmitter()
        self.current_transcript = ""
        self.llm_pipeline = LLMPipeline(self.args)
        
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paFloat32
        self.RATE = 16000 # Whisper expects 16kHz
        
        self.p = pyaudio.PyAudio()
        self.stream_mic = None
        self.stream_sys = None
        self.sys_channels = 2
        
        self.ring_buffer = AudioRingBuffer(max_seconds=90, sample_rate=self.RATE, channels=2)
        self.is_listening_stream = False
        
        logger.info("Loading Whisper model (small)... This may take a few seconds.")
        # Load whisper on CPU (M1 handles this very well)
        try:
            # Try to load locally first to prevent hanging on internet handshake checks
            self.model = WhisperModel("small", device="cpu", compute_type="int8", local_files_only=True)
            logger.info("Whisper model loaded from local cache!")
        except Exception as e:
            logger.info(f"Could not load from local cache ({e}). Trying online load from Hugging Face...")
            self.model = WhisperModel("small", device="cpu", compute_type="int8", local_files_only=False)
            logger.info("Whisper model loaded successfully!")
        
        logger.debug("Controller initialized")

    def _find_devices(self):
        mic_index = None
        sys_index = None
        
        try:
            default_in = self.p.get_default_input_device_info()
            mic_index = default_in['index']
            logger.info(f"Default Mic found: {default_in['name']} (Index {mic_index})")
        except Exception as e:
            logger.error(f"Could not find default mic: {e}")

        for i in range(self.p.get_device_count()):
            info = self.p.get_device_info_by_index(i)
            if "BlackHole" in info.get("name", "") and info.get("maxInputChannels", 0) > 0:
                sys_index = i
                logger.info(f"System Audio (BlackHole) found: {info['name']} (Index {sys_index})")
                break
                
        return mic_index, sys_index

    def start_audio_stream(self):
        mic_index, sys_index = self._find_devices()
        
        try:
            if mic_index is not None:
                self.stream_mic = self.p.open(
                    format=self.FORMAT,
                    channels=1,
                    rate=self.RATE,
                    input=True,
                    input_device_index=mic_index,
                    frames_per_buffer=self.CHUNK
                )
                logger.info("Microphone stream started.")

            if sys_index is not None:
                # BlackHole is usually 2 channels
                ch = min(2, int(self.p.get_device_info_by_index(sys_index)['maxInputChannels']))
                self.stream_sys = self.p.open(
                    format=self.FORMAT,
                    channels=ch,
                    rate=self.RATE,
                    input=True,
                    input_device_index=sys_index,
                    frames_per_buffer=self.CHUNK
                )
                self.sys_channels = ch
                logger.info("System Audio (BlackHole) stream started.")
                
            self.is_listening_stream = True
            threading.Thread(target=self._record_loop, daemon=True).start()
            
        except Exception as e:
            logger.error(f"Failed to start PyAudio streams: {e}")
            self.emitter.update_transcript.emit(f"STT Error: {e}")

    def _record_loop(self):
        """Continuously reads audio from streams and saves Mic (channel 0) and System (channel 1) audio separately."""
        while self.is_listening_stream:
            try:
                mic_data = None
                sys_data = None
                
                # Read from Mic
                if self.stream_mic and self.stream_mic.is_active():
                    # exception_on_overflow=False prevents crashes if we process too slowly
                    raw_mic = self.stream_mic.read(self.CHUNK, exception_on_overflow=False)
                    mic_data = np.frombuffer(raw_mic, dtype=np.float32)
                
                # Ensure mic_data is valid float32 numpy array of length CHUNK
                if mic_data is None or len(mic_data) != self.CHUNK:
                    mic_data = np.zeros(self.CHUNK, dtype=np.float32)

                # Read from System (BlackHole)
                if self.stream_sys and self.stream_sys.is_active():
                    raw_sys = self.stream_sys.read(self.CHUNK, exception_on_overflow=False)
                    sys_data = np.frombuffer(raw_sys, dtype=np.float32)
                    if self.sys_channels > 1:
                        # Reshape and average down to mono
                        sys_data = sys_data.reshape(-1, self.sys_channels)
                        sys_data = np.mean(sys_data, axis=1)
                
                # Ensure sys_data is valid float32 numpy array of length CHUNK
                if sys_data is None or len(sys_data) != self.CHUNK:
                    sys_data = np.zeros(self.CHUNK, dtype=np.float32)

                # Combine into stereo/2-channel frame: Channel 0 = Mic, Channel 1 = System
                # Shape: (CHUNK, 2)
                chunk_2d = np.stack((mic_data, sys_data), axis=1)
                self.ring_buffer.append(chunk_2d)
                    
            except Exception as e:
                logger.error(f"Audio read error: {e}")
                time.sleep(0.01)

    def handle_start_context(self):
        logger.info("Triggered: START_CONTEXT")
        self.is_recording_context = True
        self.current_transcript = "" 
        self.ring_buffer.clear() # Clear the buffer to start fresh
        self.emitter.update_transcript.emit("Continuous listening started...")
        self.emitter.update_status.emit("Listening (N to process, M to clear)")

    def handle_trigger_answer(self):
        logger.info("Triggered: TRIGGER_ANSWER")
        self.is_recording_context = False
        self.emitter.update_status.emit("Transcribing and processing...")
        
        # Start transcription and LLM processing in a background thread
        threading.Thread(target=self._process_audio_and_generate, daemon=True).start()

    def handle_clear(self):
        logger.info("Triggered: CLEAR")
        self.is_recording_context = False
        self.ring_buffer.clear()
        self.current_transcript = ""
        self.emitter.update_transcript.emit("[Speech will appear here]")
        self.emitter.update_status.emit("Ready (Press B to start)")

    def _parse_incremental(self, text: str) -> tuple[str, str]:
        text_clean = text.lstrip()
        
        if "**Script:**" in text_clean:
            parts = text_clean.split("**Script:**", 1)
            tldr_part = parts[0].strip()
            script_part = parts[1].strip()
            
            if tldr_part.startswith("**TL;DR:**"):
                tldr_val = tldr_part[len("**TL;DR:**"):].strip()
            elif tldr_part.startswith("TL;DR:"):
                tldr_val = tldr_part[len("TL;DR:"):].strip()
            else:
                tldr_val = tldr_part.strip()
                
            tldr = f"**TL;DR:** {tldr_val}" if tldr_val else "**TL;DR:**"
            script = f"**Script:**\n{script_part}" if script_part else "**Script:**\n"
        else:
            tldr_part = text_clean
            if tldr_part.startswith("**TL;DR:**"):
                tldr_val = tldr_part[len("**TL;DR:**"):].strip()
            elif tldr_part.startswith("TL;DR:"):
                tldr_val = tldr_part[len("TL;DR:"):].strip()
            else:
                if tldr_part in ["*", "**", "**T", "**TL", "**TL;", "**TL;D", "**TL;DR", "**TL;DR:", "**TL;DR:*", "**TL;DR:**"]:
                    tldr_val = ""
                else:
                    tldr_val = tldr_part.strip()
                    
            tldr = f"**TL;DR:** {tldr_val}" if tldr_val else "**TL;DR:**"
            script = "Waiting for script..."
            
        return tldr, script

    def _diarize_and_merge(self, mic_audio: np.ndarray, sys_audio: np.ndarray) -> str:
        # Transcribe Mic (Candidate)
        mic_segments, _ = self.model.transcribe(mic_audio, beam_size=5, vad_filter=True)
        mic_seg_list = list(mic_segments)
        
        # Transcribe System (Interviewer)
        sys_segments, _ = self.model.transcribe(sys_audio, beam_size=5, vad_filter=True)
        sys_seg_list = list(sys_segments)
        
        # Merge and sort
        merged_dialogue = []
        for seg in mic_seg_list:
            merged_dialogue.append({
                'start': seg.start,
                'speaker': 'Candidate',
                'text': seg.text.strip()
            })
        for seg in sys_seg_list:
            merged_dialogue.append({
                'start': seg.start,
                'speaker': 'Interviewer',
                'text': seg.text.strip()
            })
            
        merged_dialogue.sort(key=lambda x: x['start'])
        
        # Format lines
        dialogue_lines = []
        for item in merged_dialogue:
            dialogue_lines.append(f"[{item['speaker']}]: {item['text']}")
            
        return "\n".join(dialogue_lines)

    def _process_audio_and_generate(self):
        # 1. Retrieve the last 60 seconds from the ring buffer
        logger.info("Retrieving last 60 seconds of audio...")
        audio_slice = self.ring_buffer.get_last_seconds(60)
        
        if len(audio_slice) == 0:
            self.emitter.update_transcript.emit("Error: No audio recorded.")
            self.emitter.update_status.emit("Ready")
            return
            
        mic_audio = audio_slice[:, 0]
        sys_audio = audio_slice[:, 1]
        
        # 2. Transcribe and diarize
        logger.info("Running Whisper transcription and diarization...")
        try:
            self.current_transcript = self._diarize_and_merge(mic_audio, sys_audio)
            logger.info(f"Diarized Transcript:\n{self.current_transcript}")
            
            if not self.current_transcript:
                self.emitter.update_transcript.emit("(Silence or unintelligible audio)")
                self.emitter.update_status.emit("Ready")
                return
            else:
                self.emitter.update_transcript.emit(self.current_transcript)
            
        except Exception as e:
            logger.error(f"Whisper transcription failed: {e}")
            self.emitter.update_transcript.emit("Error during transcription.")
            self.emitter.update_status.emit("Ready")
            return

        # 3. Send to LLM Pipeline (Direct, Search RAG, or Conversational Agent)
        self.emitter.update_status.emit("Generating response...")
        try:
            response_gen = self.llm_pipeline.generate_response(self.current_transcript)
            
            full_text = ""
            for chunk in response_gen:
                if chunk:
                    full_text += chunk
                    tldr, script = self._parse_incremental(full_text)
                    self.emitter.update_ui.emit(tldr, script)
            
            logger.info("Received LLM response.")
            self.emitter.update_status.emit("Done (Press M to clear)")
            
        except Exception as e:
            logger.error(f"LLM Generation failed: {e}")
            self.emitter.update_ui.emit("**TL;DR:** Error generating response.", f"**Script:** {str(e)}")
            self.emitter.update_status.emit("Error")

def main():
    parser = argparse.ArgumentParser(description="Go Technical Interview Assistant (Dual Stream Whisper mode)")
    parser.add_argument("--backend", type=str, choices=["direct", "search", "agent-builder", "dialogflow"], default="direct",
                        help="LLM backend: 'direct' Gemini completion, 'search' RAG data store search, 'agent-builder' playbook agent, or 'dialogflow' classic agent")
    parser.add_argument("--project-id", type=str, default="project-7d570aed-312f-4939-9a4",
                        help="Google Cloud Project ID")
    parser.add_argument("--location", type=str, default="eu",
                        help="Google Cloud Region/Location (e.g. eu, global)")
    parser.add_argument("--data-store-id", type=str, default="",
                        help="Discovery Engine Data Store ID (for Search-Grounded RAG)")
    parser.add_argument("--agent-id", type=str, default="",
                        help="Dialogflow CX Agent ID")
    parser.add_argument("--app-id", type=str, default="289f0946-709f-4a80-b7ff-e863aace6bde",
                        help="Agent Builder App ID")
    parser.add_argument("--version-id", type=str, default="2abf9851-9b93-405d-8420-2f73931def9a",
                        help="Agent Builder Playbook Version ID")
    parser.add_argument("--deployment-id", type=str, default="17540902-bba7-4693-b05d-52c77970c493",
                        help="Agent Builder Playbook Deployment ID")
    parser.add_argument("--session-id", type=str, default="aAOXjF",
                        help="Agent Builder Session ID")
    args, unknown = parser.parse_known_args()

    logger.info(f"Starting Interview Assistant App with backend: {args.backend}")
    app = QApplication(sys.argv)
    
    overlay = OverlayWindow()
    overlay.show()
    
    controller = Controller(args)
    controller.emitter.update_ui.connect(overlay.update_text)
    controller.emitter.update_status.connect(overlay.set_status)
    controller.emitter.update_transcript.connect(overlay.set_transcript)

    controller.start_audio_stream()

    def on_press(key):
        try:
            # Check for alphanumeric keys
            if hasattr(key, 'char'):
                k = key.char.lower()
                if k == 'b':
                    controller.handle_start_context()
                elif k == 'n':
                    controller.handle_trigger_answer()
                elif k == 'm':
                    controller.handle_clear()
            # Fallback for space bar
            elif key == keyboard.Key.space:
                controller.handle_start_context()
        except Exception as e:
            logger.error(f"Error in keyboard callback: {e}")

    # Start pynput listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    logger.info("Pynput listener started. Global hotkeys B, N, M active.")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
