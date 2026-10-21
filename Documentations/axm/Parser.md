# 🔧 Parser.py

Converts tokens into an Abstract Syntax Tree (AST).

---

## Grammar Overview

Supports:
- **Variables:** `VAR x = 5`, assignment `x = 5`, index assign `list[0] = 5`
- **Conditionals:** `IF cond`, `ELIF cond`, `ELSE` (indent-based, no braces)
- **Loops:** `FOR i IN 5`, `WHILE cond DO` (indent-based)
- **Functions:** `FUN name(params)`, `RETURN`, default params `b = 0`, type annotation `a: INT`
- **Entity actions:** `@player MOVE 5 "RIGHT"`, `@enemy DAMAGE 10`, `@player HEAL 10`
- **I/O:** `SAY`, `SAYF` (f-strings with `{expr}`)
- **Lists:** `[1, 2, 3]`, indexing `list[0]`
- **Attribute chain:** `a.b.c` (nested attribute access)
- **Entity ref:** `@player.x` (entity attribute)
- **Unary minus/plus:** `-5`, `3 + -2`
- **Type keywords as function:** `INT("42")`, `STR(42)`, `BOOL(1)`, `LIST(1,2,3)`, `NUM("3.14")`

## Operator Precedence

1. `OR`
2. `AND`
3. `NOT`
4. Comparison (`==`, `!=`, `>`, `<`, `>=`, `<=`)
5. `+`, `-` (addition)
6. `*`, `/` (multiplication)
7. Primary (literals, variables, calls, entity refs, lists, index)

## Special Cases

- **`@entity.action`**: `@player MOVE 5 "RIGHT"` → `Move(EntityRef("player"), Number(5), String("RIGHT"))`
- **`a.b.c`**: `Attribute(Attribute(Variable("a"), "b"), "c")`
- **`INT(...)`**: `FunctionCall("INT", [...])` (type keyword as function)
- **`FUN foo()`**: no-param function (fixed)

## Errors

- `ParserError`: unexpected token, missing `)`, missing indent, invalid direction