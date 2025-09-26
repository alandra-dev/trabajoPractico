import customtkinter as ctk

from tkinter import messagebox, simpledialog
from form_panel_administrador import PanelAdministrador
from form_panel_usuario import PanelUsuario
from consultas import verificar_admin, verificar_usuario, agregar_administrador, agregar_usuario


CLAVE_MAESTRA = "1234"  

#  Clase Registro de Usuario
class VentanaRegistro(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Registro de Usuario") 
        self.geometry("500x500") 

        #  Entradas
        ctk.CTkLabel(self, text="Nombre de usuario", font=("Segoe UI", 12)).pack(pady=(20, 5)) 
        self.entrada_usuario = ctk.CTkEntry(self)
        self.entrada_usuario.pack(pady=5)

        ctk.CTkLabel(self, text="Contraseña", font=("Segoe UI", 12)).pack(pady=(20, 5))
        self.entrada_contrasenia = ctk.CTkEntry(self, show="*")
        self.entrada_contrasenia.pack(pady=5)
        
        # Menu desplegable de tipo de usuario
        ctk.CTkLabel(self, text="Tipo de usuario", font=("Segoe UI", 12)).pack(pady=(20, 5))
        self.selector_tipo = ctk.CTkOptionMenu(self, values=["Administrador", "Usuario"], command=self.mostrar_clave_maestra)
        self.selector_tipo.pack(pady=5)

        # Campo oculto para clave maestra
        self.label_clave = ctk.CTkLabel(self, text="Clave maestra", font=("Segoe UI", 12))
        self.entrada_clave = ctk.CTkEntry(self, show="*")

        #  Botón 
        ctk.CTkButton(self, text="Registrar", command=self.registrar_usuario).pack(pady=20)

    #mostrar u ocultar campo clave maestra
    def mostrar_clave_maestra(self, tipo):
        if tipo == "Administrador":
            self.label_clave.pack(pady=(10, 5))
            self.entrada_clave.pack(pady=5)
        else:
            self.label_clave.pack_forget()
            self.entrada_clave.pack_forget()
    # Registrar usuario
    def registrar_usuario(self):
        usuario = self.entrada_usuario.get().strip()
        contrasenia = self.entrada_contrasenia.get().strip()
        tipo = self.selector_tipo.get()
        # Verificación
        if not usuario or not contrasenia:
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return

        if tipo == "Administrador":
            clave_ingresada = self.entrada_clave.get().strip()
            if clave_ingresada != CLAVE_MAESTRA:
                messagebox.showerror("Error", "Clave maestra incorrecta")
                return
            exito = agregar_administrador(usuario, contrasenia)
        else:
            exito = agregar_usuario(usuario, contrasenia)

        if exito:
            messagebox.showinfo("Éxito", f"{tipo} registrado correctamente")
            self.destroy()
        else:
            messagebox.showwarning("Error", "El usuario ya existe")

# Clase Aplicación Login
class AplicacionLogin:
    def __init__(self, ventana_principal):
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        # Configuración de la ventana principal
        self.ventana = ventana_principal
        self.ventana.title("Login Biblioteca El Rincón del Saber")
        self.ventana.geometry("500x400")

        # Configuración de la interfaz
        self.label_tipo = ctk.CTkLabel(self.ventana, text="Tipo de usuario", font=("Segoe UI", 14)) # Título
        self.label_tipo.pack(pady=(30,10))
        # Menu desplegable para seleccionar tipo de usuario
        self.tipo_usuario = ctk.CTkOptionMenu(self.ventana, values=["Administrador", "Usuario"]) # Menú desplegable
        self.tipo_usuario.pack(pady=10)

        self.label_usuario = ctk.CTkLabel(self.ventana, text="Usuario", font=("Segoe UI", 12))
        self.label_usuario.pack(pady=(20,5))
        self.entrada_usuario = ctk.CTkEntry(self.ventana)
        self.entrada_usuario.pack(pady=5)

        self.label_contrasenia = ctk.CTkLabel(self.ventana, text="Contraseña", font=("Segoe UI", 12))
        self.label_contrasenia.pack(pady=(20,5))
        self.entrada_contrasenia = ctk.CTkEntry(self.ventana, show="*")
        self.entrada_contrasenia.pack(pady=5)

        # Botones
        self.boton_login = ctk.CTkButton(self.ventana, text="Iniciar Sesión", command=self.verificar_login)
        self.boton_login.pack(pady=20)

        self.boton_registro = ctk.CTkButton(self.ventana, text="Registrarse", command=self.registro_usuario)
        self.boton_registro.pack(pady=5)

    # Verificar login
    def verificar_login(self):
        usuario = self.entrada_usuario.get().strip()
        contrasenia = self.entrada_contrasenia.get().strip()
        tipo = self.tipo_usuario.get()

        if tipo == "Administrador":
            valido = verificar_admin(usuario, contrasenia)
        else:
            valido = verificar_usuario(usuario, contrasenia)
        # Si es valido, abrir panel correspondiente
        if valido:
            messagebox.showinfo("Login correcto", f"Bienvenido {usuario}!")
            self.ventana.destroy()
            nueva_ventana = ctk.CTk()
            if tipo == "Administrador":
                PanelAdministrador(nueva_ventana, usuario)
            else:
                PanelUsuario(nueva_ventana, usuario)
            nueva_ventana.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    # Abrir ventana de registro
    def registro_usuario(self):
        VentanaRegistro(self.ventana)



# Punto de entrada
if __name__ == "__main__":
    ventana_principal = ctk.CTk()
    AplicacionLogin(ventana_principal)
    ventana_principal.mainloop()
