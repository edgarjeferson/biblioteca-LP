import tkinter as tk
from tkinter import ttk
from autores import AutoresApp
from categorias import CategoriasApp
from libros import LibrosApp
from libros_autores import LibrosAutoresApp
from prestamos import PrestamosApp
from roles import RolesApp
from usuarios import UsuariosApp

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Biblioteca")
        self.geometry("800x600")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        self.autores_app = AutoresApp(self.notebook)
        self.notebook.add(self.autores_app, text="Autores")

        self.categorias_app = CategoriasApp(self.notebook)
        self.notebook.add(self.categorias_app, text="Categorías")

        self.libros_app = LibrosApp(self.notebook)
        self.notebook.add(self.libros_app, text="Libros")

        self.libros_autores_app = LibrosAutoresApp(self.notebook)
        self.notebook.add(self.libros_autores_app, text="Libros y Autores")

        self.prestamos_app = PrestamosApp(self.notebook)
        self.notebook.add(self.prestamos_app, text="Préstamos")

        self.roles_app = RolesApp(self.notebook)
        self.notebook.add(self.roles_app, text="Roles")

        self.usuarios_app = UsuariosApp(self.notebook)
        self.notebook.add(self.usuarios_app, text="Usuarios")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
