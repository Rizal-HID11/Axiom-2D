# engine/Entity.py 

class Entity:
    _NEXT_ID = 1
    
    def __init__(self, name, role, health, x, y, z=0):
        self.id = Entity._NEXT_ID
        Entity._NEXT_ID += 1
        
        self.name = name
        self.role = role 
        self.health = int(health)
        
        # entity velocity 
        self.vx = 0 
        self.vy = 0 
        self.vz = 0
        
        # single source 
        self._position = [x, y, z]
    
    @property 
    def position(self):
        return tuple(self._position)
    
    @position.setter 
    def position(self, value):
        if len(value) not in (2, 3):
            raise ValueError("position must be (x, y) or (x, y, z)")
        x, y = value[0], value[1]
        z = value[2] if len(value) == 3 else 0 
        self._position = [x, y, z]
    
    # axis shortcuts 
    @property
    def x(self): return self._position[0]
    
    @property
    def y(self): return self._position[1]
    
    @property
    def z(self): return self._position[2]
    
    # AXM method
    @property 
    def IsDead(self):
        return self.health <= 0
    @property 
    def IsAlive(self):
        return self.health > 0     
    
    # tick update 
    def update(self, world):
        if self.IsDead:
            return 
        
        if self.vx or self.vy or self.vz:
            print(f"[TICK] {self.name} moving with v=({self.vx},{self.vy}) from ({self.x},{self.y})")
            success, blocker = world.try_move(self, self.vx, self.vy, self.vz)
            if success:
                print(f"[TICK] {self.name} moved to ({self.x},{self.y})")
                # reset velocity
                self.vx = self.vy = self.vz = 0 
            else:
                print(f"[TICK] {self.name} collision!")
                self.vx = self.vy = self.vz = 0
    
    # actions
    def _move_by(self, dx, dy, dz=0):
        self._position[0] += dx 
        self._position[1] += dy
        self._position[2] += dz 
    
    def damage(self, amount):
        self.health = max(0, self.health - int(amount))