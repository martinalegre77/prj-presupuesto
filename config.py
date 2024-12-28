# Configuración general (paths, constantes, etc.)

from tkinter import ttk


LOGO_PATH = "assets/logo.png"
PDF_OUTPUT_DIR = "output/"
ICONO = "assets/icono.ico"
ICONO_DRINK = "assets/icono_drink.ico"
ICONO_DESSERT = "assets/icono_dessert.ico"

# colores
BLUE_WILLOW = "#9cb3c5" 
STEEL_PINK = "#A13E97" 
TURQUESA = "#85b8cb"
PISTACHO = "#d1dddb" 

def valoresxy(root, wwin, hwin):
        wtotal = root.winfo_screenwidth()
        htotal = root.winfo_screenheight()
        vx = round(wtotal/2-wwin/2)
        vy = round(htotal/2-(hwin)/2)
        # return str(vx)+"+"+str(vy-30)
        return vx, vy


# Estilo para las pestañas
def style_notebook():
        style = ttk.Style()
        style.theme_use('default')  # Asegura que el tema sea personalizable
        
        # Configurar el color de fondo de las pestañas
        style.configure('TNotebook', background=TURQUESA, tabmargins=[2, 5, 2, 0])
        style.configure('TNotebook.Tab', background=PISTACHO, foreground='black', padding=[80, 10])
        style.map('TNotebook.Tab', background=[('selected', BLUE_WILLOW)])  # Color de pestaña activa

        # Color de fondo del contenido de las pestañas
        style.configure('TFrame', background=BLUE_WILLOW)