# Control Statements

## for

Go has only one looping construct, the `for` loop.

The basic `for` loop has three components separated by semicolons:

- **init statement**: executed before the first iteration
- **condition expression**: evaluated before every iteration
- **post statement**: executed at the end of every iteration

The init statement will often be a short variable declaration, and the variables declared there are visible only in the scope of the `for` statement. The loop will stop iterating once the boolean condition evaluates to `false`.

```go
for i := 0; i < 5; i++ {
    fmt.Println(i)
}
// 0 1 2 3 4
```

## "while"

The init and post statements are optional:

```go
n := 1
for n < 100 {
    n *= 2
}
fmt.Println(n) // 128
```

This is equivalent to a while statement in many other programming languages

## forever

If you omit the loop condition it loops forever, so an infinite loop is compactly expressed:

```go
for {
    // runs forever
}
```

## If

```go
func sqrt(x float64) string {
	if x < 0 {
		return sqrt(-x) + "i"
	}
	return fmt.Sprint(math.Sqrt(x))
}
```

Like for, the if statement can start with a short statement to execute before the condition.

Variables declared by the statement are only in scope until the end of the if.

```go
func pow(x, n, lim float64) float64 {
	if v := math.Pow(x, n); v < lim {
		return v
	}
	return lim
}
```

Variables declared inside an if short statement are also available inside any of the else blocks

## Switch

A switch statement is a shorter way to write a sequence of if - else statements. It runs the first case whose value is equal to the condition expression.

Go's switch is like the one in C, C++, Java, JavaScript, and PHP, except that Go only runs the selected case, not all the cases that follow. In effect, the `break` statement that is needed at the end of each case in those languages is provided automatically in Go. Another important difference is that Go's switch cases need not be constants, and the values involved need not be integers.

```go
package main

import (
    "fmt"
    "runtime"
)

func main() {
    fmt.Print("Go runs on ")
    switch os := runtime.GOOS; os {
    case "darwin":
        fmt.Println("macOS.")
    case "linux":
        fmt.Println("Linux.")
    default:
        // freebsd, openbsd,
        // plan9, windows...
        fmt.Printf("%s.\n", os)
    }
}
```

## Switch with no condition

Switch without a condition is the same as `switch true`.

This construct can be a clean way to write long if-then-else chains.

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    t := time.Now()
    switch {
    case t.Hour() < 12:
        fmt.Println("Good morning!")
    case t.Hour() < 17:
        fmt.Println("Good afternoon.")
    default:
        fmt.Println("Good evening.")
    }
}
```

## Defer

A `defer` statement defers the execution of a function until the surrounding function returns.

The deferred call's arguments are evaluated immediately, but the function call is not executed until the surrounding function returns.

> **Surrounding function** refers to the function that directly contains the `defer` statement. When that function finishes — whether by reaching the end, a `return`, or a `panic` — the deferred call runs.

```go
package main

import "fmt"

func main() {
    defer fmt.Println("world")
    fmt.Println("hello")
}
// Output:
// hello
// world
```

Deferred function calls are pushed onto a stack. When a function returns, its deferred calls are executed in last-in, first-out (LIFO) order.

```go
func main() {
    for i := 0; i < 3; i++ {
        defer fmt.Println(i)
    }
}
// Output:
// 2
// 1
// 0
```

Common use cases include closing files, releasing locks, and other cleanup tasks — guaranteed to run even if the function panics.

Article: [Defer, Panic, and Recover](https://go.dev/blog/defer-panic-and-recover)