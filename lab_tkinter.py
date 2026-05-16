import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import lab 

usuario_actual = None

def mostrar_pantalla_inicial():
    for widget in ventana_acceso.winfo_children():
        widget.destroy()
    ventana_acceso.title("🔒 ClinicData - Acceso")
    
    canvas_perfil = tk.Canvas(ventana_acceso, width=80, height=80, bg="#f4f6f9", highlightthickness=0)
    canvas_perfil.pack(pady=15)
    canvas_perfil.create_oval(25, 10, 55, 40, fill="#7f8c8d", outline="")
    canvas_perfil.create_oval(10, 45, 70, 90, fill="#7f8c8d", outline="")
    
    tk.Label(ventana_acceso, text="CLINICDATA LOGIN", font=("Arial", 14, "bold"), bg="#f4f6f9", fg="#2c3e50").pack(pady=5)
    
    frame_opciones = tk.Frame(ventana_acceso, bg="#f4f6f9")
    frame_opciones.pack(pady=20)
    
    tk.Button(frame_opciones, text="🔑 Iniciar Sesión", command=mostrar_formulario_login, bg="#2ecc71", fg="white", width=18, font=("Arial", 10, "bold"), pady=5).pack(pady=5)
    tk.Button(frame_opciones, text="📝 Registrarse (Doctores)", command=mostrar_formulario_registro, bg="#3498db", fg="white", width=18, font=("Arial", 10, "bold"), pady=5).pack(pady=5)

def mostrar_formulario_login():
    global entry_email, entry_password
    for widget in ventana_acceso.winfo_children():
        widget.destroy()
    ventana_acceso.title(" ClinicData - Login")
    tk.Label(ventana_acceso, text="INICIAR SESIÓN", font=("Arial", 12, "bold"), bg="#f4f6f9", fg="#2c3e50").pack(pady=15)
    
    frame_fields = tk.Frame(ventana_acceso, bg="#f4f6f9")
    frame_fields.pack(pady=5)
    tk.Label(frame_fields, text="Correo Electrónico:").grid(row=0, column=0, sticky="w", pady=5)
    entry_email = tk.Entry(frame_fields, width=25)
    entry_email.grid(row=0, column=1, pady=5, padx=5)
    
    tk.Label(frame_fields, text="Contraseña:").grid(row=1, column=0, sticky="w", pady=5)
    entry_password = tk.Entry(frame_fields, width=25, show="*")
    entry_password.grid(row=1, column=1, pady=5, padx=5)
    
    frame_btns = tk.Frame(ventana_acceso, bg="#f4f6f9")
    frame_btns.pack(pady=20)
    tk.Button(frame_btns, text="Entrar", command=ejecutar_login, bg="#2ecc71", fg="white", width=12, font=("Arial", 9, "bold")).pack(side="left", padx=5)
    tk.Button(frame_btns, text="Volver", command=mostrar_pantalla_inicial, bg="#95a5a6", fg="white", width=12).pack(side="left", padx=5)

def mostrar_formulario_registro():
    global entry_email, entry_password
    for widget in ventana_acceso.winfo_children():
        widget.destroy()
    ventana_acceso.title(" ClinicData - Alta Doctores")
    tk.Label(ventana_acceso, text="REGISTRO EN DOCUMENTO 'DOCTORES'", font=("Arial", 11, "bold"), bg="#f4f6f9", fg="#2c3e50").pack(pady=15)
    
    frame_fields = tk.Frame(ventana_acceso, bg="#f4f6f9")
    frame_fields.pack(pady=5)
    tk.Label(frame_fields, text="Correo Electrónico:").grid(row=0, column=0, sticky="w", pady=5)
    entry_email = tk.Entry(frame_fields, width=25)
    entry_email.grid(row=0, column=1, pady=5, padx=5)
    
    tk.Label(frame_fields, text="Contraseña:").grid(row=1, column=0, sticky="w", pady=5)
    entry_password = tk.Entry(frame_fields, width=25, show="*")
    entry_password.grid(row=1, column=1, pady=5, padx=5)
    
    frame_btns = tk.Frame(ventana_acceso, bg="#f4f6f9")
    frame_btns.pack(pady=20)
    tk.Button(frame_btns, text="Registrar", command=ejecutar_registro, bg="#3498db", fg="white", width=12, font=("Arial", 9, "bold")).pack(side="left", padx=5)
    tk.Button(frame_btns, text="Volver", command=mostrar_pantalla_inicial, bg="#95a5a6", fg="white", width=12).pack(side="left", padx=5)

