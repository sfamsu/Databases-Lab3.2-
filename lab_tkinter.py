import ssl
import os

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

import os
import tkinter as tk
from tkinter import ttk, messagebox
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone
import threading
import time

# --- 1. Inicialización y Conexión a Firebase ---
# Construimos la ruta absoluta para evitar errores de "Archivo no encontrado"
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_credenciales = os.path.join(directorio_actual, 'credentials', 'serviceAccountKey.json')

try:
    cred = credentials.Certificate(ruta_credenciales)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Conexión a Firestore establecida en segundo plano.")
except Exception as e:
    # Si falla la conexión inicial, ni siquiera abrimos la interfaz
    print(f"❌ Error crítico al conectar con Firebase: {e}")
    exit()

# --- 2. Lógica de la Base de Datos vinculada a la Interfaz ---

# Variables globales para autenticación
usuario_actual = None
ventana_login = None
ventana_registro = None

# Funciones para AUTENTICACIÓN (simulada para demostración)
def mostrar_login():
    global ventana_login
    ventana_login = tk.Toplevel(root)
    ventana_login.title("Iniciar Sesión")
    ventana_login.geometry("400x300")
    ventana_login.grab_set()  # Modal
    
    frame_login = tk.Frame(ventana_login, padx=20, pady=20)
    frame_login.pack(fill="both", expand=True)
    
    tk.Label(frame_login, text="🔐 Iniciar Sesión", font=("Arial", 16, "bold")).pack(pady=10)
    
    tk.Label(frame_login, text="Email:").pack(anchor="w")
    entry_login_email = tk.Entry(frame_login, width=30)
    entry_login_email.pack(pady=5)
    
    tk.Label(frame_login, text="Contraseña:").pack(anchor="w")
    entry_login_pass = tk.Entry(frame_login, width=30, show="*")
    entry_login_pass.pack(pady=5)
    
    def login():
        email = entry_login_email.get().strip()
        password = entry_login_pass.get().strip()
        
        if not email or not password:
            messagebox.showwarning("Advertencia", "Complete todos los campos.")
            return
        
        try:
            # Simulación de autenticación - en producción usar Firebase Auth SDK
            # Aquí verificamos si existe el usuario en Firestore
            docs = db.collection('usuarios').where('email', '==', email).stream()
            usuario_encontrado = None
            for doc in docs:
                usuario_encontrado = doc.to_dict()
                usuario_encontrado['id'] = doc.id
                break
            
            if usuario_encontrado:
                global usuario_actual
                usuario_actual = usuario_encontrado
                messagebox.showinfo("Éxito", f"Bienvenido, {usuario_actual['nombre_completo']}!")
                ventana_login.destroy()
                actualizar_interfaz_usuario()
            else:
                messagebox.showerror("Error", "Usuario no encontrado. Regístrese primero.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar sesión:\n{e}")
    
    btn_login = tk.Button(frame_login, text="Iniciar Sesión", command=login, bg="lightblue", width=20)
    btn_login.pack(pady=10)
    
    btn_registro = tk.Button(frame_login, text="Crear Cuenta", command=lambda: [ventana_login.destroy(), mostrar_registro()], width=20)
    btn_registro.pack(pady=5)
    
    def cerrar_login():
        ventana_login.destroy()
    
    ventana_login.protocol("WM_DELETE_WINDOW", cerrar_login)

