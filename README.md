
# Axiom-2D
A simple 2D game engine with a DSL programming language from scratch named AXM.
=======

# Axiom 2D - Tick-Based Game Engine

![Version](https://img.shields.io/badge/version-1.0.0-blue)
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
git clone https://github.com/yourusername/Axiom2D.git
cd Axiom2D

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
└── examples/
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

**License**
This project is licensed under the `MIT License` - see the `LICENSE` file.