def ejecutar_login():
    global usuario_actual
    email = entry_email.get().strip()
    password = entry_password.get().strip()
    if not email or not password:
        messagebox.showwarning("Campos vacíos", "Introduce correo y contraseña.")
        return
    try:
        usuario_actual = lab.iniciar_sesion_simulado(email, password)
        nombre_limpio = email.split('@')[0]
        messagebox.showinfo("Éxito", f"¡Bienvenido, Doctor/a {nombre_limpio}!")
        ventana_acceso.destroy()
        abrir_ventana_principal()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def ejecutar_registro():
    email = entry_email.get().strip()
    password = entry_password.get().strip()
    if not email or not password:
        messagebox.showwarning("Campos vacíos", "Introduce datos para el registro.")
        return
    if len(password) < 6:
        messagebox.showwarning("Contraseña corta", "La contraseña debe tener al menos 6 caracteres.")
        return
    try:
        lab.registrar_usuario_email(email, password)
        nombre_limpio = email.split('@')[0]
        messagebox.showinfo("Éxito", f"Doctor/a {nombre_limpio} guardado correctamente en 'Doctores'.")
        mostrar_pantalla_inicial()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def agregar_desde_gui():
    edad = entry_edad.get().strip()
    peso = entry_peso.get().strip()
    historial = entry_historial.get().strip()
    tipo_m = entry_tipo_muestra.get().strip()
    estado_m = entry_estado_muestra.get().strip()

    if not edad or not peso or not historial or not tipo_m or not estado_m:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
        return

    try:
        doc_id = lab.agregar_datos_clinicos(usuario_actual.email, edad, historial, peso, tipo_m, estado_m)
        messagebox.showinfo("Éxito", f"Paciente añadido debajo del 4005.\nID asignado: {doc_id}")
        
        entry_edad.delete(0, tk.END)
        entry_peso.delete(0, tk.END)
        entry_historial.delete(0, tk.END)
        entry_tipo_muestra.delete(0, tk.END)
        entry_estado_muestra.delete(0, tk.END)
        cargar_tabla_completa() 
    except Exception as e:
        messagebox.showerror("Error", str(e))


def cerrar_sesion_gui():
    global usuario_actual
    if messagebox.askyesno("Cerrar Sesión", "¿Seguro que deseas salir del sistema clínico?"):
        usuario_actual = None  # Olvidamos al doctor actual
        # Buscamos la ventana principal activa de los pacientes y la destruimos
        for widget in ventana_acceso.master.winfo_children() if hasattr(ventana_acceso, 'master') else []:
            pass
            # El truco más limpio: cerramos todo y reiniciamos la app desde el login
        root_actual = tk._default_root
        if root_actual:
            root_actual.destroy()  # Cierra la pantalla médica

        # Volvemos a arrancar la ventanita de inicio de sesión obligatoria
        os.system("python lab_tkinter.py")

def cargar_tabla_completa():
    for row in tree.get_children():
        tree.delete(row)
    try:
        filas = lab.leer_todo_el_panel()
        for f in filas:
            tree.insert("", tk.END, values=(f['id'], f['Age'], f['Peso'], f['Doctor'], f['tipo_muestra'], f['estado_muestra'], f['Historial']))
    except Exception as e:
         messagebox.showerror("Error", f"Error de sincronización:\n{e}")

