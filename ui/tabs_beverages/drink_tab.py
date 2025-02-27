
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import config
from models import BebidasModel

class DrinkTab:
    def __init__(self, parent, master):

        self.parent = parent  # Referencia al Notebook donde se agregará la pestaña
        self.master = master  # Referencia a la ventana principal
        self.frame = ttk.Frame(self.parent, style=config.style_notebook())
        # Obtengo todas las bebidas
        self.bebidas_model = BebidasModel()
        self.bebidas = self.bebidas_model.read_all()
        self.setup_ui()


    def setup_ui(self):
        # Aplicar estilos
        config.style_notebook()
        
        # interfaz de la pestaña
        tk.Label(self.frame, text="LISTA DE BEBIDAS", bg=config.TAPIZ, font=("Arial", 18, "bold")).pack(ipady=25)
        
        # Frame principal para organizar tabla y botones
        main_frame = ttk.Frame(self.frame, style="TFrame")
        main_frame.pack(expand=True, fill='both')  # Ocupa toda la pestaña
        
        # Centrar el contenido con grid
        main_frame.columnconfigure(0, weight=1)  # Columna izquierda para espacio vacío
        main_frame.columnconfigure(1, weight=0)  # Columna central para el contenido
        main_frame.columnconfigure(2, weight=1)  # Columna derecha para espacio vacío
        
        # Frame para la tabla (Treeview + Scrollbar)
        table_frame = ttk.Frame(main_frame, style="TFrame")
        table_frame.grid(row=0, column=1, sticky='n', padx=10, pady=10)
        
        # Tabla (Treeview) con Scrollbar
        self.tree = ttk.Treeview(table_frame, columns=("id", "Tipo", "Nombre", "Presentación", "Costo", "Venta"), 
                                show="headings", 
                                height=10,
                                style="Treeview")
        self.tree.heading("id", text="ID")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Presentación", text="Presentación")
        self.tree.heading("Costo", text="Costo")
        self.tree.heading("Venta", text="Venta")
        
        # Ajustar el ancho de las columnas
        self.tree.column("id", width=0, stretch=False)
        self.tree.column("Tipo", width=190)
        self.tree.column("Nombre", width=190)
        self.tree.column("Presentación", width=160)
        self.tree.column("Costo", width=120)
        self.tree.column("Venta", width=120)
        
        # Barra de desplazamiento para la tabla
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set, style="Treeview")
        self.tree.pack(side='left', fill='both')
        scrollbar.pack(side='right', fill='y')
        
        # Llenar la tabla
        self.populate_table(self.bebidas)
        
        # Botones de acción
        button_frame = ttk.Frame(main_frame, style="TFrame")
        button_frame.grid(row=1, column=1, pady=20, sticky="ew")  # Alineación arriba y expandido horizontalmente
        
        # Botones dentro del frame
        add_button = ttk.Button(button_frame, text="➕ Agregar Bebida", command=self.add_item, cursor='hand2', style="Accent.TButton")
        add_button.grid(row=0, column=0, padx=10, sticky="ew")
        
        modify_button = ttk.Button(button_frame, text="✏️ Modificar Bebida", command=self.modify_item, cursor='hand2', style="Accent.TButton")
        modify_button.grid(row=0, column=1, padx=10, sticky="ew")
        
        delete_button = ttk.Button(button_frame, text="❌ Eliminar Bebida", command=self.delete_item, cursor='hand2', style="Accent.TButton")
        delete_button.grid(row=0, column=2, padx=10, sticky="ew")
        
        # Ajustar las columnas del frame
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)


    def populate_table(self, bebidas):
        # Llenar la tabla con los datos
        
        # Limpiar la tabla antes de llenarla
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Insertar las bebidas en la tabla
        for bebida in bebidas:
            self.tree.insert("", "end", values=(
                bebida['id'],
                f"     {bebida['tipo'].title()}",
                f"     {bebida['nombre'].title()}",
                f"          {bebida['presentacion']} ml",
                f"          $ {bebida['precio_compra']}",
                f"          $ {bebida['precio_venta']}"
            ))


    def add_item(self):
        # Agregar nueva bebida
        modal = tk.Toplevel(self.frame)
        modal.title("Agregar Bebida")
        window_width = 360
        window_height = 250
        vx, vy = config.valoresxy(self.frame, window_width, window_height)
        modal.geometry(str(window_width)+"x"+str(window_height)+"+"+str(vx)+"+"+str(vy-30))
        modal.transient(self.frame)
        modal.iconbitmap(config.ICONO_DRINK)
        modal.focus() 
        modal.grab_set()

        # Crear campos de edición
        valores_tipo = config.valores_tipo(self.bebidas)
        tk.Label(modal, text="Tipo").grid(row=0, column=0, padx=10, pady=5)
        tipo_combobox = ttk.Combobox(modal, values=valores_tipo, height=8)
        tipo_combobox.set(valores_tipo[0])
        tipo_combobox.grid(row=0, column=1, padx=(18, 5), pady=5)

        tk.Label(modal, text="Nombre").grid(row=1, column=0, padx=10, pady=5)
        nombre_entry = tk.Entry(modal)
        nombre_entry.insert(0, "")
        nombre_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(modal, text="Presentación - ml").grid(row=2, column=0, padx=10, pady=5)
        presentacion_combobox = ttk.Combobox(modal, values=config.MILILITROS, state='readonly', height=5)
        presentacion_combobox.set(config.MILILITROS[0])
        presentacion_combobox.grid(row=2, column=1, padx=(18, 5), pady=5)

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
        
        # Botón Guardar
        tk.Button(modal, text="Guardar", command=lambda: self.save_drink(modal,
                                                                    tipo_combobox.get().lower(),
                                                                    nombre_entry.get().lower(),
                                                                    presentacion_combobox.get(),
                                                                    costo_entry.get(),
                                                                    venta_entry.get()), 
                                                                    width=20, 
                                                                    background=config.BARRA_TOOLS).grid(row=5, column=1, columnspan=1, pady=20)


    def modify_item(self):
        # Modificar bebida
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Sin Selección", "Por favor selecciona una bebida para modificar.")
            return
        
        # Obtener el ID desde los metadatos del TreeView
        selected_item = selected_item[0]
        id_item = self.tree.set(selected_item, 'id')
        if not id_item:
            messagebox.showerror("Error", "No se encontró la bebida seleccionada.")
            return
        
        # Obtener datos de la base de datos usando el ID
        bebida = self.bebidas_model.read_by_id(int(id_item))
        if not bebida:
            messagebox.showerror("Error", "No se pudo encontrar la bebida en la base de datos.")
            return

        # Ventana para modificar los valores
        modal = tk.Toplevel(self.frame)
        modal.title("Modificar Bebida")
        window_width = 360
        window_height = 250
        vx, vy = config.valoresxy(self.frame, window_width, window_height)
        modal.geometry(str(window_width)+"x"+str(window_height)+"+"+str(vx)+"+"+str(vy-30))
        modal.transient(self.frame)
        modal.iconbitmap(config.ICONO_DRINK)
        modal.focus() 
        modal.grab_set()

        # Crear campos de edición
        valores_tipo = config.valores_tipo(self.bebidas)
        tk.Label(modal, text="Tipo").grid(row=0, column=0, padx=10, pady=5)
        tipo_combobox = ttk.Combobox(modal, values=valores_tipo, height=8)
        tipo_combobox.set(bebida['tipo'].title())
        tipo_combobox.grid(row=0, column=1, padx=(15, 5), pady=5)

        tk.Label(modal, text="Nombre").grid(row=1, column=0, padx=10, pady=5)
        nombre_entry = tk.Entry(modal)
        nombre_entry.insert(0, bebida['nombre'].title())
        nombre_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(modal, text="Presentación - ml").grid(row=2, column=0, padx=10, pady=5)
        presentacion_combobox = ttk.Combobox(modal, values=config.MILILITROS, state='readonly', height=5)
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
        
        # Botón Guardar cambios
        tk.Button(modal, text="Guardar", command=lambda: self.save_drink(modal, 
                                                                    tipo_combobox.get().lower(),
                                                                    nombre_entry.get().lower(),
                                                                    presentacion_combobox.get(),
                                                                    costo_entry.get(),
                                                                    venta_entry.get(),
                                                                    id_item),
                                                                    width=20, 
                                                                    background=config.BARRA_TOOLS).grid(row=5, column=1, columnspan=1, pady=20)


    def delete_item(self):
        # Eliminar bebida 
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Sin Selección", "Por favor selecciona una bebida para eliminar.")
            # Devolver el foco a la pestaña de bebidas
            self.frame.focus_force()
            return
        
        confirm = messagebox.askyesno("Eliminar Bebida", "¿Estás seguro de que deseas eliminar esta bebida?")
        if confirm:
            try:
                # Obtener el ID desde los metadatos del TreeView
                selected_item = selected_item[0]
                id_item = self.tree.set(selected_item, 'id')
                self.bebidas_model.delete(int(id_item))
                
                # Minimizar la ventana principal
                # self.master.iconify()
                messagebox.showinfo("Eliminado", "La bebida ha sido eliminada correctamente.")
                
                # Devolver el foco a la pestaña de bebidas
                self.frame.focus_force()
                
                # Actualizar en el TreeView
                for row in self.tree.get_children():
                    self.tree.delete(row)
                
                # Llenar la tabla
                self.bebidas = self.bebidas_model.read_all()
                self.populate_table(self.bebidas)
            except ValueError:
                messagebox.showerror("Error", "La bebida no se pudo eliminar.")


    def save_drink(self, modal, tipo, nombre, presentacion, costo, venta, id_item=0):
        # Guardar datos
        nueva_bebida = {
                        'tipo': tipo,
                        'nombre': nombre,
                        'presentacion': int(presentacion),
                        'precio_compra': float(costo),
                        'precio_venta': float(venta)
                    }
        try:
            if id_item:
                self.bebidas_model.update(int(id_item), nueva_bebida)
                modal.destroy()
                messagebox.showinfo("Éxito", "Bebida modificada correctamente.")
            else:
                self.bebidas_model.create(nueva_bebida)
                modal.destroy()
                messagebox.showinfo("Éxito", "Bebida agregada correctamente.")
            
            # Devolver el foco a la pestaña de bebidas
            self.frame.focus_force()
            
            # Actualizar en el TreeView
            for row in self.tree.get_children():
                self.tree.delete(row)
            
            # Llenar la tabla
            self.bebidas = self.bebidas_model.read_all()
            self.populate_table(self.bebidas)
        except ValueError:
            messagebox.showerror("Error", "Los valores de Costo y Venta deben ser números válidos.")
