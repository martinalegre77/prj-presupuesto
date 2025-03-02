# Configuración general (paths, constantes, etc.)

import tkinter as tk
from tkinter import ttk

# RUTAS
LOGO_PATH = "assets/logo.png"
PDF_OUTPUT_DIR = "output/"
ICONO = "assets/icono.ico"
ICONO_DRINK = "assets/icono_drink.ico"
ICONO_DESSERT = "assets/icono_dessert.ico"

# COLORES DE VENTANAS
# BLUE_WILLOW = "#9cb3c5" 
STEEL_PINK = "#A13E97" 
# TURQUESA = "#85b8cb"
# PISTACHO = "#d1dddb" 

BARRA_TITULO = "#f3f3f3"
BARRA_MENU = "#bfdbff"
BARRA_TOOLS = "#b9cbe1"
TAPIZ = "#ece9d8"
FONDO_GIDGET = "#ffffff"
GRIS_BOTONES  = "#d9d9d9"

MILILITROS = [200, 250, 500, 700, 750, 800, 900, 1000, 1250] # ESTO DEBE IR EN LA DB

CANT_MILILITROS = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80] # ESTO DEBE IR EN LA DB

# FUNCIONES GENERALES

def valoresxy(root, wwin, hwin):
    # Para centrar ventanas
    wtotal = root.winfo_screenwidth()
    htotal = root.winfo_screenheight()
    vx = round(wtotal/2-wwin/2)
    vy = round(htotal/2-(hwin)/2)
    # return str(vx)+"+"+str(vy-30)
    return vx, vy


def style_notebook():
    style = ttk.Style()
    style.theme_use('default')  # Asegura que el tema sea personalizable
    
    # Estilo para las pestañas - Color de fondo
    style.configure('TNotebook', background=BARRA_MENU, tabmargins=[2, 5, 2, 0]) 
    style.configure('TNotebook.Tab', background=BARRA_TOOLS, foreground='black', padding=[80, 10]) 
    style.map('TNotebook.Tab', background=[('selected', TAPIZ)])  # Color de pestaña activa BLUE_WILLOW
    
    # Color de fondo del contenido de las pestañas
    style.configure('TFrame', background=TAPIZ)

    # Estilos adicionales para otros elementos
    style.configure("Trago.TCheckbutton", background=FONDO_GIDGET, foreground="black", font=("Arial", 12))
    style.configure("Accent.TButton", font=("Arial", 12, "bold"), foreground="black", background="#D9D9D9")
    style.configure("Treeview", rowheight=30, font=("Arial", 12), background="white", fieldbackground="white", foreground="black")  # Aumenta el alto de fila y la letra
    style.configure("Treeview.Heading", font=("Arial", 14, "bold"))  # Encabezados más grandes

    # Fondo para el Frame donde están los Checkbuttons
    style.configure("ScrollableFrame.TFrame", background=FONDO_GIDGET)

    # Fondo para el LabelFrame que contiene la lista
    style.configure("TragosFrame.TLabelframe", background=FONDO_GIDGET)
    style.configure("TragosFrame.TLabelframe.Label", background=FONDO_GIDGET, foreground="black")

    # Fondo para el Frame donde están los Checkbuttons
    style.configure("ComboBoxFrame.TLabelframe", background=GRIS_BOTONES, foreground="black")

    style.configure('TCombobox', 
                background=FONDO_GIDGET, 
                foreground='black', 
                fieldbackground=FONDO_GIDGET, 
                selectbackground=GRIS_BOTONES, 
                selectforeground='black', 
                font=("Arial", 12))



def on_close(root, modal):
    # Evento al cerrar la ventana 
    modal.destroy()
    root.geometry("300x370")  # Restaurar tamaño original de la ventana principal
    root.deiconify()  # Asegurarse de que la ventana principal se muestre correctamente


def increment(entry):
    # BOTON DE Incremento 
    value = float(entry.get()) if entry.get() else 0.0
    entry.delete(0, tk.END)
    entry.insert(0, f"{value + 1:.2f}")

def decrement(entry):
    # BOTON DE Decremento
    value = float(entry.get()) if entry.get() else 0.0
    entry.delete(0, tk.END)
    entry.insert(0, f"{max(value - 1, 0):.2f}")


def validate_numeric_input(new_value):
    # VALIDAR NUMEROS ENTEROS
    if new_value == "":
        return True  # Permite borrar el contenido
    return new_value.isdigit()  # Solo permite dígitos


def validate_float_input(new_value):
    # VALIDAR NUMEROS DECIMALES
    if new_value == "":
        return True  # Permite borrar el contenido
    try:
        float(new_value)
        return True  # Permite números enteros y decimales
    except ValueError:
        return False  # Rechaza cualquier otro valor


def valores_tipo(bebidas):
    # Crear lista con los tipos de bebidas
    valores_tipo = [bebida['tipo'].title() for bebida in bebidas if isinstance(bebida, dict) and 'tipo' in bebida]
    return valores_tipo