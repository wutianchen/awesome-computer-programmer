# Naked Returns

Normally when you return from a function, you specify what to return:

```go
func add(a, b int) int {
    return a + b
}
```

Go lets you name your return values in the function signature. When you do that, a plain `return` with no values — a **naked return** — automatically returns whatever those named variables currently hold.

```go
func add(a, b int) (result int) {
    result = a + b
    return  // same as: return result
}
```

`result` is declared by the signature, assigned inside the function, and the bare `return` sends it back.

---

## A More Useful Example

Named returns are most useful when a function returns multiple values:

```go
func minMax(nums []int) (min, max int) {
    min, max = nums[0], nums[0]

    for _, n := range nums[1:] {
        if n < min {
            min = n
        }
        if n > max {
            max = n
        }
    }

    return  // returns min and max
}

func main() {
    lo, hi := minMax([]int{3, 1, 7, 2, 9})
    fmt.Println(lo, hi)  // 1 9
}
```

Instead of writing `return min, max` at the end, the naked `return` picks them up automatically.

---

## When to Use (and Avoid) Them

**Use naked returns** in short functions where the named variables make the intent clearer.

**Avoid them** in long functions — a bare `return` buried deep in a long function is hard to reason about because you have to scroll back to the signature to know what's being returned.

```go
// Hard to read — what does this return?
func process(data []byte) (result string, err error) {
    // ... 50 lines of code ...
    return  // ← unclear without scrolling up
}

// Clearer
func process(data []byte) (string, error) {
    // ... 50 lines of code ...
    return result, err  // explicit
}
```

> The Go community generally prefers explicit returns in anything longer than a few lines.
