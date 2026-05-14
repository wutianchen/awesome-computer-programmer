# Callback

A **callback** is a function you hand to another piece of code and say *"call this back when something happens."* You pass the function itself (not its result) as a value, and the receiver invokes it later.

## The shape

```js
function greet(name, onDone) {
  console.log("Hi", name);
  onDone();              // ← the callback fires here
}

greet("Alex", () => console.log("greeting finished"));
```

You didn't *call* `onDone` — you handed it to `greet`, which decided when to invoke it.

## Two main uses

### 1. Inversion of control (sync)

Let the caller customize a generic algorithm without rewriting it. Classic: passing a comparator to sort.

```js
[3, 1, 2].sort((a, b) => a - b);   // the lambda is a callback
```

### 2. Async notification

Resume work when a slow operation finishes — disk I/O, network, timers.

```js
setTimeout(() => console.log("1 second later"), 1000);

fs.readFile("data.txt", (err, contents) => { /* ... */ });
```

## Why "callback" and not just "function argument"?

Any function passed as an argument *is* technically a callback. But the term emphasizes the **temporal / control inversion**: you're not asking for an immediate result — you're registering interest in a future event. The receiver controls *when* and *whether* it runs.

## Callback hell and what replaced it

Chaining async callbacks gets ugly:

```js
readUser(id, (err, user) => {
  readPosts(user, (err, posts) => {
    readComments(posts, (err, comments) => {
      // pyramid of doom
    });
  });
});
```

Modern alternatives that all build on the same callback idea:

| Mechanism | What it is under the hood |
| --- | --- |
| **Promises** | An object with `.then(callback)` — the callback fires when the value resolves |
| **async / await** | Syntactic sugar over promises — the compiler rewrites your code into callbacks |
| **Observables / streams** | Callbacks invoked many times, once per emitted value |
| **Event emitters** | `emitter.on("event", callback)` — callback per event occurrence |

## Variants you'll see named

- **Continuation** — a callback that represents "the rest of the program." Same idea, theoretical framing (continuation-passing style).
- **Handler / listener** — a callback registered for a specific event type.
- **Hook** — a callback the framework invokes at a defined lifecycle point.
- **Higher-order function** — any function that takes or returns functions; the receiver of a callback is one.

## TL;DR

A callback is a function passed as a value so someone else can invoke it later. It's how you express *"do X **when** Y happens"* in a language where functions are first-class.
