import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import pandas as pd

class UsuariosApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Agregar campo de búsqueda en un LabelFrame
        search_frame = ttk.LabelFrame(self, text="Buscar Usuario")
        search_frame.pack(pady=10, padx=10, fill='x')
        
        search_label = ttk.Label(search_frame, text="Buscar:")
        search_label.pack(side=tk.LEFT, padx=5)
        
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        search_button = ttk.Button(search_frame, text="Buscar", command=self.search_usuario)
        search_button.pack(side=tk.LEFT, padx=5)
        
        show_all_button = ttk.Button(search_frame, text="Mostrar Todos", command=self.show_all_usuarios)
        show_all_button.pack(side=tk.LEFT, padx=5)

        # Botones de Importar y Exportar
        import_export_frame = ttk.Frame(search_frame)
        import_export_frame.pack(side=tk.RIGHT)
        
        import_button = ttk.Button(import_export_frame, text="Importar desde Excel", command=self.import_from_excel)
        import_button.pack(side=tk.LEFT, padx=5)
        
        convert_button = ttk.Button(import_export_frame, text="Convertir a Excel", command=self.export_to_excel)
        convert_button.pack(side=tk.LEFT, padx=5)

        # Configuración del Treeview
        self.tree = ttk.Treeview(self, columns=('idusuario', 'DNI', 'NOMBRES', 'APELLIDOS', 'IMAGEN', 'DIRECCION', 'CELULAR'), show='headings')
        self.tree.heading('idusuario', text='ID')
        self.tree.heading('DNI', text='DNI')
        self.tree.heading('NOMBRES', text='Nombres')
        self.tree.heading('APELLIDOS', text='Apellidos')
        self.tree.heading('IMAGEN', text='Imagen')
        self.tree.heading('DIRECCION', text='Dirección')
        self.tree.heading('CELULAR', text='Celular')
        self.tree.pack(expand=True, fill='both', pady=10)

        # Botón de Agregar Usuario
        self.add_button = ttk.Button(self, text="Agregar", command=self.open_add_usuario_window)
        self.add_button.pack(pady=10)

        self.populate_tree()

        # Menú contextual
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Editar", command=self.open_edit_window)
        self.context_menu.add_command(label="Eliminar", command=self.delete_usuario)

        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<Double-1>", self.on_double_click)
        self.selected_item = None

    def execute_query(self, query, parameters=()):
        connection = sqlite3.connect('biblioteca.db')
        cursor = connection.cursor()
        cursor.execute(query, parameters)
        connection.commit()
        connection.close()

    def populate_tree(self, search_term=""):
        for row in self.tree.get_children():
            self.tree.delete(row)

        connection = sqlite3.connect('biblioteca.db')
        cursor = connection.cursor()
        if search_term:
            cursor.execute('SELECT * FROM usuarios WHERE NOMBRES LIKE ? OR APELLIDOS LIKE ?', ('%' + search_term + '%', '%' + search_term + '%'))
        else:
            cursor.execute('SELECT * FROM usuarios')
        usuarios = cursor.fetchall()
        for usuario in usuarios:
            self.tree.insert('', tk.END, values=usuario)
        connection.close()

    def add_usuario(self, dni, nombres, apellidos, imagen, direccion, celular):
        if dni and nombres and apellidos and imagen and direccion and celular:
            self.execute_query('''
                INSERT INTO usuarios (DNI, NOMBRES, APELLIDOS, IMAGEN, DIRECCION, CELULAR) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (dni, nombres, apellidos, imagen, direccion, celular))
            messagebox.showinfo("Éxito", "Usuario agregado correctamente")
            self.populate_tree()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def open_add_usuario_window(self):
        add_usuario_window = tk.Toplevel(self)
        add_usuario_window.title("Agregar Usuario")

        form_frame = ttk.Frame(add_usuario_window)
        form_frame.pack(pady=10, padx=10)

        ttk.Label(form_frame, text="DNI:").grid(row=0, column=0, padx=10, pady=10)
        dni_entry = ttk.Entry(form_frame)
        dni_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(form_frame, text="Nombres:").grid(row=1, column=0, padx=10, pady=10)
        nombres_entry = ttk.Entry(form_frame)
        nombres_entry.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(form_frame, text="Apellidos:").grid(row=2, column=0, padx=10, pady=10)
        apellidos_entry = ttk.Entry(form_frame)
        apellidos_entry.grid(row=2, column=1, padx=10, pady=10)
        
        ttk.Label(form_frame, text="Imagen:").grid(row=3, column=0, padx=10, pady=10)
        imagen_button = ttk.Button(form_frame, text="Seleccionar Imagen", command=lambda: self.select_image(add_usuario_window))
        imagen_button.grid(row=3, column=1, padx=10, pady=10)
        
        ttk.Label(form_frame, text="Dirección:").grid(row=4, column=0, padx=10, pady=10)
        direccion_entry = ttk.Entry(form_frame)
        direccion_entry.grid(row=4, column=1, padx=10, pady=10)
        
        ttk.Label(form_frame, text="Celular:").grid(row=5, column=0, padx=10, pady=10)
        celular_entry = ttk.Entry(form_frame)
        celular_entry.grid(row=5, column=1, padx=10, pady=10)
        
        save_button = ttk.Button(form_frame, text="Guardar", 
                                 command=lambda: self.save_usuario(
                                     add_usuario_window,
                                     dni_entry.get(),
                                     nombres_entry.get(),
                                     apellidos_entry.get(),
                                     self.imagen_path,
                                     direccion_entry.get(),
                                     celular_entry.get()
                                 ))
        save_button.grid(row=6, column=0, columnspan=2, pady=10)

    def select_image(self, window):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
        if file_path:
            self.imagen_path = file_path

    def save_usuario(self, window, dni, nombres, apellidos, imagen_path, direccion, celular):
        self.add_usuario(dni, nombres, apellidos, imagen_path, direccion, celular)
        window.destroy()

    def search_usuario(self):
        search_term = self.search_entry.get()
        self.populate_tree(search_term)

    def show_all_usuarios(self):
        self.search_entry.delete(0, tk.END)
        self.populate_tree()

    def show_context_menu(self, event):
        self.selected_item = self.tree.identify_row(event.y)
        if self.selected_item:
            self.tree.selection_set(self.selected_item)
            self.context_menu.post(event.x_root, event.y_root)

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        values = self.tree.item(item, "values")
        self.open_detail_window(values)

    def open_detail_window(self, values):
        detail_window = tk.Toplevel(self)
        detail_window.title("Detalle de Usuario")

        form_frame = ttk.Frame(detail_window)
        form_frame.pack(pady=10, padx=10)

        ttk.Label(form_frame, text="ID:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(form_frame, text=values[0]).grid(row=0, column=1, sticky=tk.W)

        ttk.Label(form_frame, text="DNI:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(form_frame, text=values[1]).grid(row=1, column=1, sticky=tk.W)

        ttk.Label(form_frame, text="Nombres:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(form_frame, text=values[2]).grid(row=2, column=1, sticky=tk.W)

        ttk.Label(form_frame, text="Apellidos:").grid(row=3, column=0, sticky=tk.W)
        ttk.Label(form_frame, text=values[3]).grid(row=3, column=1, sticky=tk.W)

        ttk.Label(form_frame, text="Imagen:").grid(row=4, column=0, sticky=tk.W)
        image_label = ttk.Label(form_frame)
        image_label.grid(row=4, column=1, sticky=tk.W)
        image = Image.open(values[4])
        image.thumbnail((100, 100))
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo

        ttk.Label(form_frame, text="Dirección:").grid(row=5, column=0, sticky=tk.W)
        ttk.Label(form_frame, text=values[5]).grid(row=5, column=1, sticky=tk.W)

        ttk.Label(form_frame, text="Celular:").grid(row=6, column=0, sticky=tk.W)
        ttk.Label(form_frame, text=values[6]).grid(row=6, column=1, sticky=tk.W)

    def open_edit_window(self):
        item = self.tree.item(self.selected_item)
        values = item['values']
        if not values:
            return

        edit_window = tk.Toplevel(self)
        edit_window.title("Editar Usuario")

        form_frame = ttk.Frame(edit_window)
        form_frame.pack(pady=10, padx=10)

        ttk.Label(form_frame, text="DNI:").grid(row=0, column=0)
        dni_entry = ttk.Entry(form_frame)
        dni_entry.insert(0, values[1])
        dni_entry.grid(row=0, column=1)

        ttk.Label(form_frame, text="Nombres:").grid(row=1, column=0)
        nombres_entry = ttk.Entry(form_frame)
        nombres_entry.insert(0, values[2])
        nombres_entry.grid(row=1, column=1)

        ttk.Label(form_frame, text="Apellidos:").grid(row=2, column=0)
        apellidos_entry = ttk.Entry(form_frame)
        apellidos_entry.insert(0, values[3])
        apellidos_entry.grid(row=2, column=1)

        ttk.Label(form_frame, text="Imagen:").grid(row=3, column=0)
        imagen_button = ttk.Button(form_frame, text="Seleccionar Imagen", command=lambda: self.select_image(edit_window))
        imagen_button.grid(row=3, column=1)

        ttk.Label(form_frame, text="Dirección:").grid(row=4, column=0)
        direccion_entry = ttk.Entry(form_frame)
        direccion_entry.insert(0, values[5])
        direccion_entry.grid(row=4, column=1)

        ttk.Label(form_frame, text="Celular:").grid(row=5, column=0)
        celular_entry = ttk.Entry(form_frame)
        celular_entry.insert(0, values[6])
        celular_entry.grid(row=5, column=1)

        save_button = ttk.Button(form_frame, text="Guardar", 
                                 command=lambda: self.update_usuario(
                                     values[0], 
                                     dni_entry.get(),
                                     nombres_entry.get(),
                                     apellidos_entry.get(),
                                     self.imagen_path if hasattr(self, 'imagen_path') else values[4],
                                     direccion_entry.get(),
                                     celular_entry.get()
                                 ))
        save_button.grid(row=6, column=0, columnspan=2, pady=10)

    def update_usuario(self, idusuario, dni, nombres, apellidos, imagen_path, direccion, celular):
        self.execute_query('''
            UPDATE usuarios SET DNI=?, NOMBRES=?, APELLIDOS=?, IMAGEN=?, DIRECCION=?, CELULAR=? 
            WHERE idusuario=?
        ''', (dni, nombres, apellidos, imagen_path, direccion, celular, idusuario))
        messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
        self.populate_tree()

    def delete_usuario(self):
        item = self.tree.item(self.selected_item)
        if not item['values']:
            return

        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar este usuario?")
        if confirm:
            self.execute_query('DELETE FROM usuarios WHERE idusuario=?', (item['values'][0],))
            self.populate_tree()

    def export_to_excel(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            connection = sqlite3.connect('biblioteca.db')
            df = pd.read_sql_query("SELECT * FROM usuarios", connection)
            df.to_excel(file_path, index=False)
            connection.close()
            messagebox.showinfo("Éxito", "Datos exportados a Excel correctamente")

    def import_from_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df = pd.read_excel(file_path)
            connection = sqlite3.connect('biblioteca.db')
            cursor = connection.cursor()
            for _, row in df.iterrows():
                cursor.execute('''
                    INSERT INTO usuarios (DNI, NOMBRES, APELLIDOS, IMAGEN, DIRECCION, CELULAR)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (row['DNI'], row['NOMBRES'], row['APELLIDOS'], row['IMAGEN'], row['DIRECCION'], row['CELULAR']))
            connection.commit()
            connection.close()
            self.populate_tree()
            messagebox.showinfo("Éxito", "Datos importados desde Excel correctamente")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestión de Usuarios")
    UsuariosApp(root).pack(expand=True, fill='both')
    root.mainloop()
