# Go Modules vs. Packages

A **package** is a single directory of `.go` files — the unit of code organisation.

A **module** is a collection of packages, versioned together and declared by a single `go.mod` file at the root.

---

**Package** = one directory, one logical unit of code.
**Module** = a whole project (or library), containing one or many packages.

```
myapp/              ← module root (declared in go.mod)
├── go.mod          ← "module myapp, go 1.22"
├── main.go         ← package main
├── greet/
│   └── greet.go   ← package greet
└── db/
    └── db.go      ← package db
```

Here `myapp` is one **module** containing three **packages** (`main`, `greet`, `db`).

---

## `go.mod` — What Makes Something a Module

`go.mod` is what makes something a module. It declares:

- the module's import path root (`module myapp`)
- the Go version
- external dependencies and their versions

```
module myapp

go 1.22

require (
    github.com/some/library v1.2.3
)
```

Without `go.mod`, Go doesn't know what module your packages belong to, and cross-package imports within your project won't resolve.

---

## Practical Rule of Thumb

- Create one `go.mod` per project (or per publishable library).
- Create a new package (subdirectory) whenever you want to group related code or control visibility boundaries.