# 🌍 World.py

Manages all entities and physics in the game world.

---

## Properties

- `world_name` - World name (default: "UnnamedWorld")
- `entities` - Dict `{id: Entity}`
- `entity_names` - Dict `{name: Entity}` (for fast lookup)
- `bounds` - Optional dict (`None` = infinite world)
- `debug` - Debug flag (print `[TICK]` logs if True)

## Main Methods

- `add_entity(name, role, health, x, y, z=0)` - Create and add new entity (auto-remove old entity with same name)
- `remove_entity(entity_id)` - Remove entity by ID
- `get_entity(entity_id)` - Find entity by ID
- `get_entity_by_name(name)` - Find entity by name
- `get_entities()` - List all entities
- `tick()` - Update all entities, process movement, remove dead ones
- `try_move(entity, dx, dy, dz)` - Attempt movement with collision + bounds check
- `is_adjacent(e1, e2)` - Check if two entities are next to each other
- `_in_bounds(pos)` - Check if position is within bounds (return True if no bounds)
- `cleanup_dead_entities()` - Remove dead entities, return count

## Collision

- **Entity collision**: `other.position == target` (exact match, per step)
- **Adjacency**: Manhattan distance `abs(x1-x2) + abs(y1-y2) == 1` and same Z level
- **Step-by-step**: `try_move` moves one step at a time, stops if blocked
- **Complexity**: O(n^2) - each entity checks all others (no spatial index yet)

## Bounds (Optional)

Set via `WORLD_BOUNDS` in config:

    "WORLD_BOUNDS": {
      "min_x": 0, "max_x": 10,
      "min_y": 0, "max_y": 10
    }

- If `None` -> infinite world
- Axis without min/max -> infinite on that axis
- Out-of-bounds -> `try_move` returns `(False, None)` (blocker = None, not an entity)

## Example

    world = World("TestWorld")
    world.debug = True
    world.bounds = {"min_x": 0, "max_x": 10, "min_y": 0, "max_y": 10}

    player = world.add_entity("player", "ENTITY", 100, 0, 0)
    enemy = world.add_entity("enemy", "ENTITY", 100, 5, 0)

    player.vx = 20  # try to move 20 right
    world.tick()    # player stops at (4, 0) - blocked by enemy at (5, 0)