def mostrar_registro():
    global ventana_registro
    ventana_registro = tk.Toplevel(root)
    ventana_registro.title("Registrarse")
    ventana_registro.geometry("400x350")
    ventana_registro.grab_set()
    
    frame_registro = tk.Frame(ventana_registro, padx=20, pady=20)
    frame_registro.pack(fill="both", expand=True)
    
    tk.Label(frame_registro, text="📝 Crear Cuenta", font=("Arial", 16, "bold")).pack(pady=10)
    
    tk.Label(frame_registro, text="Nombre Completo:").pack(anchor="w")
    entry_reg_nombre = tk.Entry(frame_registro, width=30)
    entry_reg_nombre.pack(pady=5)
    
    tk.Label(frame_registro, text="Email:").pack(anchor="w")
    entry_reg_email = tk.Entry(frame_registro, width=30)
    entry_reg_email.pack(pady=5)
    
    tk.Label(frame_registro, text="Contraseña:").pack(anchor="w")
    entry_reg_pass = tk.Entry(frame_registro, width=30, show="*")
    entry_reg_pass.pack(pady=5)
    
    tk.Label(frame_registro, text="Confirmar Contraseña:").pack(anchor="w")
    entry_reg_pass_confirm = tk.Entry(frame_registro, width=30, show="*")
    entry_reg_pass_confirm.pack(pady=5)
    
    def registrar():
        nombre = entry_reg_nombre.get().strip()
        email = entry_reg_email.get().strip()
        password = entry_reg_pass.get().strip()
        password_confirm = entry_reg_pass_confirm.get().strip()
        
        if not nombre or not email or not password:
            messagebox.showwarning("Advertencia", "Complete todos los campos.")
            return
        
        if password != password_confirm:
            messagebox.showwarning("Advertencia", "Las contraseñas no coinciden.")
            return
        
        try:
            # Verificar si el email ya existe
            docs = db.collection('usuarios').where('email', '==', email).stream()
            if list(docs):
                messagebox.showerror("Error", "Este email ya está registrado.")
                return
            
            # Crear usuario en Firestore
            datos_usuario = {
                'nombre_completo': nombre,
                'email': email,
                'fecha_registro': datetime.now(timezone.utc),
                'rol': 'tecnico'
            }
            
            _, doc_ref = db.collection('usuarios').add(datos_usuario)
            messagebox.showinfo("Éxito", "Cuenta creada exitosamente. Ahora puede iniciar sesión.")
            ventana_registro.destroy()
            mostrar_login()
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar:\n{e}")
    
    btn_registrar = tk.Button(frame_registro, text="Registrarse", command=registrar, bg="lightgreen", width=20)
    btn_registrar.pack(pady=10)
    
    btn_cancelar = tk.Button(frame_registro, text="Cancelar", command=lambda: [ventana_registro.destroy(), mostrar_login()], width=20)
    btn_cancelar.pack(pady=5)
    
    def cerrar_registro():
        ventana_registro.destroy()
        mostrar_login()
    
    ventana_registro.protocol("WM_DELETE_WINDOW", cerrar_registro)

def logout():
    global usuario_actual
    usuario_actual = None
    actualizar_interfaz_usuario()
    messagebox.showinfo("Sesión", "Has cerrado sesión exitosamente.")

def actualizar_interfaz_usuario():
    global usuario_actual
    
    if usuario_actual:
        # Usuario logueado
        label_usuario.config(text=f"👤 {usuario_actual['nombre_completo']}", fg="green")
        btn_login.config(state="disabled")
        btn_registro.config(state="disabled")
        btn_logout.config(state="normal")
    else:
        # Usuario no logueado
        label_usuario.config(text="👤 No logueado", fg="red")
        btn_login.config(state="normal")
        btn_registro.config(state="normal")
        btn_logout.config(state="disabled")

# Funciones para CATEGORIAS
def agregar_categoria():
    nombre = entry_cat_nombre.get().strip()
    descripcion = entry_cat_descripcion.get().strip()

    if not nombre:
        messagebox.showwarning("Advertencia", "El nombre de la categoría no puede estar vacío.")
        return

    try:
        datos_categoria = {
            'nombre': nombre,
            'descripcion': descripcion,
            'fecha_creacion': datetime.now(timezone.utc)
        }
        
        _, doc_ref = db.collection('categorias').add(datos_categoria)
        messagebox.showinfo("Éxito", f"Categoría agregada correctamente.\nID: {doc_ref.id}")
        
        entry_cat_nombre.delete(0, tk.END)
        entry_cat_descripcion.delete(0, tk.END)
        
        cargar_categorias_gui()
        cargar_categorias_combo()
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al agregar la categoría:\n{e}")

