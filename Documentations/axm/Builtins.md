# 🛠️ Builtins.py

`Built-in` functions available in AXM scripts.

---

## Entity Actions

- `MOVE(entity, steps, direction)` - Set entity velocity
- `DAMAGE(entity, amount)` - Reduce health
- `HEAL(entity, amount)` - Increase health

## List Operations

- `LEN(list)` - Get length
- `APPEND(list, item)` - Add item
- `POP(list, index=-1)` - Remove and return item
- `REMOVE(list, item)` - Remove first occurrence
- `INSERT(list, index, item)` - Insert at index
- `SORT(list, reverse=False)` - Sort list
- `CONTAINS(list, item)` - Check membership
- `INDEX_OF(list, item)` - Find index (-1 if not found)

## String Operations

- `SPLIT(string, delimiter)` - Split string into list

## Math Operations

* **Rounding & Absolute**

  - `FLOOR(x)` - Round down to integer 
  - `CEIL(x)` - Round up to integer 
  - `ROUND(x, decimals=0)` - Round to specific decimals
  - `ABS(x)` - Get absolute value

* **Min/Max/Mid**

  - `MIN(a, b)` - Return smaller value
  - `MAX(a, b)` - Return larger value 
  - `MID(x)` - Return middle value (floor of x/2)

* **Power & Root**

  - `POW(base, exponent)` - Raise to power
  - `SQRT(x)` - Square root
  - `EXP(x)` - Exponential (e^x)

* **Trigonometry**

  - `SIN(x)` - Sine (radians)
  - `COS(x)` - Cosine (radians)
  - `TAN(x)` - Tangent (radians)

* **Logarithm**

  - `LOG(x, base=10)` - Logarithm with base
  - `LN(x)` - Natural logarithm

* **Arithmetic**

  - `MOD(a, b)` - Modulo (remainder)
  - `CLAMP(x, min, max)` - Clamp value between min and max
  - `SIGN(x)` - Get sign (-1, 0, or 1)

* **Random**

  - `RAND(min=0, max=100)` - Random integer in range  
  - `RAND_FLOAT(min=0.0, max=1.0)` - Random float in range

## Type Checking

- `IS_INT(x)`, `IS_STR(x)`, `IS_LIST(x)`, `IS_BOOL(x)`

## Output

- `SAY(text)` - Print with `[AXIOM]` prefix
- `SAYF(text)` - Print (used by SAYF statement)

---