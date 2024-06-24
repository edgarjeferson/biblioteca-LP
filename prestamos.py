import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

class PrestamosApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.tree = ttk.Treeview(self, columns=('idprestamo', 'idlibro', 'idusuario', 'fecha_prestamo', 'fecha_devolucion'), show='headings')
        self.tree.heading('idprestamo', text='ID')
        self.tree.heading('idlibro', text='ID Libro')
        self.tree.heading('idusuario', text='ID Usuario')
        self.tree.heading('fecha_prestamo', text='Fecha Prestamo')
        self.tree.heading('fecha_devolucion', text='Fecha Devolucion')
        self.tree.pack(expand=True, fill='both')

        self.form_frame = ttk.Frame(self)
        self.form_frame.pack(pady=10)

        self.idlibro_label = ttk.Label(self.form_frame, text="ID Libro:")
        self.idlibro_label.grid(row=0, column=0)
        self.idlibro_entry = ttk.Entry(self.form_frame)
        self.idlibro_entry.grid(row=0, column=1)

        self.idusuario_label = ttk.Label(self.form_frame, text="ID Usuario:")
        self.idusuario_label.grid(row=1, column=0)
        self.idusuario_entry = ttk.Entry(self.form_frame)
        self.idusuario_entry.grid(row=1, column=1)

        self.fecha_prestamo_label = ttk.Label(self.form_frame, text="Fecha Prestamo (YYYY-MM-DD):")
        self.fecha_prestamo_label.grid(row=2, column=0)
        self.fecha_prestamo_entry = ttk.Entry(self.form_frame)
        self.fecha_prestamo_entry.grid(row=2, column=1)

        self.fecha_devolucion_label = ttk.Label(self.form_frame, text="Fecha Devolucion (YYYY-MM-DD):")
        self.fecha_devolucion_label.grid(row=3, column=0)
        self.fecha_devolucion_entry = ttk.Entry(self.form_frame)
        self.fecha_devolucion_entry.grid(row=3, column=1)

        self.add_button = ttk.Button(self.form_frame, text="Agregar", command=self.add_prestamo)
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
        cursor.execute('SELECT * FROM prestamos')
        prestamos = cursor.fetchall()
        for prestamo in prestamos:
            self.tree.insert('', tk.END, values=prestamo)
        connection.close()

    def add_prestamo(self):
        idlibro = self.idlibro_entry.get()
        idusuario = self.idusuario_entry.get()
        fecha_prestamo = self.fecha_prestamo_entry.get()
        fecha_devolucion = self.fecha_devolucion_entry.get()

        if idlibro and idusuario and fecha_prestamo:
            self.execute_query('''
                INSERT INTO prestamos (idlibro, idusuario, fecha_prestamo, fecha_devolucion) 
                VALUES (?, ?, ?, ?)
            ''', (idlibro, idusuario, fecha_prestamo, fecha_devolucion))
            messagebox.showinfo("Éxito", "Préstamo agregado correctamente")
            self.populate_tree()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

