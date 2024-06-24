import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

class LibrosApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.tree = ttk.Treeview(self, columns=('idlibro', 'TITULO', 'idcategoria'), show='headings')
        self.tree.heading('idlibro', text='ID')
        self.tree.heading('TITULO', text='Título')
        self.tree.heading('idcategoria', text='ID Categoría')
        self.tree.pack(expand=True, fill='both')

        self.form_frame = ttk.Frame(self)
        self.form_frame.pack(pady=10)

        self.titulo_label = ttk.Label(self.form_frame, text="Título:")
        self.titulo_label.grid(row=0, column=0)
        self.titulo_entry = ttk.Entry(self.form_frame)
        self.titulo_entry.grid(row=0, column=1)

        self.idcategoria_label = ttk.Label(self.form_frame, text="ID Categoría:")
        self.idcategoria_label.grid(row=1, column=0)
        self.idcategoria_entry = ttk.Entry(self.form_frame)
        self.idcategoria_entry.grid(row=1, column=1)

        self.add_button = ttk.Button(self.form_frame, text="Agregar", command=self.add_libro)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

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
        cursor.execute('SELECT * FROM libros')
        libros = cursor.fetchall()
        for libro in libros:
            self.tree.insert('', tk.END, values=libro)
        connection.close()

    def add_libro(self):
        titulo = self.titulo_entry.get()
        idcategoria = self.idcategoria_entry.get()

        if titulo and idcategoria:
            self.execute_query('''
                INSERT INTO libros (TITULO, idcategoria) 
                VALUES (?, ?)
            ''', (titulo, idcategoria))
            messagebox.showinfo("Éxito", "Libro agregado correctamente")
            self.populate_tree()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
