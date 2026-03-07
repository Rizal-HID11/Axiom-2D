# axm/builtins.py
import sys 
import os 

import time 
import re 
import math 
import random 

class Builtins:
    def __init__(self, runtime):
        self.runtime = runtime
        self.world = runtime.world
    
    DIR_MAP = {
        "W": (0, 1, 0),    # Up
        "A": (-1, 0, 0),   # Left
        "S": (0, -1, 0),   # Down
        "D": (1, 0, 0),    # Right
    
        "UP": (0, 1, 0),
        "DOWN": (0, -1, 0),
        "LEFT": (-1, 0, 0),
        "RIGHT": (1, 0, 0),
    
        "NORTH": (0, 1, 0),
        "SOUTH": (0, -1, 0),
        "WEST": (-1, 0, 0),
        "EAST": (1, 0, 0),
    
        "TOP": (0, 0, 1),
        "BOTTOM": (0, 0, -1),
        "UP_Z": (0, 0, 1),
        "DOWN_Z": (0, 0, -1),
    
        "ARROW_UP": (0, 1, 0),
        "ARROW_DOWN": (0, -1, 0),
        "ARROW_LEFT": (-1, 0, 0),
        "ARROW_RIGHT": (1, 0, 0),
}

    # =========================
    # OUTPUT
    # =========================
    def SAY(self, text):
        print(f"[AXIOM] {text}")

    # SAYF
    def SAYF(self, text):
        print(f"[AXIOM] {text}")

    # =========================
    # ENTITY ACTIONS
    # =========================
    def MOVE(self, entity, steps, direction):
        # Validate
        if not isinstance(steps, (int, float)):
            raise RuntimeError("MOVE steps must be number")
        if not isinstance(direction, str):
            raise RuntimeError("MOVE direction must be string")
        if not hasattr(entity, "vx") or not hasattr(entity, "vy"):
            raise RuntimeError("MOVE target is not Entity")
        
        dir_key = direction.upper()
        
        if dir_key not in self.DIR_MAP:
            raise RuntimeError(f"Unknown direction: {direction}")
        
        dx, dy, dz = self.DIR_MAP[dir_key]
        
        entity.vx = dx * steps 
        entity.vy = dy * steps 
        entity.vz = dz * steps 
        
        return True
            

    def DAMAGE(self, entity, amount):
        if not isinstance(amount, (int, float)):
            raise RuntimeError(f"DAMAGE amount must be number, got {type(amount).__name__}")
        
        if not hasattr(entity, 'health'):
            raise RuntimeError(f"Expected Entity object, got {type(entity).__name__}")
        
        old_health = entity.health
        entity.damage(amount)
        return entity.health
    
    def HEAL(self, entity, amount):
        # Validate 
        if not isinstance(amount, (int, float)):
            raise RuntimeError(f"HEAL amount must be number, got {type(amount).__name__}")
        
        if amount < 0:
            raise RuntimeError(f"HEAL amount must be positive, got {amount}")
        
        from engine.Entity import Entity 
        if not isinstance(entity, Entity):
            raise RuntimeError(f"HEAL target is not Entity, got {type(entity).__name__}")
        
        if not hasattr(entity, 'health'):
            raise RuntimeError(f"Expected Entity object, got {type(entity).__name__}")
        
        # Healing (add health, but not more than max health?)
        # If you want to have max health, you can add the max_health attribute in Entity.
        old_health = entity.health 
        entity.health = entity.health + amount 
        
        # Optional: if you want to have max health 
        # if hasattr(entity, 'max_health'):
        #     entity.health = min(entity.health, entity.max_health)
    
    
    # LISTS OPERATIONS 
    def LEN(self, obj):
        if hasattr(obj, 'value'):
            obj = obj.value
    
        # Check supported data type
        if isinstance(obj, (list, str)):
            return len(obj)
        else:
            raise RuntimeError(f"LEN: expected list or string, got {type(obj).__name__}")
    def APPEND(self, lst, item):
        if not isinstance(lst, list):
            raise RuntimeError(f"APPEND: expected list, got {type(lst).__name__}")
        lst.append(item)
        return lst 
    def POP(self, lst, idx=-1):
        if not isinstance(lst, list):
            raise RuntimeError(f"POP: expected list, got {type(lst).__name__}")
        try:
            return lst.pop(idx)
        except IndexError:
            raise RuntimeError(f"POP: index {idx} out of range")
    def REMOVE(self, lst, item):
        if not isinstance(lst, list):
            raise RuntimeError(f"REMOVE: expected list, got {type(lst).__name__}")
        try:
            lst.remove(item)
            return True 
        except ValueError:
            return False 
    def INSERT(self, lst, idx, item):
        if not isinstance(lst, list):
            raise RuntimeError(f"INSERT: expected list, got {type(lst).__name__}")
        lst.insert(idx, item)
        return lst 
    def SORT(self, lst, reverse=False):
        if not isinstance(lst, list):
            raise RuntimeError(f"SORT: expected list, got {type(lst).__name__}")
        try:
            lst.sort(reverse=reverse)
            return lst 
        except TypeError as e:
            raise RuntimeError(f"SORT: cannot sort list - {e}")
    def CONTAINS(self, lst, item):
        if not isinstance(lst, list):
            raise RuntimeError(f"CONTAINS: expected list, got {type(lst).__name__}")
        return item in lst 
    def INDEX_OF(self, lst, item):
        if not isinstance(lst, list):
            raise RuntimeError(f"INDEX_OF: expected list, got {type(lst).__name__}")
        try:
            return lst.index(item)
        except ValueError:
            return -1
    def SPLIT(self, t, delimeter=None):
        if delimeter is None:
            delimeter = " " # default space 
        
        result = [] 
        curr = ""
        
        i = 0
        while i < len(t):
            # check if found delimeter 
            if i + len(delimeter) <= len(t) and t[i:i+len(delimeter)] == delimeter:
                if curr: # dont add new empty str
                    result.append(curr)
                    curr = ""
                i += len(delimeter)
            else:
                curr += t[i]
                i+=1
        
        if curr:
            result.append(curr)
        
        return result 
    
    # IS_[TYPE] OPERATIONS
    def IS_INT(self, dt):
        return isinstance(dt, int)
    def IS_STR(self, dt):
        return isinstance(dt, str)
    def IS_LIST(self, dt):
        return isinstance(dt, list)
    def IS_BOOL(self, dt):
        return isinstance(dt, bool)
    
    # MATH OPERATIONS
    def FLOOR(self, n):
        return math.floor(n)
    def CEIL(self, n):
        return math.ceil(n)
     
    def ROUND(self, n, decimals=0):
        return round(n, decimals)
    
    def ABS(self, n):
        return abs(n)
    
    def MIN(self, a,b):
        return min(a,b)
    def MAX(self, a,b):
        return max(a,b)
    
    def MID(self, n):
        return math.floor(n / 2)
    
    def POW(self, base, exponent):
        return base ** exponent
    
    def SQRT(self, n):
        if n<0:
            raise RuntimeError(f"SQRT: cannot calculate square root of negative numbers: {n}")
        return math.sqrt(n)
    
    def MOD(self, a,b):
        if b==0:
            raise RuntimeError("MOD: division by zero")
        
        return a % b
    
    def RAND(self, minv=0, maxv=100):
        return random.randint(minv, maxv)
    def RAND_FLOAT(self, minv=0.0, maxv=1.0):
        return random.uniform(minv, maxv)
    
    def SIN(self, n):
        return math.sin(n)
    def COS(self, n):
        return math.cos(n)
    def TAN(self, n):
        return math.tanh(n)
    
    def LOG(self, n, base=10):
        if n<=0:
            raise RuntimeError(f"LOG: cannot calculate log of non-positive number: {n}")
        if base==10:
            return math.log10(n)
        return math.log(n, base)
    
    def LN(self, n):
        if n<=0:
            raise RuntimeError(f"LN: cannot calculate natural log of non-positive number: {n}")
        return math.log(n)
    
    def EXP(self, n):
        return math.exp(n)
    def CLAMP(self, n, minv, maxv):
        return max(minv, min(maxv, n))
    
    def SIGN(self, n):
        if n>0:
            return 1
        elif n<0:
            return -1
        return 0