import tkinter as tk
from tkinter import messagebox
import datetime
import os

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Llantera - Cliente")
ventana.geometry("600x700")

# Variables globales
seleccionados = []
cantidad_seleccionada = tk.IntVar(value=1)
modelo_seleccionado = tk.StringVar(value="")
promocion_seleccionada = tk.StringVar(value="")
tipo_pago = tk.StringVar(value="")

# Precios por modelo
precios = {
    "205/55 R16": 500,
    "195/65 R15": 450,
    "225/45 R17": 550
}

# Función para seleccionar producto
def seleccionar_producto(producto):
    if producto in precios:
        modelo_seleccionado.set(producto)
    seleccionados.append(producto)
    messagebox.showinfo("Producto seleccionado", f"Seleccionaste: {producto}")
    print("Seleccionados:", seleccionados)

# Función para seleccionar promoción
def seleccionar_promocion(promo):
    if promocion_seleccionada.get():
        messagebox.showwarning("Exceso de promociones", "Ya se ha seleccionado una promoción.")
        return
    promocion_seleccionada.set(promo)
    seleccionados.append(promo)
    messagebox.showinfo("Promoción seleccionada", f"Seleccionaste: {promo}")
    print("Promoción seleccionada:", promo)

# Función para confirmar cantidad y mostrar total
def confirmar_cantidad():
    modelo = modelo_seleccionado.get()
    cantidad = cantidad_seleccionada.get()

    if modelo not in precios:
        messagebox.showwarning("Error", "Primero selecciona un modelo de llanta.")
        return

    precio_unitario = precios[modelo]
    total = cantidad * precio_unitario
    mensaje = f"Modelo: {modelo}\nCantidad: {cantidad}\nPrecio unitario: ${precio_unitario}\nTotal: ${total}"
    messagebox.showinfo("Cantidad confirmada", mensaje)
    print(mensaje)

# Función para mostrar resumen y solicitar tipo de pago
def mostrar_resumen():
    modelo = modelo_seleccionado.get()
    cantidad = cantidad_seleccionada.get()
    if modelo not in precios:
        messagebox.showwarning("Error", "Debes seleccionar un modelo de llanta.")
        return
    precio_unitario = precios[modelo]
    promo = promocion_seleccionada.get()
    total_original = cantidad * precio_unitario

    # Aplicar promoción
    if promo == "2X1":
        cantidad_cobrada = (cantidad + 1) // 2
        total = cantidad_cobrada * precio_unitario
    elif promo == "30% de descuento":
        total = total_original * 0.7
    else:
        total = total_original

    resumen = (
        f"Modelo: {modelo}\nCantidad: {cantidad}\nPrecio unitario: ${precio_unitario}\n"
        f"Promoción: {promo if promo else 'Ninguna'}\nTotal estimado: ${round(total,2)}"
    )
    if messagebox.askyesno("Resumen de compra", resumen + "\n\n¿Deseas continuar con el pago?"):
        mostrar_formulario_pago(total)

# Función para mostrar formulario de pago
def mostrar_formulario_pago(total):
    def confirmar_pago():
        tarjeta = entry_tarjeta.get()
        titular = entry_titular.get()
        if not tarjeta.isdigit() or len(tarjeta) != 16:
            messagebox.showerror("Error", "Ingresa un número de tarjeta válido (16 dígitos)")
            return
        if not titular.strip():
            messagebox.showerror("Error", "Ingresa el nombre del titular")
            return
        tipo = tipo_pago.get()
        if tipo not in ("Crédito", "Débito"):
            messagebox.showerror("Error", "Selecciona el tipo de pago")
            return
        
        generar_ticket(total)
        messagebox.showinfo("Éxito", "Tu compra ha sido exitosa. Gracias por tu compra.")
        ventana_pago.destroy()

    ventana_pago = tk.Toplevel(ventana)
    ventana_pago.title("Formulario de Pago")
    ventana_pago.geometry("350x250")

    tk.Label(ventana_pago, text="Tipo de pago:", font=("Arial", 12)).pack(pady=5)
    tk.Radiobutton(ventana_pago, text="Crédito", variable=tipo_pago, value="Crédito").pack()
    tk.Radiobutton(ventana_pago, text="Débito", variable=tipo_pago, value="Débito").pack()

    tk.Label(ventana_pago, text="Número de tarjeta:", font=("Arial", 12)).pack(pady=5)
    entry_tarjeta = tk.Entry(ventana_pago)
    entry_tarjeta.pack()

    tk.Label(ventana_pago, text="Titular de la tarjeta:", font=("Arial", 12)).pack(pady=5)
    entry_titular = tk.Entry(ventana_pago)
    entry_titular.pack()

    tk.Button(ventana_pago, text="Confirmar pago", command=confirmar_pago).pack(pady=15)

