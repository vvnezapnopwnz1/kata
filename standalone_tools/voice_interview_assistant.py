import sys
import queue
import threading
import os
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import google.generativeai as genai
from pynput import keyboard

# Инициализация LLM
API_KEY = os.environ.get("GEMINI_API_KEY", "ВАШ_GEMINI_API_KEY")
if API_KEY == "ВАШ_GEMINI_API_KEY":
    print("[ВНИМАНИЕ] Не забудьте установить переменную окружения GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
llm_model = genai.GenerativeModel('gemini-2.5-flash')

# Инициализация Whisper
print("Загрузка локальной Whisper модели 'base' (около 140MB)...")
whisper_model = WhisperModel("base", device="cpu", compute_type="int8")

audio_queue = queue.Queue()
transcript_buffer = []
buffer_lock = threading.Lock()

def audio_callback(indata, frames, time, status):
    """Callback-функция для захвата аудиопотока."""
    if status:
        print(f"Audio status: {status}", file=sys.stderr)
    
    # indata имеет форму (frames, channels). 
    # Так как мы можем захватывать объединенное устройство (Mic + BlackHole), 
    # каналов может быть несколько. Мы микшируем их в моно (один канал), 
    # усредняя значения по всем каналам, чтобы Whisper слышал и тебя, и интервьюера.
    if indata.shape[1] > 1:
        mono_data = np.mean(indata, axis=1, keepdims=True)
    else:
        mono_data = indata
        
    audio_queue.put(mono_data.copy())

def transcription_worker():
    """Фоновый поток для непрерывного распознавания речи."""
    samplerate = 16000
    chunk_duration = 3  # Распознаем аудио блоками по 3 секунды для меньшей задержки
    chunk_samples = samplerate * chunk_duration
    audio_buffer = np.zeros((0, 1), dtype=np.float32)
    
    print("Голосовой захват запущен. Начните говорить (микрофон + системный звук)...")
    
    while True:
        data = audio_queue.get()
        audio_buffer = np.append(audio_buffer, data, axis=0)
        
        if len(audio_buffer) >= chunk_samples:
            process_data = audio_buffer[:chunk_samples]
            audio_buffer = audio_buffer[chunk_samples:]
            
            # Конвертируем в формат для Whisper (1D float32)
            audio_data = process_data.flatten()
            
            # Запускаем локальную транскрипцию
            segments, info = whisper_model.transcribe(audio_data, beam_size=3, language="ru")
            
            text = " ".join([segment.text for segment in segments]).strip()
            if text:
                with buffer_lock:
                    transcript_buffer.append(text)
                    # Храним историю последних ~2 минут разговора
                    if len(transcript_buffer) > 30:
                        transcript_buffer.pop(0)
                print(f"[Live-STT]: {text}")

def get_answer_from_llm():
    """Отправляет накопленный лог разговора в LLM для генерации подсказки."""
    with buffer_lock:
        context = " ".join(transcript_buffer).strip()
        
    if not context:
        print("\n[ИИ] Буфер транскрипции пуст. Нечего анализировать.")
        return
        
    print("\n" + "🌀" * 10 + " АНАЛИЗ ДИАЛОГА " + "🌀" * 10)
    
    prompt = f"""
    Ты - ассистент на техническом интервью по Go. Перед тобой транскрипт текущего разговора (он включает и реплики кандидата, и вопросы интервьюера).
    Проанализируй контекст, найди последний сложный технический вопрос, на который сейчас нужно ответить кандидату, и дай лаконичный технический ответ.
    
    Формат ответа:
    1. **Суть ответа:** (1-2 предложения)
    2. **Краткие тезисы (для устного ответа):** 3-4 буллита с ключевыми терминами Go (GMP, каналы, семантика указателей и т.д.).
    3. **Пример (если уместно):** 2-5 строчек идиоматичного кода.
    
    Транскрипт разговора:
    {context}
    """
    
    try:
        response = llm_model.generate_content(prompt)
        print("\n" + "💡" * 15 + " ШПАРГАЛКА ИИ " + "💡" * 15)
        print(response.text)
        print("="*60 + "\n")
    except Exception as e:
        print(f"Ошибка вызова LLM: {e}")

def on_activate_hotkey():
    get_answer_from_llm()

def print_devices():
    print("\nДоступные аудиоустройства (входы):")
    devices = sd.query_devices()
    for idx, dev in enumerate(devices):
        if dev['max_input_channels'] > 0:
            print(f"Индекс [{idx}]: {dev['name']} (Каналов: {dev['max_input_channels']})")

if __name__ == "__main__":
    print_devices()
    print("\nДля захвата и себя, и интервьюера, укажите индекс вашего 'Объединенного устройства' (Aggregate Device).")
    try:
        idx_input = input("Введите индекс устройства (или нажмите Enter для дефолтного): ")
        device_idx = int(idx_input) if idx_input.strip() else None
    except ValueError:
        print("Используется устройство по умолчанию.")
        device_idx = None
        
    # Получаем кол-во каналов выбранного устройства, чтобы читать их все
    device_info = sd.query_devices(device_idx, 'input')
    channels = device_info['max_input_channels']
    print(f"Запуск потока с устройства '{device_info['name']}' (Каналов: {channels})...")
    
    stream = sd.InputStream(
        device=device_idx,
        channels=channels,
        samplerate=16000,
        callback=audio_callback
    )
    
    # Запуск фонового транскрибатора
    threading.Thread(target=transcription_worker, daemon=True).start()
    
    print("\n>>> Нажмите Ctrl+Option+A (или Ctrl+Alt+A) для вызова ИИ по текущему логу... <<<")
    print(">>> Нажмите Ctrl+C в консоли для выхода. <<<")
    
    try:
        with stream:
            # pynput корректнее работает с глобальными хоткеями на macOS без прав root
            with keyboard.GlobalHotKeys({'<ctrl>+<alt>+a': on_activate_hotkey}) as h:
                h.join()
    except KeyboardInterrupt:
        print("\nЗавершение работы...")
        sys.exit(0)
