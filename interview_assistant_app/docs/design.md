# Real-time AI Interview Assistant - Design Specification

## Overview
This document outlines the design for a real-time AI assistant that acts as an invisible teleprompter during online interviews. It captures audio from both the interviewer and the user, processes the question when triggered by hotkeys, and displays a conversational response in a transparent, always-on-top window on the user's primary monitor.

## 1. Architecture & Components

The system is composed of three main logical components running in a unified Python environment.

### 1.1 Audio Capture & Control
*   **Audio Routing:** Requires a virtual audio cable (e.g., BlackHole on macOS). The system's output (Zoom/Meet audio) is routed to a Multi-Output Device (sending audio to both headphones and the virtual cable).
*   **Dual-Stream Capture:** A Python script continuously captures audio from two sources:
    1.  Virtual Audio Cable (Interviewer's voice).
    2.  System Microphone (User's voice).
*   **Ring Buffer:** Audio is stored in a continuous ring buffer (e.g., keeping the last 2-3 minutes) to minimize memory usage while ensuring context is always available.
*   **Hotkey Controls:**
    *   **Hotkey 1 (Start Context):** Marks the beginning of an important segment (e.g., the interviewer starts asking a question).
    *   **Hotkey 2 (Trigger Answer):** Slices the audio buffer from the start marker to the current time and initiates the processing pipeline.

### 1.2 Processing & LLM Pipeline
*   **Primary Provider:** Google Cloud Vertex AI (via `gcloud` authentication) utilizing the latest available Gemini models (e.g., Gemini 2.5 Pro/Flash, 3.1, or 3.5), or LiteLLM wrapper, to accommodate the user's subscription constraints without requiring direct API keys.
*   **Speech-to-Text (STT):** The sliced audio segment is transcribed into text quickly. (Native audio understanding capabilities of the latest Gemini models may also be explored to bypass a separate STT step if latency permits).
*   **LLM Generation:** The transcribed text (or direct audio) is sent to the LLM with a strict system prompt.
*   **Output Format:** The LLM is instructed to generate a two-part response:
    *   **TL;DR:** A single, concise sentence summarizing the core answer.
    *   **Script:** A conversational, first-person response ("I would approach this by...", "The main difference is...") designed to be read aloud naturally.
    *   *(Optional)* Bullet points for technical depth if the topic is broad.

### 1.3 User Interface (HUD / Overlay)
*   **Framework:** Python + PyQt6 (or PySide6).
*   **Window Properties:**
    *   Frameless (`FramelessWindowHint`).
    *   Always on Top (`WindowStaysOnTopHint`).
    *   Semi-transparent background to remain unobtrusive.
    *   Fixed positioning (e.g., top center, near the webcam).
*   **UI States:**
    *   **Idle:** Subtle status indicator (e.g., green for ready, red for context recording).
    *   **Processing:** Spinner or visual indicator when Hotkey 2 is pressed and API requests are in flight.
    *   **Display:** High-contrast text presentation. The TL;DR and the Script sections will be visually distinct (e.g., different colors or font weights) for quick scanning.
*   **Clear Action:** The text remains on screen until a "Clear" hotkey is pressed or Hotkey 1 is pressed again to start a new capture.

## 2. Future Considerations
*   **Automated Triggering:** Implementing a background process (using VAD - Voice Activity Detection or a lightweight local model) to automatically detect questions based on pauses or speech patterns, reducing the need for manual hotkeys.
*   **Vision Integration:** Adding a workflow (discussed for a future session) to quickly capture screen regions (e.g., for live coding tasks) and send them to a separate specialized agent.

## 3. Technology Stack Summary
*   **Language:** Python
*   **UI:** PyQt6 / PySide6
*   **Audio:** PyAudio / SoundDevice + BlackHole (macOS)
*   **AI Provider:** Google Cloud Vertex AI (Gemini) / LiteLLM
*   **Keyboard Hooks:** `keyboard` or `pynput` library
