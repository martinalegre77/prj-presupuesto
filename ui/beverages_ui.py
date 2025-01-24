
import tkinter as tk
from tkinter import ttk
# from tkinter import messagebox
import config
# from models import BebidasModel, PresupuestoBebidaModel, TragosModel
from .tabs_beverages.budget_tab import BudgetTab
from .tabs_beverages.drink_tab import DrinkTab
from .tabs_beverages.beverage_tab import BeverageTab

# Crear instancias de los modelos
# presupuesto_model = PresupuestoBebidaModel()
# bebidas_model = BebidasModel()
# tragos_model = TragosModel()

class BeveragesWindow:
    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel(self.master) # crea ventana secundaria"
        self.window.title("Barra de tragos")
        self.window.iconbitmap(config.ICONO_DRINK)
        self.window.state('zoomed') # maximizar 
        # self.window.attributes('-zoomed', True)  # Linux/macOS
        
        # Crear y configurar las pestañas
        tabs = ttk.Notebook(self.window) 

        # Instanciar cada pestaña
        self.budget_tab = BudgetTab(tabs, self.master)
        self.drink_tab = DrinkTab(tabs, self.master)
        self.beverage_tab = BeverageTab(tabs, self.master)
        # self.budget_tab = ttk.Frame(tabs, style=config.style_notebook()) # pestaña 1
        # self.drink_tab = ttk.Frame(tabs, style=config.style_notebook()) # pestaña 2
        # self.beverage_tab = ttk.Frame(tabs, style=config.style_notebook()) # pestaña 3

        # Agregar pestañas al notebook
        tabs.add(self.budget_tab.frame, text="Presupuesto")
        tabs.add(self.drink_tab.frame, text="Bebidas")
        tabs.add(self.beverage_tab.frame, text="Tragos")
        tabs.pack(expand=1, fill="both")
        # tabs.add(self.budget_tab, text="Presupuesto") # agrega la pestaña y el titulo
        # tabs.add(self.drink_tab, text="Bebidas") 
        # tabs.add(self.beverage_tab, text="Tragos") 
        # tabs.pack(expand=1, fill="both") # empaquetado

        # self.setup_budget_tab()
        # self.setup_drink_tab()
        # self.setup_beverage_tab()

        tabs.focus() # hace foco en la ventana actual
        tabs.grab_set() # no permite interacción con la ventana principal

        # Maximizar root al cerrar ésta ventana
        self.window.protocol("WM_DELETE_WINDOW", lambda: config.on_close(self.master, self.window))


    ### PRESUPUESTO ###
    # def setup_budget_tab(self):
    #     """
    #     Pestaña para realizar presupuestos de barra de bebidas
    #     """

    #     # self.budget_tab.focus_force()

    #     tk.Label(self.budget_tab, text="Cantidad de tragos").pack()
    #     tk.Entry(self.budget_tab).pack()
    #     tk.Label(self.budget_tab, text="Cantidad de personas").pack()
    #     tk.Entry(self.budget_tab).pack()
    #     tk.Button(self.budget_tab, text="Generar Presupuesto").pack()


    """### BEBIDAS ###
    def setup_drink_tab(self):

        # self.drink_tab.focus_force()

        # Obtengo todas las bebidas
        bebidas = bebidas_model.read_all()

        tk.Label(self.drink_tab, text="LISTA DE BEBIDAS", bg=config.BLUE_WILLOW, font=("Arial", 14, "bold")).pack(ipady=25)

        # Frame principal para organizar tabla y botones
        main_frame = ttk.Frame(self.drink_tab)
        main_frame.pack(expand=True, fill='both')  # Ocupa toda la pestaña

        # Centrar el contenido con grid
        main_frame.columnconfigure(0, weight=1)  # Columna izquierda para espacio vacío
        main_frame.columnconfigure(1, weight=0)  # Columna central para el contenido
        main_frame.columnconfigure(2, weight=1)  # Columna derecha para espacio vacío

        # Frame para la tabla (Treeview + Scrollbar)
        table_frame = ttk.Frame(main_frame)
        table_frame.grid(row=0, column=1, sticky='n', padx=10, pady=10)

        # Tabla (Treeview) con Scrollbar
        self.tree = ttk.Treeview(table_frame, columns=("id", "Tipo", "Nombre", "Presentación", "Costo", "Venta"), show="headings", height=10)
        self.tree.heading("id", text="ID")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Presentación", text="Presentación")
        self.tree.heading("Costo", text="Costo")
        self.tree.heading("Venta", text="Venta")

        # Ajustar el ancho de las columnas
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("Tipo", width=160)
        self.tree.column("Nombre", width=220)
        self.tree.column("Presentación", width=160)
        self.tree.column("Costo", width=120)
        self.tree.column("Venta", width=120)

        # Barra de desplazamiento para la tabla
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side='left', fill='both')
        scrollbar.pack(side='right', fill='y')

        # Llenar la tabla
        self.populate_table(bebidas)

        # Botones de acción
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=1, pady=20, sticky="ew")  # Alineación arriba y expandido horizontalmente

        # Botones dentro del frame
        add_button = ttk.Button(button_frame, text="Agregar Bebida", command=self.add_item, cursor='hand2')
        add_button.grid(row=0, column=0, padx=10, sticky="ew")

        modify_button = ttk.Button(button_frame, text="Modificar Bebida", command=self.modify_item, cursor='hand2')
        modify_button.grid(row=0, column=1, padx=10, sticky="ew")

        delete_button = ttk.Button(button_frame, text="Eliminar Bebida", command=self.delete_item, cursor='hand2')
        delete_button.grid(row=0, column=2, padx=10, sticky="ew")

        # Ajustar las columnas del frame
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)


    # Llenar la tabla con los datos
    def populate_table(self, bebidas):
        # Limpiar la tabla antes de llenarla
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insertar las bebidas en la tabla
        for bebida in bebidas:
            self.tree.insert("", "end", values=(
                bebida['id'],
                f"     {bebida['tipo'].capitalize()}",
                f"     {bebida['nombre'].capitalize()}",
                f"          {bebida['presentacion']} ml",
                f"          $ {bebida['precio_compra']}",
                f"          $ {bebida['precio_venta']}"
            ))

    # Agregar nueva bebida
    def add_item(self):
        # Ventana para agregar una bebida
        modal = tk.Toplevel(self.drink_tab)
        modal.title("Agregar Bebida")
        window_width = 360
        window_height = 250
        vx, vy = config.valoresxy(self.drink_tab, window_width, window_height)
        modal.geometry(str(window_width)+"x"+str(window_height)+"+"+str(vx)+"+"+str(vy-30))
        modal.transient(self.drink_tab)
        modal.iconbitmap(config.ICONO_DRINK)
        modal.focus() 
        modal.grab_set()

        # Crear campos de edición
        tk.Label(modal, text="Tipo").grid(row=0, column=0, padx=10, pady=5)
        tipo_combobox = ttk.Combobox(modal, values=config.TIPO)
        tipo_combobox.set(config.TIPO[0])
        tipo_combobox.grid(row=0, column=1, padx=(15, 5), pady=5)

        tk.Label(modal, text="Nombre").grid(row=1, column=0, padx=10, pady=5)
        nombre_entry = tk.Entry(modal)
        nombre_entry.insert(0, "")
        nombre_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(modal, text="Presentación - ml").grid(row=2, column=0, padx=10, pady=5)
        presentacion_combobox = ttk.Combobox(modal, values=config.MILILITROS, state='readonly')
        presentacion_combobox.set(config.MILILITROS[0])
        presentacion_combobox.grid(row=2, column=1, padx=(15, 5), pady=5)

        # Configurar validación
        vcmd = modal.register(config.validate_float_input)

        tk.Label(modal, text="Costo - $").grid(row=3, column=0, padx=10, pady=5)
        costo_entry = tk.Entry(modal, validate="key", validatecommand=(vcmd, "%P"))
        costo_entry.insert(0, "1.00")
        costo_entry.grid(row=3, column=1, padx=10, pady=5)

        costo_inc_btn = tk.Button(modal, text="+", command=lambda: config.increment(costo_entry), width=2)
        costo_inc_btn.grid(row=3, column=2, padx=5, pady=5)
        costo_dec_btn = tk.Button(modal, text="-", command=lambda: config.decrement(costo_entry), width=2)
        costo_dec_btn.grid(row=3, column=3, padx=5, pady=5)

        tk.Label(modal, text="Venta - $").grid(row=4, column=0, padx=10, pady=5)
        venta_entry = tk.Entry(modal, validate="key", validatecommand=(vcmd, "%P"))
        venta_entry.insert(0, "1.00")
        venta_entry.grid(row=4, column=1, padx=10, pady=5)

        venta_inc_btn = tk.Button(modal, text="+", command=lambda: config.increment(venta_entry), width=2)
        venta_inc_btn.grid(row=4, column=2, padx=5, pady=5)
        venta_dec_btn = tk.Button(modal, text="-", command=lambda: config.decrement(venta_entry), width=2)
        venta_dec_btn.grid(row=4, column=3, padx=5, pady=5)
        
        # Guardar datos
        def save_drink():
            try:
                bebidas_model.create(
                    {
                        'tipo': tipo_combobox.get(),
                        'nombre': nombre_entry.get(),
                        'presentacion': presentacion_combobox.get(),
                        'precio_compra': float(costo_entry.get()),
                        'precio_venta': float(venta_entry.get())
                    }
                )
                self.master.iconify()
                modal.destroy()
                messagebox.showinfo("Éxito", "Bebida agregada correctamente.")
                # Devolver el foco a la pestaña de bebidas
                self.drink_tab.focus_force()
                # Actualizar en el TreeView
                for row in self.tree.get_children():
                    self.tree.delete(row)
                # Llenar la tabla
                bebidas = bebidas_model.read_all()
                self.populate_table(bebidas)
            except ValueError:
                messagebox.showerror("Error", "Los valores de Costo y Venta deben ser números válidos.")

        # Guardar cambios
        tk.Button(modal, text="  Guardar  ", command=save_drink).grid(row=5, column=1, columnspan=1, pady=20)

    # Modificar bebida 
    def modify_item(self):

        selected_item = self.tree.selection()

        if not selected_item:
            self.master.iconify()
            messagebox.showwarning("Sin Selección", "Por favor selecciona una bebida para modificar.")
            return
        
        # Obtener el ID desde los metadatos del TreeView
        selected_item = selected_item[0]
        id_item = self.tree.set(selected_item, 'id')

        if not id_item:
            messagebox.showerror("Error", "No se encontró la bebida seleccionada.")
            return
        
        # Obtener datos de la base de datos usando el ID
        bebida = bebidas_model.read_by_id(int(id_item))

        if not bebida:
            messagebox.showerror("Error", "No se pudo encontrar la bebida en la base de datos.")
            return

        # Ventana para modificar los valores
        modal = tk.Toplevel(self.drink_tab)
        modal.title("Modificar Bebida")
        window_width = 360
        window_height = 250
        vx, vy = config.valoresxy(self.drink_tab, window_width, window_height)
        modal.geometry(str(window_width)+"x"+str(window_height)+"+"+str(vx)+"+"+str(vy-30))
        modal.transient(self.drink_tab)
        modal.iconbitmap(config.ICONO_DRINK)
        modal.focus() 
        modal.grab_set()

        # Crear campos de edición
        tk.Label(modal, text="Tipo").grid(row=0, column=0, padx=10, pady=5)
        tipo_combobox = ttk.Combobox(modal, values=config.TIPO)
        tipo_combobox.set(bebida['tipo'])
        tipo_combobox.grid(row=0, column=1, padx=(15, 5), pady=5)

        tk.Label(modal, text="Nombre").grid(row=1, column=0, padx=10, pady=5)
        nombre_entry = tk.Entry(modal)
        nombre_entry.insert(0, bebida['nombre'])
        nombre_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(modal, text="Presentación - ml").grid(row=2, column=0, padx=10, pady=5)
        presentacion_combobox = ttk.Combobox(modal, values=config.MILILITROS, state='readonly')
        presentacion_combobox.set(bebida['presentacion'])
        presentacion_combobox.grid(row=2, column=1, padx=(15, 5), pady=5)

        tk.Label(modal, text="Costo - $").grid(row=3, column=0, padx=10, pady=5)
        costo_entry = tk.Entry(modal)
        costo_entry.insert(0, bebida['precio_compra'])
        costo_entry.grid(row=3, column=1, padx=10, pady=5)

        costo_inc_btn = tk.Button(modal, text="+", command=lambda: config.increment(costo_entry), width=2)
        costo_inc_btn.grid(row=3, column=2, padx=5, pady=5)
        costo_dec_btn = tk.Button(modal, text="-", command=lambda: config.decrement(costo_entry), width=2)
        costo_dec_btn.grid(row=3, column=3, padx=5, pady=5)

        tk.Label(modal, text="Venta - $").grid(row=4, column=0, padx=10, pady=5)
        venta_entry = tk.Entry(modal)
        venta_entry.insert(0, bebida['precio_venta'])
        venta_entry.grid(row=4, column=1, padx=10, pady=5)

        venta_inc_btn = tk.Button(modal, text="+", command=lambda: config.increment(venta_entry), width=2)
        venta_inc_btn.grid(row=4, column=2, padx=5, pady=5)
        venta_dec_btn = tk.Button(modal, text="-", command=lambda: config.decrement(venta_entry), width=2)
        venta_dec_btn.grid(row=4, column=3, padx=5, pady=5)
        
        # Guardar cambios
        def save_changes():
        # Actualizar en la base de datos
            try:
                bebidas_model.update(
                    int(id_item),
                    {
                        'tipo': tipo_combobox.get(),
                        'nombre': nombre_entry.get(),
                        'presentacion': presentacion_combobox.get(),
                        'precio_compra': float(costo_entry.get()),
                        'precio_venta': float(venta_entry.get())
                    }
                )
                # Minimizar la ventana principal
                self.master.iconify()
                modal.destroy()
                messagebox.showinfo("Éxito", "Bebida modificada correctamente.")
                # Devolver el foco a la pestaña de bebidas
                self.drink_tab.focus_force()
                # Actualizar en el TreeView
                for row in self.tree.get_children():
                    self.tree.delete(row)
                # Llenar la tabla
                bebidas = bebidas_model.read_all()
                self.populate_table(bebidas)
            except ValueError:
                messagebox.showerror("Error", "Los valores de Costo y Venta deben ser números válidos.")

        # Botón Guardar cambios
        tk.Button(modal, text="  Guardar  ", command=save_changes).grid(row=5, column=1, columnspan=1, pady=20)

    # Eliminar bebida 
    def delete_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            self.master.iconify()
            messagebox.showwarning("Sin Selección", "Por favor selecciona una bebida para eliminar.")
            # Devolver el foco a la pestaña de bebidas
            self.drink_tab.focus_force()
            return
        
        confirm = messagebox.askyesno("Eliminar Bebida", "¿Estás seguro de que deseas eliminar esta bebida?")
        if confirm:
            try:
                # Obtener el ID desde los metadatos del TreeView
                selected_item = selected_item[0]
                id_item = self.tree.set(selected_item, 'id')
                bebidas_model.delete(int(id_item))
                # Minimizar la ventana principal
                # self.master.iconify()
                messagebox.showinfo("Eliminado", "La bebida ha sido eliminada correctamente.")
                # Devolver el foco a la pestaña de bebidas
                self.drink_tab.focus_force()
                # Actualizar en el TreeView
                for row in self.tree.get_children():
                    self.tree.delete(row)
                # Llenar la tabla
                bebidas = bebidas_model.read_all()
                self.populate_table(bebidas)
            except ValueError:
                messagebox.showerror("Error", "La bebida no se pudo eliminar.") """


    ### TRAGOS ### 
    """
    def setup_beverage_tab(self):

        # self.beverage_tab.focus_force()

        tragos = tragos_model.read_all()
        
        tk.Label(self.beverage_tab, text="LISTA DE TRAGOS", bg=config.BLUE_WILLOW, font=("Arial", 14, "bold")).pack(ipady=25)

        # Frame principal para organizar tabla y combobox
        main_frame = ttk.Frame(self.beverage_tab)
        main_frame.pack(expand=True, fill='both')  # Ocupa toda la pestaña

        # Centrar el contenido con grid
        main_frame.columnconfigure(0, weight=1)  # Columna izquierda para espacio vacío
        main_frame.columnconfigure(1, weight=0)  # Columna central para el contenido
        main_frame.columnconfigure(2, weight=1)  # Columna derecha para espacio vacío

        # Frame para tabla (Treeview + Scrollbar) y Combobox juntos
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=0, column=1, sticky='n', padx=10, pady=10)

        # Tabla (Treeview) con Scrollbar
        table_frame = ttk.Frame(content_frame)
        table_frame.pack(side='left', padx=10, anchor="n")

        self.tree = ttk.Treeview(table_frame, columns=("id", "Nombre", "Ingredientes"), show="headings", height=10)
        self.tree.heading("id", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Ingredientes", text="Ingredientes")

        # Ajustar el ancho de las columnas
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("Nombre", width=220)
        self.tree.column("Ingredientes", width=150, anchor="center")

        # Barra de desplazamiento para la tabla
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side='left', fill='both')
        scrollbar.pack(side='right', fill='y')

        # Llenar la tabla con datos
        self.populate_table_beverage(tragos)

        # Combobox para ingredientes (a la derecha del scrollbar)
        combobox_frame = ttk.Frame(content_frame)
        combobox_frame.pack(side='left', padx=10, anchor="n")

        tk.Label(combobox_frame, text="Detalle", font=("Arial", 12, "bold")).pack(pady=5)
        self.ingredientes_combobox = ttk.Combobox(combobox_frame, state="readonly", width=40,)
        self.ingredientes_combobox.pack(pady=10, fill='x')
        self.ingredientes_combobox.set("Seleccione un trago")

        # Botones de acción
        self.button_frame = ttk.Frame(main_frame)
        self.button_frame.grid(row=1, column=1, pady=20, sticky="ew")  # Alineación arriba y expandido horizontalmente

        # Botones dentro del frame
        add_button = ttk.Button(self.button_frame, text="Agregar Trago", command=self.add_beverage)
        add_button.grid(row=0, column=0, padx=10, sticky="ew")

        edit_button = ttk.Button(self.button_frame, text="Editar Trago", command=self.modify_beverage)
        edit_button.grid(row=0, column=1, padx=10, sticky="ew")

        delete_button = ttk.Button(self.button_frame, text="Eliminar Trago", command=self.delete_beverage)
        delete_button.grid(row=0, column=2, padx=10, sticky="ew")

        # Ajustar las columnas del frame
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)


    # Llenar la tabla con los datos
    def populate_table_beverage(self, tragos):
        for trago in tragos:
            self.tree.insert("", "end", values=(
                trago['id'],
                f"      {trago['nombre'].capitalize()}",
                trago['cantidad_ingredientes'],
            ))

        def on_tree_selection(event):

            selected_item = self.tree.selection()
            bebidas = bebidas_model.read_all()

            if selected_item:
                item = self.tree.item(selected_item)
                trago_id = item['values'][0]  # Capturar el ID del trago seleccionado
                
                # Buscar el trago por ID
                trago = next((t for t in tragos if t['id'] == trago_id), None)

                if trago:
                    # Formatear los detalles de los ingredientes usando el ID de la bebida
                    ingredientes = []
                    for ing in trago['ingredientes']:
                        # Buscar la bebida por su ID en la lista 'bebidas'
                        bebida = next((b for b in bebidas if b['id'] == ing['bebida_id']), None)
                        if bebida:
                            ingrediente_str = f"{bebida['tipo'].capitalize()} - {bebida['nombre']} - {ing['cantidad']} ml"
                            ingredientes.append(ingrediente_str)

                    if ingredientes:
                        self.ingredientes_combobox['values'] = ingredientes
                        self.ingredientes_combobox.set("Despliegue para ver los ingredientes")
                    else:
                        self.ingredientes_combobox['values'] = ["Sin ingredientes"]
                        self.ingredientes_combobox.set("Sin ingredientes")

        # Asociar el evento al TreeView
        self.tree.bind("<<TreeviewSelect>>", on_tree_selection)

    # Agregar nuevo trago
    def add_beverage(self):
        # Ventana para agregar un trago
        modal = tk.Toplevel(self.beverage_tab)
        modal.title("Agregar Trago")
        window_width = 450
        window_height = 350
        vx, vy = config.valoresxy(self.beverage_tab, window_width, window_height)
        modal.geometry(str(window_width)+"x"+str(window_height)+"+"+str(vx)+"+"+str(vy-30))
        modal.transient(self.beverage_tab)
        modal.iconbitmap(config.ICONO_DRINK)
        modal.focus() 
        modal.grab_set()

        # Obtener las bebidas
        bebidas = bebidas_model.read_all()

        # Crear lista de bebidas en formato "Tipo - Nombre"
        bebidas_list = [f"{bebida['tipo'].capitalize()} - {bebida['nombre']}" for bebida in bebidas]

        # Crear campos de edición
        tk.Label(modal, text="Nombre").grid(row=0, column=0, padx=10, pady=5)
        nombre_entry = tk.Entry(modal)
        nombre_entry.insert(0, "")
        nombre_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(modal, text="Cantidad de ingredientes").grid(row=1, column=0, padx=10, pady=5)
        # Guardar cantidad_combobox como atributo de la clase
        cantidad_combobox = ttk.Combobox(modal, values=list(range(1, 8)), state="readonly")  # Hasta 7 ingredientes
        cantidad_combobox.set("1")
        cantidad_combobox.grid(row=1, column=1, padx=(15, 5), pady=5)

        # Contenedor dinámico para los ingredientes
        ingredientes_frame = ttk.Frame(modal)
        ingredientes_frame.grid(row=2, column=0, columnspan=2, padx=30, pady=10)

        def update_ingredient_fields(event, cantidad_combobox):
            # try:
            #     # Validar si el widget aún existe antes de usarlo
            #     if cantidad_combobox is None or not cantidad_combobox.winfo_exists():
            #         print("El combobox no existe o ha sido destruido.")
            #         return

            # Obtener la cantidad seleccionada
            cantidad = int(cantidad_combobox.get())

            # Limpiar el contenedor de ingredientes
            for widget in ingredientes_frame.winfo_children():
                widget.destroy()

            # Crear campos para la cantidad seleccionada de ingredientes
            for i in range(cantidad):
                tk.Label(ingredientes_frame, text=f"Ingrediente {i + 1}").grid(row=i, column=0, padx=5, pady=2)

                bebida_combobox = ttk.Combobox(ingredientes_frame, values=bebidas_list, state="readonly", width=30)
                bebida_combobox.grid(row=i, column=1, padx=5, pady=2)
                bebida_combobox.set("Bebida...")

                cantidad_combobox = ttk.Combobox(ingredientes_frame, values=config.CANT_MILILITROS, state="readonly", width=10)
                cantidad_combobox.grid(row=i, column=2, padx=5, pady=2)
                cantidad_combobox.set("ml...")

            # except TclError as e:
            #     print(f"Error al acceder al combobox: {e}")

        # Asociar evento al ComboBox
        cantidad_combobox.bind("<<ComboboxSelected>>", lambda event: update_ingredient_fields(event, cantidad_combobox))
        
        # Inicializar con un ingrediente
        update_ingredient_fields(None, cantidad_combobox)

        # Botón para guardar el trago
        tk.Button(modal, text="  Guardar  ", command=lambda: self.save_beverage(nombre_entry, ingredientes_frame)).grid(row=4, column=0, columnspan=2, pady=10)

    def save_beverage(self, nombre_entry, ingredientes_frame):
        nombre = nombre_entry.get()
        ingredientes = []

        # Recoger datos de los ingredientes
        for row in ingredientes_frame.winfo_children():
            if isinstance(row, tk.Entry):
                ingredientes.append(row.get())







    # Modificar trago
    def modify_beverage(self):
        pass

    # Eliminar trago
    def delete_beverage(self):
        pass

"""