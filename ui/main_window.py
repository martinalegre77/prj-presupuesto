import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
from ui.beverages_ui import BeveragesWindow
from ui.desserts_ui import DessertsWindow
import config


class MainWindow:
    """
    Ventana inicial con selección de bebidas/postres
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(0,0)
        wwin = 300
        hwin = 370
        vx, vy = config.valoresxy(self.root, wwin, hwin)
        self.root.geometry(str(wwin)+"x"+str(hwin)+"+"+str(vx)+"+"+str(vy-30))
        self.root.title("App Presupuestos")
        self.root.iconbitmap(config.ICONO)

        main_frame = tk.Frame(self.root, 
                                bg = config.STEEL_PINK, 
                                relief = 'solid', 
                                borderwidth=1, 
                                highlightbackground="white",  # Color del borde inactivo
                                highlightcolor="white",       # Color del borde activo
                                highlightthickness=1)         # Grosor del borde destacado
        main_frame.place(relwidth=1, relheight=1, relx=0, rely=0)

        self.img_bg = ImageTk.PhotoImage(Image.open('./assets/imagen1.png').resize((296,296)))
        label_img_bg = ttk.Label(self.root, image=self.img_bg, relief = 'flat')
        label_img_bg.place_configure(x=0, y=0)

        btn_bebidas = tk.Button(self.root, 
                                text="Tragos", 
                                # fg=config.COLOR_1, 
                                # bg=config.COLOR_3,
                                font = ("Arial", 11, "bold"),
                                relief = 'raised', 
                                command=self.open_beverages, 
                                cursor='hand2')
        btn_bebidas.place(x=46, y=240, width=84, height=30)

        btn_postres = tk.Button(self.root, 
                                text="Postres", 
                                # fg=config.COLOR_1, 
                                # bg=config.COLOR_3,
                                font = ("Arial", 11, "bold"),
                                relief = 'raised', 
                                command=self.open_desserts, 
                                cursor='hand2')
        btn_postres.place(x=170, y=240, width=84, height=30)

        btn_salir = tk.Button(self.root,
                                text='Salir',
                                # fg=config.COLOR_1, 
                                # bg=config.COLOR_2,
                                font = ("Arial", 11, "bold"),
                                relief = 'raised', 
                                command=self.exit, 
                                cursor='hand2')
        btn_salir.place(x=108, y=320, width=84, height=30)

    def open_beverages(self):
        self.root.iconify()
        BeveragesWindow(self.root)

    def open_desserts(self):
        self.root.iconify()
        DessertsWindow(self.root)

    def run(self):
        self.root.mainloop()

    def exit(self):
        if messagebox.askokcancel(
                        title='Advertencia',
                        message='¿Confirma que desea salir de la aplicación?'
                        ):
            self.root.destroy()
        else:
            pass
