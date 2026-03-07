# ⚙️ Runtime.py

Executes the AST and manages program state.

---

## Key Components

- **Scope stack** - Local variables for functions/blocks
- **Globals** - Global variables
- **Functions** - User-defined functions
- **Program counter** - Current execution position

## Execution Flow

1. `load(ast)` - Load program
2. `tick()` called from main loop - executes one statement
3. Statements evaluated, builtins called, entities modified
4. Control flow via `ReturnSignal` and `BreakSignal`

## Expression Evaluation

Handles numbers, strings, variables, entity refs (`@player`), attributes (`@player.health`), binary ops, logical ops, function calls, lists, indexing.

---