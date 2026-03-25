# axm/ast.py

class Node:
    def __repr__(self):
        return f"<{self.__class__.__name__}>"

# ========== Statements ==========
class Say(Node):
    def __init__(self, expr): 
        self.expr = expr
    def __repr__(self):
        return f'Say("{self.expr}")'

class SayF(Node):
    def __init__(self, parts):  # parts = list of Expr
        self.parts = parts
    def __repr__(self):
        return f'SayF({self.parts})'

class Move(Node):
    def __init__(self, entity, amount, direction):
        self.entity = entity      # Expr
        self.amount = amount      # Expr
        self.direction = direction  # Expr
    def __repr__(self):
        return f"Move({self.entity}, {self.amount}, {self.direction})"
 

class Sleep(Node):
    def __init__(self, duration, unit: str):
        self.duration = duration  # Expr
        self.unit = unit          # Expr
    def __repr__(self):
        return f"Sleep({self.duration}, {self.unit})"

class For(Node):
    def __init__(self, var_name, times, body):
        self.var_name = var_name
        self.times = times        # Expr
        self.body = body
    def __repr__(self):
        return f"For({self.var_name} range {self.times})"

class If(Node):
    def __init__(self, condition, body, elifs, else_body=None):
        self.condition = condition
        self.body = body
        self.elifs = elifs 
        self.else_body = else_body if else_body is not None else []
    def __repr__(self):
        return f"If(cond={self.condition}, body={self.body}, elifs={self.elifs}, else={self.else_body})"

class While(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        self._index = 0
    def __repr__(self):
        return f"While({self.condition}, body={self.body})"

class Damage(Node):
    def __init__(self, entity, amount):
        self.entity = entity      # Expr
        self.amount = amount      # Expr
    def __repr__(self):
        return f'Damage({self.entity}, {self.amount})'

class Heal(Node):
    def __init__(self, entity, amount):
        self.entity = entity # Expr (EntityRef)
        self.amount = amount # Expr (Number)
    def __repr__(self):
        return f'Heal({self.entity}, {self.amount})'

class Var(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value        # Expr
    def __repr__(self):
        return f"Var({self.name} = {self.value})"

class Assignment(Node):
    def __init__(self, name, value):
        self.name = name 
        self.value = value
    def __repr__(self):
        return f"Assignment({self.name} = {self.value})"

class ListLiteral(Node):
    def __init__(self, elements):
        self.elements = elements

    def __repr__(self):
        return f"List({self.elements})"

class IndexAccess(Node):
    def __init__(self, target, index):
        self.target = target
        self.index = index

    def __repr__(self):
        return f"Index({self.target}[{self.index}])"

class FunctionDef(Node):
    def __init__(self, name, params, defaults, body):
        self.name = name 
        self.params = params # List format: ['p1','p2']
        self.defaults = defaults # Dict {'name': String('User'), ...}
        self.body = body 
    def __repr__(self):
        params_str = ', '.join([
            f"{p}={self.defaults[p]}" if p in self.defaults else p 
            for p in self.params 
        ])
        return f"FunctionDef({self.name}({params_str}))"
     
class FunctionCall(Node):
    def __init__(self, name, args):
        self.name = name 
        self.args = args 
    def __repr__(self):
        return f"FunctionCall({self.name}({self.args}))"

class Return(Node):
    def __init__(self, value):
        self.value = value    # Expr or None
    def __repr__(self):
        return f"Return({self.value})"

class Break(Node):
    def __repr__(self):
        return "Break"

# ========== Expressions ==========
class Expr(Node):
    pass

class BinaryOp(Expr):
    def __init__(self, left, op, right):
        self.left = left   
        self.op = op       
        self.right = right 
    
    def __repr__(self):
        return f"BinaryOp({self.left} {self.op} {self.right})"

class LogicalOp(Expr):
    def __init__(self, left, op, right=None):
        self.left = left    
        self.op = op        
        self.right = right  
    def __repr__(self):
        if self.op == 'NOT':
            return f"LogicalOp(NOT {self.left})"
        return f"LogicalOp({self.left} {self.op} {self.right})"

class Number(Expr):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Number({self.value})"

class String(Expr):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f'String("{self.value}")'

class Boolean(Expr):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Boolean({self.value})"

class Variable(Expr):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Variable({self.name})"

class EntityRef(Expr):
    def __init__(self, name):
        self.name = name 
    def __repr__(self):
        return f"EntityRef(@{self.name})"

class Attribute(Expr):
    def __init__(self, obj, attr):
        self.obj = obj      # Expr (usually Variable)
        self.attr = attr    # string
    def __repr__(self):
        return f"Attribute({self.obj}.{self.attr})"