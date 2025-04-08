import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class InventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario - El Niño")
        self.root.geometry("700x500")

        # Etiquetas
        self.etiqueta_titulo = tk.Label(self.root, text="Sistema de Inventario", font=("Arial", 16))
        self.etiqueta_titulo.grid(row=0, column=1, pady=10)

        # Campos para "Número"
        self.etiqueta_numero = tk.Label(self.root, text="Número")
        self.etiqueta_numero.grid(row=1, column=0, padx=10, pady=5)
        self.entry_numero = tk.Entry(self.root)
        self.entry_numero.grid(row=1, column=1, padx=10, pady=5)

        # Campos de Entrada de Producto
        self.etiqueta_producto = tk.Label(self.root, text="Producto")
        self.etiqueta_producto.grid(row=2, column=0, padx=10, pady=5)
        self.entry_producto = tk.Entry(self.root)
        self.entry_producto.grid(row=2, column=1, padx=10, pady=5)

        # Campos de Descripción
        self.etiqueta_descripcion = tk.Label(self.root, text="Descripción")
        self.etiqueta_descripcion.grid(row=3, column=0, padx=10, pady=5)
        self.entry_descripcion = tk.Entry(self.root)
        self.entry_descripcion.grid(row=3, column=1, padx=10, pady=5)

        # Campos de Cantidad
        self.etiqueta_cantidad = tk.Label(self.root, text="Cantidad")
        self.etiqueta_cantidad.grid(row=4, column=0, padx=10, pady=5)
        self.entry_cantidad = tk.Entry(self.root)
        self.entry_cantidad.grid(row=4, column=1, padx=10, pady=5)

        # Campos de Precio
        self.etiqueta_precio = tk.Label(self.root, text="Precio")
        self.etiqueta_precio.grid(row=5, column=0, padx=10, pady=5)
        self.entry_precio = tk.Entry(self.root)
        self.entry_precio.grid(row=5, column=1, padx=10, pady=5)

        # Botones de Acción
        self.boton_agregar = tk.Button(self.root, text="Agregar Producto", command=self.agregar_producto)
        self.boton_agregar.grid(row=6, column=0, padx=10, pady=5)

        self.boton_generar_resumen = tk.Button(self.root, text="Generar Resumen", command=self.generar_resumen)
        self.boton_generar_resumen.grid(row=6, column=1, padx=10, pady=5)

        self.boton_guardar = tk.Button(self.root, text="Guardar", command=self.guardar_pdf)
        self.boton_guardar.grid(row=6, column=2, padx=10, pady=5)

        self.boton_editar = tk.Button(self.root, text="Editar Producto", command=self.editar_producto)
        self.boton_editar.grid(row=6, column=3, padx=10, pady=5)

        # Configuración de la tabla para mostrar los productos
        self.tabla_inventario = ttk.Treeview(self.root, columns=("Número", "Producto", "Descripción", "Cantidad", "Precio"), show="headings")
        self.tabla_inventario.grid(row=7, column=0, columnspan=4, padx=10, pady=10)

        # Configurar encabezados de la tabla
        self.tabla_inventario.heading("Número", text="Número")
        self.tabla_inventario.heading("Producto", text="Producto")
        self.tabla_inventario.heading("Descripción", text="Descripción")
        self.tabla_inventario.heading("Cantidad", text="Cantidad")
        self.tabla_inventario.heading("Precio", text="Precio")

        # Configurar ancho de las columnas
        self.tabla_inventario.column("Número", width=100)
        self.tabla_inventario.column("Producto", width=150)
        self.tabla_inventario.column("Descripción", width=200)
        self.tabla_inventario.column("Cantidad", width=100)
        self.tabla_inventario.column("Precio", width=100)

        self.productos = []

    def agregar_producto(self):
        numero = self.entry_numero.get()
        producto = self.entry_producto.get()
        descripcion = self.entry_descripcion.get()
        cantidad = self.entry_cantidad.get()
        precio = self.entry_precio.get()

        if numero and producto and descripcion and cantidad and precio:
            self.tabla_inventario.insert("", tk.END, values=(numero, producto, descripcion, cantidad, f"Q{precio}"))
            self.productos.append((numero, producto, descripcion, cantidad, precio))
            
            # Limpiar campos
            self.entry_numero.delete(0, tk.END)
            self.entry_producto.delete(0, tk.END)
            self.entry_descripcion.delete(0, tk.END)
            self.entry_cantidad.delete(0, tk.END)
            self.entry_precio.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Por favor ingresa todos los datos")

    def generar_resumen(self):
        # Obtener los productos de la tabla
        if len(self.tabla_inventario.get_children()) > 0:
            resumen = "Resumen de Inventario:\n\n"
            for item in self.tabla_inventario.get_children():
                values = self.tabla_inventario.item(item)["values"]
                resumen += f"Producto: {values[1]}, Cantidad: {values[3]}, Precio: {values[4]}\n"
            messagebox.showinfo("Resumen", resumen)
        else:
            messagebox.showerror("Error", "No hay productos en el inventario para generar un resumen")

    def guardar_pdf(self):
        if self.productos:
            # Crear un archivo PDF
            c = canvas.Canvas("inventario.pdf", pagesize=letter)
            c.setFont("Helvetica", 12)

            # Títulos
            c.drawString(50, 750, "Numero  Producto    Cantidad   Precio")
            y = 730  # Coordenada para los datos

            # Agregar productos al PDF
            for producto in self.productos:
                c.drawString(50, y, f"{producto[0]}     {producto[1]}    {producto[3]}    Q{producto[4]}")
                y -= 20  # Espacio entre filas

            c.save()
            messagebox.showinfo("Guardado", "El archivo PDF se ha guardado como 'inventario.pdf'")
        else:
            messagebox.showerror("Error", "No hay productos para guardar en el PDF")

    def editar_producto(self):
        selected_item = self.tabla_inventario.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor selecciona un producto para editar")
            return

        item_values = self.tabla_inventario.item(selected_item[0])["values"]
        numero, producto, descripcion, cantidad, precio = item_values

        # Rellenar campos con los valores actuales del producto
        self.entry_numero.delete(0, tk.END)
        self.entry_numero.insert(0, numero)
        self.entry_producto.delete(0, tk.END)
        self.entry_producto.insert(0, producto)
        self.entry_descripcion.delete(0, tk.END)
        self.entry_descripcion.insert(0, descripcion)
        self.entry_cantidad.delete(0, tk.END)
        self.entry_cantidad.insert(0, cantidad)
        self.entry_precio.delete(0, tk.END)
        self.entry_precio.insert(0, precio)

        # Eliminar el producto viejo de la tabla
        self.tabla_inventario.delete(selected_item[0])

        # Actualizar la lista de productos
        self.productos = [producto for producto in self.productos if producto[0] != numero]


# Crear la ventana principal de la aplicación
root = tk.Tk()
app = InventarioApp(root)
root.mainloop()
