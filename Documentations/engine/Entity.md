# 🧩 Entity.py

Represents all objects in the game world.

---

## Properties

- `id` - Unique identifier
- `name`, `role` - Entity identity
- `health` - Hit points
- `x`, `y`, `z` - Position coordinates
- `vx`, `vy`, `vz` - Velocity (applied on next tick)
- `IsDead` / `IsAlive` - Status checks

## Key Methods

- `update(world)` - Called each tick, moves entity based on velocity
- `damage(amount)` - Reduce health
- `_move_by(dx, dy, dz)` - Internal position change