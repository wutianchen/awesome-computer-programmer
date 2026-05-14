# Argument Passing Strategy

## Patterns

| Pattern | Copy made? | Mutate original? | Rebind original? | Languages |
|---|---|---|---|---|
| Pass by value | Yes | No | No | Go (structs), Python (immutables) |
| Pass by reference | No | Yes | Yes | C++, PHP |
| Pass by pointer | Yes (pointer) | Yes (via `*`) | No | C, Go |
| Pass by object reference | Yes (reference) | Yes (object contents) | No | Python, Java, JavaScript |
| Pass by name | No | Yes | Yes | Some functional languages, macros |

> See [binding.md](binding.md) for an explanation of variable binding, rebinding, and mutation — concepts that are central to understanding the differences between these patterns.

**1. Pass by value** — a copy of the value is made; the function cannot mutate or rebind the original (Go structs, Python immutables)

```go
// Go — struct is copied; mutation does not affect the original
func double(v Vertex) {
    v.X *= 2  // only affects the local copy
}
```

```python
# Python — immutable int; rebinding does not affect the original
def change(n):
    n = 99  # rebinds the local variable only
x = 1
change(x)
print(x)  # 1 — unchanged
```

**2. Pass by reference** — the function receives the actual variable binding; both mutation and rebinding affect the original (C++ `&`, PHP `&`)

> **vs. Pass by pointer (pattern 3):** Both allow mutation of the original, but pass by reference is implicit — the caller's syntax is identical to pass by value and the language handles aliasing automatically. Pass by pointer is explicit: the caller takes the address (`&i`) and the function dereferences (`*n`). Go only supports pass by pointer, not true pass by reference.
>
> **vs. Pass by object reference (pattern 4):** The key difference is rebinding. In pass by reference, rebinding inside the function updates the caller's variable. In pass by object reference, rebinding only changes the local copy of the reference — the caller's binding is unaffected. Mutation of the object's contents is visible to the caller in both cases.

**3. Pass by pointer** — a copy of the memory address is passed; the function can mutate the original by dereferencing, but cannot rebind the caller's variable (C, Go with `*T`)

```go
// Go — pass a pointer to mutate the original
func increment(n *int) { *n++ }  // mutates via dereference

i := 1
increment(&i)
fmt.Println(i) // 2
```

**4. Pass by object reference** — a copy of the reference is passed; the function can mutate the object's contents (visible to the caller), but rebinding the variable only affects the local copy (Python, Java, JavaScript)

```python
# Mutation — affects the original object
def change(obj):
    obj["x"] = 99  # mutates the object the reference points to

v = {"x": 1}
change(v)
print(v)  # {"x": 99} — changed!
```

```python
# Rebinding — does NOT affect the caller's variable
def reassign(obj):
    obj = {"x": 99}  # rebinds the local reference only

v = {"x": 1}
reassign(v)
print(v)  # {"x": 1} — unchanged
```

**5. Pass by name / lazy evaluation** — the expression is re-evaluated each time it's used inside the function (rare, e.g. some functional languages, macros)

In practice, most modern languages use **pass by value** or **pass by object reference**, with pointers/references as an opt-in when mutation is needed.

---

## Go
Structs are passed by value in Go. This means when you assign a struct to a new variable or pass it to a function, Go makes a full copy of all its fields. Changes to the copy do not affect the original.

```go
v1 := Vertex{1, 2}
v2 := v1   // v2 is a copy of v1
v2.X = 99
fmt.Println(v1.X) // 1 — v1 is unchanged
fmt.Println(v2.X) // 99
```

## Python

Python uses **pass by object reference**. The behavior depends on whether the object is mutable or immutable.

**Immutable types** (int, str, tuple) behave like pass by value — changes don't affect the original:

```python
x = 1
def change(n):
    n = 99
change(x)
print(x)  # 1 — unchanged
```

**Mutable types** (list, dict, class instances) behave like pass by reference — changes affect the original:

```python
v = {"x": 1, "y": 2}
def change(obj):
    obj["x"] = 99
change(v)
print(v)  # {"x": 99, "y": 2} — changed!
```

A Python class instance would be mutated inside a function without needing a pointer — unlike Go where you explicitly need `*T` to mutate the original.