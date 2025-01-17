from cProfile import label
import tkinter as tk
from tkinter import Label, messagebox, ttk
import os
import json

logros = [
    {"nombre": "Ejemplo: Logro inicial", "categoria": "Ejemplo", "descripcion": "Este es un logro de ejemplo para mostrar cómo funciona el programa.", "tipo": "Bronce", "completado": True}
]

PROGRESS_FILE = "data.json"

def guardar_progreso():
    with open(PROGRESS_FILE, "w") as f:
        json.dump(logros, f)
    messagebox.showinfo("¡Listo!", "Ya guardamos tus logros, sigue así")

def cargar_progreso():
    global logros
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            logros = json.load(f)
            messagebox.showinfo("Bienvenido de nuevo", "Que bueno verte otra vez!")

    else:
        messagebox.showinfo("Holaaaaa", "Vemos que eres nuevo, empieza ahora")

def toggle_completado(index):
    logros[index]["completado"] = not logros[index]["completado"]
    actualizar_ui()

def mostrar_descripcion(index):
    texto_descripcion.config(state="normal")
    texto_descripcion.delete(1.0, tk.END)
    texto_descripcion.insert(tk.END, f"Descripción: {logros[index]['descripcion']}")
    texto_descripcion.config(state="disabled")

def actualizar_ui():
    for widget in frame_logros.winfo_children():
        widget.destroy()

    categoria_seleccionada = combobox_categorias.get()
    logros_filtrados = [logro for logro in logros if logro["categoria"] == categoria_seleccionada]

    for i, logro in enumerate(logros_filtrados):
        estado = "✔" if logro["completado"] else "✘"
        color = "green" if logro["completado"] else "red"

        tk.Label(frame_logros, text=f"{estado}", fg=color, width=3).grid(row=i, column=0)
        tk.Button(frame_logros, text=logro['nombre'], anchor="w", command=lambda idx=logros.index(logro): mostrar_descripcion(idx)).grid(row=i, column=1, sticky="w")
        tk.Button(frame_logros, text="Cambiar", command=lambda idx=logros.index(logro): toggle_completado(idx)).grid(row=i, column=2)

def agregar_meta():
    nombre = entrada_nombreMeta.get()
    categoria = combobox_nueva_categoria.get() or entrada_nueva_categoria.get()
    descripcion = entrada_descripcion.get("1.0", tk.END).strip()
    tipo = combobox_tipo.get()

    if not nombre or not categoria or not descripcion or not tipo:
        messagebox.showerror("Error", "Parece que olvidaste algo, completa todos los campos para continuar.")
        return

    if categoria not in categorias:
        categorias.append(categoria)
        combobox_categorias["values"] = categorias
        combobox_nueva_categoria["values"] = categorias

    logros.append({"nombre": nombre, "categoria": categoria, "descripcion": descripcion, "tipo": tipo, "completado": False})
    guardar_progreso()
    actualizar_ui()
    entrada_nombreMeta.delete(0, tk.END)
    entrada_descripcion.delete("1.0", tk.END)
    combobox_nueva_categoria.set("")
    entrada_nueva_categoria.delete(0, tk.END)
    combobox_tipo.set("")
    messagebox.showinfo("Listo", "Tu meta fue agregada y está lista para ser realizada")

# Crear la ventana principal
root = tk.Tk()
root.title("logrosTracker")
root.geometry("800x800")

# Cargar progreso previo
cargar_progreso()

# Categorías disponibles
categorias = list(set(logro["categoria"] for logro in logros))

# Combobox para seleccionar categoría
frame_seleccion = tk.Frame(root)
frame_seleccion.pack(fill="x", padx=10, pady=5)

combobox_categorias = ttk.Combobox(frame_seleccion, values=categorias, state="readonly")
combobox_categorias.set(categorias[0])
combobox_categorias.pack(side="left", padx=5)
combobox_categorias.bind("<<ComboboxSelected>>", lambda e: actualizar_ui())

# Marco para los logros
frame_logros = tk.Frame(root)
frame_logros.pack(fill="both", expand=True, padx=10, pady=10)

# Texto para descripción
texto_descripcion = tk.Text(root, height=4, wrap="word", state="disabled")
texto_descripcion.pack(fill="x", padx=10, pady=10)

# Sección para agregar metas
frame_agregar = tk.Frame(root, relief="groove", borderwidth=2)
frame_agregar.pack(fill="x", padx=10, pady=10)

label_agregar = tk.Label(frame_agregar, text="Añadir nueva meta")
label_agregar.grid(row=0, column=0, columnspan=2, pady=5)

label_nombreMeta = tk.Label(frame_agregar, text="Nombre:")
label_nombreMeta.grid(row=1, column=0, sticky="e")
entrada_nombreMeta = tk.Entry(frame_agregar)
entrada_nombreMeta.grid(row=1, column=1, sticky="w")

label_categoria = tk.Label(frame_agregar, text="Categoría:")
label_categoria.grid(row=2, column=0, sticky="e")
combobox_nueva_categoria = ttk.Combobox(frame_agregar, values=categorias, state="readonly")
combobox_nueva_categoria.grid(row=2, column=1, sticky="w")

label_o_categoria = tk.Label(frame_agregar, text="Nueva categoria:")
label_o_categoria.grid(row=3, column=0, sticky="e")
entrada_nueva_categoria = tk.Entry(frame_agregar)
entrada_nueva_categoria.grid(row=3, column=1, sticky="w")

label_descripcion = tk.Label(frame_agregar, text="Descripción:")
label_descripcion.grid(row=4, column=0, sticky="ne")
entrada_descripcion = tk.Text(frame_agregar, height=4, width=40)
entrada_descripcion.grid(row=4, column=1, sticky="w")

label_tipo = tk.Label(frame_agregar, text="Trofeo:")
label_tipo.grid(row=5, column=0, sticky="e")
combobox_tipo = ttk.Combobox(frame_agregar, values=["Bronce", "Plata", "Oro", "Platino"], state="readonly")
combobox_tipo.grid(row=5, column=1, sticky="w")

boton_agregar = tk.Button(frame_agregar, text="Añadir Meta", command=agregar_meta)
boton_agregar.grid(row=6, column=0, columnspan=2, pady=5)

# Botones de guardar progreso
frame_botones = tk.Frame(root)
frame_botones.pack(fill="x", padx=10, pady=5)

boton_guardar = tk.Button(frame_botones, text="Guardar Progreso", command=guardar_progreso)
boton_guardar.pack(side="left", padx=5)

actualizar_ui()

root.mainloop()