def actualizar_registro_gui():
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccione un registro de la lista.")
        return
    
    item = tree.item(seleccion)
    valores = item['values']
    paciente_id = str(valores[0])

    nueva_edad = simpledialog.askstring("Modificar", "Nueva Edad (Age):", initialvalue=valores[1])
    if nueva_edad is None: return
    nuevo_peso = simpledialog.askstring("Modificar", "Nuevo Peso:", initialvalue=valores[2])
    if nuevo_peso is None: return
    nuevo_tipo = simpledialog.askstring("Modificar", "Nuevo Tipo de Muestra:", initialvalue=valores[4])
    if nuevo_tipo is None: return
    nuevo_estado = simpledialog.askstring("Modificar", "Nuevo Estado de Muestra:", initialvalue=valores[5])
    if nuevo_estado is None: return
    nuevo_historial = simpledialog.askstring("Modificar", "Historial Clínico:", initialvalue=valores[6])
    if nuevo_historial is None: return

    try:
        nombre_doc = usuario_actual.email.split('@')[0]
        datos_p = {'Age': int(nueva_edad), 'Peso': float(nuevo_peso), 'Historial': nuevo_historial, 'Doctor': str(nombre_doc)}
        datos_m = {'tipo_muestra': nuevo_tipo, 'estado_muestra': nuevo_estado}
        
        lab.actualizar_datos_clinicos(paciente_id, datos_p, datos_m)
        messagebox.showinfo("Éxito", "Campos actualizados correctamente.")
        cargar_tabla_completa()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def borrar_muestra_gui():
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccione un registro primero.")
        return
    item = tree.item(seleccion)
    valores = item['values']
    paciente_id = str(valores[0])

    if messagebox.askyesno("Confirmar", f"¿Eliminar el campo del paciente {paciente_id}?"):
        try:
            lab.eliminar_datos_clinicos(paciente_id)
            messagebox.showinfo("Éxito", "Campo eliminado del documento.")
            cargar_tabla_completa()
        except Exception as e:
             messagebox.showerror("Error", str(e))

