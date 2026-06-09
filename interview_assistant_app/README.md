# Инструкция по использованию AI Interview Assistant

Этот инструмент помогает получать подсказки от ИИ в реальном времени во время интервью. Он слушает ваш голос и голос интервьюера, а затем выводит готовый сценарий ответа в прозрачное окно поверх всех окон.

## 1. Подготовка (Настройка звука)

Для работы на Mac вам понадобится **BlackHole** (виртуальный аудиокабель):

1.  Установите BlackHole (через `brew install blackhole-2ch`).
2.  Откройте программу **"Настройка Audio-MIDI"** (Audio MIDI Setup).
3.  Создайте **"Многовыходное устройство"** (Multi-Output Device).
4.  Отметьте галочками ваши наушники и **BlackHole 2ch**.
5.  В системных настройках звука выберите это новое устройство как "Выход". Теперь звук из Zoom/Meet будет идти и в уши, и в нашу программу.

## 2. Запуск ассистента

Убедитесь, что виртуальное окружение настроено, и выберите один из поддерживаемых бэкендов для работы. Ниже приведены подробные инструкции и команды для каждого режима.

---

### 🚀 Варианты запуска (Бэкенды)

Программа поддерживает 4 варианта работы с LLM. Выберите подходящий и запустите с соответствующими флагами:

#### 1. Стандартный Gemini (`--backend=direct`)
*   **Описание**: Прямой стриминговый запрос к модели `gemini-2.5-flash` через Vertex AI (посредством `litellm`).
*   **Тарификация**: Стандартная оплата за токены Vertex AI.
*   **Команда запуска**:
    ```bash
    PYTHONPATH=. .venv/bin/python src/interview_assistant/main.py \
      --backend=direct \
      --project-id="your-gcp-project-id" \
      --location="global"
    ```

#### 2. Поиск по базе знаний RAG (`--backend=search`)
*   **Описание**: Подключает Vertex AI Search (Gen App Builder) с поиском по вашему Data Store (резюме, шпаргалки, статьи). Сначала выполняется семантический поиск, после чего релевантный контекст передается в Gemini для формулирования ответа.
*   **Тарификация**: Оплата за поисковые запросы Vertex AI Search + токены LLM.
*   **Команда запуска**:
    ```bash
    PYTHONPATH=. .venv/bin/python src/interview_assistant/main.py \
      --backend=search \
      --project-id="your-gcp-project-id" \
      --location="global" \
      --data-store-id="your-data-store-id"
    ```

#### 3. Агент из CX Agent Studio (`--backend=agent-builder`)
*   **Описание**: Подключается к разговорному Playbook-агенту из CX Agent Studio (Vertex AI Agent Builder). Поддерживает потоковый вывод токенов в реальном времени через REST-метод `:streamRunSession`.
*   **Тарификация**: Сессионная тарификация Gen AI App Builder (покрывается грантом в $1000).
*   **Команда запуска**:
    ```bash
    PYTHONPATH=. .venv/bin/python src/interview_assistant/main.py \
      --backend=agent-builder \
      --project-id="your-gcp-project-id" \
      --location="eu" \
      --app-id="your-app-id" \
      --version-id="your-version-id" \
      --deployment-id="your-deployment-id" \
      --session-id="your-session-id"
    ```

#### 4. Классический агент Dialogflow CX (`--backend=dialogflow`)
*   **Описание**: Интеграция с классическим Dialogflow CX агентом через REST API-метод `detectIntent`.
*   **Тарификация**: Сессионная тарификация Dialogflow CX.
*   **Команда запуска**:
    ```bash
    PYTHONPATH=. .venv/bin/python src/interview_assistant/main.py \
      --backend=dialogflow \
      --project-id="your-gcp-project-id" \
      --location="eu" \
      --agent-id="your-agent-id" \
      --session-id="your-session-id"
    ```

---

## 3. Горячие клавиши (Hotkeys)

Во время интервью используйте следующие клавиши (фокус на окне приложения не требуется, клавиатурный слушатель глобальный):

*   **`B` или `Space` (Start Context):** Нажмите, когда интервьюер начал задавать вопрос. Очистит буфер и перейдет в режим прослушивания ("Listening...").
*   **`N` (Process & Answer):** Нажмите, когда вопрос закончен. ИИ получит диаризованную расшифровку (последние 60 секунд), отправит ее на выбранный бэкенд и выведет ответ.
*   **`M` (Clear):** Нажмите для очистки экрана и перевода окна в режим ожидания "Ready", если текущий ответ больше не нужен.

---

## 4. Формат подсказок

Окно оверлея состоит из двух основных секций:
1.  **TL;DR (желтым шрифтом):** Краткая суть ответа в одно-два предложения для быстрого ориентирования.
2.  **Script (белым шрифтом):** Готовый разговорный сценарий ответа.

---

## 5. Важные требования
*   **Авторизация GCP**: Перед запуском убедитесь, что вы вошли в ваш Google Cloud аккаунт в терминале:
    ```bash
    gcloud auth application-default login
    ```
*   **BlackHole на Mac**: Обязательно создайте многовыходное устройство (Multi-Output Device) в аудио-MIDI настройках Mac, чтобы звук шел и в наушники, и в BlackHole.

