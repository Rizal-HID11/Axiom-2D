# 🛠️ Builtins.py

Built-in functions available in AXM scripts.

---

## Entity Actions

- `MOVE(entity, steps, direction)` - Set entity velocity (applied next tick)
- `DAMAGE(entity, amount)` - Reduce health (clamped to 0)
- `HEAL(entity, amount)` - Increase health (returns new health)

## List Operations

- `LEN(list)` - Get length (also works on strings)
- `APPEND(list, item)` - Add item (returns list)
- `POP(list, index=-1)` - Remove and return item
- `REMOVE(list, item)` - Remove first occurrence (returns True/False)
- `INSERT(list, index, item)` - Insert at index (returns list)
- `SORT(list, reverse=False)` - Sort list (returns list)
- `CONTAINS(list, item)` - Check membership (returns bool)
- `INDEX_OF(list, item)` - Find index (-1 if not found)

## String Operations

- `SPLIT(string, delimiter=None)` - Split string into list (uses str.split())

## Type Conversion

- `INT(value)` / `CINT(value)` - Converts strings or numbers to integers
- `STR(value)` / `CSTR(value)` - Converts any value to a string
- `BOOL(value)` - Converts to boolean
- `LIST(*args)` - Create list from args
- `NUM(value)` - Converts to float

## Math Operations

* **Rounding & Absolute**

  - `FLOOR(x)` - Round down to integer
  - `CEIL(x)` - Round up to integer
  - `ROUND(x, decimals=0)` - Round to specific decimals
  - `ABS(x)` - Get absolute value

* **Min/Max/Mid**

  - `MIN(*args)` - Return smallest value (1+ args)
  - `MAX(*args)` - Return largest value (1+ args)
  - `MID(x)` - Return middle value (floor of x/2)

* **Power & Root**

  - `POW(base, exponent)` - Raise to power
  - `SQRT(x)` - Square root (error if x < 0)
  - `EXP(x)` - Exponential (e^x)

* **Trigonometry**

  - `SIN(x)` - Sine (radians)
  - `COS(x)` - Cosine (radians)
  - `TAN(x)` - Tangent (radians)

* **Logarithm**

  - `LOG(x, base=10)` - Logarithm with base (error if x <= 0)
  - `LN(x)` - Natural logarithm (error if x <= 0)

* **Arithmetic**

  - `MOD(a, b)` - Modulo (error if b == 0)
  - `CLAMP(x, min, max)` - Clamp value between min and max
  - `SIGN(x)` - Get sign (-1, 0, or 1)

* **Random**

  - `RAND(min=0, max=100)` / `RANDOM(min=0, max=100)` - Random integer in range
  - `RAND_FLOAT(min=0.0, max=1.0)` / `RANDOM_FLOAT(min=0.0, max=1.0)` - Random float in range

## Type Checking

- `IS_INT(x)`, `IS_STR(x)`, `IS_LIST(x)`, `IS_BOOL(x)`

## Output

- `SAY(text)` - Print with `[AXIOM]` prefix
- `SAYF(text)` - Print formatted (used by SAYF statement)

## Others

- `TIME()` - Current time in milliseconds