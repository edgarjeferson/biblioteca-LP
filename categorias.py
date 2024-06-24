import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

class CategoriasApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.tree = ttk.Treeview(self, columns=('idcategoria', 'NOMBRE'), show='headings')
        self.tree.heading('idcategoria', text='ID')
        self.tree.heading('NOMBRE', text='Nombre')
        self.tree.pack(expand=True, fill='both')

        self.form_frame = ttk.Frame(self)
        self.form_frame.pack(pady=10)

        self.nombre_label = ttk.Label(self.form_frame, text="Nombre:")
        self.nombre_label.grid(row=0, column=0)
        self.nombre_entry = ttk.Entry(self.form_frame)
        self.nombre_entry.grid(row=0, column=1)

        self.add_button = ttk.Button(self.form_frame, text="Agregar", command=self.add_categoria)
        self.add_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.populate_tree()

    def execute_query(self, query, parameters=()):
        connection = sqlite3.connect('biblioteca.db')
        cursor = connection.cursor()
        cursor.execute(query, parameters)
        connection.commit()
        connection.close()

    def populate_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        connection = sqlite3.connect('biblioteca.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM categorias')
        categorias = cursor.fetchall()
        for categoria in categorias:
            self.tree.insert('', tk.END, values=categoria)
        connection.close()

    def add_categoria(self):
        nombre = self.nombre_entry.get()

        if nombre:
            self.execute_query('''
                INSERT INTO categorias (NOMBRE) 
                VALUES (?)
            ''', (nombre,))
            messagebox.showinfo("Éxito", "Categoría agregada correctamente")
            self.populate_tree()
        else:
            messagebox.showerror("Error", "El campo nombre es obligatorio")
