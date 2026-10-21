# Signals.py

Implements control flow using marker objects (not exceptions).

---

## Signals

- `Signal` - Base marker class (not an Exception)
- `ReturnSignal(value)` - Returned by `RETURN` statements, caught by function calls
- `BreakSignal` - Returned by `BREAK` statements, caught by loops

## Usage

The runtime checks `isinstance(result, Signal)` to implement non-local control flow.
Signals are **returned** (not raised), so no try/except needed for control flow.

## Why not exceptions?

Marker objects are simpler and avoid the overhead of exception handling for
normal control flow. The runtime propagates signals up the call stack by
returning them from `execute_node` and `execute_block`.

## Example

    # In execute_node:
    elif isinstance(node, Return):
        value = self.eval(node.value) if node.value else None
        return ReturnSignal(value)

    # In execute_block:
    result = self.execute_node(stmt)
    if isinstance(result, Signal):
        return result  # propagate