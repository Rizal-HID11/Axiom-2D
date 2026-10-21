# Getting Started

## Requirements
- Python 3.8 or newer
- Terminal / Command Prompt

## Running AXM Files Guide

- **1.** Open Terminal
- **2.** Navigate to Axiom 2D root folder (or your root folder that has Axiom 2D there)
- **3.** Make sure you don't change the location of `axiom.py` file!
- **4.** Run this command:

    python axiom.py

The program will automatically read `GAME_CONFIG.json` and execute the configured `.axm` file.

---

## Creating an AXM File Guide

- **1.** Create a new file with `.axm` extension
- **2.** Write your AXM Code inside
- **3.** Update GAME_CONFIG.json:

    {
        "AXM_FILE_TO_RUN": "your-file.axm"
    }

- **4.** Do the **Running AXM Files Guide** again to run your AXM file.

---

## Your First AXM File

Create `hello.axm`:

    // THIS MAY NOT WORK IF YOU MODIFY THE GAME_CONFIG.json file!
    SAYF "Player health: {@player.health}"
    SAYF "Enemy health: {@enemy.health}"
    @enemy DAMAGE 10
    IF @enemy.health < 100
      SAY "Enemy attacked!"

Run it. Output:

    [AXIOM] Player health: 100
    [AXIOM] Enemy health: 90
    [AXIOM] Enemy attacked!

**The output would be not 100% similar if you turn on the DEBUG mode.**

---

## Debug Mode

To see tokens and AST output, set `DEBUG` to `true` in `GAME_CONFIG.json`:

    {
        "DEBUG": true
    }

This is useful for debugging problematic code.

**Debug output includes**:
- `TOKENS` - Lexer output
- `AST` - Parser output
- `[TICK]` - Entity movement logs (from `world.debug`)

---

## Optional Config

    {
        "MAX_WHILE_ITERATIONS": 10000,
        "WORLD_BOUNDS": {
            "min_x": 0,
            "max_x": 10,
            "min_y": 0,
            "max_y": 10
        }
    }

- `MAX_WHILE_ITERATIONS` - Prevent infinite `WHILE` loop (default: 10000)
- `WORLD_BOUNDS` - Limit world size (optional, infinite if not set)