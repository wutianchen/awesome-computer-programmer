# Go Variables

A variable declaration in Go is made up of four components:

```
var   age   int   = 30
───   ───   ───   ────
 │     │     │     │
 │     │     │     └─ initializer  — the starting value
 │     │     └─────── type        — what kind of data it holds
 │     └─────────────  name        — how you refer to it
 └─────────────────── symbol      — how you declare it
```

---

## Symbol

The **symbol** is how you tell Go you are declaring a variable. There are two:

| Symbol | Where | Notes |
|---|---|---|
| `var` | anywhere | explicit; required at package level |
| `:=` | inside functions only | shorthand; type and symbol combined |

> **Note — why does `:=` exist if `var` also infers types?**
>
> Both support type inference, so the only real difference is:
>
> | | `var` | `:=` |
> |---|---|---|
> | Type inference | yes | yes |
> | Explicit type | yes | no |
> | Where | anywhere | inside functions only |
>
> `:=` is strictly a shorter way to write `var` without a type, usable only inside functions. The sole practical reason to prefer it is fewer keystrokes.

---

## Name

The **name** is the identifier you use to refer to the variable. Go convention is `camelCase`.

```go
var userName string
var totalCount int
```

---

## Type

The **type** tells Go what kind of data the variable holds. Common types:

| Type | Example values |
|---|---|
| `int` | `0`, `42`, `-7` |
| `float64` | `3.14`, `-0.5` |
| `string` | `"hello"`, `""` |
| `bool` | `true`, `false` |

The type can be written explicitly or inferred from the initializer. Both of the following are equivalent:

```go
var age int = 30  // explicit type
var age = 30      // type inferred as int
```

If no type is written and no initializer is given, the type must be explicit:

```go
var age int  // valid — type explicit, initializer omitted
var age      // invalid — Go has nothing to infer from
```

---

## Initializer

The **initializer** is the starting value assigned to the variable. It is optional.

When omitted, Go assigns the **zero value** for that type automatically:

| Type | Zero value |
|---|---|
| `int`, `float64` | `0` |
| `string` | `""` |
| `bool` | `false` |
| pointer, slice, map | `nil` |

```go
var score int     // initializer omitted — score is 0
var name string   // initializer omitted — name is ""
```

---

## Var Block

When declaring multiple variables at the package level, repeating `var` for each one gets noisy. A `var` block groups them under a single `var` keyword:

```go
// without block — repetitive
var host string = "localhost"
var port int    = 8080
var debug bool

// with block — cleaner
var (
    host  string = "localhost"
    port  int    = 8080
    debug bool                  // zero value false
)
```

Each line inside the block is an independent declaration — they can have different types and each component (type, initializer) follows the same rules as a standalone `var`.

Var blocks are idiomatic at the package level but can also be used inside functions when declaring several variables up front makes the code clearer.

---

## Putting It Together

```go
// var  name   type    initializer
   var  city   string = "London"

// var  name   type    (initializer omitted — zero value "")
   var  city   string

// var  name   (type inferred)  initializer
   var  city                  = "London"

// :=  name   (type and symbol combined)  initializer
    city      :=                          "London"
```

All four lines declare a `string` variable named `city`.

---

## Scope

A variable's **scope** is the region of code where it can be accessed. In Go, scope is determined by curly braces `{}`.

There are three levels:

**Package scope** — declared outside any function, accessible across all files in the same package.

```go
var appName = "myapp"  // accessible everywhere in the package

func main() {
    fmt.Println(appName)  // works
}
```

**Function scope** — declared inside a function, accessible only within that function.

```go
func greet() {
    name := "Alice"       // only exists inside greet()
    fmt.Println(name)
}

func main() {
    fmt.Println(name)     // error — name is not defined here
}
```

**Block scope** — declared inside an `if`, `for`, or any `{}` block, accessible only within that block.

```go
func main() {
    if true {
        msg := "hello"    // only exists inside this if block
        fmt.Println(msg)  // works
    }
    fmt.Println(msg)      // error — msg is not defined here
}
```

When an inner scope declares a variable with the same name as an outer one, the inner variable **shadows** the outer — the outer is still there but temporarily hidden:

```go
x := "outer"

if true {
    x := "inner"      // new variable, shadows the outer x
    fmt.Println(x)    // inner
}

fmt.Println(x)        // outer — unchanged
```

---

## Key Rules

- `:=` is only valid inside functions; use `var` at the package level.
- All declared variables must be used — the compiler rejects unused variables.
- Type cannot change after declaration.
