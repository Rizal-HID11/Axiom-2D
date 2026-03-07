# axm/parser.py

from .ast import *
import re 
from .lexer import lex 

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.stop_tokens = {}
        self.pos = 0

    # ---------- basic helpers ----------
    def cur(self):
        if self.pos >= len(self.tokens):
            return Token("EOF", None)
        return self.tokens[self.pos]

    def eat(self, type_):
        if self.cur().type == type_:
            self.pos += 1
        else:
            raise ParserError(
                f"Expected {type_}, got {self.cur().type} at line {self.cur().line}"
            )

    def skip_newlines(self):
        while self.cur().type == "NEWLINE":
            self.eat("NEWLINE")
    
    def parse_entity_action_from_expr(self, subject):
        if self.cur().type == "MOVE":
            self.eat("MOVE")
            amount = self.parse_expression()
            
            if self.cur().type not in ("DIRECTION", "STRING"):
                raise ParserError(f"Expected direction, got {self.cur().type}")
            
            direction = self.parse_expression()
            self.skip_newlines()
            return Move(subject, amount, direction)
        
        if self.cur().type == "DAMAGE":
            self.eat("DAMAGE")
            amount = self.parse_expression()
            self.skip_newlines()
            return Damage(subject, amount)
        
        if self.cur().type == "HEAL":
            self.eat("HEAL")
            amount = self.parse_expression()
            self.skip_newlines()
            return Heal(subject, amount)
        
        raise ParserError("Invalid entity action")
    
    def parse_block(self):
        body = []
        while self.cur().type != "DEDENT":
            if self.cur().type == "NEWLINE":
                self.eat("NEWLINE")
                continue
            
            stmt = self.statement()
            if stmt is not None:
                body.append(stmt)
       
        self.eat("DEDENT")
        return body 

    # ---------- expression parser ----------
    def parse_expression(self, stop_tokens=None):
        return self.parse_or()
    
    def parse_or(self):
        left = self.parse_and()
        while self.cur().type == "OR":
            op = self.cur().value
            self.eat("OR")
            right = self.parse_and()
            left = LogicalOp(left, "OR", right)
        return left
    
    def parse_and(self):
        left = self.parse_not()
        while self.cur().type == "AND":
            op = self.cur().value 
            self.eat("AND")
            right = self.parse_not()
            left = LogicalOp(left, "AND", right)
        return left 
    
    def parse_not(self):
        if self.cur().type == "NOT":
            self.eat("NOT")
            expr = self.parse_not()
            return LogicalOp(expr, "NOT")
        return self.parse_comparison()
    
    def parse_comparison(self):
        left = self.parse_addition()
        while self.cur().type == "OP" and self.cur().value in ("==", ">", "<", "!=", ">=", "<="):
            op = self.cur().value 
            self.eat("OP")
            right = self.parse_addition()
            left = BinaryOp(left, op, right)
        return left 
    
    def parse_addition(self):
        left = self.parse_multiplication()
        while self.cur().type == "OP" and self.cur().value in ("+", "-"):
            op = self.cur().value 
            self.eat("OP")
            right = self.parse_multiplication()
            left = BinaryOp(left, op, right)
        return left 
    
    def parse_multiplication(self):
        left = self.parse_primary()
        while self.cur().type == "OP" and self.cur().value in ("*", "/"):
            op = self.cur().value 
            self.eat("OP")
            right = self.parse_primary()
            left = BinaryOp(left, op, right)
        return left 
    
    def parse_primary_atom(self):
        token = self.cur()
        from .ast import EntityRef 
        
        # @entity 
        if token.type == "AT":
            self.eat("AT")
            if self.cur().type != "IDENT":
                raise ParserError("Expected entity name after '@'")
            name = self.cur().value 
            self.eat("IDENT")
            
            expr = EntityRef(name)
            
            # support @<ent>.prop 
            while self.cur().type=="DOT":
                self.eat("DOT")
                if self.cur().type!="IDENT":
                    raise ParserError("Expected attribute name after '.'")
                attr = self.cur().value 
                self.eat("IDENT")
                expr = Attribute(expr,attr)
            
            return expr 
            
        if token.type == "IDENT":
            name = token.value 
            self.eat("IDENT")
            
            if self.cur().type == "LPAREN":
                return self.parse_function_call(name)
            
            # attr access 
            if self.cur().type == "DOT":
                self.eat("DOT")
                attr = self.cur().value 
                self.eat("IDENT")
                return Attribute(Variable(name), attr)
            
            return Variable(name)
                
        elif token.type == "NUMBER":
            val = token.value 
            self.eat("NUMBER")
            return Number(val)
        
        elif token.type == "STRING":
            val = token.value 
            self.eat("STRING")
            return String(val)
        
        elif token.type == "BOOLEAN":
            val = token.value 
            self.eat("BOOLEAN")
            return Boolean(val)
        
        elif token.type == "DIRECTION":
            val = token.value 
            self.eat("DIRECTION")
            return String(val)
        
        elif token.type == "LPAREN":
            self.eat("LPAREN")
            expr = self.parse_expression()
            self.eat("RPAREN")
            return expr 
        elif token.type == "LBRACKET":
            self.eat("LBRACKET")
            elements = [] 
            
            self.skip_newlines()
            
            if self.cur().type != "RBRACKET":
                elements.append(self.parse_expression())
                self.skip_newlines()
                
                while self.cur().type == "COMMA":
                    self.eat("COMMA")
                    self.skip_newlines()
                    elements.append(self.parse_expression())
                    self.skip_newlines()
            
            self.eat("RBRACKET")
            return ListLiteral(elements)
        else:
            raise ParserError(f"Unexpected token in expression: {token.type}")
        
    def parse_primary(self):
        expr = self.parse_primary_atom()
        
        while self.cur().type == "LBRACKET":
            self.eat("LBRACKET")
            index = self.parse_expression()
            self.eat("RBRACKET")
            expr = IndexAccess(expr, index)
        
        return expr 

    # ---------- f-string parser ----------
    def parse_fstring_parts(self, rawtt):
        
        parts = [] 
        i = 0
        length = len(rawtt)
        
        while i < length:
            if rawtt[i] == '{':
                
                # Search closing brace 
                j = i + 1
                brace = 1 
                while j < length and brace > 0:
                    if rawtt[j] == '{':
                        brace += 1
                    elif rawtt[j] == '}':
                        brace -= 1
                    j += 1
                
                if brace != 0:
                    raise ParserError("Unclosed { in f-string")
                
                expr_code = rawtt[i+1:j-1].strip()
                
                tokens = lex(expr_code)
                parser = Parser(tokens)
                expr = parser.parse_expression()
                
                parts.append(expr)
                i = j 
            else:
                start = i 
                while i < length and rawtt[i] != '{':
                    i += 1
                if start < i:
                    parts.append(String(rawtt[start:i]))

        return parts
    
    def parse_function_call(self, name):
        self.eat("LPAREN")
        args = [] 
        if self.cur().type != "RPAREN":
            args.append(self.parse_expression())
            while self.cur().type == "COMMA":
                self.eat("COMMA")
                args.append(self.parse_expression())
        self.eat("RPAREN")
        return FunctionCall(name, args)

    # ---------- entry ----------
    def parse(self):
        nodes = []
        while self.cur().type != "EOF":
            if self.cur().type == "NEWLINE":
                self.eat("NEWLINE")
                continue 
            
            stmt = self.statement()
            if stmt is not None:
                nodes.append(stmt)
        
        return nodes 

    # ---------- statements ----------
    def statement(self):
        t = self.cur()
        
        if t.type == "FUN":
            return self.parse_function_def()
        if t.type == "RETURN":
            return self.parse_return()
        if t.type == "IF":
            return self.parse_if()
        if t.type == "WHILE":
            return self.parse_while()
        if t.type == "SAY":
            return self.parse_say()
        if t.type == "SAYF":
            return self.parse_sayf()
        if t.type == "SLEEP":
            return self.parse_sleep()
        if t.type == "FOR":
            return self.parse_for()
        if t.type == "BREAK":
            self.eat("BREAK")
            self.skip_newlines()
            return Break()
        if t.type == "VAR":
            return self.parse_var_declaration()
        
        if t.type == "AT":
            expr = self.parse_primary()
            
            if self.cur().type in ("MOVE", "DAMAGE", "HEAL"):
                return self.parse_entity_action_from_expr(expr)
            
            return expr 
        
        if t.type == "IDENT":
            name = t.value 
            next_token = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else Token("EOF")
            
            # index assignment
            if next_token and next_token.type == "LBRACKET":
                var_expr = self.parse_primary()
                
                if self.cur().type == "ASSIGN":
                    self.eat("ASSIGN")
                    value = self.parse_expression()
                    self.skip_newlines()
                    return Assignment(var_expr, value)
                else:
                    # if not an assignment, return as expr 
                    return var_expr
            
            # regular assignment (name = value)
            elif next_token and next_token.type == "ASSIGN":
                self.eat("IDENT")
                self.eat("ASSIGN")
                value = self.parse_expression()
                self.skip_newlines()
                return Assignment(name, value)
            
            # function call 
            elif next_token.type == "LPAREN":
                self.eat("IDENT")
                return self.parse_function_call(name)
                
            # common variable 
            else:
                self.eat("IDENT")
                return Variable(name)
                
        if t.type == "NEWLINE":
            self.eat("NEWLINE")
            return None

        raise ParserError(f"Unexpected token {t.type} at line {t.line}")

    # ---------- parsers ----------
    def parse_var_declaration(self):
        self.eat("VAR")
        if self.cur().type != "IDENT":
            raise ParserError(f"Expected variable name after VAR, got {self.cur().type}")
        var_name = self.cur().value
        self.eat("IDENT")
        self.eat("ASSIGN")
        value_expr = self.parse_expression()
        self.skip_newlines()
        return Var(var_name, value_expr)
    
    def parse_return(self):
        self.eat("RETURN")
        if self.cur().type in ("NEWLINE", "DEDENT"):
            self.skip_newlines()
            return Return(None)
        value = self.parse_expression()
        self.skip_newlines()
        return Return(value)

    def parse_if(self):
        self.eat("IF")
        condition = self.parse_expression()
        self.skip_newlines()
        self.eat("INDENT")
        
        body = self.parse_block()
        
        elifs = []
        else_body = []
        
        while self.cur().type == "ELIF":
            self.eat("ELIF")
            elif_cond = self.parse_expression()
            self.skip_newlines()
            self.eat("INDENT")
            elif_body = self.parse_block()
            elifs.append((elif_cond, elif_body))
        
        if self.cur().type == "ELSE":
            self.eat("ELSE")
            self.skip_newlines()
            self.eat("INDENT")
            else_body = self.parse_block()
        
        return If(condition, body, elifs, else_body)
        
    
    def parse_while(self):
        self.eat("WHILE")
        condition = self.parse_expression()
        self.eat("DO")
        self.skip_newlines()
        self.eat("INDENT")
        
        body = self.parse_block()
        return While(condition, body)
    
    def parse_function_def(self):
        self.eat("FUN")
        if self.cur().type != "IDENT":
            raise ParserError("Expected function name")
        name = self.cur().value 
        self.eat("IDENT")
        
        params = [] 
        if self.cur().type == "LPAREN":
            self.eat("LPAREN")
            if self.cur().type != "RPAREN":
                params.append(self.cur().value)
                self.eat("IDENT")
                while self.cur().type == "COMMA":
                    self.eat("COMMA")
                    params.append(self.cur().value)
                    self.eat("IDENT")
            self.eat("RPAREN")
        
        self.skip_newlines()
        self.eat("INDENT")
        
        body = self.parse_block()
        return FunctionDef(name, params, body)

    def parse_say(self):
        self.eat("SAY")
        if self.cur().type == "STRING":
            # String literal 
            text = self.cur().value 
            self.eat("STRING")
            self.skip_newlines()
            return Say(String(text))
        else:
            # Expression (variable, attribute, dll)
            expr = self.parse_expression()
            self.skip_newlines()
            return Say(expr)

    def parse_sayf(self):
        self.eat("SAYF")
        raw_text = self.cur().value
        self.eat("STRING")
        parts = self.parse_fstring_parts(raw_text)
        self.skip_newlines()
        return SayF(parts)

    def parse_sleep(self):
        self.eat("SLEEP")
        duration = self.parse_expression()
        
        if self.cur().type != "TIME_UNIT":
            raise ParserError("Expected time unit after SLEEP duration")
        
        unit = self.cur().value 
        self.eat("TIME_UNIT")
        
        self.skip_newlines()
        return Sleep(duration, String(unit))

    def parse_for(self):
        self.eat("FOR")
        var_name = self.cur().value 
        self.eat("IDENT")
        self.eat("IN")
        times = self.parse_expression()
        self.skip_newlines()
        self.eat("INDENT")
        
        body = self.parse_block()
        return For(var_name, times, body)


# ---------- public API ----------
def parse(tokens):
    return Parser(tokens).parse()