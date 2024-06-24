import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

class AutoresApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.tree = ttk.Treeview(self, columns=('idautor', 'NOMBRES', 'APELLIDOS', 'DNI', 'NACIONALIDAD'), show='headings')
        self.tree.heading('idautor', text='ID')
        self.tree.heading('NOMBRES', text='Nombres')
        self.tree.heading('APELLIDOS', text='Apellidos')
        self.tree.heading('DNI', text='DNI')
        self.tree.heading('NACIONALIDAD', text='Nacionalidad')
        self.tree.pack(expand=True, fill='both')

        self.form_frame = ttk.Frame(self)
        self.form_frame.pack(pady=10)

        self.nombres_label = ttk.Label(self.form_frame, text="Nombres:")
        self.nombres_label.grid(row=0, column=0)
        self.nombres_entry = ttk.Entry(self.form_frame)
        self.nombres_entry.grid(row=0, column=1)

        self.apellidos_label = ttk.Label(self.form_frame, text="Apellidos:")
        self.apellidos_label.grid(row=1, column=0)
        self.apellidos_entry = ttk.Entry(self.form_frame)
        self.apellidos_entry.grid(row=1, column=1)

        self.dni_label = ttk.Label(self.form_frame, text="DNI:")
        self.dni_label.grid(row=2, column=0)
        self.dni_entry = ttk.Entry(self.form_frame)
        self.dni_entry.grid(row=2, column=1)

        self.nacionalidad_label = ttk.Label(self.form_frame, text="Nacionalidad:")
        self.nacionalidad_label.grid(row=3, column=0)
        self.nacionalidad_entry = ttk.Entry(self.form_frame)
        self.nacionalidad_entry.grid(row=3, column=1)

        self.add_button = ttk.Button(self.form_frame, text="Agregar", command=self.add_autor)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

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
        cursor.execute('SELECT * FROM autores')
        autores = cursor.fetchall()
        for autor in autores:
            self.tree.insert('', tk.END, values=autor)
        connection.close()

    def add_autor(self):
        nombres = self.nombres_entry.get()
        apellidos = self.apellidos_entry.get()
        dni = self.dni_entry.get()
        nacionalidad = self.nacionalidad_entry.get()

        if nombres and apellidos and dni and nacionalidad:
            self.execute_query('''
                INSERT INTO autores (NOMBRES, APELLIDOS, DNI, NACIONALIDAD) 
                VALUES (?, ?, ?, ?)
            ''', (nombres, apellidos, dni, nacionalidad))
            messagebox.showinfo("Éxito", "Autor agregado correctamente")
            self.populate_tree()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
