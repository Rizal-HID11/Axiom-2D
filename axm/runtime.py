# axm/runtime.py
from .builtins import Builtins
import time
from .ast import *
from .signals import Signal, ReturnSignal, BreakSignal

class AXMRuntimeError(Exception):
    pass

class Runtime:
    def __init__(self, world):
        self.world = world
        self.globals = {}
        self.functions = {}
        
        self.running = True
        self.pc = 0
        self.program = []
        
        self.scope_stack = []
        
        self.builtins = Builtins(self)

    # Basic tools
    def get_entity(self, name):
        ent = self.world.get_entity_by_name(name)
        if not ent:
            raise AXMRuntimeError(f"Entity '{name}' not found")
        return ent
    
    def axm_format_bool(self, value):
        if isinstance(value, bool):
            return "TRUE" if value else "FALSE"
        return str(value)
    
    def is_truthy(self, value):
        if isinstance(value, bool):
            return value 
        if value is None:
            return False 
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return value != ""
        return True 
    
    def push_scope(self, initial=None):
        self.scope_stack.append(initial or {})
    
    def pop_scope(self):
        self.scope_stack.pop()
    
    def current_scope(self):
        return self.scope_stack[-1] if self.scope_stack else None
    
    def load(self, ast):
        self.program = ast 
        self.pc = 0

    # =========================
    # EXPRESSION EVALUATOR
    # =========================
    def eval(self, expr):
        if isinstance(expr, Number):
            return expr.value 
        elif isinstance(expr, String):
            return expr.value 
        elif isinstance(expr, Boolean):
            return expr.value 
        elif isinstance(expr, Variable):
            name = expr.name 
        
            scope = self.current_scope()
            if scope and name in scope:
                return scope[name]
            
            if name in self.globals:
                return self.globals[name]
             
            raise AXMRuntimeError(f"Unknown variable or entity '{name}'")
        
        elif isinstance(expr, EntityRef):
            return self.get_entity(expr.name)
        
        elif isinstance(expr, Attribute):            
            obj = self.eval(expr.obj)
            attr_name = expr.attr
            
            
            from engine.Entity import Entity 
            if not isinstance(obj, Entity):
                raise AXMRuntimeError(
                    f"'{expr.obj.name}' is not an entity. Use @{expr.obj.name}"
                )
            
            if not hasattr(obj, attr_name):
                raise AXMRuntimeError(
                    f"Entity '{obj.name}' has no attribute '{attr_name}'"
                )
            
            value = getattr(obj, attr_name)
            return value 
    
        elif isinstance(expr, BinaryOp):
            left = self.eval(expr.left)
            right = self.eval(expr.right)
            op = expr.op 
        
            if op == "+":
                return left + right 
            elif op == "-":
                return left - right 
            elif op == "*":
                return left * right 
            elif op == "/":
                if right == 0:
                    raise AXMRuntimeError("Division by zero")
                return left / right 
            elif op == "==":
                return left == right 
            elif op == ">":
                return left > right 
            elif op == "<":
                return left < right 
            elif op == "!=":
                return left != right 
            elif op == ">=":
                return left >= right 
            elif op == "<=":
                return left <= right
            else:
                raise AXMRuntimeError(f"Unsupported operator: {op}")
        
        elif isinstance(expr, LogicalOp):
            left = self.eval(expr.left)
            
            if expr.op == "NOT":
                # convert to bool first 
                left_bool = bool(left)
                return not left_bool
            
            right = self.eval(expr.right)
            
            # Convert to bool 
            left_bool = bool(left)
            right_bool = bool(right)
            
            if expr.op == "AND":
                return left_bool and right_bool
            elif expr.op == "OR":
                return left_bool or right_bool
            else:
                raise AXMRuntimeError(f"Unknown logical operator: {expr.op}")
             
        elif isinstance(expr, FunctionCall):
            func = self.functions.get(expr.name)
            
            # if None, Check in builtins
            if not func:
                builtinf = getattr(self.builtins, expr.name, None)
                if builtinf and callable(builtinf):
                    arg_vals = [self.eval(arg) for arg in expr.args]
                    return builtinf(*arg_vals)
             
            # If still None, error 
            if not func:
                raise AXMRuntimeError(f"Function '{expr.name}' not defined")
             
            # this is for user func 
            arg_vals = [self.eval(arg) for arg in expr.args]
             
            if len(arg_vals) != len(func.params):
                raise AXMRuntimeError(
                   f"Function '{expr.name}' expected {len(func.params)} args, got {len(arg_vals)}"
                )
             
            old_dpth = len(self.scope_stack)
            self.push_scope(dict(zip(func.params, arg_vals)))
             
            try:
                result = self.execute_block(func.body)
                if isinstance(result, ReturnSignal):
                    return result.value 
                return None 
            finally:
                while len(self.scope_stack) > old_dpth:
                    self.pop_scope()
            
        elif isinstance(expr, ListLiteral):
            return [self.eval(e) for e in expr.elements]
        elif isinstance(expr, IndexAccess):
            target = self.eval(expr.target)
            index = self.eval(expr.index)
            
            if not isinstance(target, list):
                raise AXMRuntimeError("Indexing non-list value")
            
            if not isinstance(index, int):
                raise AXMRuntimeError("List index must be integer")
            
            try:
                return target[index]    
            except IndexError:
                raise AXMRuntimeError("List index out of range")
        else:
            raise AXMRuntimeError(f"Cannot evaluate expression: {expr}")
        

    # =========================
    # EXECUTION
    # =========================
    def execute(self, ast_nodes):
        self.program = ast_nodes
        self.pc = 0 
        self.running = True 
    
    def execute_block(self, body):
        for stmt in body:
            result = self.execute_node(stmt)
         
            if isinstance(result, Signal):
                return result 
                
        return None  
    
    def tick(self):
        if not self.running:
            return

        if self.pc >= len(self.program):
            self.running = False
            return

        node = self.program[self.pc]
        result = self.execute_node(node)

        if isinstance(result, ReturnSignal):
            self.running = False
            return

        if isinstance(result, BreakSignal):
            self.pc += 1
            return

        self.pc += 1       

    def execute_node(self, node):

        # SAY
        if isinstance(node, Say):
            value = self.eval(node.expr)
            text = self.axm_format_bool(value)
            self.builtins.SAY(text)

        # SAYF
        elif isinstance(node, SayF):
            text = ""
            for part in node.parts:
                val = self.eval(part)
                text += self.axm_format_bool(val)
            self.builtins.SAYF(text)

        # MOVE
        elif isinstance(node, Move):
            entity = self.eval(node.entity)
            
            from engine.Entity import Entity 
            if not isinstance(entity, Entity):
                raise AXMRuntimeError("MOVE target is not an entity. use @entity")
            
            amount = self.eval(node.amount)
            direction = self.eval(node.direction)
            self.builtins.MOVE(entity, amount, direction)

        # SLEEP
        elif isinstance(node, Sleep):
            duration = self.eval(node.duration)
            unit = self.eval(node.unit)
            
            if unit == "MS":
                seconds = duration / 1000
            elif unit == "S":
                seconds = duration 
            elif unit == "M":
                seconds = duration * 60 
            else:
                raise AXMRuntimeError(f"Invalid time unit: {unit}")
            
            if seconds > 0:
                time.sleep(seconds)
            
        # DAMAGE
        elif isinstance(node, Damage):
            entity = self.eval(node.entity)
            amount = self.eval(node.amount)
            self.builtins.DAMAGE(entity, amount)
        
        # HEAL 
        elif isinstance(node, Heal):
            entity = self.eval(node.entity)
            amount = self.eval(node.amount)
            self.builtins.HEAL(entity, amount)

        # FOR
        elif isinstance(node, For):
            times = self.eval(node.times)
            if not isinstance(times, int):
                raise AXMRuntimeError("FOR loop times must be integer")

            self.push_scope()
            
            try:
                for i in range(times):
                    self.current_scope()[node.var_name] = i 
                    
                    result = self.execute_block(node.body)
                    if isinstance(result, BreakSignal):
                        break 
                    if isinstance(result, ReturnSignal):
                        return result 
            finally:
                self.pop_scope()


        # VAR DECL
        elif isinstance(node, Var):
            value = self.eval(node.value)
            self.globals[node.name] = value
        
        # Var Assignment 
        elif isinstance(node, Assignment):
            value = self.eval(node.value)
            
            # Index Assignment 
            if isinstance(node.name, IndexAccess):
                # Evaluate target list and index
                target = self.eval(node.name.target)
                index = self.eval(node.name.index)
                
                # Validate
                if not isinstance(target, list):
                    raise AXMRuntimeError(f"Cannot assign to index of non-list: {type(target).__name__}")
                if not isinstance(index, int):
                    raise AXMRuntimeError(f"List index must be integer, got {type(index).__name__}")
                
                # Assign to list 
                try:
                    target[index] = value 
                except IndexError:
                    raise AXMRuntimeError(f"List index {index} out of range (length {len(target)})")
                
                return value          
                
            # Regular var assignment 
            elif isinstance(node.name, str):
                scope = self.current_scope()
                var_name = node.name 
                
                found = False 
                for scope in reversed(self.scope_stack):
                    if var_name in scope:
                        scope[var_name] = value 
                        found = True 
                        break
                
                if not found:
                    if var_name in self.globals:
                        self.globals[var_name] = value 
                    else:
                        raise AXMRuntimeError(f"Undefined variable '{node.name}'")
                
                return value
            
            else:
                raise AXMRuntimeError(f"Invalid assignment target: {type(node.name).__name__}")
                 
            
        # FunctionDef
        elif isinstance(node, FunctionDef):
            self.functions[node.name] = node 
        
        elif isinstance(node, FunctionCall):
            result = self.eval(node)
            if isinstance(result, Signal):
                return result 
            return None 
        
        elif isinstance(node, Return):
            value = self.eval(node.value) if node.value else None 
            return ReturnSignal(value)

        # BREAK
        elif isinstance(node, Break):
            
            return BreakSignal()
        
        # IF
        elif isinstance(node, If):
            # IF 
            if self.is_truthy(self.eval(node.condition)):
                result = self.execute_block(node.body)
                if isinstance(result, Signal):
                    return result 
                return None 
            
            # ELIF(s)
            for elif_cond, elif_body in node.elifs:
                if self.is_truthy(self.eval(elif_cond)):
                    result = self.execute_block(elif_body)
                    if isinstance(result, Signal):
                        return result 
                    return None 
            
            # ELSE 
            if node.else_body:
                result = self.execute_block(node.else_body)
                if isinstance(result, Signal):
                    return result 
        
        elif isinstance(node, While):
            while self.is_truthy(self.eval(node.condition)):
                result = self.execute_block(node.body)

                if isinstance(result, BreakSignal):
                    break

                if isinstance(result, ReturnSignal):
                    return result

            return None