def cargar_categorias_gui():
    for row in tree_categorias.get_children():
        tree_categorias.delete(row)

    try:
        docs = db.collection('categorias').order_by('fecha_creacion').stream()
        for doc in docs:
            data = doc.to_dict()
            tree_categorias.insert("", tk.END, values=(
                doc.id,
                data.get('nombre', 'N/A'),
                data.get('descripcion', 'N/A')
            ))
    except Exception as e:
        messagebox.showerror("Error", f"Error al leer las categorías:\n{e}")

def cargar_categorias_combo():
    try:
        categorias = []
        docs = db.collection('categorias').stream()
        for doc in docs:
            data = doc.to_dict()
            categorias.append(data.get('nombre', 'N/A'))
        combo_categoria['values'] = categorias
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar categorías en el combo:\n{e}")

def borrar_categoria():
    seleccion = tree_categorias.selection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccione una categoría primero.")
        return

    item = tree_categorias.item(seleccion)
    doc_id = item['values'][0]

    confirmacion = messagebox.askyesno("Confirmar Borrado", f"¿Está seguro de borrar la categoría {doc_id}?")
    
    if confirmacion:
        try:
            doc_ref = db.collection('categorias').document(doc_id)
            doc_ref.delete()
            messagebox.showinfo("Éxito", "Categoría eliminada.")
            cargar_categorias_gui()
            cargar_categorias_combo()
        except Exception as e:
            messagebox.showerror("Error", f"Error al borrar categoría:\n{e}")



def agregar_desde_gui():
    nombre = entry_nombre.get().strip()
    descripcion = entry_descripcion.get().strip()
    categoria_seleccionada = combo_categoria.get()

    # Validación básica
    if not nombre:
        messagebox.showwarning("Advertencia", "El nombre no puede estar vacío.")
        return
    
    if not categoria_seleccionada:
        messagebox.showwarning("Advertencia", "Debe seleccionar una categoría.")
        return

    try:
        # Obtener el ID de la categoría seleccionada
        categoria_id = None
        docs = db.collection('categorias').where('nombre', '==', categoria_seleccionada).stream()
        for doc in docs:
            categoria_id = doc.id
            break
        
        if not categoria_id:
            messagebox.showerror("Error", "No se encontró la categoría seleccionada.")
            return

        datos_muestra = {
            'nombre': nombre,
            'descripcion': descripcion,
            'fecha_registro': datetime.now(timezone.utc),
            'estado': 'pendiente',
            'categoria_id': categoria_id,
            'categoria_nombre': categoria_seleccionada,
            'usuario_id': usuario_actual['id'] if usuario_actual else None,
            'usuario_nombre': usuario_actual['nombre_completo'] if usuario_actual else 'Anónimo'
        }
        
        _, doc_ref = db.collection('muestras').add(datos_muestra)
        messagebox.showinfo("Éxito", f"Muestra agregada correctamente.\nID: {doc_ref.id}")
        
        # Limpiamos los campos del formulario
        entry_nombre.delete(0, tk.END)
        entry_descripcion.delete(0, tk.END)
        combo_categoria.set('')
        
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
                data.get('categoria_nombre', 'N/A'),
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
root.title("🔬 Gestor de Laboratorio V3 (GUI + Auth)")
root.geometry("700x650")

# --- Barra Superior: Información de Usuario ---
frame_usuario = tk.Frame(root, pady=5)
frame_usuario.pack(fill="x", padx=10)

label_usuario = tk.Label(frame_usuario, text="👤 No logueado", font=("Arial", 10), fg="red")
label_usuario.pack(side="left")

frame_botones_auth = tk.Frame(frame_usuario)
frame_botones_auth.pack(side="right")

btn_login = tk.Button(frame_botones_auth, text="Login", command=mostrar_login, width=8)
btn_login.pack(side="left", padx=2)

btn_registro = tk.Button(frame_botones_auth, text="Registro", command=mostrar_registro, width=8)
btn_registro.pack(side="left", padx=2)

