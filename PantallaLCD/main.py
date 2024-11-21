import requests
import tkinter as tk
from tkinter import messagebox, ttk
import subprocess


def open_keyboard():
    """Abre el teclado virtual."""
    global keyboard_process
    if keyboard_process is None:
        keyboard_process = subprocess.Popen(["matchbox-keyboard"])


def close_keyboard():
    """Cierra el teclado virtual."""
    global keyboard_process
    if keyboard_process is not None:
        keyboard_process.terminate()
        keyboard_process = None


def confirmar():
    """Valida las credenciales con el backend."""
    nombre = nombre_entry.get()
    password = password_entry.get()

    data = {"nombre": nombre, "contraseña": password}

    url = "http://10.87.25.38:8000/login"

    # Enviar solicitud POST
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Datos enviados correctamente:", response.json())
        messagebox.showinfo("Confirmación", f"¡Inicio de sesión exitoso!")
        mostrar_hola()  # Cambia la interfaz para mostrar "HOLA"
    else:
        print("Error en el envío:", response.status_code, response.text)
        messagebox.showerror("Error", "Credenciales incorrectas")


def scan_networks():
    """Escanea redes Wi-Fi y llena el ComboBox con los SSID."""
    result = subprocess.run(["nmcli", "-t", "-f", "SSID", "dev", "wifi"], capture_output=True, text=True)
    networks = [line for line in result.stdout.strip().splitlines() if line]
    network_combo['values'] = networks
    if networks:
        network_combo.current(0)


def connect_to_wifi():
    """Conecta a la red seleccionada con la contraseña dada."""
    ssid = network_combo.get()
    password = wifi_password_entry.get()
    if not ssid:
        messagebox.showwarning("Red no seleccionada", "Por favor, selecciona una red Wi-Fi.")
        return
    if not password:
        messagebox.showwarning("Contraseña faltante", "Por favor, ingresa la contraseña de la red Wi-Fi.")
        return

    result = subprocess.run(["nmcli", "dev", "wifi", "connect", ssid, "password", password],
                            capture_output=True, text=True)
    if result.returncode == 0:
        messagebox.showinfo("Conexión exitosa", f"Conectado a la red '{ssid}'")
    else:
        messagebox.showerror("Error de conexión", "No se pudo conectar a la red.\n" + result.stderr)


def mostrar_hola():
    """Cambia la interfaz para mostrar un mensaje 'HOLA'."""
    # Eliminar todos los widgets de la ventana
    for widget in root.winfo_children():
        widget.destroy()

    # Mostrar mensaje central
    tk.Label(root, text="HOLA", font=("Arial", 24), fg="blue").pack(expand=True)


# Crear la ventana principal
root = tk.Tk()
root.title("Formulario de Login")
root.geometry("400x500")

keyboard_process = None

# Etiqueta y campo de entrada para el nombre
tk.Label(root, text="Nombre:").pack(pady=5)
nombre_entry = tk.Entry(root)
nombre_entry.pack(pady=5)
nombre_entry.bind("<FocusIn>", lambda event: open_keyboard())
nombre_entry.bind("<FocusOut>", lambda event: close_keyboard())

# Etiqueta y campo de entrada para la contraseña
tk.Label(root, text="Contraseña:").pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)
password_entry.bind("<FocusIn>", lambda event: open_keyboard())
password_entry.bind("<FocusOut>", lambda event: close_keyboard())

# Botón de confirmación
tk.Button(root, text="Confirmar", command=confirmar).pack(pady=10)

# Marco para la conexión Wi-Fi
wifi_frame = tk.LabelFrame(root, text="Conexión Wi-Fi", padx=10, pady=10)
wifi_frame.pack(fill=tk.BOTH, expand=True, pady=10)

# ComboBox para seleccionar la red Wi-Fi
tk.Label(wifi_frame, text="Selecciona Red Wi-Fi:").pack(pady=5)
network_combo = ttk.Combobox(wifi_frame, state="readonly")
network_combo.pack(pady=5)
scan_networks()

# Entrada de contraseña de Wi-Fi
tk.Label(wifi_frame, text="Contraseña de Wi-Fi:").pack(pady=5)
wifi_password_entry = tk.Entry(wifi_frame, show="*")
wifi_password_entry.pack(pady=5)

# Botón para conectarse a la red Wi-Fi
tk.Button(wifi_frame, text="Conectar", command=connect_to_wifi).pack(pady=10)

# Cerrar el teclado al cerrar la ventana principal
root.protocol("WM_DELETE_WINDOW", close_keyboard)

# Iniciar el bucle principal
root.mainloop()