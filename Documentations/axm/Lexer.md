# 🔤 Lexer.py

Converts AXM source code into tokens for the parser.

---

## Token Types

- Keywords: `SAY`, `IF`, `FOR`, `MOVE`, `VAR`, `FUN`, etc.
- Identifiers: Variable/function names
- Literals: Numbers, strings, booleans
- Directions: `UP`, `DOWN`, `LEFT`, `RIGHT`, `WASD`, etc.
- Time units: `MS`, `S`, `M`
- Operators: `+`, `-`, `*`, `/`, `==`, `>`, etc.
- Special: `@` (entity ref), `.` (attr access), `[]` (lists)

## Indentation

Uses 2 spaces per level, generates INDENT/DEDENT tokens.