# ⚙️ Runtime.py

Executes the AST and manages program state.

---

## Key Components

- **Scope stack** - Local variables for functions/IF/WHILE/FOR (push/pop)
- **Globals** - Global variables (top-level `VAR`)
- **Functions** - User-defined functions
- **Program counter** - Current execution position (`pc`)
- **Sleep timer** - Non-blocking `SLEEP` (`sleep_until`)

## Execution Flow

1. `load(ast)` - Load program
2. `tick()` called from main loop:
   - Check sleep timer (skip if still sleeping)
   - Loop: execute node until yield point (`MOVE`, `DAMAGE`, `HEAL`, `SLEEP`) or program end
   - Yield points only at **top-level** (nested blocks execute immediately)
3. Statements evaluated, builtins called, entities modified
4. Control flow via `ReturnSignal` and `BreakSignal` (marker objects, not exceptions)

## Expression Evaluation

Handles:
- Numbers, strings, booleans
- Variables (scope lookup with Levenshtein suggestion)
- Entity refs (`@player`)
- Attributes (`@player.health`, `a.b.c`)
- Binary ops (`+`, `-`, `*`, `/`, `==`, `!=`, `>`, `<`, `>=`, `<=`)
- Logical ops (`AND`, `OR`, `NOT`)
- Function calls (user + builtins)
- Lists, indexing
- Method calls (planned, not yet implemented)

## Scope Rules

- **Top-level** → global (`self.globals`)
- **Function** → local scope (push/pop)
- **`IF`/`WHILE`/`FOR`** → local scope per block/iteration (push/pop)
- **`VAR`** → local if inside block, global if top-level
- **`Assignment`** (`x = 5`) → search scope first (inner → outer), then global

## While Guard

- Max iterations: `MAX_WHILE_ITERATIONS` (default 10000)
- Raises `AXMRuntimeError` if exceeded (prevent infinite loop)

## Sleep (Non-blocking)

- `SLEEP duration unit` sets `sleep_until = time.time() + seconds`
- `tick()` skips if `time.time() < sleep_until`
- No `time.sleep()` blocking

## Errors

- `AXMRuntimeError`: unknown variable/function, type mismatch, division by zero, invalid entity, etc.
- Suggestion via Levenshtein distance (`Did you mean 'x'?`)