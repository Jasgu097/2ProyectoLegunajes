import tkinter as tk
from tkinter import messagebox

# Se importan las clases a utilizar
from prue1 import Parser
from prue1 import SemanticAnalyzer
from prue1 import lex


# Crear la ventana principal de la aplicación
root = tk.Tk()
root.title("Analizador Léxico y Sintáctico")

# Crear el área de texto para ingresar el código
code_input_label = tk.Label(root, text="Introduce el código:")
code_input_label.pack()

code_input = tk.Text(root, height=10, width=50)
code_input.pack()

# Crear áreas de texto para mostrar resultados
lexical_output_label = tk.Label(root, text="Resultado Léxico (Tokens):")
lexical_output_label.pack()

lexical_output = tk.Text(root, height=10, width=50, state=tk.DISABLED)
lexical_output.pack()

ast_output_label = tk.Label(root, text="Árbol Sintáctico (AST):")
ast_output_label.pack()

ast_output = tk.Text(root, height=10, width=50, state=tk.DISABLED)
ast_output.pack()

semantic_output_label = tk.Label(root, text="Resultado Semántico:")
semantic_output_label.pack()

semantic_output = tk.Text(root, height=10, width=50, state=tk.DISABLED)
semantic_output.pack()


# Función para analizar el código
def analyze_code():
    code = code_input.get("1.0", tk.END)

    try:
        # Análisis léxico
        tokens = lex(code)  # Utiliza tu función léxica
        display_lexical(tokens)

        # Análisis sintáctico
        parser = Parser(tokens)  # Utiliza tu parser
        ast = parser.parse()
        display_ast(ast)

        # Análisis semántico
        semantic_analyzer = SemanticAnalyzer()  # Utiliza tu analizador semántico
        semantic_analyzer.analyze(ast)
        display_semantic(semantic_analyzer.symbol_table)

    except SyntaxError as e:
        messagebox.showerror("Error", f"Error de análisis: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado: {e}")


# Funciones para mostrar los resultados
def display_lexical(tokens):
    lexical_output.config(state=tk.NORMAL)
    lexical_output.delete("1.0", tk.END)
    for token in tokens:
        lexical_output.insert(tk.END, f"{token}\n")
    lexical_output.config(state=tk.DISABLED)


def display_ast(node, indent=""):
    ast_output.config(state=tk.NORMAL)
    ast_output.delete("1.0", tk.END)
    _display_ast_recursive(node, indent)
    ast_output.config(state=tk.DISABLED)


def _display_ast_recursive(node, indent=""):
    ast_output.insert(tk.END, f"{indent}{node.type}: {node.value}\n")
    for child in node.children:
        _display_ast_recursive(child, indent + "  ")


def display_semantic(symbol_table):
    semantic_output.config(state=tk.NORMAL)
    semantic_output.delete("1.0", tk.END)
    for var, var_type in symbol_table.items():
        semantic_output.insert(tk.END, f"Variable '{var}' asignada con tipo {var_type}\n")
    semantic_output.config(state=tk.DISABLED)


# Botón para el análisis
analyze_button = tk.Button(root, text="Analizar", command=analyze_code)
analyze_button.pack()

# Inicia la interfaz
root.mainloop()
