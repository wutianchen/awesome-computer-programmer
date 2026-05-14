# Mutation Testing

Mutation testing evaluates the quality of your **test suite**, not your code. The premise: if your tests are good, deliberately breaking the code should make them fail.

Line/branch coverage tells you what *ran*; mutation testing tells you what *would be caught if it broke*. A file at 100% line coverage can have a 10% mutation score — tests that execute code without asserting on its behavior.

## How it works

1. **Generate mutants** — a tool makes small, mechanical edits to your source code that should break the specification in the code. Each mutant is one tweak.
2. **Run your test suite against each mutant.**
3. **Score each mutant:**
   - **Killed** → at least one test failed. Good — your tests caught the bug.
   - **Survived** → all tests still passed despite broken code. Bad — coverage gap.
4. **Mutation score** = killed / total mutants. Higher is better.

## Common mutation operators

| Operator | Example |
| --- | --- |
| Relational | `>` → `>=`, `==` → `!=` |
| Arithmetic | `+` → `-`, `*` → `/` |
| Boolean    | `true` → `false`, `&&` → `\|\|` |
| Constant   | `return x` → `return 0` / `return null` |
| Statement  | delete a line, skip a branch |
| Conditional boundary | `<` → `<=` (off-by-one) |

## Example

```python
def is_adult(age):
    return age >= 18
```

The mutation tool generates mutants like:

- `return age > 17`    (off-by-one)
- `return age <= 18`   (inverted)
- `return True`        (constant)

If your only test is:

```python
assert is_adult(18) == True
```

**All three mutants survive** — you "covered" the line but never verified the boundary or the operator.

Add boundary tests:

```python
assert is_adult(17) == False   # kills `>` (would return False at 18 too — actually kills `<=`)
assert is_adult(18) == True    # kills `> 18` and `return False`
assert is_adult(25) == True
```

Now the mutants die and the mutation score climbs.

## Tools by language

| Language | Tool |
| --- | --- |
| Java     | PIT (gold standard) |
| Python   | mutmut, cosmic-ray |
| JS / TS  | Stryker |
| Rust     | cargo-mutants |
| C#       | Stryker.NET |
| Go       | go-mutesting |

## Tradeoffs

- **Expensive** — N mutants × full test run. Usually gated to CI nightly or to changed files only.
- **Equivalent mutants** — some mutations don't change observable behavior (e.g. `i++` vs `++i` in isolation, dead-code edits). These survive but aren't real holes; manual triage required.
- **Best ROI** — business logic, parsers, validators, financial/medical code. Less useful for glue code or thin wrappers.
