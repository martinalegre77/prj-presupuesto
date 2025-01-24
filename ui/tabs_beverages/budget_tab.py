
import tkinter as tk
from tkinter import ttk

import config

class BudgetTab:
    def __init__(self, parent, master):
        self.parent = parent  # Referencia al Notebook donde se agregará la pestaña
        self.master = master  # Referencia a la ventana principal
        self.frame = ttk.Frame(self.parent, style=config.style_notebook())
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.frame, text="PRESUPUESTO", bg=config.TAPIZ, font=("Arial", 14, "bold")).pack(ipady=25)
        # Frame principal para organizar tabla y botones
        main_frame = ttk.Frame(self.frame, style=config.style_notebook())
        main_frame.pack(expand=True, fill='both')  # Ocupa toda la pestaña

        tk.Label(main_frame, text="Cantidad de tragos", bg=config.TAPIZ).pack()
        tk.Entry(main_frame).pack()
        tk.Label(main_frame, text="Cantidad de personas", bg=config.TAPIZ).pack()
        tk.Entry(main_frame).pack()
        tk.Button(main_frame, text="Generar Presupuesto", command=self.generate_budget).pack()

    def generate_budget(self):
        """
        Lógica para generar presupuesto.
        """
        print("Generar presupuesto")