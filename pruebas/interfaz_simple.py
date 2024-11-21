import tkinter as tk
from tkinter import messagebox

# Función para ejecutar al presionar el botón
def show_message():
    messagebox.showinfo("Mensaje", "¡Hola desde la Raspberry Pi!")

# Crear la ventana principal
root = tk.Tk()
root.title("Interfaz LCD Raspberry Pi")
root.geometry("1280x720")  # Ajusta el tamaño según tu pantalla

# Configura una tecla para salir (por ejemplo, Esc)
root.bind("<Escape>", lambda e: root.destroy())

# Crear un botón y una etiqueta
label = tk.Label(root, text="Presiona el botón para un mensaje:")
label.pack(pady=20)

button = tk.Button(root, text="Mostrar Mensaje", command=show_message)
button.pack(pady=20)

# Ejecutar la aplicación
root.mainloop()