# Función para generar ticket
def generar_ticket(total):
    ahora = datetime.datetime.now()
    fecha_hora = ahora.strftime("%Y-%m-%d %H:%M:%S")
    folio = ahora.strftime("%Y%m%d%H%M%S")
    modelo = modelo_seleccionado.get()
    cantidad = cantidad_seleccionada.get()
    promo = promocion_seleccionada.get()
    precio_unitario = precios.get(modelo, 0)

    ticket = f"=== TICKET DE COMPRA ===\n"
    ticket += f"Folio: {folio}\n"
    ticket += f"Fecha y hora: {fecha_hora}\n"
    ticket += f"Modelo: {modelo}\n"
    ticket += f"Cantidad de llantas: {cantidad}\n"
    ticket += f"Precio unitario: ${precio_unitario}\n"
    ticket += f"Promoción aplicada: {promo if promo else 'Ninguna'}\n"
    ticket += f"Total pagado: ${round(total, 2)}\n"
    ticket += f"Tipo de pago: {tipo_pago.get()}\n\n"
    ticket += "Elementos adicionales seleccionados:\n"

    adicionales = [item for item in seleccionados if item != modelo and item != promo]
    if adicionales:
        for item in adicionales:
            ticket += f"- {item}\n"
    else:
        ticket += "Ninguno\n"

    messagebox.showinfo("Ticket de compra", ticket)

    carpeta = "tickets"
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, f"ticket_{folio}.txt")
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(ticket)

    print(f"Ticket guardado en: {ruta}")

# Función para borrar selección
def borrar_seleccion():
    confirmacion = messagebox.askyesno("Confirmar borrado", "¿Estás seguro de que deseas borrar toda la selección?")
    if confirmacion:
        seleccionados.clear()
        cantidad_seleccionada.set(1)
        modelo_seleccionado.set("")
        promocion_seleccionada.set("")
        tipo_pago.set("")
        messagebox.showinfo("Selección borrada", "Se eliminaron todos los productos y promociones.")
        print("Selección reiniciada:", seleccionados)
    else:
        print("Borrado cancelado por el usuario.")


# Diccionario para secciones
secciones = {}

# NAVBAR
menu = tk.Frame(ventana, bg="black")
menu.pack(fill='x')

botones = ["Inicio", "Tienda", "Cantidades", "Vehículo", "Liquidación"]
for nombre in botones:
    tk.Button(menu, text=nombre, bg="orange", fg="black", width=15,
              command=lambda n=nombre.lower(): mostrar_seccion(n)).pack(side="left")

# Botón Ticket
tk.Button(menu, text="🎫 Ticket", bg="green", fg="white", width=15,
          command=mostrar_resumen).pack(side="right")

# Botón Borrar
tk.Button(menu, text="🗑 Borrar", bg="red", fg="white", width=15,
          command=borrar_seleccion).pack(side="right")

# INICIO
inicio = tk.Frame(ventana)
tk.Label(inicio, text="Bienvenido a la Llantera", font=("Arial", 16)).pack(pady=20)
tk.Label(inicio, text="Recomendaciones, anuncios y formas de pago.").pack()
secciones["inicio"] = inicio

# TIENDA
tienda = tk.Frame(ventana)
tk.Label(tienda, text="Catálogo de Llantas", font=("Arial", 16)).pack(pady=10)

modelos_llantas = ["205/55 R16", "195/65 R15", "225/45 R17"]
for modelo in modelos_llantas:
    precio = precios[modelo]
    frame = tk.Frame(tienda, bd=1, relief="solid", padx=10, pady=10)
    texto = f"Modelo: {modelo} - Precio: ${precio}"
    tk.Label(frame, text=texto, font=("Arial", 12)).pack(side="left", padx=10)
    tk.Button(frame, text="Seleccionar", command=lambda m=modelo: seleccionar_producto(m)).pack(side="right")
    frame.pack(fill="x", padx=20, pady=5)
