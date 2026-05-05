# Complex data structure

## Struct

```go
package main

import "fmt"

type Vertex struct {
	X int
	Y int
}

func main() {
	v := Vertex{1, 2}
	v.X = 4
	fmt.Println(v.X)
}
```

Structs are passed by value in Go. This means when you assign a struct to a new variable or pass it to a function, Go makes a full copy of all its fields. Changes to the copy do not affect the original.

```go
v1 := Vertex{1, 2}
v2 := v1   // v2 is a copy of v1
v2.X = 99
fmt.Println(v1.X) // 1 — v1 is unchanged
fmt.Println(v2.X) // 99
```

## Arrays

The type `[n]T` is an array of `n` values of type `T`.

```go
var a [10]int
```

This declares a variable `a` as an array of ten integers.

An array's length is part of its type, so arrays cannot be resized. This seems limiting, but don't worry; Go provides a convenient way of working with arrays.

## Slices

An array has a fixed size. A slice, on the other hand, is a dynamically-sized, flexible view into the elements of an array. In practice, slices are much more common than arrays.

The type `[]T` is a slice with elements of type `T`.

A slice is formed by specifying two indices, a low and high bound, separated by a colon:

```go
a[low : high]
```

This selects a half-open range which includes the first element, but excludes the last one.

The following expression creates a slice which includes elements 1 through 3 of `a`:

```go
a[1:4]
```

> **Important:** Slices are like references to arrays. A slice does not store any data, it just describes a section of an underlying array. Changing the elements of a slice modifies the corresponding elements of its underlying array. Other slices that share the same underlying array will see those changes.

### Slice literals

A slice literal is like an array literal without the length.

This is an array literal:

```go
[3]bool{true, true, false}
```

And this creates the same array as above, then builds a slice that references it:

```go
[]bool{true, true, false}
```

### Slice of a slice

You can slice a slice. All resulting slices share the same underlying array, so modifying one affects the others.

```go
s := []int{1, 2, 3, 4, 5}
s2 := s[1:4]   // [2, 3, 4]
s3 := s2[0:2]  // [2, 3]

s3[0] = 99
fmt.Println(s)   // [1, 99, 3, 4, 5]
fmt.Println(s2)  // [99, 3, 4]
fmt.Println(s3)  // [99, 3]
```

### Slice length and capacity

- **Length** (`len()`) — how many elements the slice contains
- **Capacity** (`cap()`) — how many elements exist in the underlying array from the slice's start position

```go
s := []int{1, 2, 3, 4, 5}   // len=5, cap=5
s2 := s[1:4]                  // len=3, cap=4 (starts at index 1, so 4 elements remain)
s3 := s2[0:2]                 // len=2, cap=4 (same start as s2, same capacity)
```

You can re-extend a slice up to its capacity, but not beyond (that panics):

```go
s4 := s2[0:2]  // [2, 3]       — len=2, cap=4
s5 := s4[0:4]  // [2, 3, 4, 5] — len=4, cap=4 ← extended back
s6 := s4[0:5]  // runtime panic: slice bounds out of range
```