import time
import io
import os
from PIL import ImageGrab, Image
import google.generativeai as genai

# Настройка API ключа (лучше задать через переменную окружения)
API_KEY = os.environ.get("GEMINI_API_KEY", "ВАШ_GEMINI_API_KEY")
if API_KEY == "ВАШ_GEMINI_API_KEY":
    print("[WARNING] Не забудьте указать настоящий API-ключ Gemini!")

genai.configure(api_key=API_KEY)
# Используем скоростную и точную мультимодальную модель
model = genai.GenerativeModel('gemini-2.5-flash')

def get_clipboard_image():
    """Извлекает изображение из буфера обмена, если оно там есть."""
    try:
        im = ImageGrab.grabclipboard()
        if isinstance(im, Image.Image):
            return im
    except Exception as e:
        pass
    return None

def main():
    print("="*60)
    print("ИИ-Ассистент (Vision Clipboard) запущен.")
    print("Инструкция:")
    print("1. Сделайте скриншот области экрана в БУФЕР ОБМЕНА:")
    print("   - macOS:  Cmd + Shift + Ctrl + 4")
    print("   - Windows: Win + Shift + S")
    print("2. Скрипт автоматически распознает задачу и выдаст Go-код.")
    print("="*60)
    
    last_img_hash = None
    
    while True:
        try:
            img = get_clipboard_image()
            if img is not None:
                # Генерируем простой хэш картинки, чтобы не обрабатывать один и тот же скриншот по кругу
                img_hash = hash(img.tobytes()[:10000])
                
                if img_hash != last_img_hash:
                    last_img_hash = img_hash
                    print(f"\n[{time.strftime('%H:%M:%S')}] 📸 Обнаружен новый скриншот в буфере! Отправка в Gemini...")
                    
                    # Конвертируем изображение в байты для API
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='PNG')
                    img_bytes = img_byte_arr.getvalue()
                    
                    # Промпт, оптимизированный под Go-собеседования
                    prompt = """
                    Ты - Senior Go-разработчик, помогающий кандидату на техническом интервью.
                    Проанализируй изображение задачи и выдай строго структурированный ответ:
                    
                    1. **Идея (1-2 предложения):** Какая структура данных или алгоритм оптимальны (например, sliding window, hash-map, mutex для thread-safety).
                    2. **Сложность:** Временная O(...) и пространственная O(...) сложности.
                    3. **Решение на Go:** Напиши чистый, оптимизированный, идиоматичный Go-код. Используй современные фичи языка (если применимо). Избегай лишних импортов. Обрабатывай ошибки!
                    4. **Шпаргалка (3 коротких буллита):** О чем важно сказать устно при защите этого решения (например: "используем make для преаллокации слайса", "закрываем канал в defer").
                    
                    Пиши максимально кратко, структурировано, без лишнего вводного текста. Только суть.
                    """
                    
                    # Формируем контент для API
                    contents = [
                        prompt,
                        {"mime_type": "image/png", "data": img_bytes}
                    ]
                    
                    start_time = time.time()
                    response = model.generate_content(contents)
                    elapsed = time.time() - start_time
                    
                    print("\n" + "🔥" * 20 + f" РЕШЕНИЕ ИИ (За {elapsed:.1f} сек) " + "🔥" * 20)
                    print(response.text)
                    print("="*90 + "\n")
                    
            time.sleep(0.8)
        except KeyboardInterrupt:
            print("\nСкрипт остановлен.")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
