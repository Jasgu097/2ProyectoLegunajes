import re

# Definir los patrones para identificar tokens
token_patterns = [
    (r'[ \t\n]+', None),  # Ignorar espacios en blanco y tabulaciones
    (r'#[^\n]*', None),  # Ignorar comentarios
    (r'\d+', 'NUMBER'),  # Números
    (r'[a-zA-Z_]\w*', 'IDENTIFIER'),  # Identificadores (variables, funciones)
    (r'==|!=|<=|>=|<|>', 'COMPARISON'),  # Operadores de comparación
    (r'\+|\-|\*|\/', 'OPERATOR'),  # Operadores matemáticos
    (r'\(', 'LPAREN'),  # Paréntesis izquierdo
    (r'\)', 'RPAREN'),  # Paréntesis derecho
    (r'\=', 'ASSIGN'),  # Asignación
    (r';', 'SEMICOLON'),  # Punto y coma
]


# Función para escanear el código y convertirlo en tokens
def lex(code):
    pos = 0
    tokens = []

    while pos < len(code):
        match = None
        for token_regex, token_type in token_patterns:
            regex = re.compile(token_regex)
            match = regex.match(code, pos)
            if match:
                if token_type:  # Solo agregar si no es un token ignorado (como espacios)
                    token_text = match.group(0)
                    tokens.append((token_type, token_text))
                break
        if not match:
            raise SyntaxError(f'Error léxico en la posición {pos}')
        else:
            pos = match.end(0)

    return tokens


# Ejemplo de código a escanear
codigo_fuente = "variable1 = 42 + 8;"

# Probar el escáner léxico
tokens = lex(codigo_fuente)
print(tokens)



# Nodo básico del AST
class ASTNode:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value
        self.children = []

# Parser para construir el árbol sintáctico
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, token_type):
        if self.current_token() and self.current_token()[0] == token_type:
            self.pos += 1
        else:
            raise SyntaxError(f'Error de sintaxis, se esperaba {token_type}')

    def factor(self):
        token = self.current_token()
        if token[0] == 'NUMBER':
            self.eat('NUMBER')
            return ASTNode('NUMBER', token[1])
        elif token[0] == 'IDENTIFIER':
            self.eat('IDENTIFIER')
            return ASTNode('IDENTIFIER', token[1])

    def term(self):
        node = self.factor()
        while self.current_token() and self.current_token()[0] == 'OPERATOR':
            operator_token = self.current_token()
            self.eat('OPERATOR')
            right = self.factor()
            node = ASTNode('OPERATION', operator_token[1])
            node.children = [node, right]
        return node

    def parse(self):
        return self.term()

# Ejecutar el parser con los tokens generados anteriormente
parser = Parser(tokens)
ast = parser.parse()

# Imprimir el AST generado
def print_ast(node, indent=""):
    print(f"{indent}{node.type}: {node.value}")
    for child in node.children:
        print_ast(child, indent + "  ")

print_ast(ast)



class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}  # Tabla de símbolos para almacenar variables

    def analyze(self, node):
        if node.type == 'IDENTIFIER':
            if node.value not in self.symbol_table:
                raise NameError(f"Variable '{node.value}' no declarada.")
        elif node.type == 'ASSIGN':
            var_name = node.children[0].value
            self.symbol_table[var_name] = node.children[1].type

# Simular el análisis semántico en un AST
semantic_analyzer = SemanticAnalyzer()
semantic_analyzer.analyze(ast)
