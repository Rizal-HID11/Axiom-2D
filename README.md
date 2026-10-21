
# Axiom-2D
# Tick-Based Game Engine

![Version](https://img.shields.io/badge/version-0.2.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8%2B-yellow)

**Axiom 2D** is a lightweight tick-based game engine written in Python, featuring a custom scripting language called **AXM**. The engine separates game logic (Python core) from gameplay scripting (AXM) for maximum flexibility.

> **Core Concept**: World ticks → Entities move → AXM scripts react

---

## Quick Features

- **3D World Space** (x, y, z coordinates) with 2D gameplay
- **Tick-based Loop** - Configurable interval (default 0.01s)
- **Entity System** - Health, position, velocity, collision
- **AXM Scripting Language** - Custom syntax with lexer, parser, runtime
- **JSON Configuration** - Easy world setup
- **No Dependencies** - Pure Python standard library

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Rizal-HID11/Axiom-2D.git
cd Axiom-2D

# Run with default configuration
python axiom.py
```

## Hello World in AXM
Create a file `hello.axm`:

```axm
SAY "Hello, Axiom 2D!"
```

Edit `GAME_CONFIG.json`:

```json
{
  "WORLD_NAME": "MyWorld",
  "WORLD_TICK": 0.01,
  "AXM_FILE_TO_RUN": "hello.axm",
  "DEBUG": false,
  "WORLD_ENTITY": {}
}
```

Run:

```bash
python axiom.py
# Output: [AXIOM] Hello, Axiom 2D!
```

---

## Documentation
For detailed documentation, see the `Documentations` folder:

```text
Documentations/
├── ARCHITECTURE.md
├── Usage Guide/
│   ├── started.md
│   └── Guide/
│       └── axm_syntax.md
├── engine/
│   ├── World.md
│   └── Entity.md
├── axm/
│   ├── Lexer.md
│   ├── Parser.md
│   ├── AST.md
│   ├── Runtime.md
│   ├── Builtins.md
│   └── Signals.md
└── testsuite/
    ├── basic.axm
    ├── entities.axm
    ├── lists.axm
    └── functions.axm
```

---

## Configuration
Edit `GAME_CONFIG.json`:

```json
{
  "WORLD_NAME": "TestWorld",
  "WORLD_TICK": 0.01,
  "AXM_FILE_TO_RUN": "test1.axm",
  "DEBUG": true,
  "MAX_WHILE_ITERATIONS": 10000,
  "WORLD_BOUNDS": {
    "min_x": 0,
    "max_x": 10,
    "min_y": 0,
    "max_y": 10
  },
  "WORLD_ENTITY": {
    "player": {
      "ROLE": "ENTITY",
      "HEALTH": 100,
      "X": 0,
      "Y": 0
    },
    "enemy": {
      "ROLE": "ENTITY",
      "HEALTH": 100,
      "X": 5,
      "Y": 0
    }
  }
}
```

---

### Notes:

* `WORLD_BOUNDS` **optional** — if not set, world is infinite

* `MIN_Z`/`MAX_Z` **optional** — if not set, z-axis is infinite

* `MAX_WHILE_ITERATIONS` **optional** — default 10000 (prevent infinite loop)

* `DEBUG` optional — default false (print `[TICK]` logs if true)

---

## 🐛 Recent Changes (v0.2.0-alpha)

### ⚠️ Breaking Changes

* `SLEEP 5 S` → **error**, use `SLEEP 5 SEC`

* `SLEEP 1 MIN` → **error**, use `SLEEP 1 MINUTE`

* `VAR` in function/IF/WHILE/FOR → **local**, no longer leaks to global

* `MOVE` no longer returns value (statement, not expression)

### 🐛 Bug Fixes

* **Scope:** `VAR` local in function/IF/WHILE/FOR, no global leak

* **While guard:** Max **10000** iterations (configurable), prevent infinite loop

* **Direction:** `NORTH/SOUTH/EAST/WEST/ARROW_*/UP_Z/DOWN_Z` support without quotes

* **TIME_UNITS:** `MIN` → `MINUTE`, `S` removed (conflict with South direction)

* **Delta time:** Tick rate consistent (~`WORLD_TICK`), independent of load

* **World bounds:** Optional via `WORLD_BOUNDS` in config

* **Attribute chain:** `a.b.c` support

* **Method call**: `a.b()` support (Entity method) — *planned for next release*

* **Debug flag:** `[TICK]` print only if `DEBUG: true`

* **Error handling:** Main loop try/except, clean error message

- **Builtins:**

  - `INT/STR/BOOL/LIST/NUM` as functions

  - `MIN/MAX` `*args`

  - `SPLIT` simplified (use `str.split()`)

  - `RANDOM_FLOAT` fix (NameError)

  - `TAN` fix (was `tanh`)

  - `HEAL` return health

- **Parser:**

  - `FUN foo()` no-param fix

  - Unary minus (`-5`, `3 + -2`)

  - NUMBER break on operators (`1+1` without space)

  - `Parameter.__repr__` truthy fix

  - `FunctionCall` default param truthy fix

  - `Attribute` error message fix

* **Signals:** Signal non-Exception (marker object)

* +10 smaller fixes

---

**License**

This project is licensed under the `MIT License` - see the `LICENSE` file.
