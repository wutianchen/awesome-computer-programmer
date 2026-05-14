# Go Packages

A **package** is a directory of `.go` files that share the same `package` declaration. It is the basic unit of code organisation and reuse in Go.

---

## I. Package Declaration

Every `.go` file must start with a `package` statement declaring which package it belongs to.

```go
package greet
```

All files in the same directory must use the same package name. The package name is typically short, lowercase, and matches the directory name.

---

## II. Exported vs. Unexported Identifiers

Go uses capitalisation to control visibility — no `public`/`private` keywords needed.

| Identifier | Exported? | Accessible from other packages? |
|---|---|---|
| `Greet` | Yes | Yes |
| `greet` | No | No — package-private |

```go
package greet

// Exported — visible to other packages
func Hello(name string) string {
    return "Hello, " + name + "!"
}

// Unexported — only usable within this package
func formatName(name string) string {
    return "[" + name + "]"
}
```

---

## III. The `main` Package

The `main` package is special — it defines an executable program. The `main()` function inside it is the entry point.

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, world!")
}
```

Any other package name produces a **library** — importable but not directly executable.

---

## IV. Importing Packages

Use `import` to bring in another package. The import path is the module path + subdirectory.

```go
import (
    "fmt"                          // standard library
    "math/rand"                    // standard library subfolder
    "github.com/user/myapp/greet"  // local package within your module
)
```

Go does not allow unused imports — the compiler will reject them.

---

## V. Example: Creating and Using a Custom Package

**Project layout:**
```
myapp/
├── go.mod
├── main.go
└── greet/
    └── greet.go
```

**`greet/greet.go`** — defines the package:
```go
package greet

import "fmt"

func Hello(name string) {
    fmt.Printf("Hello, %s!\n", name)
}
```

**`main.go`** — imports and uses it:
```go
package main

import "myapp/greet"

func main() {
    greet.Hello("Alice")  // Hello, Alice!
}
```

**`go.mod`** — declares the module name (the root of all import paths):
```
module myapp

go 1.22
```

The import path `"myapp/greet"` resolves to the `greet/` subdirectory relative to the module root declared in `go.mod`.

---

## VI. Key Rules

- One package per directory.
- Package name ≠ import path. The import path is the full directory path; the package name is what you use in code. They usually match, but not always (e.g. `math/rand` is imported as `rand`).
- The `main` package is the only one that produces an executable.
- Capitalise to export — lowercase stays private to the package.
