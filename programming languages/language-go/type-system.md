# Go Type System

Go is **statically and strongly typed** — every variable has a type fixed at compile time, and types cannot be mixed without an explicit conversion.

---

## I. Categories of Types

**Basic types** — the building blocks:

| Category | Types |
|---|---|
| Integer | `int`, `int8`, `int16`, `int32`, `int64` |
| Unsigned integer | `uint`, `uint8`, `uint16`, `uint32`, `uint64` |
| Float | `float32`, `float64` |
| String | `string` |
| Boolean | `bool` |
| Byte / Rune | `byte` (alias for `uint8`), `rune` (alias for `int32`) |

**Composite types** — built from other types:

| Type | Description |
|---|---|
| `array` | fixed-length sequence of elements |
| `slice` | dynamic-length sequence |
| `map` | key-value pairs |
| `struct` | group of named fields |

**Other types:** `pointer`, `function`, `channel`, `interface`.

---

## II. Static Typing — Types Are Fixed at Compile Time

```go
age := 30          // type is int — fixed
age = "thirty"     // compile error: cannot use string as int
```

The compiler catches type mismatches before the program ever runs.

---

## III. Strong Typing — No Implicit Conversion

Even between related types, Go never converts automatically. You must be explicit.

The conversion syntax is `targetType(value)`:

```go
var a int32 = 10
var b int64 = int64(a)  // int32 → int64

var f float64 = 3.99
var i int     = int(f)  // float64 → int (truncates, not rounds: i == 3)

var n int    = 65
var s string = string(n)          // int → string gives the Unicode character, not "65"
var s string = fmt.Sprintf("%d", n) // correct way to convert int to its string representation
```

Without the explicit conversion, the compiler rejects the code:

```go
var a int32 = 10
var b int64 = a      // compile error: cannot use int32 as int64

x := 3
y := 1.5
z := x + y           // compile error: mismatched types int and float64
```

---

## IV. Type Inference

Go infers the type from the value — you don't always have to write it:

```go
name := "Alice"   // string
count := 0        // int
ratio := 0.5      // float64
```

The type is still fixed — inference just saves you from writing it out.

---

## V. Custom Types

You can define your own named type based on an existing one:

```go
type Celsius float64
type UserID  int

var temp UserID = 42
```

Custom types are distinct even if the underlying type is the same — `Celsius` and `float64` are not interchangeable without a conversion. This lets you add meaning and safety to primitive values.

---

## VI. Constants

Constants are declared like variables but with the `const` keyword. Their value is fixed at compile time and can never change.

- Allowed types: character, string, boolean, and numeric values.
- Cannot be declared with `:=`.

```go
const Pi       = 3.14
const AppName  = "myapp"
const MaxRetry = 5
const Debug    = false

// const block — same as var block
const (
    StatusOK    = 200
    StatusNotFound = 404
)
```

Trying to reassign a constant is a compile error:

```go
const Pi = 3.14
Pi = 3.0  // compile error: cannot assign to Pi
```

---

## VII. The `any` Type

`any` (an alias for `interface{}`) holds a value of any type. It opts out of static typing for that variable:

```go
var val any = 42
val = "now a string"  // valid
```

Use it sparingly — you lose compile-time type safety and need type assertions to use the value meaningfully.
