# 🌉 Мост концепций: Из React/TypeScript в Go

Этот документ призван перевести сложные бэкенд-концепции Go на понятный язык фронтенд-разработчика, знающего React, JavaScript и TypeScript. Мы сопоставим ментальные модели обеих экосистем.

#react-to-go #mental-model #ts-vs-go #learning-path

---

## 🧭 Сводная таблица соответствий

| Концепция во фронтенде (JS/TS/React) | Эквивалент в Go (Golang)               | Суть и ключевое различие                                                                              |
| :----------------------------------- | :------------------------------------- | :---------------------------------------------------------------------------------------------------- |
| **`package.json`**                   | **`go.mod`**                           | Управление зависимостями проекта.                                                                     |
| **`npm install` / `pnpm`**           | **`go get` / `go mod tidy`**           | Загрузка и очистка неиспользуемых пакетов.                                                            |
| **Objects / Class instances**        | **`Structs` (Структуры)**              | Простые контейнеры для данных. В Go нет классов и наследования!                                       |
| **TypeScript Interfaces**            | **Go Interfaces**                      | В TS — структурная типизация, в Go — **неявная (implicit)** "утиная" типизация (duck typing).         |
| **`try {} catch (e) {}`**            | **`if err != nil` (Errors as values)** | В Go ошибки — это обычные возвращаемые значения, а не исключения.                                     |
| **`Promise` / `async/await`**        | **Goroutines + Channels**              | В JS один поток (Event Loop) имитирует асинхронность. В Go — истинная многопоточность (CSP модель).   |
| **`Array.prototype.map/filter`**     | **Циклы `for` (+ Generics с Go 1.18)** | В Go нет встроенных высокоуровневых функций для слайсов, пишем явные циклы (так быстрее!).            |
| **React State / Re-renders**         | **Stateless API / Struct state**       | В Go нет "реактивности". Состояние хранится в структурах бэкенда или в БД, данные передаются линейно. |

---

## 🕵️‍♂️ Детальный разбор концепций

### 1. Системы типов: TypeScript Interfaces vs Go Interfaces

В TypeScript интерфейсы описывают структуру объектов явно. Объект должен удовлетворять интерфейсу, или мы должны написать `implements`.
В Go интерфейсы реализуются **неявно** (implicit implementation). Если твоя структура имеет все методы, описанные в интерфейсе, она *автоматически* его реализует.

#### 📘 Сравнение на коде:

**TypeScript:**
```typescript
interface Greeter {
  greet(): string;
}

// Нужно явно указать соответствие (или полагаться на структурную совместимость TS)
class RussianGreeter implements Greeter {
  greet() { return "Привет!"; }
}
```

**Go:**
```go
package main

import "fmt"

// Описание интерфейса
type Greeter interface {
	Greet() string
}

// Обычная структура, никакого упоминания Greeter!
type RussianGreeter struct{}

// Метод для структуры RussianGreeter
func (r RussianGreeter) Greet() string {
	return "Привет!"
}

func SayHello(g Greeter) {
	fmt.Println(g.Greet())
}

func main() {
	rg := RussianGreeter{}
	SayHello(rg) // Работает! RussianGreeter неявно реализует Greeter
}
```

> [!important] В чём разница?
> В Go интерфейсы обычно очень маленькие (часто состоят из 1-2 методов: `io.Reader`, `io.Writer`). Это делает код невероятно гибким и модульным.

---

### 2. Асинхронность: Event Loop vs Модель CSP (Communicating Sequential Processes)

В браузере/Node.js работает **Event Loop** — один поток, который переключается между тасками с помощью коллбэков, промисов и генераторов (`async/await`).
В Go используется **многопоточная модель CSP**. Любая функция, вызванная со словом `go`, запускается в **горутине** (легковесном потоке, управляемом рантаймом Go).

#### 📘 Сравнение на коде:

**TypeScript (`Promise.all`):**
```typescript
async function fetchUserAndPosts() {
  const [user, posts] = await Promise.all([
    fetchUser(),
    fetchPosts()
  ]);
  return { user, posts };
}
```

