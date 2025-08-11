import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import utilerias.generico as utl
from formularios.form_master import PanelPrincipal

class App:
    
    def seleccionar_tipo_usuario(self, es_administrador):
        self.eleccion = es_administrador
        self.iniciar_sesion()
    
    def guardar_administrador(self):    
        administrador = self.usuario_registro.get()
        contrasenia = self.contrasenia_registro.get()
        if not administrador or not contrasenia:
            return messagebox.showerror("Error", "Todos los campos son obligatorios")
        try:
            with open("administradores.txt", "r") as archivo:
                usuarios_existentes = archivo.read()
        except FileNotFoundError:
            usuarios_existentes = ""

        if f"{administrador}," in usuarios_existentes:
            return messagebox.showerror("Error", "El administrador ya está registrado")
        
        with open("administradores.txt", "a") as archivo:
            archivo.write(f"{administrador},{contrasenia}\n")

        self.ventana_registro.destroy()
        messagebox.showinfo("Éxito", "Administrador registrado correctamente")


    
    
    def guardar_usuario(self):
        usuario = self.usuario_registro.get()
        contrasenia = self.contrasenia_registro.get()
        if not usuario or not contrasenia:
            return messagebox.showerror("Error", "Todos los campos son obligatorios")
        try:
            with open("usuarios.txt", "r") as archivo:
                usuarios_existentes = archivo.read()
        except FileNotFoundError:
            usuarios_existentes = ""

        if f"{usuario}," in usuarios_existentes:
            return messagebox.showerror("Error", "El usuario ya está registrado")

        with open("usuarios.txt", "a") as archivo:
            archivo.write(f"{usuario},{contrasenia}\n")

        self.ventana_registro.destroy()
        messagebox.showinfo("Éxito", "Usuario registrado correctamente")

                                     
    
    def verificar(self):
        usuario= self.usuario_inicio.get()
        contrasenia= self.contrasenia_inicio.get()
        if self.eleccion:
            try:
                with open("administradores.txt", "r") as archivo:
                    datos_administradores = archivo.read()
            except FileNotFoundError:
                datos_administradores = ""
            if f"{usuario},{contrasenia}" in datos_administradores:
                self.ventana_inicio.destroy()
                PanelPrincipal()
            else:
                messagebox.showerror("Error", "Nombre de Usuario o Contraseña incorrectos")
        else: 
            try:
                with open("usuarios.txt", "r") as archivo:
                    datos_usuarios = archivo.read()
            except FileNotFoundError:
                datos_usuarios = ""
            if f"{usuario},{contrasenia}" in datos_usuarios:
                self.ventana_inicio.destroy()
                PanelPrincipal()
            else:
                messagebox.showerror("Error", "Nombre de Usuario o Contraseña incorrectos")

    
    def iniciar_sesion(self):
            self.ventana.destroy()
            self.ventana_inicio = tk.Tk()
            self.ventana_inicio.title("Iniciar Sesion")
            self.ventana_inicio.geometry("800x500")
            self.ventana_inicio.config(bg="#fcfcfc")
            self.ventana_inicio.resizable(width=0, height=0)
            utl.centrar_ventana(self.ventana_inicio, 800, 500)

            self.logo_registro = utl.leer_imagen(r"C:\Users\brian\OneDrive\Desktop\TP PROGRAMACION\imagenes\El rincon del saber.png",(200, 200))

            # frame logo
            frame_logo = tk.Frame(self.ventana_inicio, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10, bg="#f1d8b5")
            frame_logo.pack(side="left", expand=tk.NO, fill=tk.BOTH)
            ventana = tk.Label(frame_logo, image=self.logo_registro, bg="#f1d8b5")
            ventana.place(x=0, y=0, relwidth=1, relheight=1)

            # frame_form
            frame_form = tk.Frame(self.ventana_inicio, bd=0, relief=tk.SOLID, bg="#fcfcfc")
            frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)

            # frame_form_arriba
            frame_form_arriba = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg="black")
            frame_form_arriba.pack(side="top", fill=tk.X)
            titulo = tk.Label(frame_form_arriba, text="Inicio de Sesion", font=("Times", 30), fg="#666a88", bg="#fcfcfc", pady=50)
            titulo.pack(expand=tk.YES, fill=tk.BOTH)

            # frame_form_llenar
            frame_form_llenar = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg="#fcfcfc")
            frame_form_llenar.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

            etiqueta_usuario = tk.Label(frame_form_llenar, text="Nombre de Usuario", font=("Times", 14), fg="#666a88", bg="#fcfcfc", anchor="w")
            etiqueta_usuario.pack(fill=tk.X, padx=20, pady=5)
            self.usuario_inicio = ttk.Entry(frame_form_llenar, font=("Times", 14))
            self.usuario_inicio.pack(fill=tk.X, padx=20, pady=10)

            etiqueta_contrasenia = tk.Label(frame_form_llenar, text="Contraseña", font=("Times", 14), fg="#666a88", bg="#fcfcfc", anchor="w")
            etiqueta_contrasenia.pack(fill=tk.X, padx=20, pady=5)
            self.contrasenia_inicio = ttk.Entry(frame_form_llenar, font=("Times", 14), show="*")
            self.contrasenia_inicio.pack(fill=tk.X, padx=20, pady=10)

            boton_inicio = tk.Button(frame_form_llenar, text="Iniciar Sesion", font=("Times", 15, BOLD), bg="#3a7ff6", bd=0, fg="#fff", command=self.verificar)
            boton_inicio.pack(fill=tk.X, padx=20, pady=20)
            
            boton_registrar = tk.Button(frame_form_llenar, text="Registrarse", font=("Times", 15, BOLD), bg="#3a7ff6", bd=0, fg="#fff", command=self.registrar)
            boton_registrar.pack(fill=tk.X, padx=20, pady=20)
        
    def registrar(self):
        self.ventana_registro = tk.Toplevel(self.ventana_inicio)
        self.ventana_registro.title("Registrarse")
        self.ventana_registro.geometry("800x500")
        self.ventana_registro.config(bg="#fcfcfc")
        self.ventana_registro.resizable(width=0, height=0)
        utl.centrar_ventana(self.ventana_registro, 800, 500)

        self.logo_registro = utl.leer_imagen(r"C:\Users\brian\OneDrive\Desktop\TP PROGRAMACION\imagenes\El rincon del saber.png",(200, 200))

        # frame logo
        frame_logo = tk.Frame(self.ventana_registro, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10, bg="#f1d8b5")
        frame_logo.pack(side="left", expand=tk.NO, fill=tk.BOTH)
        ventana = tk.Label(frame_logo, image=self.logo_registro, bg="#f1d8b5")
        ventana.place(x=0, y=0, relwidth=1, relheight=1)

        # frame_form
        frame_form = tk.Frame(self.ventana_registro, bd=0, relief=tk.SOLID, bg="#fcfcfc")
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)

        # frame_form_arriba
        frame_form_arriba = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg="black")
        frame_form_arriba.pack(side="top", fill=tk.X)
        titulo = tk.Label(frame_form_arriba, text="Registro", font=("Times", 30), fg="#666a88", bg="#fcfcfc", pady=50)
        titulo.pack(expand=tk.YES, fill=tk.BOTH)

        # frame_form_llenar
        frame_form_llenar = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg="#fcfcfc")
        frame_form_llenar.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        etiqueta_usuario = tk.Label(frame_form_llenar, text="Nombre de Usuario", font=("Times", 14), fg="#666a88", bg="#fcfcfc", anchor="w")
        etiqueta_usuario.pack(fill=tk.X, padx=20, pady=5)
        self.usuario_registro = ttk.Entry(frame_form_llenar, font=("Times", 14))
        self.usuario_registro.pack(fill=tk.X, padx=20, pady=10)

        etiqueta_contrasenia = tk.Label(frame_form_llenar, text="Contraseña", font=("Times", 14), fg="#666a88", bg="#fcfcfc", anchor="w")
        etiqueta_contrasenia.pack(fill=tk.X, padx=20, pady=5)
        self.contrasenia_registro = ttk.Entry(frame_form_llenar, font=("Times", 14), show="*")
        self.contrasenia_registro.pack(fill=tk.X, padx=20, pady=10)

        boton_registrar = tk.Button(frame_form_llenar, text="Registrarse", font=("Times", 15, BOLD), bg="#3a7ff6", bd=0, fg="#fff", command= lambda: self.guardar_administrador() if self.eleccion else self.guardar_usuario())
        boton_registrar.pack(fill=tk.X, padx=20, pady=20)
        


    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Tipo de Usuario")
        self.ventana.geometry("800x500")
        self.ventana.config(bg="#fcfcfc")
        self.ventana.resizable(width=0, height=0)
        utl.centrar_ventana(self.ventana, 800, 500)

   
        self.logo = utl.leer_imagen(r"C:\Users\brian\OneDrive\Desktop\TP PROGRAMACION\imagenes\El rincon del saber.png",(200, 200))

        
        frame_logo = tk.Frame(self.ventana, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10, bg="#f1d8b5")
        frame_logo.pack(side="left", expand=tk.NO, fill=tk.BOTH)
        ventana = tk.Label(frame_logo, image=self.logo, bg="#f1d8b5")
        ventana.place(x=0, y=0, relwidth=1, relheight=1)

        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg="#fcfcfc")
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)

        frame_form_arriba = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg="black")
        frame_form_arriba.pack(side="top", fill=tk.X)
        titulo = tk.Label(frame_form_arriba, text="Tipo de Usuario", font=("Times", 30), fg="#666a88", bg="#fcfcfc", pady=50)
        titulo.pack(expand=tk.YES, fill=tk.BOTH)

        frame_form_llenar = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg="#fcfcfc")
        frame_form_llenar.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        self.boton_administrador = tk.Button(frame_form_llenar, text="Administrador", font=("Times", 15, BOLD), bg="#3a7ff6", bd=0, fg="#fff", command=lambda: self.seleccionar_tipo_usuario(True))
        self.boton_administrador.pack(fill=tk.X, padx=20, pady=20)

        self.boton_usuario = tk.Button(frame_form_llenar, text="Usuario", font=("Times", 15, BOLD), bg="#3a7ff6", bd=0, fg="#fff", command=lambda: self.seleccionar_tipo_usuario(False))
        self.boton_usuario.pack(fill=tk.X, padx=20, pady=20)

        self.ventana.mainloop()



