import os
import tkinter as tk
from tkinter import ttk, messagebox
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone

# --- 1. Inicialización y Conexión a Firebase ---
# Construimos la ruta absoluta para evitar errores de "Archivo no encontrado"
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_credenciales = os.path.join(directorio_actual, 'credentials', 'serviceAccountKey.json')

try:
    cred = credentials.Certificate(ruta_credenciales)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print(" Conexión a Firestore establecida en segundo plano.")
except Exception as e:
    # Si falla la conexión inicial, ni siquiera abrimos la interfaz
    print(f"❌ Error crítico al conectar con Firebase: {e}")
    exit()

# --- 2. Lógica de la Base de Datos vinculada a la Interfaz ---

def agregar_desde_gui():
    nombre = entry_nombre.get().strip()
    descripcion = entry_descripcion.get().strip()

    # Validación básica
    if not nombre:
        messagebox.showwarning("Advertencia", "El nombre no puede estar vacío.")
        return

    try:
        datos_muestra = {
            'nombre': nombre,
            'descripcion': descripcion,
            'fecha_registro': datetime.now(timezone.utc),
            'estado': 'pendiente'
        }
        
        _, doc_ref = db.collection('muestras').add(datos_muestra)
        messagebox.showinfo("Éxito", f"Muestra agregada correctamente.\nID: {doc_ref.id}")
        
        # Limpiamos los campos del formulario
        entry_nombre.delete(0, tk.END)
        entry_descripcion.delete(0, tk.END)
        
        # Refrescamos la tabla automáticamente
        cargar_muestras_gui() 
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al agregar la muestra:\n{e}")

def cargar_muestras_gui():
    # Limpiamos los datos actuales de la tabla (Treeview)
    for row in tree.get_children():
        tree.delete(row)

    try:
        docs = db.collection('muestras').order_by('fecha_registro').stream()
        for doc in docs:
            data = doc.to_dict()
            # Insertamos la fila en la tabla de Tkinter
            tree.insert("", tk.END, values=(
                doc.id,
                data.get('nombre', 'N/A'),
                data.get('estado', 'N/A')
            ))
    except Exception as e:
         messagebox.showerror("Error", f"Error al leer las muestras de la base de datos:\n{e}")

def procesar_muestra_gui():
    # Obtenemos qué fila ha seleccionado el usuario
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccione una muestra de la lista primero.")
        return

    # Extraemos el ID (que está en la primera columna oculta visualmente o mostrada)
    item = tree.item(seleccion)
    doc_id = item['values']

    try:
        doc_ref = db.collection('muestras').document(doc_id)
        doc_ref.update({'estado': 'procesada'})
        messagebox.showinfo("Éxito", f"Muestra actualizada a 'procesada'.")
        cargar_muestras_gui() # Refrescar para ver el cambio
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar:\n{e}")

def borrar_muestra_gui():
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccione una muestra de la lista primero.")
        return

    item = tree.item(seleccion)
    doc_id = item['values']

    # Cuadro de diálogo de confirmación
    confirmacion = messagebox.askyesno("Confirmar Borrado", f"¿Está seguro de borrar definitivamente la muestra {doc_id}?")
    
    if confirmacion:
        try:
            doc_ref = db.collection('muestras').document(doc_id)
            doc_ref.delete()
            messagebox.showinfo("Éxito", "Muestra eliminada.")
            cargar_muestras_gui()
        except Exception as e:
             messagebox.showerror("Error", f"Error al intentar borrar:\n{e}")


# --- 3. Construcción de la Interfaz Gráfica (Ventana) ---

root = tk.Tk()
root.title("🔬 Gestor de Laboratorio V2 (GUI)")
root.geometry("650x500")

# --- Panel Superior: Formulario de Entrada ---
frame_form = tk.LabelFrame(root, text="Registrar Nueva Muestra", padx=10, pady=10)
frame_form.pack(padx=10, pady=10, fill="x")

tk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
entry_nombre = tk.Entry(frame_form, width=50)
entry_nombre.grid(row=0, column=1, pady=5, padx=5)

tk.Label(frame_form, text="Descripción:").grid(row=1, column=0, sticky="w", pady=5)
entry_descripcion = tk.Entry(frame_form, width=50)
entry_descripcion.grid(row=1, column=1, pady=5, padx=5)

btn_agregar = tk.Button(frame_form, text="Agregar Muestra", command=agregar_desde_gui, bg="lightblue")
btn_agregar.grid(row=2, columnspan=2, pady=10)


# --- Panel Central: Tabla (Treeview) ---
frame_lista = tk.LabelFrame(root, text="Muestras en la Base de Datos", padx=10, pady=10)
frame_lista.pack(padx=10, pady=5, fill="both", expand=True)

# Configuramos las columnas
columnas = ("ID", "Nombre", "Estado")
tree = ttk.Treeview(frame_lista, columns=columnas, show="headings", selectmode="browse")
tree.heading("ID", text="ID Documento")
tree.heading("Nombre", text="Nombre")
tree.heading("Estado", text="Estado")

# Tamaños de las columnas
tree.column("ID", width=180)
tree.column("Nombre", width=250)
tree.column("Estado", width=100)

tree.pack(fill="both", expand=True)


# --- Panel Inferior: Botones de Acción ---
frame_acciones = tk.Frame(root, pady=10)
frame_acciones.pack(fill="x")

btn_refrescar = tk.Button(frame_acciones, text="🔄 Refrescar Lista", command=cargar_muestras_gui)
btn_refrescar.pack(side="left", padx=10)

btn_procesar = tk.Button(frame_acciones, text="✅ Marcar como 'Procesada'", command=procesar_muestra_gui, bg="lightgreen")
btn_procesar.pack(side="left", padx=10)

btn_borrar = tk.Button(frame_acciones, text="🗑️ Borrar Muestra", command=borrar_muestra_gui, bg="salmon")
btn_borrar.pack(side="right", padx=10)

# Al iniciar el programa, cargamos la lista de muestras automáticamente
cargar_muestras_gui()

# Iniciamos el bucle de la interfaz gráfica
root.mainloop()