
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import config
from models import BebidasModel, TragosModel

class BeverageTab:

    def __init__(self, parent, master):
        self.parent = parent  # Referencia al Notebook donde se agregará la pestaña
        self.master = master  # Referencia a la ventana principal
        self.frame = ttk.Frame(self.parent, style=config.style_notebook())
        # Obtengo todos los tragos y bebidas
        self.tragos_model = TragosModel()
        self.bebidas_model = BebidasModel()
        self.tragos = self.tragos_model.read_all()
        # self.bebidas = self.bebidas_model.read_all()
        self.setup_ui()


    def setup_ui(self):
        # interfaz de la pestaña
        tk.Label(self.frame, text="LISTA DE TRAGOS", bg=config.TAPIZ, font=("Arial", 14, "bold")).pack(ipady=25)
        # Frame principal para organizar tabla y combobox
        main_frame = ttk.Frame(self.frame)
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
        self.populate_table(self.tragos)
        # Combobox para ingredientes (a la derecha del scrollbar)
        combobox_frame = ttk.Frame(content_frame)
        combobox_frame.pack(side='left', padx=10, anchor="n")
        tk.Label(combobox_frame, text="Detalle", bg=config.TAPIZ, font=("Arial", 12, "bold")).pack(pady=5)
        self.ingredientes_combobox = ttk.Combobox(combobox_frame, state="readonly", width=40,)
        self.ingredientes_combobox.pack(pady=10, fill='x')
        self.ingredientes_combobox.set("Seleccione un trago")
        # Botones de acción
        self.button_frame = ttk.Frame(main_frame)
        self.button_frame.grid(row=1, column=1, pady=20, sticky="ew")  # Alineación arriba y expandido horizontalmente
        # Botones dentro del frame
        add_button = ttk.Button(self.button_frame, text="Agregar Trago", command=self.add_item)
        add_button.grid(row=0, column=0, padx=10, sticky="ew")
        edit_button = ttk.Button(self.button_frame, text="Modificar Trago", command=self.modify_item)
        edit_button.grid(row=0, column=1, padx=10, sticky="ew")
        delete_button = ttk.Button(self.button_frame, text="Eliminar Trago", command=self.delete_item)
        delete_button.grid(row=0, column=2, padx=10, sticky="ew")
        # Ajustar las columnas del frame
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)


    def populate_table(self, tragos):
        # Llenar la tabla con los datos
        for trago in tragos:
            self.tree.insert("", "end", values=(
                trago['id'],
                f"      {trago['nombre'].title()}",
                trago['cantidad_ingredientes'],
            ))

        def on_tree_selection(event):
            selected_item = self.tree.selection()
            bebidas = self.bebidas_model.read_all()
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
                            ingrediente_str = f"{bebida['tipo'].title()} - {bebida['nombre'].title()} - {ing['cantidad']} ml"
                            ingredientes.append(ingrediente_str)

                    if ingredientes:
                        self.ingredientes_combobox['values'] = ingredientes
                        self.ingredientes_combobox.set("Despliegue para ver los ingredientes")
                    else:
                        self.ingredientes_combobox['values'] = ["Sin ingredientes"]
                        self.ingredientes_combobox.set("Sin ingredientes")

        # Asociar el evento al TreeView
        self.tree.bind("<<TreeviewSelect>>", on_tree_selection)

    
    def add_item(self):
        # Agregar nuevo tragos
        modal = tk.Toplevel(self.frame)
        modal.title("Agregar Trago")
        window_width = 450
        window_height = 350
        vx, vy = config.valoresxy(self.frame, window_width, window_height)
        modal.geometry(str(window_width)+"x"+str(window_height)+"+"+str(vx)+"+"+str(vy-30))
        modal.transient(self.frame)
        modal.iconbitmap(config.ICONO_DRINK)
        modal.focus() 
        modal.grab_set()

        # Obtener las bebidas
        bebidas = self.bebidas_model.read_all()
        # Crear lista de bebidas en formato "Tipo - Nombre"
        bebidas_list = [f"{bebida['tipo'].title()} - {bebida['nombre'].title()}" for bebida in bebidas]
        # Crear campos de edición
        tk.Label(modal, text="Nombre").grid(row=0, column=0, padx=10, pady=5)
        nombre_entry = tk.Entry(modal)
        nombre_entry.insert(0, "")
        nombre_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Label(modal, text="Cantidad de ingredientes").grid(row=1, column=0, padx=10, pady=5)
        # Guardar cantidad_combobox como atributo de la clase
        cantidad_combobox = ttk.Combobox(modal, values=list(range(1, 8)), state="readonly")  # Hasta 7 ingredientes
        cantidad_combobox.set("1")
        cantidad_combobox.grid(row=1, column=1, padx=(18, 5), pady=5)
        # Contenedor dinámico para los ingredientes
        ingredientes_frame = ttk.Frame(modal)
        ingredientes_frame.grid(row=2, column=0, columnspan=2, padx=30, pady=10)

        def update_ingredient_fields(event, cantidad_combobox):
            # Obtener la cantidad seleccionada
            cantidad = int(cantidad_combobox.get())
            # Limpiar el contenedor de ingredientes
            for widget in ingredientes_frame.winfo_children():
                widget.destroy()
            # Crear campos para la cantidad seleccionada de ingredientes
            for i in range(cantidad):
                tk.Label(ingredientes_frame, text=f"Ingrediente {i + 1}", bg=config.BARRA_TOOLS).grid(row=i, column=0, padx=5, pady=2)
                bebida_combobox = ttk.Combobox(ingredientes_frame, values=bebidas_list, state="readonly", width=30, name=f'bebida_combobox_{i}')
                bebida_combobox.grid(row=i, column=1, padx=5, pady=2)
                bebida_combobox.set("Bebida...")
                cantidad_combobox = ttk.Combobox(ingredientes_frame, values=config.CANT_MILILITROS, state="readonly", width=10, name=f'cantidad_combobox_{i}')
                cantidad_combobox.grid(row=i, column=2, padx=5, pady=2)
                cantidad_combobox.set("ml...")

        # Asociar evento al ComboBox
        cantidad_combobox.bind("<<ComboboxSelected>>", lambda event: update_ingredient_fields(event, cantidad_combobox))
        # Inicializar con un ingrediente
        update_ingredient_fields(None, cantidad_combobox)
        # Botón para guardar el trago
        tk.Button(modal, text="Guardar", 
                    command=lambda: self.save_beverage(nombre_entry, ingredientes_frame, modal), 
                    width=20, background=config.BARRA_TOOLS).grid(row=4, column=0, columnspan=2, pady=10)

        # def save_beverage(nombre_entry, ingredientes_frame):
        #     nombre = nombre_entry.get().strip()
        #     ingredientes = []
        #     # Validar que el nombre no esté vacío
        #     if not nombre:
        #         # self.master.iconify()
        #         messagebox.showerror("Error", "El nombre del trago no puede estar vacío.")
        #         # Devolver el foco a la pestaña de bebidas
        #         self.frame.focus_force()
        #         return
        #     # Recoger datos de los ingredientes
        #     filas = ingredientes_frame.grid_slaves()
        #     filas = sorted(filas, key=lambda x: x.grid_info()["row"])  # Ordenar por fila
        #     # Agrupar los widgets en filas lógicas
        #     num_filas = max(fila.grid_info()["row"] for fila in filas) + 1
        #     for i in range(num_filas):
        #         # Filtrar widgets por fila actual
        #         widgets_fila = [widget for widget in filas if widget.grid_info()["row"] == i]
        #         # Verificar que haya un Combobox para bebida y otro para cantidad
        #         bebida_combobox = next((w for w in widgets_fila if isinstance(w, ttk.Combobox) and "bebida" in w.winfo_name()), None)
        #         cantidad_combobox = next((w for w in widgets_fila if isinstance(w, ttk.Combobox) and "cantidad" in w.winfo_name()), None)

        #         if bebida_combobox and cantidad_combobox:
        #             bebida_valor = bebida_combobox.get()
        #             cantidad_valor = cantidad_combobox.get()
        #             # Validar valores
        #             if not bebida_valor or bebida_valor == "Bebida...":
        #                 # self.master.iconify()
        #                 messagebox.showerror("Error", f"Seleccione una bebida válida en la fila {i + 1}.")
        #                 return
        #             if not cantidad_valor or cantidad_valor == "ml...":
        #                 # self.master.iconify()
        #                 messagebox.showerror("Error", f"Seleccione una cantidad válida en la fila {i + 1}.")
        #                 return
        #             # Extraer tipo y nombre de la bebida
        #             tipo, nombre_bebida = bebida_valor.split(" - ", 1)
        #             # Obtener datos de la base de datos usando el ID
        #             bebida_id = self.bebidas_model.read_by_name(tipo.strip().lower(), nombre_bebida.strip().lower())
        #             bebida_id = bebida_id[0]['id']
        #             # Agregar a ingredientes
        #             ingredientes.append({
        #                                 "bebida_id": bebida_id,
        #                                 "cantidad": int(cantidad_valor.replace(" ml", "").strip())
        #                                 })
        #     # Validar que hay al menos un ingrediente
        #     if not ingredientes:
        #         messagebox.showerror("Error", "Debe agregar al menos un ingrediente válido.")
        #         # self.master.iconify()
        #         return
        #     # Guardar el trago en la base de datos
        #     nuevo_trago = {
        #                     "nombre": nombre.lower(),
        #                     "cantidad_ingredientes": len(ingredientes),
        #                     "ingredientes": ingredientes
        #                     }
        #     try:
        #         self.tragos_model.create(nuevo_trago)  # Guardar en el modelo
        #         messagebox.showinfo("Éxito", "Trago agregado exitosamente.")
        #         # self.master.iconify()
        #         modal.destroy()  
        #         # Actualizar en el TreeView
        #         for row in self.tree.get_children():
        #             self.tree.delete(row)
        #         # Llenar la tabla
        #         self.tragos = self.tragos_model.read_all()
        #         self.populate_table(self.tragos)
        #         # Devolver el foco a la pestaña de bebidas
        #         self.frame.focus_force()
        #     except Exception as e:
        #         # self.master.iconify()
        #         messagebox.showerror("Error", f"No se pudo guardar el trago: {e}")
        #         # Devolver el foco a la pestaña de bebidas
        #         self.frame.focus_force()

    
    def modify_item(self):
        # Modificar trago
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Sin Selección", "Por favor selecciona un trago para modificar.")
            return
        
        # Obtener el ID desde los metadatos del TreeView
        selected_item = selected_item[0]
        id_item = self.tree.set(selected_item, 'id')
        if not id_item:
            messagebox.showerror("Error", "No se encontró el trago seleccionado.")
            return
        
        # Obtener datos de la base de datos usando el ID
        trago = self.tragos_model.read_by_id(int(id_item))
        if not trago:
            messagebox.showerror("Error", "No se pudo encontrar el trago en la base de datos.")
            return

        # Ventana para modificar los valores
        modal = tk.Toplevel(self.frame)
        modal.title("Modificar Bebida")
        window_width = 450
        window_height = 350
        vx, vy = config.valoresxy(self.frame, window_width, window_height)
        modal.geometry(str(window_width)+"x"+str(window_height)+"+"+str(vx)+"+"+str(vy-30))
        modal.transient(self.frame)
        modal.iconbitmap(config.ICONO_DRINK)
        modal.focus() 
        modal.grab_set()

        # Obtener las bebidas
        bebidas = self.bebidas_model.read_all()
        # Crear lista de bebidas en formato "Tipo - Nombre"
        bebidas_list = [f"{bebida['tipo'].title()} - {bebida['nombre'].title()}" for bebida in bebidas]
        bebidas_dict = {
                        bebida['id']: f"{bebida['tipo'].title()} - {bebida['nombre'].title()}"
                        for bebida in bebidas
                        if 'id' in bebida and 'tipo' in bebida and 'nombre' in bebida
                        }

        # Crear campos de edición
        tk.Label(modal, text="Nombre").grid(row=0, column=0, padx=10, pady=5)
        nombre_entry = tk.Entry(modal)
        nombre_entry.insert(0, trago['nombre'].title())
        nombre_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Label(modal, text="Cantidad de ingredientes").grid(row=1, column=0, padx=10, pady=5)
        # Guardar cantidad_combobox como atributo de la clase
        cantidad_combobox = ttk.Combobox(modal, values=list(range(1, 8)), state="readonly")  # Hasta 7 ingredientes
        cantidad_combobox.set(trago['cantidad_ingredientes'])
        cantidad_combobox.grid(row=1, column=1, padx=(18, 5), pady=5)
        # Contenedor dinámico para los ingredientes
        ingredientes_frame = ttk.Frame(modal)
        ingredientes_frame.grid(row=2, column=0, columnspan=2, padx=30, pady=10)

        def update_ingredient_fields(event, cantidad_combobox):
            # Obtener la cantidad seleccionada
            cantidad = int(cantidad_combobox.get())
            # Limpiar el contenedor de ingredientes
            for widget in ingredientes_frame.winfo_children():
                widget.destroy()
            # Crear campos para la cantidad seleccionada de ingredientes
            for i in range(cantidad):
                tk.Label(ingredientes_frame, text=f"Ingrediente {i + 1}", bg=config.BARRA_TOOLS).grid(row=i, column=0, padx=5, pady=2)
                bebida_combobox = ttk.Combobox(ingredientes_frame, values=bebidas_list, state="readonly", width=30, name=f'bebida_combobox_{i}')
                bebida_combobox.grid(row=i, column=1, padx=5, pady=2)
                cantidad_combobox = ttk.Combobox(ingredientes_frame, values=config.CANT_MILILITROS, state="readonly", width=10, name=f'cantidad_combobox_{i}')
                cantidad_combobox.grid(row=i, column=2, padx=5, pady=2)
                if trago['cantidad_ingredientes'] > i:
                    bebida_id = trago['ingredientes'][i]['bebida_id']
                    bebida_combobox.set(bebidas_dict[bebida_id])
                    bebida_cantidad = trago['ingredientes'][i]['cantidad']
                    cantidad_combobox.set(bebida_cantidad)
                else:
                    bebida_combobox.set("Bebida...")
                    cantidad_combobox.set("ml...")

        # Asociar evento al ComboBox
        cantidad_combobox.bind("<<ComboboxSelected>>", lambda event: update_ingredient_fields(event, cantidad_combobox))
        # Inicializar con un ingrediente
        update_ingredient_fields(None, cantidad_combobox)
        # Botón para guardar el trago
        tk.Button(modal, text="Guardar", 
                    command=lambda: self.save_beverage(nombre_entry, ingredientes_frame, modal, id_item), 
                    width=20, background=config.BARRA_TOOLS).grid(row=4, column=0, columnspan=2, pady=10)

    
    def save_beverage(self, nombre_entry, ingredientes_frame, modal, id_trago = 0):
        # Guardar datos del trago
        nombre = nombre_entry.get().strip()
        ingredientes = []
        # Validar que el nombre no esté vacío
        if not nombre:
            messagebox.showerror("Error", "El nombre del trago no puede estar vacío.")
            # Devolver el foco a la pestaña de bebidas
            self.frame.focus_force()
            return
        # Recoger datos de los ingredientes
        filas = ingredientes_frame.grid_slaves()
        filas = sorted(filas, key=lambda x: x.grid_info()["row"])  # Ordenar por fila
        # Agrupar los widgets en filas lógicas
        num_filas = max(fila.grid_info()["row"] for fila in filas) + 1
        for i in range(num_filas):
            # Filtrar widgets por fila actual
            widgets_fila = [widget for widget in filas if widget.grid_info()["row"] == i]
            # Verificar que haya un Combobox para bebida y otro para cantidad
            bebida_combobox = next((w for w in widgets_fila if isinstance(w, ttk.Combobox) and "bebida" in w.winfo_name()), None)
            cantidad_combobox = next((w for w in widgets_fila if isinstance(w, ttk.Combobox) and "cantidad" in w.winfo_name()), None)

            if bebida_combobox and cantidad_combobox:
                bebida_valor = bebida_combobox.get()
                cantidad_valor = cantidad_combobox.get()
                # Validar valores
                if not bebida_valor or bebida_valor == "Bebida...":
                    messagebox.showerror("Error", f"Seleccione una bebida válida en la fila {i + 1}.")
                    return
                if not cantidad_valor or cantidad_valor == "ml...":
                    messagebox.showerror("Error", f"Seleccione una cantidad válida en la fila {i + 1}.")
                    return
                # Extraer tipo y nombre de la bebida
                tipo, nombre_bebida = bebida_valor.split(" - ", 1)
                # Obtener datos de la base de datos usando el ID
                bebida_id = self.bebidas_model.read_by_name(tipo.strip().lower(), nombre_bebida.strip().lower())
                bebida_id = bebida_id[0]['id']
                # Agregar a ingredientes
                ingredientes.append({
                                    "bebida_id": bebida_id,
                                    "cantidad": int(cantidad_valor.replace(" ml", "").strip())
                                    })
        # Validar que hay al menos un ingrediente
        if not ingredientes:
            messagebox.showerror("Error", "Debe agregar al menos un ingrediente válido.")
            return
        
        nuevo_trago = {
                        "nombre": nombre.lower(),
                        "cantidad_ingredientes": len(ingredientes),
                        "ingredientes": ingredientes
                        }
        try:
            if id_trago:
                # Actualizar el trago en la base de datos
                self.tragos_model.update(int(id_trago), nuevo_trago)  # Guardar en el modelo
                messagebox.showinfo("Éxito", "Trago modificado exitosamente.")
                modal.destroy()  
            else: 
                # Guardar el trago en la base de datos
                self.tragos_model.create(nuevo_trago)  # Guardar en el modelo
                messagebox.showinfo("Éxito", "Trago agregado exitosamente.")
                modal.destroy()  
            # Actualizar en el TreeView
            for row in self.tree.get_children():
                self.tree.delete(row)
            # Llenar la tabla
            self.tragos = self.tragos_model.read_all()
            self.populate_table(self.tragos)
            # Devolver el foco a la pestaña de bebidas
            self.frame.focus_force()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el trago: {e}")
            # Devolver el foco a la pestaña de bebidas
            self.frame.focus_force()


    def delete_item(self):
        # Eliminar trago
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Sin Selección", "Por favor selecciona un trago para eliminar.")
            # Devolver el foco a la pestaña 
            self.frame.focus_force()
            return
        
        confirm = messagebox.askyesno("Eliminar Trago", "¿Estás seguro de que deseas eliminar este trago?")
        if confirm:
            try:
                # Obtener el ID desde los metadatos del TreeView
                selected_item = selected_item[0]
                id_item = self.tree.set(selected_item, 'id')
                self.tragos_model.delete(int(id_item))
                messagebox.showinfo("Eliminado", "El trago ha sido eliminado correctamente.")
                # Devolver el foco a la pestaña
                self.frame.focus_force()
                # Actualizar en el TreeView
                for row in self.tree.get_children():
                    self.tree.delete(row)
                # Llenar la tabla
                self.tragos = self.tragos_model.read_all()
                self.populate_table(self.tragos)
            except ValueError:
                messagebox.showerror("Error", "El trago no se pudo eliminar.")


