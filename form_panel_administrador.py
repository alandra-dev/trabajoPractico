import customtkinter as ctk
from tkinter import messagebox, ttk
from consultas import agregar_libro, modificar_libro as modificar_libro_consulta, eliminar_libro, obtener_libros

class PanelAdministrador:  # clase para el panel de administrador
    def __init__(self, ventana, usuario):  # recibe la ventana principal y el usuario que inició sesión
        # Configuración de CustomTkinter
        ctk.set_appearance_mode("system") 
        ctk.set_default_color_theme("blue") 

        # Configuración de la ventana
        self.ventana = ventana
        self.usuario = usuario
        self.ventana.title(f"Biblioteca - Administrador: {self.usuario}")
        self.ventana.geometry("900x500")

        # Frame principal que contiene toda la interfaz
        self.frame_principal = ctk.CTkFrame(self.ventana, corner_radius=15) 
        self.frame_principal.pack(expand=True, fill="both", padx=20, pady=20) 

        # Frame para los campos de entrada de datos 
        self.frame_entradas = ctk.CTkFrame(self.frame_principal, corner_radius=15)
        self.frame_entradas.pack(side="left", fill="both", expand=True, padx=(0,10), pady=10)

        self.campos = {}
        etiquetas = [("ISBN", "isbn"), ("Título", "titulo"), ("Autor", "autor"), ("Año", "anio"), ("Género", "genero")]

        for i, (texto, clave) in enumerate(etiquetas): 
            label = ctk.CTkLabel(self.frame_entradas, text=texto, anchor="w", font=("Segoe UI", 12, "bold"))
            label.grid(row=i, column=0, padx=10, pady=10, sticky="w")
            entrada = ctk.CTkEntry(self.frame_entradas, width=300, font=("Segoe UI", 12))
            entrada.grid(row=i, column=1, padx=10, pady=10)
            self.campos[clave] = entrada

        # Frame de botones
        self.frame_botones = ctk.CTkFrame(self.frame_principal, corner_radius=15)
        self.frame_botones.pack(side="right", fill="y", padx=(10,0), pady=10)

        # Lista de botones 
        botones = [
            ("Agregar libro", self.agregar_libro, "#4CAF50"),
            ("Modificar libro", self.modificar_libro, "#2196F3"),
            ("Eliminar libro", self.eliminar_libro, "#F44336"),
            ("Limpiar campos", self.limpiar_campos, "#9E9E9E"),
            ("Cerrar sesión", self.cerrar_sesion, "#9C27B0")
        ]

        # Crear botones con estilo personalizado
        for texto, comando, color in botones:
            btn = ctk.CTkButton(self.frame_botones, text=texto, command=comando, width=180, height=50,
                                fg_color=color, text_color="white", corner_radius=10, font=("Segoe UI", 12, "bold"))
            btn.pack(pady=15)

    # Funciones
    def agregar_libro(self):
        datos = {k: v.get().strip() for k, v in self.campos.items()}
        # Verificación de todos los campos
        if not all(datos.values()):
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return
        if agregar_libro(**datos):
            messagebox.showinfo("Éxito", "Libro agregado correctamente")
            self.limpiar_campos()
        else:
            messagebox.showwarning("Error", "Ya existe un libro con ese ISBN")

    def modificar_libro(self):
        datos = {k: v.get().strip() for k, v in self.campos.items()}
        if not datos["isbn"]:
            messagebox.showwarning("Error", "Ingrese ISBN para modificar")
            return

        # Solo usar los campos que tengan datos
        palabras_clave = {}
        for campo in ("titulo", "autor", "anio", "genero"):
            if datos[campo]:
                palabras_clave[campo] = datos[campo]

        if not palabras_clave:
            messagebox.showwarning("Error", "Complete al menos un campo para modificar (Título, Autor, Año, Género).")
            return

        exito = modificar_libro_consulta(datos["isbn"], **palabras_clave)
        if exito:
            messagebox.showinfo("Éxito", "Libro modificado correctamente")
            self.limpiar_campos()
        else:
            messagebox.showwarning("Error", "No se encontró un libro con ese ISBN")

    def eliminar_libro(self):
        isbn = self.campos["isbn"].get().strip()
        if not isbn:
            messagebox.showwarning("Error", "Ingrese ISBN para eliminar")
            return
        if eliminar_libro(isbn):
            messagebox.showinfo("Éxito", "Libro eliminado correctamente")
            self.limpiar_campos()
        else:
            messagebox.showwarning("Error", "No se encontró un libro con ese ISBN")

    def limpiar_campos(self):
        for campo in self.campos.values():
            campo.delete(0, ctk.END)

    def cerrar_sesion(self):
        self.ventana.destroy()
        messagebox.showinfo("Sesión cerrada", "Has cerrado sesión correctamente")
        nueva_ventana = ctk.CTk()
        from form_login import AplicacionLogin
        AplicacionLogin(nueva_ventana)
        nueva_ventana.mainloop()