secciones["tienda"] = tienda

# CANTIDADES
cantidades = tk.Frame(ventana)
tk.Label(cantidades, text="Selecciona la cantidad de llantas", font=("Arial", 16)).pack(pady=10)

spin = tk.Spinbox(cantidades, from_=1, to=100, textvariable=cantidad_seleccionada, width=5, font=("Arial", 14))
spin.pack(pady=10)

tk.Button(cantidades, text="Confirmar cantidad", command=confirmar_cantidad).pack(pady=10)
tk.Label(cantidades, text="Elige una marca de llanta:", font=("Arial", 14)).pack(pady=10)
for marca in ["Michelin", "Goodyear", "Bridgestone"]:
    frame = tk.Frame(cantidades, bd=1, relief="solid", padx=10, pady=10)
    tk.Label(frame, text=f"Marca: {marca}").pack(side="left", padx=10)
    tk.Button(frame, text="Seleccionar", command=lambda m=marca: seleccionar_producto(m)).pack(side="right")
    frame.pack(fill="x", padx=20, pady=5)

secciones["cantidades"] = cantidades

# VEHÍCULO
vehiculo = tk.Frame(ventana)
tk.Label(vehiculo, text="Tipo de tracción recomendada", font=("Arial", 16)).pack(pady=10)

def cargar_vehiculo():
    for widget in vehiculo.winfo_children()[1:]:
        widget.destroy()

    cantidad = cantidad_seleccionada.get()
    if cantidad >= 4:
        sugerencia = "Todo terreno"
    elif cantidad == 2:
        sugerencia = "Tracción delantera"
    else:
        sugerencia = "Tracción trasera"

    tk.Label(vehiculo, text=f"Sugerencia según cantidad: {sugerencia}", font=("Arial", 12)).pack(pady=5)

    opciones = ["Todo terreno", "Tracción delantera", "Tracción trasera"]
    for tipo in opciones:
        frame = tk.Frame(vehiculo, bd=1, relief="solid", padx=10, pady=10)
        tk.Label(frame, text=f"Tipo de tracción: {tipo}").pack(side="left", padx=10)
        tk.Button(frame, text="Seleccionar", command=lambda m=tipo: seleccionar_producto(m)).pack(side="right")
        frame.pack(fill="x", padx=20, pady=5)

    tk.Label(vehiculo, text="Elige una marca compatible:", font=("Arial", 14)).pack(pady=10)
    for marca in ["Michelin", "Goodyear", "Bridgestone"]:
        frame = tk.Frame(vehiculo, bd=1, relief="solid", padx=10, pady=10)
        tk.Label(frame, text=f"Marca: {marca}").pack(side="left", padx=10)
        tk.Button(frame, text="Seleccionar", command=lambda m=marca: seleccionar_producto(m)).pack(side="right")
        frame.pack(fill="x", padx=20, pady=5)

secciones["vehículo"] = vehiculo

# LIQUIDACIÓN
liquidacion = tk.Frame(ventana)
tk.Label(liquidacion, text="Ofertas y Promociones", font=("Arial", 16)).pack(pady=20)
tk.Label(liquidacion, text="Descuentos especiales en modelos seleccionados.").pack()

for promo in ["2X1", "30% de descuento"]:
    frame = tk.Frame(liquidacion, bd=1, relief="solid", padx=10, pady=10)
    tk.Label(frame, text=f"Promoción: {promo}").pack(side="left", padx=10)
    tk.Button(frame, text="Seleccionar", command=lambda m=promo: seleccionar_promocion(m)).pack(side="right")
    frame.pack(fill="x", padx=20, pady=5)

secciones["liquidación"] = liquidacion

# FUNCIÓN CAMBIAR SECCIÓN
def mostrar_seccion(seccion):
    for s in secciones.values():
        s.pack_forget()
    if seccion == "vehículo":
        cargar_vehiculo()
    secciones[seccion].pack(fill='both', expand=True)

# MOSTRAR INICIO
mostrar_seccion("inicio")

# MAINLOOP
ventana.mainloop()
