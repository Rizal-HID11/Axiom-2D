# AXM Syntax Reference

Quick reference for AXM language syntax.

## Little Notes
- The AXM Language indent uses **2** spaces per level. Required for all blocks.
- The `DO` keyword is used in `WHILE` but **not** in `IF`, `ELIF`, `FOR`.
- `VAR` inside `IF`/`WHILE`/`FOR`/function is **local** (does not leak to global).
- **Yield points** (`MOVE`, `DAMAGE`, `HEAL`, `SLEEP`) only work at **top-level** (not inside nested blocks).

## Comments

    // Single line comment
    VAR x = 10  // Inline comment

---

## Data Types

| Type | Example |
|------|---------|
| Integer | `42` |
| Float | `3.14` |
| String | `"Hello"` or `'Hello'` |
| Boolean | `TRUE`, `FALSE` |
| List | `[1, 2, 3]` |

---

## Variable

    VAR name = "Player"        // Declaration
    health = 75                // Assignment
    items[0] = 10              // Index assignment

---

## Operators

| Arithmetic | Comparison | Logical |
|------------|------------|---------|
| `+` `-` `*` `/` | `==` `!=` `>` `<` `>=` `<=` | `AND` `OR` `NOT` |

---

## Control Flow

### IF / ELIF / ELSE

    IF condition
      // code
    ELIF condition
      // code
    ELSE
      // code

### WHILE

    WHILE condition DO
      // code

### FOR

    FOR var IN times
      // code

### BREAK

    BREAK

**Notes**:
- `BREAK` can be used in `FOR`, `WHILE` to stop loop execution. Must be inside the loop body.
- `BREAK` not designed to be inside `FUN` (except if there is a loop there), `IF`, `ELSE`, `ELIF`.

### Functions

    FUN name(param1, param2)
      RETURN value

    name(arg1, arg2)

**Default params**: `FUN add(a, b = 0)`
**Type annotation**: `FUN greet(name: STR)`

### Entity Reference

    @entity_name.property

**Properties**: `x`, `y`, `z`, `health`, `IsAlive`, `IsDead`

    @player.x
    @enemy.health
    @npc.IsAlive

---

## Statements

| Statement | Syntax |
|-----------|--------|
| SAY | `SAY expr` |
| SAYF | `SAYF "text {expr}"` |
| MOVE | `@entity MOVE steps DIRECTION` |
| DAMAGE | `@entity DAMAGE amount` |
| HEAL | `@entity HEAL amount` |
| SLEEP | `SLEEP duration UNIT` |

**Directions**: `W` `A` `S` `D` / `UP` `DOWN` `LEFT` `RIGHT` / `NORTH` `SOUTH` `EAST` `WEST` / `TOP` `BOTTOM` / `UP_Z` `DOWN_Z` / `ARROW_UP` `ARROW_DOWN` `ARROW_LEFT` `ARROW_RIGHT`

**Time Units**: `MS` (Milliseconds), `SEC` (Seconds), `MINUTE` (Minutes)

---

## Built-in Functions

### List Operations

| Function | Description |
|----------|-------------|
| `LEN(list)` | Length |
| `APPEND(list, item)` | Add item |
| `POP(list, idx)` | Remove by index |
| `REMOVE(list, item)` | Remove by value |
| `INSERT(list, idx, item)` | Insert at index |
| `SORT(list, reverse)` | Sort list |
| `CONTAINS(list, item)` | Check membership |
| `INDEX_OF(list, item)` | Find index |
| `SPLIT(str, delim)` | Split string |

### Math Operations

| Function | Description |
|----------|-------------|
| `FLOOR(x)` / `CEIL(x)` / `ROUND(x)` | Rounding |
| `ABS(x)` | Absolute value |
| `MIN(*args)` / `MAX(*args)` | Min/Max (1+ args) |
| `MID(x)` | Middle value (floor of x/2) |
| `POW(base, exp)` / `SQRT(x)` | Power & root |
| `MOD(a, b)` | Modulo |
| `RANDOM(min, max)` / `RAND(min, max)` | Random integer |
| `RANDOM_FLOAT(min, max)` / `RAND_FLOAT(min, max)` | Random float |
| `SIN(x)` / `COS(x)` / `TAN(x)` | Trigonometry |
| `LOG(x, base)` / `LN(x)` / `EXP(x)` | Logarithm |
| `CLAMP(x, min, max)` | Clamp value |
| `SIGN(x)` | Sign (-1, 0, 1) |

### Type Conversion

| Function | Description |
|----------|-------------|
| `INT(v)` / `CINT(v)` | Convert to integer |
| `STR(v)` / `CSTR(v)` | Convert to string |
| `BOOL(v)` | Convert to boolean |
| `LIST(...)` | Create list |
| `NUM(v)` | Convert to float |

### Type Checking

- `IS_INT(v)` - Is integer type
- `IS_STR(v)` - Is string type
- `IS_LIST(v)` - Is list type
- `IS_BOOL(v)` - Is boolean type

### Entity Actions

    @player MOVE 5 RIGHT
    @enemy DAMAGE 25
    @player HEAL 50

### String Interpolation

    SAYF "Name: {name}, HP: {@player.health}"

### Complete Example

    VAR score = 0

    FOR i IN 10
      VAR dmg = RANDOM(5, 20)
      @enemy DAMAGE dmg
      score = score + dmg

      IF i == MID(10)
        SAYF "Halfway! Score: {score}"

      SLEEP 500 MS

    SAYF "Final score: {score}"