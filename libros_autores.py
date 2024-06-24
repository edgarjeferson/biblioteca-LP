import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

class LibrosAutoresApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.tree = ttk.Treeview(self, columns=('idlibro', 'idautor'), show='headings')
        self.tree.heading('idlibro', text='ID Libro')
        self.tree.heading('idautor', text='ID Autor')
        self.tree.pack(expand=True, fill='both')

        self.form_frame = ttk.Frame(self)
        self.form_frame.pack(pady=10)

        self.idlibro_label = ttk.Label(self.form_frame, text="ID Libro:")
        self.idlibro_label.grid(row=0, column=0)
        self.idlibro_entry = ttk.Entry(self.form_frame)
        self.idlibro_entry.grid(row=0, column=1)

        self.idautor_label = ttk.Label(self.form_frame, text="ID Autor:")
        self.idautor_label.grid(row=1, column=0)
        self.idautor_entry = ttk.Entry(self.form_frame)
        self.idautor_entry.grid(row=1, column=1)

        self.add_button = ttk.Button(self.form_frame, text="Agregar", command=self.add_libro_autor)
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
        cursor.execute('SELECT * FROM libros_autores')
        libros_autores = cursor.fetchall()
        for libro_autor in libros_autores:
            self.tree.insert('', tk.END, values=libro_autor)
        connection.close()

    def add_libro_autor(self):
        idlibro = self.idlibro_entry.get()
        idautor = self.idautor_entry.get()

        if idlibro and idautor:
            self.execute_query('''
                INSERT INTO libros_autores (idlibro, idautor) 
                VALUES (?, ?)
            ''', (idlibro, idautor))
            messagebox.showinfo("Éxito", "Libro-autor agregado correctamente")
            self.populate_tree()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
