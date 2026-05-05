# Pointers

Go has pointers. A pointer holds the memory address of a value.

The type `*T` is a pointer to a `T` value. Its zero value is `nil`.

```go
var p *int
```

The `&` operator generates a pointer to its operand.

```go
i := 42
p = &i
```

The `*` operator denotes the pointer's underlying value.

```go
fmt.Println(*p) // read i through the pointer p
*p = 21         // set i through the pointer p
```

This is known as "dereferencing" or "indirecting".

Unlike C, Go has no pointer arithmetic.

## Pointers with Structs

Using pointers with structs serves two main purposes:

**1. Avoid copying**

Structs are passed by value in Go. If a struct is large, passing it around copies all its fields — which is expensive. A pointer passes just the memory address (8 bytes) instead.

```go
// Copies the entire User struct on every call
func greet(u User) { ... }

// Passes just a pointer — no copy
func greet(u *User) { ... }
```

**2. Mutate the original**

Without a pointer, modifications inside a function affect only the local copy and are lost when the function returns.

```go
func birthday(u User) {
    u.Age++  // only modifies the copy
}

func birthday(u *User) {
    u.Age++  // modifies the original
}
```

Methods that mutate state always use pointer receivers:

```go
type Counter struct {
    count int
}

func (c *Counter) Increment() {
    c.count++  // works on the original
}
```

Use a pointer when you need to **mutate** the struct or when the struct is **large enough** that copying it would be wasteful.
