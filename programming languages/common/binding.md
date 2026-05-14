# Variable Binding

A **variable binding** is the association between a variable name and a value (or memory location) in a program. When you declare a variable and assign it a value, you are creating a binding.

```python
x = 42  # binds the name "x" to the value 42
```

```go
x := 42  // binds the name "x" to the value 42
```

## Rebinding

Rebinding means reassigning a variable name to a different value or object. The name now refers to something new.

```python
x = 42
x = 99  # rebinding — x now points to 99, not 42
```

## Binding vs. Mutation

These are two different things:

- **Rebinding** — changes what the variable name points to; the original object is unaffected
- **Mutation** — changes the contents of the object the variable points to; the binding itself stays the same

```python
# Rebinding
x = [1, 2, 3]
x = [4, 5, 6]  # x now points to a new list; original [1, 2, 3] is unaffected

# Mutation
x = [1, 2, 3]
x.append(4)    # x still points to the same list, but its contents changed
```

## Why It Matters for [Argument Passing](argument_passing_strategies.md)

The distinction between rebinding and mutation is central to understanding argument passing strategies:

- In **pass by reference**, the function can rebind the caller's variable
- In **pass by object reference** (Python), the function can mutate the object but cannot rebind the caller's variable
- In **pass by value**, neither rebinding nor mutation affects the caller
