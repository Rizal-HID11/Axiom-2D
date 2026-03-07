# 🏗️ Axiom 2D Architecture

## System Overview
GAME_CONFIG.json ──► axiom.py ──┬─► engine/ (World + Entity)
└─► axm/ (Lexer → Parser → AST → Runtime)

---

## Game Loop

```python
while runtime.running:
    world.tick()      # Update entities (movement, collision)
    runtime.tick()    # Execute one line of AXM script
    time.sleep(world_tick)
```

---

## Component Breakdown

`engine/`
* **World.py:** Manages all entities, handles collisions, runs tick updates
* **Entity.py:** Game objects with position, health, velocity

`axm/`
  * **lexer.py:** Converts AXM source code → tokens
  * **parser.py:** Converts tokens → AST
  * **ast.py:** Defines AST node types
  * **runtime.py:** Executes AST, manages scope, calls builtins
  * **builtins.py:** Built-in functions (MOVE, DAMAGE, LEN, etc.)
  * **signals.py:** Control flow via exceptions (Return, Break)

---