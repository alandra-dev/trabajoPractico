import customtkinter as ctk
from form_login import AplicacionLogin
from bd import crear_bd

# Inicialización 
if __name__ == "__main__":
    # Crear la base de datos y tablas si no existen
    crear_bd()

    # Configuración de CustomTkinter
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    # Ventana principal
    ventana_principal = ctk.CTk()
    
    # Inicializar login
    AplicacionLogin(ventana_principal)
    
    # Ejecutar la aplicación
    ventana_principal.mainloop()
