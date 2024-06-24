import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

class RolesApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.tree = ttk.Treeview(self, columns=('idrol', 'NOMBRE'), show='headings')
        self.tree.heading('idrol', text='ID')
        self.tree.heading('NOMBRE', text='Nombre')
        self.tree.pack(expand=True, fill='both')

        self.form_frame = ttk.Frame(self)
        self.form_frame.pack(pady=10)

        self.nombre_label = ttk.Label(self.form_frame, text="Nombre:")
        self.nombre_label.grid(row=0, column=0)
        self.nombre_entry = ttk.Entry(self.form_frame)
        self.nombre_entry.grid(row=0, column=1)

        self.add_button = ttk.Button(self.form_frame, text="Agregar", command=self.add_rol)
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
        cursor.execute('SELECT * FROM roles')
        roles = cursor.fetchall()
        for rol in roles:
            self.tree.insert('', tk.END, values=rol)
        connection.close()

    def add_rol(self):
        nombre = self.nombre_entry.get()

        if nombre:
            self.execute_query('''
                INSERT INTO roles (NOMBRE) 
                VALUES (?)
            ''', (nombre,))
            messagebox.showinfo("Éxito", "Rol agregado correctamente")
            self.populate_tree()
        else:
            messagebox.showerror("Error", "El campo nombre es obligatorio")
