# 🔧 Parser.py

Converts tokens into an Abstract Syntax Tree (AST).

---

## Grammar Overview

`Supports:`
- **Variables:** `VAR x = 5`
- **Conditionals:** `IF condition { ... } ELIF { ... } ELSE { ... }`
- **Loops:** `FOR i IN 5 { ... }`, `WHILE condition DO { ... }`
- **Functions:** `FUN name(params) { ... }`, `RETURN`
- **Entity actions:** `MOVE @player 5 "RIGHT"`, `DAMAGE @enemy 10`
- **I/O:** `SAY`, `SAYF` (f-strings)
- **Lists:** `[1, 2, 3]`, indexing `list[0]`

## Operator Precedence

1. `OR`
2. `AND`
3. `NOT`
4. Comparison (`==`, `>`, `<`, etc.)
5. `+`, `-`
6. `*`, `/`
7. Primary (literals, variables, calls)

---