def abrir_ventana_principal():
    global entry_edad, entry_peso, entry_historial, entry_tipo_muestra, entry_estado_muestra, tree
    root = tk.Tk()
    root.title("🔬 ClinicData - Sistema Integrado")
    root.geometry("900x600")
    
    frame_header = tk.Frame(root, bg="#2c3e50", height=50)
    frame_header.pack(fill="x", side="top")
    tk.Label(frame_header, text=" CLINICDATA - ARCHIVO DE PACIENTES", font=("Arial", 11, "bold"), fg="white", bg="#2c3e50").pack(side="left", padx=15, pady=10)
    tk.Button(frame_header, text="🚪 Cerrar Sesión", command=cerrar_sesion_gui, bg="#e74c3c", fg="white", font=("Arial", 9, "bold"), padx=10).pack(side="right", padx=10, pady=10)

    avatar_canvas = tk.Canvas(frame_header, width=35, height=35, bg="#2c3e50", highlightthickness=0)
    avatar_canvas.pack(side="right", padx=15, pady=5)
    avatar_canvas.create_oval(2, 2, 33, 33, fill="#3498db", outline="")
    
    nombre_doc = usuario_actual.email.split('@')[0]
    avatar_canvas.create_text(18, 18, text=nombre_doc[:4].upper(), fill="white", font=("Arial", 8, "bold"))
    tk.Label(frame_header, text=f"Doctor/a: {nombre_doc}", font=("Arial", 9), fg="white", bg="#2c3e50").pack(side="right", padx=5)

    frame_form = tk.LabelFrame(root, text=" Formulario Clínico (Guardado en documento 'Pacientes') ", padx=10, pady=10)
    frame_form.pack(padx=15, pady=10, fill="x")
    
    tk.Label(frame_form, text="Edad (Age):").grid(row=0, column=0, sticky="w", pady=5)
    entry_edad = tk.Entry(frame_form, width=15)
    entry_edad.grid(row=0, column=1, pady=5, padx=5, sticky="w")
    
    tk.Label(frame_form, text="Peso (Kg):").grid(row=0, column=2, sticky="w", pady=5, padx=15)
    entry_peso = tk.Entry(frame_form, width=15)
    entry_peso.grid(row=0, column=3, pady=5, padx=5, sticky="w")
    
    tk.Label(frame_form, text="Tipo Muestra:").grid(row=0, column=4, sticky="w", pady=5, padx=15)
    entry_tipo_muestra = tk.Entry(frame_form, width=20)
    entry_tipo_muestra.grid(row=0, column=5, pady=5, padx=5, sticky="w")

    tk.Label(frame_form, text="Estado Muestra:").grid(row=1, column=0, sticky="w", pady=5)
    entry_estado_muestra = tk.Entry(frame_form, width=15)
    entry_estado_muestra.grid(row=1, column=1, pady=5, padx=5, sticky="w")

    tk.Label(frame_form, text="Historial Clínico:").grid(row=1, column=2, sticky="w", pady=5, padx=15)
    entry_historial = tk.Entry(frame_form, width=52)
    entry_historial.grid(row=1, column=3, columnspan=3, pady=5, padx=5, sticky="w")
    
    tk.Button(frame_form, text="Guardar Registro Clínico", command=agregar_desde_gui, bg="#3498db", fg="white", font=("Arial", 9, "bold")).grid(row=2, columnspan=6, pady=10)

    frame_lista = tk.LabelFrame(root, text=" Campos del documento 'Pacientes' en Tiempo Real ", padx=10, pady=10)
    frame_lista.pack(padx=15, pady=5, fill="both", expand=True)

    columnas = ("ID", "Edad", "Peso", "Doctor", "TipoMuestra", "EstadoMuestra", "Historial")
    tree = ttk.Treeview(frame_lista, columns=columnas, show="headings", selectmode="browse")
    tree.heading("ID", text="ID Mapa")
    tree.heading("Edad", text="Edad (Age)")
    tree.heading("Peso", text="Peso")
    tree.heading("Doctor", text="Doctor")
    tree.heading("TipoMuestra", text="Tipo Muestra")
    tree.heading("EstadoMuestra", text="Estado Muestra")
    tree.heading("Historial", text="Historial")
    
    tree.column("ID", width=90, anchor="center")
    tree.column("Edad", width=70, anchor="center")
    tree.column("Peso", width=70, anchor="center")
    tree.column("Doctor", width=100, anchor="center")
    tree.column("TipoMuestra", width=120, anchor="center")
    tree.column("EstadoMuestra", width=120, anchor="center")
    tree.column("Historial", width=220)
    tree.pack(fill="both", expand=True)

    frame_acciones = tk.Frame(root, pady=10)
    frame_acciones.pack(fill="x", padx=15)

    tk.Button(frame_acciones, text=" Actualizar Registro", command=actualizar_registro_gui, bg="#2ecc71", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)
    tk.Button(frame_acciones, text=" Eliminar Ficha", command=borrar_muestra_gui, bg="#e74c3c", fg="white", font=("Arial", 10, "bold")).pack(side="right", padx=5)

    cargar_tabla_completa()
    root.mainloop()

# --- ARRANQUE ---
if lab.db is None:
    root_err = tk.Tk()
    root_err.withdraw()
    messagebox.showerror("Error", "No se detecta la base de datos.")
    exit()

ventana_acceso = tk.Tk()
ventana_acceso.geometry("380x300")
ventana_acceso.resizable(False, False)
ventana_acceso.configure(bg="#f4f6f9")
mostrar_pantalla_inicial()
ventana_acceso.mainloop()
