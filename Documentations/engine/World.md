# 🌍 World.py

Manages all entities and physics in the game world.

---

## Main Methods

- `add_entity(name, role, health, x, y, z=0)` - Create and add new entity
- `remove_entity(entity_id)` - Remove entity by ID
- `get_entity(name)` / `get_entity_by_name(name)` - Find entities
- `tick()` - Update all entities, process movement, remove dead ones
- `try_move(entity, dx, dy, dz)` - Attempt movement with collision detection
- `is_adjacent(e1, e2)` - Check if two entities are next to each other

## Collision

Uses Manhattan distance: `abs(x1-x2) + abs(y1-y2) == 1` and same Z level.