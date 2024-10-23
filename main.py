import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Para usar Scrollbar más fácilmente

# Se importan las clases a utilizar
from prue1 import Parser
from prue1 import SemanticAnalyzer
from prue1 import lex


# Crear la ventana principal de la aplicación
root = tk.Tk()
root.title("Analizador Léxico y Sintáctico")

# Hacer que la ventana sea redimensionable
root.geometry("600x400")  # Puedes ajustar el tamaño inicial aquí
root.resizable(True, True)  # Permitir que la ventana se redimensione

# Crear un frame con scrollbar para el contenido
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Añadir un canvas para incluir el scrollbar
canvas = tk.Canvas(main_frame)
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

# Conectar el canvas con el scrollbar
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Empaquetar el canvas y el scrollbar
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Crear el área de texto para ingresar el código
code_input_label = tk.Label(scrollable_frame, text="Introduce el código:")
code_input_label.pack()

code_input = tk.Text(scrollable_frame, height=10, width=50)
code_input.pack()

# Crear áreas de texto para mostrar resultados
lexical_output_label = tk.Label(scrollable_frame, text="Resultado Léxico (Tokens):")
lexical_output_label.pack()

lexical_output = tk.Text(scrollable_frame, height=10, width=50, state=tk.DISABLED)
lexical_output.pack()

ast_output_label = tk.Label(scrollable_frame, text="Árbol Sintáctico (AST):")
ast_output_label.pack()

ast_output = tk.Text(scrollable_frame, height=10, width=50, state=tk.DISABLED)
ast_output.pack()

semantic_output_label = tk.Label(scrollable_frame, text="Resultado Semántico:")
semantic_output_label.pack()

semantic_output = tk.Text(scrollable_frame, height=10, width=50, state=tk.DISABLED)
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
    lexical_output.delete(1.0, tk.END)
    lexical_output.insert(tk.END, str(tokens))
    lexical_output.config(state=tk.DISABLED)


def display_ast(ast):
    ast_output.config(state=tk.NORMAL)
    ast_output.delete(1.0, tk.END)
    ast_output.insert(tk.END, str(ast))
    ast_output.config(state=tk.DISABLED)


def display_semantic(symbol_table):
    semantic_output.config(state=tk.NORMAL)
    semantic_output.delete(1.0, tk.END)
    semantic_output.insert(tk.END, str(symbol_table))
    semantic_output.config(state=tk.DISABLED)


# Crear el botón para ejecutar el análisis
analyze_button = tk.Button(scrollable_frame, text="Analizar", command=analyze_code)
analyze_button.pack()

# Ejecutar la ventana principal
root.mainloop()
