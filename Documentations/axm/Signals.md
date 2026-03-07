# Signals.py

Implements control flow using exceptions.

---

## Signals

- `ReturnSignal(value)` - Raised by `RETURN` statements, caught by function calls
- `BreakSignal` - Raised by `BREAK` statements, caught by loops

## Usage

The runtime catches these signals to implement non-local control flow without complex stack management.

---