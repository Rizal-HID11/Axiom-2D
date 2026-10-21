# 🧩 Entity.py

Represents all objects in the game world.

---

## Properties

- `id` - Unique identifier (auto-increment via `_NEXT_ID`)
- `name`, `role` - Entity identity
- `health` - Hit points
- `position` - `(x, y, z)` tuple (getter/setter, supports 2D or 3D)
- `x`, `y`, `z` - Position shortcuts (read-only)
- `vx`, `vy`, `vz` - Velocity (applied on next tick)
- `IsDead` / `IsAlive` - Status checks (property)
- `_last_move` - Last move info (`{"direction": str, "steps": int}`), set by `MOVE` builtin

## Key Methods

- `update(world)` - Called each tick, moves entity based on velocity (debug print if `world.debug`)
- `damage(amount)` - Reduce health (clamped to 0)
- `_move_by(dx, dy, dz)` - Internal position change (no collision check)

## Position

`position` is a property with validation:
- Setter accepts `(x, y)` or `(x, y, z)` (z defaults to 0)
- Internal `_position` list is single source of truth

## Example

    entity = Entity("player", "ENTITY", 100, 0, 0, 0)
    entity.vx = 5  # set velocity
    # next tick: entity.update(world) -> try_move -> position updated

    entity.damage(10)  # health: 100 -> 90
    print(entity.IsAlive)  # True