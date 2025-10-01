import customtkinter as ctk
from tkinter import messagebox, ttk
from consultas import obtener_libros, agregar_favorito, obtener_favoritos, verificar_usuario

class PanelUsuario:
    def __init__(self, ventana, usuario):
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.ventana = ventana
        self.usuario = usuario
        self.ventana.title(f"Biblioteca - Usuario: {self.usuario}")
        self.ventana.geometry("900x600")

        # Frame principal  //contenedor dentro de la ventana principal.
        self.frame_principal = ctk.CTkFrame(self.ventana, corner_radius=15)
        self.frame_principal.pack(expand=True, fill="both", padx=20, pady=20)

        # Entradas
        self.campos = {}
        etiquetas = [
            ("ISBN", "isbn"),
            ("Título", "titulo"),
            ("Autor", "autor"),
            ("Año", "anio"),
            ("Género", "genero")
        ]
        for i, (texto, clave) in enumerate(etiquetas): #enumerate para recorrer el iterable y obtener el índice
            label = ctk.CTkLabel(self.frame_principal, text=texto, font=("Segoe UI", 12, "bold"), anchor="w")
            label.grid(row=i, column=0, padx=10, pady=10, sticky="w")
            entrada = ctk.CTkEntry(self.frame_principal, width=400, font=("Segoe UI", 12))
            entrada.grid(row=i, column=1, padx=10, pady=10) 
            self.campos[clave] = entrada

        # Botones
        botones = [
            ("Buscar", self.buscar_libros, "#4CAF50"),
            ("Ver todos", self.ver_todos_los_libros, "#2196F3"),
            ("Agregar a favoritos", self.agregar_a_favoritos, "#FF9800"),
            ("Lista de favoritos", self.mostrar_favoritos, "#9C27B0"),
            ("Limpiar campos", self.limpiar_campos, "#9E9E9E"),
            ("Cerrar sesión", self.cerrar_sesion, "#F44336")
        ]

        for i, (texto, comando, color) in enumerate(botones):
            btn = ctk.CTkButton(self.frame_principal, text=texto, command=comando, width=180, height=40,
                                 fg_color=color, text_color="white", corner_radius=10, font=("Segoe UI", 12, "bold"))
            btn.grid(row=i, column=2, padx=10, pady=10)

    # Funciones
    def buscar_libros(self):
        filtro = {k: v.get().strip() for k, v in self.campos.items()} 
        resultados = obtener_libros(filtro)
        self.mostrar_resultados(resultados, modo="busqueda")


    def ver_todos_los_libros(self):
        resultados = obtener_libros()
        self.mostrar_resultados(resultados, modo="busqueda")


    def mostrar_resultados(self, lista_libros, modo="busqueda"):
        if not lista_libros:
            messagebox.showinfo("Resultados", "No se encontraron libros")
            return

        self.ventana_resultados = ctk.CTkToplevel(self.ventana)
        self.ventana_resultados.title("Favoritos" if modo == "favoritos" else "Resultados de búsqueda")
        self.ventana_resultados.geometry("800x400")

    # Ventana modal
        self.ventana_resultados.transient(self.ventana)
        self.ventana_resultados.grab_set()
        self.ventana_resultados.focus()

        columnas = ("ISBN", "Titulo", "Autor", "Año", "Genero") 
        tree = ttk.Treeview(self.ventana_resultados, columns=columnas, show="headings", height=15)
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")

        for libro in lista_libros:
            tree.insert("", "end", values=libro)
        tree.pack(fill="both", expand=True, padx=20, pady=20)

    # Botones
        frame_botones = ctk.CTkFrame(self.ventana_resultados)
        frame_botones.pack(pady=10)

        btn_detalles = ctk.CTkButton(frame_botones, text="Ver detalles",
        command=lambda: self.ver_detalles(tree))
        btn_detalles.pack(side="left", padx=10)

        if modo == "busqueda":
            btn_fav = ctk.CTkButton(frame_botones, text="Agregar a favoritos",
            command=lambda: self.agregar_desde_resultados(tree))
            btn_fav.pack(side="left", padx=10)
        else:  # Favoritos
            btn_fav = ctk.CTkButton(
            frame_botones, text="Eliminar de favoritos",
            command=lambda: self.eliminar_desde_resultados(tree))
            btn_fav.pack(side="left", padx=10)


    def ver_detalles(self, tree):
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un libro")
            return
        valores = tree.item(seleccionado)["values"]
        mensaje = f"ISBN: {valores[0]}\nTítulo: {valores[1]}\nAutor: {valores[2]}\nAño: {valores[3]}\nGénero: {valores[4]}"
        messagebox.showinfo("Detalles del libro", mensaje)


    def agregar_desde_resultados(self, tree):
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un libro")
            return
        valores = tree.item(seleccionado)["values"]
        isbn = valores[0]

        # Obtener id del usuario
        import sqlite3
        conexion = sqlite3.connect("biblioteca.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE usuario=?", (self.usuario,))
        usuario_id = cursor.fetchone()[0] #fetchone devuelve una tupla
        conexion.close()
        
        if agregar_favorito(usuario_id, isbn):
            messagebox.showinfo("Favoritos", "Libro agregado a favoritos")
        else:
            messagebox.showinfo("Favoritos", "El libro ya estaba en favoritos")

            
    #  Favoritos 
    def agregar_a_favoritos(self):
        isbn = self.campos["isbn"].get().strip()
        if not isbn:
            messagebox.showwarning("Atención", "Ingrese ISBN del libro para agregar a favoritos")
            return

        # Obtener id del usuario
        import sqlite3
        conexion = sqlite3.connect("biblioteca.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE usuario=?", (self.usuario,))
        usuario_id = cursor.fetchone()[0] #fetchone devuelve una tupla
        conexion.close()
        
        if agregar_favorito(usuario_id, isbn):
            messagebox.showinfo("Favoritos", "Libro agregado a favoritos")
        else:
            messagebox.showinfo("Favoritos", "El libro ya estaba en favoritos")

    def mostrar_favoritos(self):
        import sqlite3
        conexion = sqlite3.connect("biblioteca.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE usuario=?", (self.usuario,))
        usuario_id = cursor.fetchone()[0]
        conexion.close()

        favoritos = obtener_favoritos(usuario_id)
        if not favoritos:
            messagebox.showinfo("Favoritos", "Lista de favoritos vacía")
        else:
            self.mostrar_resultados(favoritos, modo="favoritos")


    def agregar_desde_resultados(self, tree):
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un libro")
            return
        isbn = tree.item(seleccionado)["values"][0]

        import sqlite3
        conexion = sqlite3.connect("biblioteca.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE usuario=?", (self.usuario,))
        usuario_id = cursor.fetchone()[0]
        conexion.close()

        if agregar_favorito(usuario_id, isbn):
            messagebox.showinfo("Favoritos", "Libro agregado a favoritos")
        else:
            messagebox.showinfo("Favoritos", "El libro ya estaba en favoritos")


    def eliminar_desde_resultados(self, tree):
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un libro")
            return
        isbn = tree.item(seleccionado)["values"][0]

        import sqlite3
        conexion = sqlite3.connect("biblioteca.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE usuario=?", (self.usuario,))
        usuario_id = cursor.fetchone()[0]
        conexion.close()

        from consultas import eliminar_favorito
        if eliminar_favorito(usuario_id, isbn):
            messagebox.showinfo("Favoritos", "Libro eliminado de favoritos")
            tree.delete(seleccionado)  # 🔹 borra la fila de la tabla
        else:
            messagebox.showwarning("Favoritos", "No se pudo eliminar")

    # Limpiar campos
    def limpiar_campos(self):
        for campo in self.campos.values():
            campo.delete(0, ctk.END)

    # Cerrar sesión
    def cerrar_sesion(self):
        self.ventana.destroy()
        try:
            from form_login import AplicacionLogin
            nueva_ventana = ctk.CTk()
            AplicacionLogin(nueva_ventana)
            nueva_ventana.mainloop()
        except Exception:
            # si algo falla al reabrir el login, solo mostrar mensaje
            messagebox.showinfo("Sesión cerrada", "Has cerrado sesión correctamente")
        messagebox.showinfo("Sesión cerrada", "Has cerrado sesión correctamente")