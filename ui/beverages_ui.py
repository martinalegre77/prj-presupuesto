
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import config
from models import BebidasModel, PresupuestoBebidaModel, TragosModel

# Crear instancias de los modelos
presupuesto_model = PresupuestoBebidaModel()
bebidas_model = BebidasModel()
tragos_model = TragosModel()

class BeveragesWindow:

    def __init__(self, master):
        self.window = tk.Toplevel(master) # crea ventana secundaria"
        self.window.title("Barra de tragos")
        self.window.iconbitmap(config.ICONO_DRINK)
        self.window.state('zoomed') # maximizar 
        # self.window.attributes('-zoomed', True)  # Linux/macOS

        tabs = ttk.Notebook(self.window) # ventana para pestañas
        self.budget_tab = ttk.Frame(tabs, style=config.style_notebook()) # pestaña 1
        self.drink_tab = ttk.Frame(tabs, style=config.style_notebook()) # pestaña 2
        self.beverage_tab = ttk.Frame(tabs, style=config.style_notebook()) # pestaña 3

        tabs.add(self.budget_tab, text="Presupuesto") # agrega la pestaña y el titulo
        tabs.add(self.drink_tab, text="Bebidas") 
        tabs.add(self.beverage_tab, text="Tragos") 
        tabs.pack(expand=1, fill="both") # empaquetado

        self.setup_budget_tab()
        self.setup_drink_tab()
        self.setup_beverage_tab()

        tabs.focus() # hace foco en la ventana actual
        tabs.grab_set() # no permite interacción con la ventana principal


    def setup_budget_tab(self):
        """
        Pestaña para realizar presupuestos de barra de bebidas
        """
        tk.Label(self.budget_tab, text="Cantidad de tragos").pack()
        tk.Entry(self.budget_tab).pack()
        tk.Label(self.budget_tab, text="Cantidad de personas").pack()
        tk.Entry(self.budget_tab).pack()
        tk.Button(self.budget_tab, text="Generar Presupuesto").pack()


    def setup_drink_tab(self):
        """
        Pestaña para gestión de bebidas para realizar los tragos
        """
        bebidas = bebidas_model.read_all()

        tk.Label(self.drink_tab, text="LISTA DE BEBIDAS", bg=config.BLUE_WILLOW, font=("Arial", 14, "bold")).pack(ipady=25)

        # Estilo de la tabla
        style = ttk.Style()
        style.configure("Treeview", rowheight=30)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        #  Frame para la tabla y el scrollbar
        table_frame = ttk.Frame(self.drink_tab)
        table_frame.pack(padx=100, pady=5)

        # Tabla con Scrollbar
        self.tree = ttk.Treeview(table_frame, columns=("Tipo", "Nombre", "Presentación", "Costo", "Venta"), show="headings", height=10)
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Presentación", text="Presentación")
        self.tree.heading("Costo", text="Costo")
        self.tree.heading("Venta", text="Venta")

        # Ajustar el ancho de las columnas
        self.tree.column("Tipo", width=160)
        self.tree.column("Nombre", width=220)
        self.tree.column("Presentación", width=160)
        self.tree.column("Costo", width=120)
        self.tree.column("Venta", width=120)

        # Barra de desplazamiento
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side='left', fill='x', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Llenar la tabla
        self.populate_table(bebidas)

        # Botones de acción
        self.button_frame = ttk.Frame(self.drink_tab)
        self.button_frame.pack(padx=200, pady=30, fill='x')

        self.add_button = ttk.Button(self.button_frame, text="Agregar Bebida", command=self.add_item, cursor='hand2')
        self.add_button.pack(side='left', padx=5, pady=5, expand=True)

        self.modify_button = ttk.Button(self.button_frame, text="Modificar Bebida", command=self.modify_item, cursor='hand2')
        self.modify_button.pack(side='left', padx=5, pady=5, expand=True)

        self.delete_button = ttk.Button(self.button_frame, text="Eliminar Bebida", command=self.delete_item, cursor='hand2')
        self.delete_button.pack(side='left', padx=5, pady=5, expand=True)

    def populate_table(self, bebidas):
        for bebida in bebidas:
            item_id = self.tree.insert("", "end", values=(
                f"     {bebida['tipo'].capitalize()}",
                f"     {bebida['nombre'].capitalize()}",
                f"          {bebida['presentacion']} ml",
                f"          $ {bebida['precio_compra']}",
                f"          $ {bebida['precio_venta']}"
            ))

    # Agregar nueva bebida
    def add_item(self):
        messagebox.showinfo("Agregar", "Abrir ventana para agregar una nueva bebida.")

    # Modificar bebida seleccionada
    def modify_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Sin Selección", "Por favor selecciona una bebida para modificar.")
            return
        
        bebida = self.tree.item(selected_item, "values")
        messagebox.showinfo("Modificar Bebida", f"Modificando la bebida: {bebida[1]}")

    # Eliminar bebida seleccionada
    def delete_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Sin Selección", "Por favor selecciona una bebida para eliminar.")
            return
        
        confirm = messagebox.askyesno("Eliminar Bebida", "¿Estás seguro de que deseas eliminar esta bebida?")
        if confirm:
            self.tree.delete(selected_item)
            messagebox.showinfo("Eliminado", "La bebida ha sido eliminada correctamente.")

    # TRAGOS
    def setup_beverage_tab(self):
        """
        Pestaña para gestionar los tragos y sus ingredientes
        """
        tragos = tragos_model.read_all()
        
        tk.Label(self.beverage_tab, text="LISTA DE TRAGOS", bg=config.BLUE_WILLOW, font=("Arial", 14, "bold")).pack(ipady=25)

