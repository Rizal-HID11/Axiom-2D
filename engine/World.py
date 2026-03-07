# engine/World.py

from .Entity import Entity

class World:
    def __init__(self, name="UnnamedWorld"):
        self.world_name = name
        self.entities = {}
        self.entity_names = {}
    
    def add_entity(self, name, role, health, x, y, z=0):
        if name in self.entity_names:
            old = self.entity_names[name]
            self.remove_entity(old.id)
        
        entity = Entity(name, role, health, x, y, z)
        self.entities[entity.id] = entity 
        self.entity_names[entity.name] = entity 
        return entity 
    
    def remove_entity(self, entity_id):
        ent = self.entities.pop(entity_id, None)
        if ent:
            self.entity_names.pop(ent.name, None)
    
    def cleanup_dead_entities(self):
        dead_ids = []
        for entity_id, entity in self.entities.items():
            if entity.IsDead:
                dead_ids.append(entity_id)
        
        for entity_id in dead_ids:
            self.remove_entity(entity_id)
        
        return len(dead_ids)
    
    def get_entity(self, entity_id):
        return self.entities.get(entity_id)
    
    def get_entity_by_name(self, name):
        return self.entity_names.get(name)
    
    def get_entities(self):
        return list(self.entities.values())
    
    # game tick 
    def tick(self):
        for entity in list(self.entities.values()):
            entity.update(self)
        self.cleanup_dead_entities()
    
    def is_adjacent(self, e1, e2):
        x1, y1, z1 = e1.position 
        x2, y2, z2 = e2.position 
        return abs(x1 - x2) + abs(y1 - y2) == 1 and z1 == z2 
    
    def try_move(self, entity, dx, dy, dz=0):
        ex, ey, ez = entity.position
        
        # Determine step dir (normalize)
        step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
        step_y = 0 if dy == 0 else (1 if dy > 0 else -1)
        step_z = 0 if dz == 0 else (1 if dz > 0 else -1)
        
        steps = max(abs(dx), abs(dy), abs(dz))
        
        # Move step by step, stop if blocked
        blocker = None 
        moved = 0
        
        for s in range(steps):
            next_x = ex+step_x
            next_y = ey+step_y
            next_z = ez+step_z
            target = (next_x, next_y, next_z)
            
            # Check collision 
            blocked = False 
            for other in self.entities.values():
                if other is entity:
                    continue 
                if other.position == target:
                    blocked = True 
                    blocker = other 
                    break 
            
            if blocked:
                break 
            
            # Move one step 
            ex, ey, ez = next_x, next_y, next_z
            moved += 1
        
        # Apply final position         
        if moved > 0:
            entity._position = [ex,ey,ez]
        
        return moved > 0, blocker 
        