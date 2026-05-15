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
    
    def lookup(self, name):
        for scope in reversed(self.scope_stack):
            if name in scope:
                return scope[name]
        
        if name in self.globals:
            return self.globals[name] 
        
        # suggestion 
        all_names = self._get_all_variable_name()
        suggestion = self._closest_match(name, all_names)
        
        if suggestion:
            raise AXMRuntimeError(
                f"Unknown variable or function '{name}'. Did you mean '{suggestion}'?"
            )
        else:
            raise AXMRuntimeError(f"Unknown variable or function '{name}'")
        
    def _closest_match(self, name, candidates, maxDist=3):
        if not candidates:
            return None 
        
        # Simple cases: exact match (shouldn't happen but safety)
        if name in candidates:
            return name 
        
        best_match = None 
        best_distance = maxDist + 1 
        
        for candidate in candidates:
            distance = self._levenshtein(name, candidate)
            if distance < best_distance:
                best_distance = distance 
                best_match = candidate 
        
        return best_match if best_distance <= maxDist else None 
        
    def _levenshtein(self, s1, s2):
        if len(s1) < len(s2):
            return self._levenshtein(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                # Insert, delete, substitute 
                insertions = previous_row[j + 1] + 1 
                deletions = current_row[j] + 1 
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def _get_all_variable_name(self):
        names = set()
        
        # from scope_stack
        for scope in self.scope_stack:
            names.update(scope.keys())
        
        # From globals 
        names.update(self.globals.keys())
        
        # From functions 
        names.update(self.functions.keys())
        
        # From builtins 
        for name in dir(self.builtins):
            if not name.startswith('_') and callable(getattr(self.builtins, name)):
                names.add(name)
        
        return names 
    
    def get_type_name(self, val):
        if isinstance(val, str):
            return "STR"
        elif isinstance(val, bool):
            return "BOOL"
        elif isinstance(val, int):
            return "INT"
        elif isinstance(val, float):
            return "NUM"
        elif isinstance(val, list):
            return "LIST"
        return "UNKNOWN"
    
    def is_type_match(self, expected, actual):
        if expected == actual:
            return True 
        if expected == "NUM" and actual in ("INT", "NUM"):
            return True 
        if expected == "INT" and actual == "INT":
            return True
        return False 
    
    def push_scope(self, initial=None):
        self.scope_stack.append(initial or {})
    
    def pop_scope(self):
        if self.scope_stack:
            return self.scope_stack.pop()
        return None
    
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
            return self.lookup(expr.name)
        
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
            # Check user func 
            func = self.functions.get(expr.name)
            
            # If not user func, check builtins 
            if not func:
                builtinf = getattr(self.builtins, expr.name, None)
                if builtinf and callable(builtinf):
                    arg_vals = [self.eval(arg) for arg in expr.args]
                    return builtinf(*arg_vals)
                
                # Suggestion for function 
                all_names = self._get_all_variable_name()
                suggestion = self._closest_match(expr.name, all_names)
                if suggestion:
                    raise AXMRuntimeError(
                        f"Function '{expr.name}' not defined. Did you mean '{suggestion}'?"
                    )
                else:
                    raise AXMRuntimeError(f"Function '{expr.name}' not defined")
            
            # User function 
            arg_vals = [self.eval(arg) for arg in expr.args]
            
            if len(arg_vals) != len(func.params):
                raise AXMRuntimeError(
                    f"Function '{expr.name}' expected {len(func.params)} args, got {len(arg_vals)}"
                )
            
            # Save depth for cleanup 
            old_depth = len(self.scope_stack)
            self.push_scope({})
            func_scope = self.current_scope()
            
            # Bind params 
            for i, param in enumerate(func.params):
                if param.param_type:
                    expected_type = param.param_type
                    actual_type = self.get_type_name(arg_vals[i])
                    if not self.is_type_match(expected_type, actual_type):
                        while len(self.scope_stack) > old_depth:
                            self.pop_scope()
                        raise AXMRuntimeError(
                            f"Parameter '{param.name}' expects {expected_type}, got {actual_type}"
                        )
                func_scope[param.name] = arg_vals[i]
           
            try:                
                result = self.execute_block(func.body)
                if isinstance(result, ReturnSignal):
                    return result.value 
                return None 
            finally:
                while len(self.scope_stack) > old_depth:
                    self.pop_scope()
            
            
        elif isinstance(expr, ListLiteral):
            return [self.eval(e) for e in expr.elements]
        elif isinstance(expr, IndexAccess):
            target = self.eval(expr.target)
            index = self.eval(expr.index)
            
            if not isinstance(index, int):
                raise AXMRuntimeError(f"Index must be integer, got {type(index).__name__}")
            
            # Support string indexing 
            if isinstance(target, str):
                try:
                    return target[index] 
                except IndexError:
                    raise AXMRuntimeError(f"String index {index} out of range (length {len(target)})")
           
            # Support list indexing 
            if isinstance(target, list):
                try:
                    return target[index]
                except IndexError:
                    raise AXMRuntimeError(f"List index {index} out of range (length {len(target)})")
            
            raise AXMRuntimeError(f"Cannot index type: {type(target).__name__}")
            
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
 
            self.push_scope({})
            
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
                target = self.eval(node.name.target)
                index = self.eval(node.name.index)
                
                if not isinstance(target, list):
                    raise AXMRuntimeError(f"Cannot assign to index of non-list: {type(target).__name__}")
                if not isinstance(index, int):
                    raise AXMRuntimeError(f"List index must be integer, got {type(index).__name__}")
                
                try:
                    target[index] = value 
                except IndexError:
                    raise AXMRuntimeError(f"List index {index} out of range (length {len(target)})")
                
                return value 
           
            # Regular assignment 
            elif isinstance(node.name, str):
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
                        raise AXMRuntimeError(f"Undefined variable '{var_name}'")
               
                return value 
           
            else:
                raise AXMRuntimeError(f"Invalid assignment target: {type(node.name).__name__}")
           
        # FunctionDef
        elif isinstance(node, FunctionDef):
            # Save func def
            self.functions[node.name] = node 
        
        # FunctionCall
        elif isinstance(node, FunctionCall):
            # get func def
            funcdef = self.functions.get(node.name)
            if not funcdef:
                # Try builtins 
                builtinf = getattr(self.builtins, node.name, None)
                if builtinf and callable(builtinf):
                    arg_vals = [self.eval(arg) for arg in node.args]
                    return builtinf(*arg_vals)
                
                # Suggestion for function 
                all_names = self._get_all_variable_name()
                suggestion = self._closest_match(node.name, all_names)
                if suggestion:
                    raise AXMRuntimeError(
                        f"Function '{node.name}' not defined. Did you mean '{suggestion}'?"
                    )
                else:
                    raise AXMRuntimeError(f"Function '{node.name}' not defined")
            
            if not isinstance(funcdef, FunctionDef):
                raise AXMRuntimeError(f"'{node.name}' is not a function")
            
            # Evaluate args 
            args = [self.eval(arg) for arg in node.args]
            
            # create new scope for function 
            self.push_scope({})
            # Get the scope we just pushed 
            func_scope = self.current_scope()
            
            # Bind params with args 
            for i, param in enumerate(funcdef.params):
                if i < len(args):
                    arg_value = args[i]
                    
                    # Type checking 
                    if param.param_type:
                        expected_type = param.param_type
                        actual_type = self.get_type_name(arg_value)
                        if not self.is_type_match(expected_type, actual_type):
                            self.pop_scope()
                            raise AXMRuntimeError(
                                f"Parameter '{param.name}' expects {expected_type}, got {actual_type}"
                            )
                    
                    func_scope[param.name] = arg_value
                
                elif param.default:
                    # Use default value 
                    defaultval = self.eval(param.default)
                    func_scope[param.name] = defaultval
                else:
                    self.pop_scope()
                    raise AXMRuntimeError(
                        f"Missing required parameter '{param.name}' for function '{node.name}'"
                    )
            
            # Execute function body 
            try:
                for stmt in funcdef.body:
                    result = self.execute_node(stmt)
                    if isinstance(result, ReturnSignal):
                        return result.value 
            finally:
                self.pop_scope()
            
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
