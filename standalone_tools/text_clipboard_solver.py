import time
import os
import pyperclip
import google.generativeai as genai

# Настройка API ключа (лучше задать через переменную окружения)
API_KEY = os.environ.get("GEMINI_API_KEY", "ВАШ_GEMINI_API_KEY")
if API_KEY == "ВАШ_GEMINI_API_KEY":
    print("[WARNING] Не забудьте указать настоящий API-ключ Gemini!")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def main():
    print("="*60)
    print("ИИ-Ассистент (Text Clipboard) запущен.")
    print("Просто копируйте текст задачи (Ctrl+C / Cmd+C).")
    print("Скрипт автоматически применит Go-контекст и выдаст решение.")
    print("="*60)
    
    last_text = ""
    
    while True:
        try:
            text = pyperclip.paste().strip()
            # Обрабатываем только если текст изменился и он длиннее 25 символов (чтобы исключить мелкие копирования)
            if text and text != last_text and len(text) > 25:
                last_text = text
                print(f"\n[{time.strftime('%H:%M:%S')}] 📝 Скопирован новый текст ({len(text)} симв.). Запрос к ИИ...")
                
                prompt = f"""
                Ты - эксперт по Go. Реши следующую задачу по программированию.
                Дай чистый, идиоматичный и компилируемый Go-код. 
                Укажи временную/пространственную сложность. 
                Дай 3 коротких тезиса для устного объяснения.
                
                Задача:
                {text}
                """
                
                start_time = time.time()
                response = model.generate_content(prompt)
                elapsed = time.time() - start_time
                
                print("\n" + "🚀" * 20 + f" РЕШЕНИЕ ИИ ({elapsed:.1f} сек) " + "🚀" * 20)
                print(response.text)
                print("="*90 + "\n")
                
            time.sleep(0.5)
        except KeyboardInterrupt:
            print("\nСкрипт остановлен.")
            break
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
