import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

class UsuariosApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.tree = ttk.Treeview(self, columns=('idusuario', 'NOMBRES', 'APELLIDOS', 'EMAIL', 'idrol'), show='headings')
        self.tree.heading('idusuario', text='ID')
        self.tree.heading('NOMBRES', text='Nombres')
        self.tree.heading('APELLIDOS', text='Apellidos')
        self.tree.heading('EMAIL', text='Email')
        self.tree.heading('idrol', text='ID Rol')
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

        self.email_label = ttk.Label(self.form_frame, text="Email:")
        self.email_label.grid(row=2, column=0)
        self.email_entry = ttk.Entry(self.form_frame)
        self.email_entry.grid(row=2, column=1)

        self.idrol_label = ttk.Label(self.form_frame, text="ID Rol:")
        self.idrol_label.grid(row=3, column=0)
        self.idrol_entry = ttk.Entry(self.form_frame)
        self.idrol_entry.grid(row=3, column=1)

        self.add_button = ttk.Button(self.form_frame, text="Agregar", command=self.add_usuario)
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
        cursor.execute('SELECT * FROM usuarios')
        usuarios = cursor.fetchall()
        for usuario in usuarios:
            self.tree.insert('', tk.END, values=usuario)
        connection.close()

    def add_usuario(self):
        nombres = self.nombres_entry.get()
        apellidos = self.apellidos_entry.get()
        email = self.email_entry.get()
        idrol = self.idrol_entry.get()

        if nombres and apellidos and email and idrol:
            self.execute_query('''
                INSERT INTO usuarios (NOMBRES, APELLIDOS, EMAIL, idrol) 
                VALUES (?, ?, ?, ?)
            ''', (nombres, apellidos, email, idrol))
            messagebox.showinfo("Éxito", "Usuario agregado correctamente")
            self.populate_tree()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
