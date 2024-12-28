# Ventanas/pestañas para gestión de postres.

import tkinter as tk
from tkinter import ttk

class DessertsWindow:
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("Presupuesto de Postres")

        tabs = ttk.Notebook(self.window)
        self.update_tab = ttk.Frame(tabs)
        self.budget_tab = ttk.Frame(tabs)

        tabs.add(self.update_tab, text="Actualizar Postres")
        tabs.add(self.budget_tab, text="Generar Presupuesto")
        tabs.pack(expand=1, fill="both")

        self.setup_update_tab()
        self.setup_budget_tab()

    def setup_update_tab(self):
        tk.Label(self.update_tab, text="Editar Ingredientes").pack()

    def setup_budget_tab(self):
        tk.Label(self.budget_tab, text="Cantidad de porciones").pack()
        tk.Entry(self.budget_tab).pack()
        tk.Label(self.budget_tab, text="Cantidad de personas").pack()
        tk.Entry(self.budget_tab).pack()
        tk.Button(self.budget_tab, text="Generar Presupuesto").pack()
