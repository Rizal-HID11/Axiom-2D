# AXM Syntax Reference
Quick reference for AXM language syntax.

## Little Notes
- The `AXM Language` indent use **2** spaces per level. Required for all blocks.
- The `DO` keywords in `AXM Language` is it not used in `IF`, `ELIF`, `FOR`.

## Comments
```axm
// Single line commentVAR x = 10  // Inline comment
```

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
```axm
VAR name = "Player"        // Declaration
health = 75                // Assignment
items[0] = 10              // Index assignment
```

---

## Operators
| Arithmetic | Comparison | Logical |
|------------|------------|---------|
| `+` `-` `*` `/` | `==` `!=` `>` `<` `>=` `<=` | `AND` `OR` `NOT` |

---

## Control Flow

### IF / ELIF / ELSE 
```axm
IF condition
  // code
ELIF condition
  // code
ELSE
  // code
```

### WHILE 
```axm
WHILE condition DO
  // code
```

### FOR
```axm
FOR var IN times
  // code
```

### BREAK 
```axm
BREAK 
```
* Notes:
  * `BREAK` could be used in `FOR`, `WHILE` to stop the loop execution it must be placed inside the `FOR`, `WHILE` body.
  * `BREAK` not desgined to be inside of non-body.
  * `BREAK` not designed to be inside of `FUN` (except you had loop execution syntax there), `IF`, `ELSE`, `ELIF`.

### Functions
```axm
FUN name(param1, param2)
  RETURN value 

name(arg1, arg2)
```

### Entity Reference
```axm
@entity_name.property
```

**Properties:** `x`, `y`, `z`, `health`, `IsAlive`, `IsDead`

```axm
@player.x
@enemy.health 
@npc.IsAlive
```

## Statements 
| Statement | Syntax |
|-----------|--------|
| SAY | `SAY expr` |
| SAYF | `SAYF "text {expr}"` |
| MOVE | `@entity MOVE steps DIRECTION` |
| DAMAGE | `@entity DAMAGE amount` |
| HEAL | `@entity HEAL amount` |
| SLEEP | `SLEEP duration UNIT` |

**Directions:** `W` `A` `S` `D` / `UP` `DOWN` `LEFT` `RIGHT` / `NORTH` `SOUTH` `EAST` `WEST` / `TOP` `BOTTOM`
**Time Units:** `MS (Miliseconds)` `S (Seconds)` `M (Minutes)`

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
| `MIN(a, b)` / `MAX(a, b)` | Min/Max |
| `MID(x)` | Middle value (floor of x/2) |
| `POW(base, exp)` / `SQRT(x)` | Power & root |
| `MOD(a, b)` | Modulo |
| `RANDOM(min, max)` | Random integer |
| `RANDOM_FLOAT(min, max)` | Random float |
| `SIN(x)` / `COS(x)` / `TAN(x)` | Trigonometry |
| `LOG(x, base)` / `LN(x)` / `EXP(x)` | Logarithm |
| `CLAMP(x, min, max)` | Clamp value |
| `SIGN(x)` | Sign (-1, 0, 1) |

### Type Checking 
- `IS_INT(v)` - Is integer type
- `IS_STR(v)` - Is string type 
- `IS_LIST(v)` - Is list type 
- `IS_BOOL(v)` - Is boolean type 

### Entity Actions
```axm
@player MOVE 5 RIGHT
@enemy DAMAGE 25
@player HEAL 50
```

### String Interpolation
```axm
SAYF "Name: {name}, HP: {@player.health}"
```

### Complete Example 
```axm
VAR score = 0

FOR i IN 10
  VAR dmg = RANDOM(5, 20)
  @enemy DAMAGE dmg
  score = score + dmg
  
  IF i == MID(10)
    SAYF "Halfway! Score: {score}"
  
  SLEEP 500 MS

SAYF "Final score: {score}"
```

---