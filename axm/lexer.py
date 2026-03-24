# axm/lexer.py

KEYWORDS = {
    "SAY", "SAYF", "FOR", "IF", "ELSE", 
    "MOVE", "SLEEP", "DAMAGE", "IN", "BREAK", 
    "VAR", "TRUE", "FALSE", "FUN", "RETURN", 
    "NOT", "AND", "OR", "WHILE", "DO", "ELIF",
    "HEAL"
}
DIRECTIONS = {
    "W", "A", "S", "D",
    "UP", "DOWN", "LEFT", "RIGHT",
    "TOP", "BOTTOM"
}
TIME_UNITS = {"MS", "S", "M"}

class Token:
    def __init__(self, type_, value=None, line=0):
        self.type = type_
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class LexerError(Exception):
    pass

def strip_comment(line):
    in_str = False 
    i = 0 
    while i < len(line) - 1:
        ch = line[i]
        
        if ch == '"':
            in_str = not in_str
        if not in_str and line[i:i+2] == "//":
            return line[:i]
        
        i += 1
    
    return line

def lex(code: str):
    tokens = []
    indent_stack = [0]
    lines = code.splitlines()
    bracket_lines = 0

    for line_no, raw in enumerate(lines, 1):
        if not raw.strip():
            tokens.append(Token("NEWLINE", line=line_no))
            continue

        # --- strip comment ---
        raw = strip_comment(raw)
        
        if bracket_lines == 0:
            indent = len(raw) - len(raw.lstrip(' '))
            if indent % 2 != 0:
                raise LexerError(f"Indent harus kelipatan 2 spasi (line {line_no})")

            indent //= 2

            if indent > indent_stack[-1]:
                tokens.append(Token("INDENT", line=line_no))
                indent_stack.append(indent)
            while indent < indent_stack[-1]:
                tokens.append(Token("DEDENT", line=line_no))
                indent_stack.pop()

            i = indent * 2
        else:
            i = 0
        line = raw[i:]

        pos = 0
        while pos < len(line):
            ch = line[pos]

            if ch.isspace():
                pos += 1
                continue

            # STRING
            if ch == '"' or ch == "'":
                quote_char = ch
                pos += 1
                start = pos
                while pos < len(line) and line[pos] != quote_char:
                    pos += 1
                if pos >= len(line):
                    raise LexerError(f"Unterminated string (line {line_no})")
                tokens.append(Token("STRING", line[start:pos], line_no))
                pos += 1
                continue

            if ch == '@':
                tokens.append(Token("AT", "@", line_no))
                pos += 1 
                continue

            # PARENTHESES, BRACKETS & COMMA
            if ch == '(':
                tokens.append(Token("LPAREN", "(", line_no))
                pos += 1
                continue
            if ch == ')':
                tokens.append(Token("RPAREN", ")", line_no))
                pos += 1
                continue
            if ch == '[':
                tokens.append(Token("LBRACKET", "[", line_no))
                bracket_lines += 1
                pos += 1 
                continue
            if ch == ']':
                tokens.append(Token("RBRACKET", "]", line_no))
                bracket_lines -= 1
                pos += 1 
                continue
            if ch == ',':
                tokens.append(Token("COMMA", ",", line_no))
                pos += 1
                continue

            # OPERATORS
            if line.startswith("==", pos):
                tokens.append(Token("OP", "==", line_no))
                pos += 2
                continue
            if line.startswith("!=", pos):
                tokens.append(Token("OP", "!=", line_no))
                pos += 2 
                continue 
            if line.startswith(">=", pos):
                tokens.append(Token("OP", ">=", line_no))
                pos += 2
                continue
            if line.startswith("<=", pos):
                tokens.append(Token("OP", "<=", line_no))
                pos += 2
                continue
            
            if ch in "+-*/<>=":
                if ch == '=':
                    tokens.append(Token("ASSIGN", "=", line_no))
                else:
                    tokens.append(Token("OP", ch, line_no))
                pos += 1 
                continue

            # DOT
            if ch == '.':
                tokens.append(Token("DOT", ".", line_no))
                pos += 1
                continue
            
            # WORD / NUMBER 
            start = pos 
            
            isnum = ch.isdigit()
            
            if isnum:
                dotseen = False 
                while pos < len(line):
                    ch2 = line[pos]
                    if ch2.isspace():
                        break 
                    if ch2 == '.':
                        if dotseen:
                            break 
                        dotseen = True 
                        pos += 1
                        continue
                    if ch2 in '()[]{},':
                        break 
                    pos += 1
               
                word = line[start:pos]
                if '.' in word:
                    tokens.append(Token("NUMBER", float(word), line_no))
                else:
                    tokens.append(Token("NUMBER", int(word), line_no))
                continue
                    
            else:
                # parse as identifier 
                while pos < len(line):
                    ch2 = line[pos]
                    if ch2.isspace():
                        break 
                    if ch2 == '.':
                        break 
                    if ch2 in '()[]{},+-*/<>=!':
                        break 
                    pos += 1
                
                word = line[start:pos]
                if not word:
                    pos += 1
                    continue 
            
            if word in KEYWORDS:
                if word in {"TRUE", "FALSE"}:
                    tokens.append(Token("BOOLEAN", word == "TRUE", line_no))
                else:
                    tokens.append(Token(word, word, line_no))
            elif word in TIME_UNITS:
                tokens.append(Token("TIME_UNIT", word, line_no))
            elif word in DIRECTIONS:
                tokens.append(Token("DIRECTION", word, line_no))
            else:
                tokens.append(Token("IDENT", word, line_no))
                    
                
        tokens.append(Token("NEWLINE"))

    while len(indent_stack) > 1:
        tokens.append(Token("DEDENT"))
        indent_stack.pop()

    tokens.append(Token("EOF"))
    return tokens