**Go (с использованием `sync.WaitGroup` и каналов):**
```go
package main

import "sync"

func fetchUserData(wg *sync.WaitGroup, userChan chan<- User) {
	defer wg.Done()
	userChan <- fetchUser() // Пишем в канал
}

func fetchPostsData(wg *sync.WaitGroup, postsChan chan<- []Post) {
	defer wg.Done()
	postsChan <- fetchPosts() // Пишем в канал
}

func FetchAll() (User, []Post) {
	var wg sync.WaitGroup
	userChan := make(chan User, 1)
	postsChan := make(chan []Post, 1)

	wg.Add(2)
	go fetchUserData(&wg, userChan)  // Запуск в горутине 1
	go fetchPostsData(&wg, postsChan) // Запуск в горутине 2

	wg.Wait() // Ждем выполнения обеих горутин
	
	return <-userChan, <-postsChan
}
```

> [!note] Различие ментальных моделей
> В JS асинхронность нужна, чтобы *не блокировать* единственный поток рендеринга.
> В Go параллелизм используется для *максимальной утилизации ядер процессора*. Каналы (`channels`) — это трубы, по которым горутины обмениваются данными безопасно.

---

### 3. Обработка ошибок: Исключения vs Возвращаемые значения

В JS/TS при ошибке мы выбрасываем исключение (`throw new Error()`) и ловим его где-то выше по стеку в `try/catch`. Если забыли поймать — приложение падает (или происходит unhandled rejection).
В Go ошибки — это **обычные значения** (`error` интерфейс), которые функция возвращает последним аргументом. Ты обязан проверить ошибку сразу.

#### 📘 Сравнение на коде:

**TypeScript:**
```typescript
try {
  const data = JSON.parse(rawJson);
} catch (err) {
  console.error("Не удалось распарсить JSON", err);
}
```

**Go:**
```go
import "encoding/json"

var data User
err := json.Unmarshal([]byte(rawJson), &data)
if err != nil {
    // Явная обработка ошибки прямо на месте
    log.Printf("Не удалось распарсить JSON: %v", err)
    return err
}
```

> [!warning] Мышление Go-разработчика
> Поначалу обилие конструкций `if err != nil` кажется уродливым фронтендеру, привыкшему к красивым цепочкам. Однако это делает поток выполнения программы на 100% прозрачным. Ты всегда видишь, где именно может произойти сбой, и как он обрабатывается.

---

### 4. Мутабельность: Ссылки (References) vs Указатели (Pointers)

В JS объекты и массивы передаются по ссылке, а примитивы — по значению. В React мы боремся с мутабельностью с помощью концепции *immutability* (копирование через `...spread` оператор, использование Immer), чтобы React понимал, когда делать ререндер.
В Go всё передается **по значению** (копируется), если только ты явно не передаешь **указатель** (`*type`).

#### 📘 Сравнение на коде:

**TypeScript (React State Immutability):**
```typescript
// Чтобы обновить состояние, мы создаем новый объект
setUser(prevUser => ({
  ...prevUser,
  age: prevUser.age + 1
}));
```

**Go (Указатели):**
```go
type User struct {
	Name string
	Age  int
}

// Функция принимает копию (передача по значению)
func UpdateAgeValue(u User) {
	u.Age += 1 // Изменит только локальную копию!
}

// Функция принимает указатель (ссылку на память)
func UpdateAgePointer(u *User) {
	u.Age += 1 // Изменит оригинальный объект!
}
```

---

## 💡 Топ-3 совета для быстрого старта

1. **Забудь про функциональный оверхед JS.** В Go нет встроенного `.map()`, `.filter()` или `.reduce()`. Не пытайся тащить сторонние библиотеки для этого. Пиши обычный цикл `for` — он работает молниеносно и читается всеми Go-разработчиками одинаково.
2. **Перестань бояться указателей.** Указатель в Go — это просто адрес переменной в памяти. Используй его, когда хочешь мутировать структуру (изменить данные внутри функции) или передать большую структуру без копирования.
3. **Думай о потоках данных, а не о UI.** В React мы думаем о "состоянии и его отрисовке". В Go думай о "входном http-запросе, его валидации, обработке в бизнес-логике, сохранении в БД и возврате ответа". Архитектура Go линейна и предсказуема.