btn_logout = tk.Button(frame_botones_auth, text="Logout", command=logout, width=8, state="disabled")
btn_logout.pack(side="left", padx=2)

# --- Panel Superior: Formulario de Entrada ---
frame_form = tk.LabelFrame(root, text="Registrar Nueva Muestra", padx=10, pady=10)
frame_form.pack(padx=10, pady=10, fill="x")

tk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
entry_nombre = tk.Entry(frame_form, width=50)
entry_nombre.grid(row=0, column=1, pady=5, padx=5)

tk.Label(frame_form, text="Descripción:").grid(row=1, column=0, sticky="w", pady=5)
entry_descripcion = tk.Entry(frame_form, width=50)
entry_descripcion.grid(row=1, column=1, pady=5, padx=5)

tk.Label(frame_form, text="Categoría:").grid(row=2, column=0, sticky="w", pady=5)
combo_categoria = ttk.Combobox(frame_form, width=47)
combo_categoria.grid(row=2, column=1, pady=5, padx=5)

cargar_categorias_combo()

btn_agregar = tk.Button(frame_form, text="Agregar Muestra", command=agregar_desde_gui, bg="lightblue")
btn_agregar.grid(row=3, columnspan=2, pady=10)



# --- Panel Central: Tabla (Treeview) ---
frame_lista = tk.LabelFrame(root, text="Muestras en la Base de Datos", padx=10, pady=10)
frame_lista.pack(padx=10, pady=5, fill="both", expand=True)

# Configuramos las columnas
columnas = ("ID", "Nombre", "Categoría", "Estado")
tree = ttk.Treeview(frame_lista, columns=columnas, show="headings", selectmode="browse")
tree.heading("ID", text="ID Documento")
tree.heading("Nombre", text="Nombre")
tree.heading("Categoría", text="Categoría")
tree.heading("Estado", text="Estado")

# Tamaños de las columnas
tree.column("ID", width=150)
tree.column("Nombre", width=200)
tree.column("Categoría", width=150)
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

# --- Panel de Categorías ---
frame_categorias = tk.LabelFrame(root, text="Gestión de Categorías", padx=10, pady=10)
frame_categorias.pack(padx=10, pady=10, fill="x")

# Formulario de categorías
tk.Label(frame_categorias, text="Nombre Categoría:").grid(row=0, column=0, sticky="w", pady=5)
entry_cat_nombre = tk.Entry(frame_categorias, width=30)
entry_cat_nombre.grid(row=0, column=1, pady=5, padx=5)

tk.Label(frame_categorias, text="Descripción:").grid(row=1, column=0, sticky="w", pady=5)
entry_cat_descripcion = tk.Entry(frame_categorias, width=30)
entry_cat_descripcion.grid(row=1, column=1, pady=5, padx=5)

btn_agregar_cat = tk.Button(frame_categorias, text="Agregar Categoría", command=agregar_categoria, bg="lightyellow")
btn_agregar_cat.grid(row=2, column=0, columnspan=2, pady=5)

# Tabla de categorías
columnas_cat = ("ID", "Nombre", "Descripción")
tree_categorias = ttk.Treeview(frame_categorias, columns=columnas_cat, show="headings", selectmode="browse", height=4)
tree_categorias.heading("ID", text="ID")
tree_categorias.heading("Nombre", text="Nombre")
tree_categorias.heading("Descripción", text="Descripción")
tree_categorias.column("ID", width=150)
tree_categorias.column("Nombre", width=150)
tree_categorias.column("Descripción", width=300)
tree_categorias.grid(row=3, column=0, columnspan=2, pady=5, sticky="nsew")

btn_borrar_cat = tk.Button(frame_categorias, text="🗑️ Borrar Categoría", command=borrar_categoria, bg="salmon")
btn_borrar_cat.grid(row=4, column=0, columnspan=2, pady=5)

# Cargar categorías al inicio
cargar_categorias_gui()

# Al iniciar el programa, cargamos la lista de muestras automáticamente
cargar_muestras_gui()

# Iniciamos el bucle de la interfaz gráfica
root.mainloop()