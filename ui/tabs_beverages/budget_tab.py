
import tkinter as tk
from tkinter import ttk
import config
from models import TragosModel

class BudgetTab:
    def __init__(self, parent, master):
        self.parent = parent  # Referencia al Notebook donde se agregará la pestaña
        self.master = master  # Referencia a la ventana principal
        self.frame = ttk.Frame(self.parent, style=config.style_notebook())
        
        # Obtengo todos los tragos
        self.tragos_model = TragosModel()
        self.tragos = self.tragos_model.read_all()
        
        # Diccionario para almacenar los estados de los checkboxes
        self.selected_tragos = {}
        
        # Creación de la interfaz 
        self.setup_ui()

    def setup_ui(self):
        # Aplicar estilos
        config.style_notebook()

        # interfaz de la pestaña
        self.frame.pack(expand=True, fill="both")

        # Contenedor principal centrado
        container = ttk.Frame(self.frame, padding=20)
        container.place(relx=0.5, rely=0.3, anchor="center")

        # Título
        title_label = tk.Label(container, text="PRESUPUESTO", bg=config.TAPIZ, font=("Arial", 18, "bold"))
        title_label.pack(pady=15)

        # Marco con borde para la lista de tragos
        tragos_frame = ttk.LabelFrame(container, text="Selecciona los tragos", padding=10)
        tragos_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Contenedor con Scrollbar
        list_frame = ttk.Frame(tragos_frame, style="ScrollableFrame.TFrame")
        list_frame.pack(expand=True, fill="both")

        canvas = tk.Canvas(list_frame, height=250, bg=config.FONDO_GIDGET)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="ScrollableFrame.TFrame")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mostrar lista de tragos con Checkbuttons
        for trago in self.tragos:
            trago_nombre = trago["nombre"].capitalize()
            var = tk.BooleanVar()
            self.selected_tragos[trago_nombre] = var  # Asociar el Checkbutton a la variable

            
            chk = ttk.Checkbutton(scrollable_frame, text=trago_nombre, variable=var, style="Trago.TCheckbutton")
            chk.pack(anchor="w", padx=10, pady=5) # Espaciado entre filas

            chk.configure(style="Trago.TCheckbutton")

        # Botón para generar presupuesto
        btn_generar = ttk.Button(
            container, text="Generar Presupuesto", command=self.generate_budget, style="Accent.TButton"
        )
        btn_generar.pack(pady=15, ipadx=10, ipady=5)


    def get_selected_tragos(self):
        """Devuelve una lista con los tragos seleccionados."""
        return [trago for trago, var in self.selected_tragos.items() if var.get()]
        

    def generate_budget(self):
        """
        Lógica para generar presupuesto.
        """
        seleccionados = self.get_selected_tragos()
        print("Generar presupuesto")