import tkinter as tk
from tkinter.font import BOLD
import utilerias.generico as utl

class PanelPrincipal:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Panel Principal")
        alto, ancho = self.ventana.winfo_screenwidth(), self.ventana.winfo_screenheight()
        self.ventana.geometry("%dx%d+0+0" % (alto,ancho))
        self.ventana.config(bg="#f1d8b5")
        self.ventana.resizable(width=0, height=0)

        self.logo =utl.leer_imagen(r"C:\Users\brian\OneDrive\Desktop\TP PROGRAMACION\imagenes\El rincon del saber.png", (500,500))
        
        ventana_imagen =tk.Label(self.ventana,image=self.logo,bg="#f1d8b5")
        ventana_imagen.image= self.logo
        ventana_imagen.place(relx=0.5,rely=0.5,anchor="center")

        
        self.ventana.mainloop()