import re

# Definir los patrones para identificar tokens
token_patterns = [
    (r'\b(entero|decimal|booleano|cadena|si|sino|mientras|hacer|verdadero|falso)\b','RESERVED'),  # Palabras reservadas
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
print("Tokens:", tokens)


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
        else:
            raise SyntaxError(f'Error de sintaxis inesperado: {token[1]}')

    def term(self):
        node = self.factor()
        while self.current_token() and self.current_token()[0] == 'OPERATOR':
            operator_token = self.current_token()
            self.eat('OPERATOR')
            right = self.factor()
            new_node = ASTNode('OPERATION', operator_token[1])
            new_node.children = [node, right]
            node = new_node
        return node

    def assignment(self):
        # Reconoce una asignación
        identifier = self.current_token()
        if identifier[0] == 'IDENTIFIER':
            left = ASTNode('IDENTIFIER', identifier[1])
            self.eat('IDENTIFIER')
            self.eat('ASSIGN')
            right = self.term()
            assign_node = ASTNode('ASSIGN', '=')
            assign_node.children = [left, right]
            return assign_node
        else:
            raise SyntaxError("Se esperaba un identificador para la asignación")

    def condition(self):
        """Reconoce y procesa una condición 'if'."""
        self.eat('IF')
        self.eat('OPEN_PAREN')  # Espera un paréntesis de apertura
        condition_expr = self.term()  # La condición es una expresión
        self.eat('CLOSE_PAREN')  # Espera un paréntesis de cierre
        self.eat('OPEN_BRACE')  # Cuerpo del if entre llaves
        if_body = self.assignment()  # Otras estructuras se pueden añadir aquí
        self.eat('CLOSE_BRACE')

        if_node = ASTNode('IF', None)
        if_node.children = [condition_expr, if_body]
        return if_node

    def while_loop(self):
        """Reconoce y procesa un bucle 'while'."""
        self.eat('WHILE')
        self.eat('OPEN_PAREN')
        condition_expr = self.term()
        self.eat('CLOSE_PAREN')
        self.eat('OPEN_BRACE')
        while_body = self.assignment()  # Otras instrucciones
        self.eat('CLOSE_BRACE')

        while_node = ASTNode('WHILE', None)
        while_node.children = [condition_expr, while_body]
        return while_node

    def function_declaration(self):
        """Reconoce y procesa una declaración de función."""
        self.eat('FUNCTION')
        func_name = self.current_token()
        self.eat('IDENTIFIER')
        self.eat('OPEN_PAREN')

        params = []
        while self.current_token()[0] != 'CLOSE_PAREN':
            params.append(self.current_token())
            self.eat('IDENTIFIER')
            if self.current_token()[0] == 'COMMA':
                self.eat('COMMA')

        self.eat('CLOSE_PAREN')
        self.eat('OPEN_BRACE')
        func_body = self.assignment()  # Podrías agregar un ciclo aquí para más instrucciones
        self.eat('CLOSE_BRACE')

        func_node = ASTNode('FUNC_DECL', func_name[1])
        func_node.children = [params, func_body]
        return func_node

    def parse(self):
        # Añadir la detección de funciones
        if self.current_token()[0] == 'FUNCTION':
            return self.function_declaration()
        elif self.current_token()[0] == 'IF':
            return self.condition()
        elif self.current_token()[0] == 'WHILE':
            return self.while_loop()
        else:
            return self.assignment()  # Por ahora mantenemos asignaciones simples
class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}  # Tabla de símbolos para almacenar variables y funciones

    def analyze(self, node):
        if node.type == 'IDENTIFIER':
            if node.value not in self.symbol_table:
                raise NameError(f"Variable '{node.value}' no declarada.")
        elif node.type == 'ASSIGN':
            var_name = node.children[0].value
            self.symbol_table[var_name] = node.children[1].type  # Almacena el tipo de la variable
            print(f"Variable '{var_name}' asignada con valor de tipo {node.children[1].type}")
        elif node.type == 'OPERATION':
            for child in node.children:
                self.analyze(child)
        elif node.type == 'IF':
            # Verificar la validez de la condición
            self.analyze(node.children[0])  # Evaluar la expresión condicional
            self.analyze(node.children[1])  # Evaluar el cuerpo del if
        elif node.type == 'WHILE':
            # Verificar la validez de la condición en el bucle
            self.analyze(node.children[0])
            self.analyze(node.children[1])
        elif node.type == 'FUNC_DECL':
            # Verificar declaración de funciones
            func_name = node.value
            params = node.children[0]
            self.symbol_table[func_name] = {'params': params, 'body': node.children[1]}  # Guardar función en la tabla
            print(f"Función '{func_name}' declarada con {len(params)} parámetros.")

# Ejecutar el parser con los tokens generados anteriormente
parser = Parser(tokens)
ast = parser.parse()

# Imprimir el AST generado
def print_ast(node, indent=""):
    print(f"{indent}{node.type}: {node.value}")
    for child in node.children:
        print_ast(child, indent + "  ")


print("AST:")
print_ast(ast)


# Análisis semántico
class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}  # Tabla de símbolos para almacenar variables

    def analyze(self, node):
        if node.type == 'IDENTIFIER':
            if node.value not in self.symbol_table:
                raise NameError(f"Variable '{node.value}' no declarada.")
        elif node.type == 'ASSIGN':
            var_name = node.children[0].value
            self.symbol_table[var_name] = node.children[1].type  # Almacena el tipo de la variable
            print(f"Variable '{var_name}' asignada con valor de tipo {node.children[1].type}")
        elif node.type == 'OPERATION':
            for child in node.children:
                self.analyze(child)


# Simular el análisis semántico en un AST
semantic_analyzer = SemanticAnalyzer()
semantic_analyzer.analyze(ast)