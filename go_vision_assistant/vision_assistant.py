import os
import io
import time
import sys
import threading
import mss
from PIL import Image
from pynput import keyboard
import google.generativeai as genai

# =====================================================================
# КОНФИГУРАЦИЯ И КЛЮЧИ API
# =====================================================================
# Вставьте ваш API-ключ Gemini сюда или установите переменную окружения GEMINI_API_KEY
GEMINI_API_KEY = "ВАШ_GEMINI_API_KEY"

# Приоритет отдается переменной окружения
api_key = os.environ.get("GEMINI_API_KEY", GEMINI_API_KEY)

# Настройка клиента Gemini API
if api_key == "ВАШ_GEMINI_API_KEY":
    print("⚠️ [WARNING] У вас не задан API-ключ в константе GEMINI_API_KEY!")
    print("⚠️ Пожалуйста, замените плейсхолдер или запустите скрипт с переменной окружения GEMINI_API_KEY.")
else:
    genai.configure(api_key=api_key)

# =====================================================================
# ШАБЛОН HTML ИНТЕРФЕЙСА ВЫВОДА
# =====================================================================
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Go Interview Vision Co-Pilot</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/go.min.js"></script>
    <style>
        :root {
            --bg-color: #0f0f11;
            --panel-bg: #1a1a1e;
            --border-color: #2c2c35;
            --text-main: #e2e8f0;
            --text-muted: #94a3b8;
            --accent-green: #10b981;
            --accent-blue: #3b82f6;
            --accent-purple: #8b5cf6;
            --accent-orange: #f59e0b;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            padding: 30px;
            font-size: 24px;
            line-height: 1.6;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 20px;
            margin-bottom: 30px;
        }

        h1 {
            font-size: 32px;
            font-weight: 700;
            color: var(--accent-green);
        }

        .status-container {
            display: flex;
            gap: 15px;
            align-items: center;
        }

        .badge {
            padding: 8px 16px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 18px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: flex;
            align-items: center;
            gap: 8px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .status-idle {
            background-color: #1e1e24;
            color: var(--text-muted);
        }

        .status-pending {
            background-color: rgba(245, 158, 11, 0.15);
            color: var(--accent-orange);
            border-color: rgba(245, 158, 11, 0.3);
            animation: pulse 1.5s infinite alternate;
        }

        .status-success {
            background-color: rgba(16, 185, 129, 0.15);
            color: var(--accent-green);
            border-color: rgba(16, 185, 129, 0.3);
        }

        .queue-badge {
            background-color: rgba(59, 130, 246, 0.15);
            color: var(--accent-blue);
            border-color: rgba(59, 130, 246, 0.3);
        }

        @keyframes pulse {
            0% { opacity: 0.6; }
            100% { opacity: 1; }
        }

        main {
            background-color: var(--panel-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 35px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            min-height: 500px;
        }

        /* Стили для Маркдауна */
        #output h1, #output h2, #output h3 {
            color: var(--accent-green);
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            font-weight: 700;
        }
        #output h1 { font-size: 34px; border-bottom: 1px solid var(--border-color); padding-bottom: 8px; }
        #output h2 { font-size: 30px; }
        #output h3 { font-size: 26px; }

        #output p {
            margin-bottom: 1.2em;
        }

        #output ul, #output ol {
            margin-bottom: 1.2em;
            padding-left: 30px;
        }

        #output li {
            margin-bottom: 8px;
        }

        #output pre {
            background-color: #0b0b0d;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            overflow-x: auto;
            margin: 1.5em 0;
        }

        #output code {
            font-family: 'JetBrains Mono', monospace;
            font-size: 20px;
            background-color: #0b0b0d;
            padding: 2px 6px;
            border-radius: 4px;
        }

        #output pre code {
            padding: 0;
            background-color: transparent;
            font-size: 20px;
        }

        /* Переопределение стилей подсветки highlight.js */
        .hljs {
            background: transparent !important;
        }

        /* Индикатор автообновления */
        .refresh-indicator {
            position: fixed;
            bottom: 15px;
            right: 15px;
            font-size: 14px;
            color: var(--text-muted);
            opacity: 0.5;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .refresh-dot {
            width: 8px;
            height: 8px;
            background-color: var(--accent-green);
            border-radius: 50%;
            display: inline-block;
            animation: blink 2s infinite;
        }
        @keyframes blink {
            0%, 100% { opacity: 0.2; }
            50% { opacity: 1; }
        }
    </style>
</head>
<body>
    <header>
        <h1>🐹 Go Vision Co-Pilot</h1>
        <div class="status-container">
            <div class="badge queue-badge">📸 Скриншотов в очереди: {{queue_size}}</div>
            <div class="badge {{status_class}}">{{status_text}}</div>
        </div>
    </header>

    <main>
        <textarea id="raw-markdown" style="display: none;">{{raw_markdown}}</textarea>
        <div id="output">Загрузка контента...</div>
    </main>

    <div class="refresh-indicator">
        <span class="refresh-dot"></span>
        Автообновление страницы каждые 2с
    </div>

    <script>
        const rawMarkdown = document.getElementById('raw-markdown').value;
        if (rawMarkdown.trim()) {
            document.getElementById('output').innerHTML = marked.parse(rawMarkdown);
            hljs.highlightAll();
        } else {
            document.getElementById('output').innerHTML = '<p style="color: var(--text-muted); text-align: center; margin-top: 150px;">Ожидание первого запроса... Нажмите <b>Cmd + Alt + 1</b> чтобы добавить скриншот, и <b>Cmd + Alt + 2</b> для отправки.</p>';
        }

        // Автоматическая перезагрузка страницы
        setTimeout(() => {
            location.reload();
        }, 2000);
    </script>
</body>
</html>
"""

# =====================================================================
# СОСТОЯНИЕ АССИСТЕНТА
# =====================================================================
class AssistantState:
    def __init__(self):
        self.lock = threading.Lock()
        self.buffer = []
        self.status_text = "Ожидание"
        self.status_class = "status-idle"
        self.last_response = ""
        self.desktop_path = os.path.expanduser('~/Desktop/go_assistant.html')

state = AssistantState()

# =====================================================================
# ОБНОВЛЕНИЕ HTML ФАЙЛА
# =====================================================================
def update_html(state_obj):
    raw_md = state_obj.last_response.replace('</textarea>', '&lt;/textarea&gt;')
    
    html_content = (HTML_TEMPLATE
                    .replace('{{queue_size}}', str(len(state_obj.buffer)))
                    .replace('{{status_text}}', state_obj.status_text)
                    .replace('{{status_class}}', state_obj.status_class)
                    .replace('{{raw_markdown}}', raw_md))
    
    try:
        with open(state_obj.desktop_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    except Exception as e:
        print(f"❌ [{time.strftime('%H:%M:%S')}] Не удалось обновить HTML файл на Рабочем столе: {e}")

# =====================================================================
# ОБРАБОТЧИКИ ХОТКЕЕВ
# =====================================================================
def take_screenshot():
    with state.lock:
        try:
            with mss.mss() as sct:
                # Берем основной монитор (1-й в списке, так как 0-й — это объединенный холст)
                monitor = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
                sct_img = sct.grab(monitor)
                
                # Конвертируем снимок экрана в Pillow Image напрямую в памяти
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                state.buffer.append(img)
                
                state.status_text = "Скриншот добавлен"
                state.status_class = "status-success"
                
            print(f"📸 [{time.strftime('%H:%M:%S')}] Скриншот добавлен в буфер. Всего снимков: {len(state.buffer)}")
            update_html(state)
        except Exception as e:
            print(f"❌ [{time.strftime('%H:%M:%S')}] Ошибка при захвате экрана: {e}")

def trigger_api_call():
    with state.lock:
        if not state.buffer:
            print("⚠️ [{time.strftime('%H:%M:%S')}] Буфер пуст! Нечего отправлять.")
            state.status_text = "Буфер пуст"
            state.status_class = "status-idle"
            update_html(state)
            return
        
        # Меняем статус на "Gemini думает..."
        state.status_text = "Gemini думает..."
        state.status_class = "status-pending"
        update_html(state)
        
    # Запуск API-запроса в фоновом потоке, чтобы не блокировать поток клавиатурного хука
    threading.Thread(target=gemini_worker, daemon=True).start()

def clear_buffer():
    with state.lock:
        state.buffer.clear()
        state.status_text = "Буфер очищен"
        state.status_class = "status-idle"
        update_html(state)
    print(f"🧹 [{time.strftime('%H:%M:%S')}] Буфер скриншотов успешно очищен.")

# =====================================================================
# ФОНОВЫЙ ПОТОК ЗАПРОСОВ К GEMINI
# =====================================================================
def gemini_worker():
    # Проверка ключа
    global api_key
    if api_key == "ВАШ_GEMINI_API_KEY":
        with state.lock:
            state.status_text = "Ошибка API"
            state.status_class = "status-pending"
            state.last_response = "### ❌ Ошибка выполнения запроса\n\nНе задан рабочий **GEMINI_API_KEY**. Пожалуйста, пропишите его в коде скрипта или передайте через переменную окружения."
            update_html(state)
        print("❌ [{time.strftime('%H:%M:%S')}] Ошибка: API ключ не сконфигурирован.")
        return

    print(f"🌀 [{time.strftime('%H:%M:%S')}] Запуск запроса к Gemini API...")
    start_time = time.time()
    
    # Забираем изображения из буфера и очищаем его
    with state.lock:
        images_to_send = list(state.buffer)
        state.buffer.clear()
        
    contents = []
    
    # Добавляем текстовый промпт
    prompt = "Проанализируй скриншоты и реши задачу."
    contents.append(prompt)
    
    # Форматируем картинки в байты для отправки
    for img in images_to_send:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        contents.append({
            "mime_type": "image/png",
            "data": img_byte_arr.getvalue()
        })
        
    try:
        # Инициализируем модель с жестко заданным System Prompt
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=(
                "Ты — Senior Go Developer. Перед тобой скриншот(ы) задачи по лайвкодингу. "
                "Анализируй их как единое целое. Выдай ответ СТРОГО в формате: "
                "1. Сложность (Time/Space). "
                "2. Оптимальное решение на Go (чистый, идиоматичный код). "
                "3. Построчный разбор 2-3 ключевых строк (память, escape-анализ, конкурентность). "
                "Пиши крупно, лаконично, без приветствий и воды."
            )
        )
        
        # Запрос к API
        response = model.generate_content(contents)
        elapsed = time.time() - start_time
        
        with state.lock:
            state.last_response = response.text
            state.status_text = f"Ответ за {elapsed:.2f} с"
            state.status_class = "status-success"
            update_html(state)
            
        print(f"✅ [{time.strftime('%H:%M:%S')}] Успешный ответ от Gemini за {elapsed:.2f} сек!")
        
    except Exception as e:
        elapsed = time.time() - start_time
        error_msg = str(e)
        
        with state.lock:
            state.status_text = "Ошибка API"
            state.status_class = "status-pending"
            state.last_response = f"### ❌ Ошибка выполнения запроса\n\n```\n{error_msg}\n```\n\nПроверьте API-ключ, подключение к сети или лимиты тарифа."
            update_html(state)
            
        print(f"❌ [{time.strftime('%H:%M:%S')}] Ошибка API за {elapsed:.2f} сек: {e}")

# =====================================================================
# ТОЧКА ВХОДА И ЗАПУСК
# =====================================================================
def main():
    print("=" * 60)
    print("🐹 Go Vision Co-Pilot Assistant запущен!")
    print(f"📂 Вывод записывается в: {state.desktop_path}")
    print("=" * 60)
    print("Управление глобальными хоткеями:")
    print("  • Cmd + Alt + 1 : Захватить экран и добавить в буфер")
    print("  • Cmd + Alt + 2 : Отправить буфер скриншотов в Gemini API")
    print("  • Cmd + Alt + 3 : Очистить буфер без отправки в API")
    print("=" * 60)
    print("💡 Убедитесь, что вашему терминалу выданы права на Screen Recording!")
    print("💡 Для выхода нажмите Ctrl + C в терминале.")
    print("-" * 60)

    # Инициализация HTML при старте
    update_html(state)

    # Регистрируем глобальные хоткеи
    # На macOS Cmd транслируется в <cmd>, Option/Alt транслируется в <alt>
    hotkey_map = {
        '<cmd>+<alt>+1': take_screenshot,
        '<cmd>+<alt>+2': trigger_api_call,
        '<cmd>+<alt>+3': clear_buffer
    }
    
    try:
        with keyboard.GlobalHotKeys(hotkey_map) as listener:
            # Бесконечный цикл ожидания событий
            listener.join()
    except KeyboardInterrupt:
        print("\n👋 Скрипт остановлен пользователем.")
    except Exception as e:
        print(f"\n❌ Критическая ошибка при работе хуков: {e}")
        print("Подсказка: возможно, терминалу не хватает прав Accessibility.")

if __name__ == "__main__":
    main()
