import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import lab 

usuario_actual = None

def mostrar_pantalla_inicial():
    for widget in ventana_acceso.winfo_children():
        widget.destroy()
    ventana_acceso.title(" ClinicData - Acceso")
    
    canvas_perfil = tk.Canvas(ventana_acceso, width=80, height=80, bg="#f4f6f9", highlightthickness=0)
    canvas_perfil.pack(pady=15)
    canvas_perfil.create_oval(25, 10, 55, 40, fill="#7f8c8d", outline="")
    canvas_perfil.create_oval(10, 45, 70, 90, fill="#7f8c8d", outline="")
    
    tk.Label(ventana_acceso, text="CLINICDATA LOGIN", font=("Arial", 14, "bold"), bg="#f4f6f9", fg="#2c3e50").pack(pady=5)
    
    frame_opciones = tk.Frame(ventana_acceso, bg="#f4f6f9")
    frame_opciones.pack(pady=20)
    
    tk.Button(frame_opciones, text="Iniciar Sesión", command=mostrar_formulario_login, bg="#2ecc71", fg="white", width=18, font=("Arial", 10, "bold"), pady=5).pack(pady=5)
    tk.Button(frame_opciones, text="Registrarse (Doctores)", command=mostrar_formulario_registro, bg="#3498db", fg="white", width=18, font=("Arial", 10, "bold"), pady=5).pack(pady=5)

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
        # Le pasamos el email y la contraseña a lab para que los verifique de verdad
        usuario_actual = lab.iniciar_sesion_simulado(email, password)

        nombre_limpio = email.split('@')[0]
        messagebox.showinfo("Éxito", f"¡Bienvenido, Doctor/a {nombre_limpio}!")
        ventana_acceso.destroy()
        abrir_ventana_principal()
    except Exception as e:
        messagebox.showerror("Error de Acceso", str(e))

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
    doc_id = entry_doc_id.get().strip()
    sintoma = entry_sintoma.get().strip()
    test_res = entry_test.get().strip()
    historial = entry_historial.get().strip()

    if not edad or not peso or not doc_id or not sintoma or not test_res or not historial:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
        return

    try:
        nuevo_id = lab.agregar_datos_clinicos(doc_id, edad, historial, peso, sintoma, test_res)
        messagebox.showinfo("Éxito", f"Paciente cardíaco añadido con ID: {nuevo_id}")

        # Vaciamos los campos nuevos de forma correcta para que no queden textos viejos
        entry_edad.delete(0, tk.END)
        entry_peso.delete(0, tk.END)
        entry_doc_id.delete(0, tk.END)
        entry_sintoma.delete(0, tk.END)
        entry_test.delete(0, tk.END)
        entry_historial.delete(0, tk.END)

        cargar_tabla_completa()
    except Exception as e:
        messagebox.showerror("Error", str(e))


def cerrar_sesion_gui():
    global usuario_actual
    if messagebox.askyesno("Cerrar Sesión", "¿Seguro que deseas salir del sistema clínico?"):
        usuario_actual = None  # Olvidamos al doctor actual

        # Cerramos de forma segura la ventana principal actual
        root_actual = tk._default_root
        if root_actual:
            root_actual.destroy()

        # Reiniciamos la aplicación limpia desde el archivo principal
        os.system("python lab_tkinter.py")

def cargar_tabla_completa():
    for row in tree.get_children():
        tree.delete(row)
    try:
        filas = lab.leer_todo_el_panel()

        # Buscamos el ID numérico para hacer el filtro de forma matemática
        filtro_actual = combo_filtro.get() if 'combo_filtro' in globals() else "Todos"
        id_doc_actual = usuario_actual.id_doctor_num if usuario_actual and hasattr(usuario_actual,'id_doctor_num') else ""

        for f in filas:
            # Comparamos el ID numérico guardado en el paciente con el del doctor logueado
            if filtro_actual == "Mis Pacientes" and str(f['Doctor']) != str(id_doc_actual):
                continue

            tree.insert("", tk.END, values=(
                f['id'],
                f['Edad'],
                f['Peso'],
                f['Doctor'],
                f['sintoma'],
                f['test_resultado'],
                f['Historial']
            ))
    except Exception as e:
         messagebox.showerror("Error", f"Error de sincronización:\n{e}")


def actualizar_registro_gui():
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un paciente de la tabla.")
        return

    item = tree.item(seleccion)
    valores = item['values']
    p_id = str(valores[0])  # El ID del paciente seleccionado

    # 🟢 Opciones reales y humanas según vuestro Firebase del hospital
    menu_opciones = "Opciones disponibles:\n• Edad\n• Peso\n• ID Doctor\n• Síntomas\n• Test\n• Historial"
    campo = simpledialog.askstring("Actualizar Registro", menu_opciones)

    if not campo:
        return
    campo = campo.lower().strip()

    try:
        if campo in ["edad", "age"]:
            n = simpledialog.askstring("Modificar Edad", "Nueva edad del paciente:", initialvalue=valores[1])
            if n: lab.actualizar_datos_clinicos(p_id, {'Edad': int(n)}, {})

        elif campo in ["peso"]:
            n = simpledialog.askstring("Modificar Peso", "Nuevo peso del paciente:", initialvalue=valores[2])
            if n: lab.actualizar_datos_clinicos(p_id, {'Peso': float(n)}, {})

        elif campo in ["id doctor", "doctor", "id_doctor"]:
            n = simpledialog.askstring("Modificar Médico", "Nuevo ID del Doctor asignado:", initialvalue=valores[3])
            if n: lab.actualizar_datos_clinicos(p_id, {'Doctor': int(n)}, {})

        elif campo in ["síntomas", "sintomas", "síntoma", "sintoma"]:
            n = simpledialog.askstring("Modificar Síntomas", "Nueva descripción del síntoma cardíaco:",
                                       initialvalue=valores[4])
            if n: lab.actualizar_datos_clinicos(p_id, {}, {'Descripción': n})  # Va a la subcolección Sintomas

        elif campo in ["test", "resultados", "resultado"]:
            n = simpledialog.askstring("Modificar Test", "Nuevos resultados del test (Ej: ECG):",
                                       initialvalue=valores[5])
            if n: lab.actualizar_datos_clinicos(p_id, {}, {'Results': n})  # Va a la subcolección test

        elif campo in ["historial", "diagnóstico", "diagnostico"]:
            n = simpledialog.askstring("Modificar Historial", "Actualizar historial clínico:", initialvalue=valores[6])
            if n: lab.actualizar_datos_clinicos(p_id, {'Historial': n}, {})
        else:
            messagebox.showwarning("Campo no reconocido", "Por favor, escribe una opción válida de la lista.")
            return

        cargar_tabla_completa()
        messagebox.showinfo("Éxito", f"¡Registro del paciente {p_id} actualizado correctamente!")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar:\n{e}")

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
    global entry_edad, entry_peso, entry_historial, entry_doc_id, entry_sintoma, entry_test, tree, frame_lista
    root = tk.Tk()
    root.title("ClinicData - Sistema Integrado")
    root.geometry("900x600")
    
    frame_header = tk.Frame(root, bg="#2c3e50", height=50)
    frame_header.pack(fill="x", side="top")
    tk.Label(frame_header, text=" CLINICDATA - ARCHIVO DE PACIENTES", font=("Arial", 11, "bold"), fg="white", bg="#2c3e50").pack(side="left", padx=15, pady=10)

    # Añadir menú desplegable
    menu_perfil = tk.Menu(root, tearoff=0)

    def modificar_perfil():
        nuevo_nom = simpledialog.askstring("Perfil", "Editar Nombre Completo:", initialvalue=nombre_doc)
        if nuevo_nom:
            messagebox.showinfo("Perfil Actualizado", f"Nombre cambiado a: {nuevo_nom}")

    menu_perfil.add_command(label="📝 Editar Mi Nombre", command=modificar_perfil)
    menu_perfil.add_separator()
    menu_perfil.add_command(label="🚪 Cerrar Sesión", command=cerrar_sesion_gui)

    def mostrar_menu():
        menu_perfil.post(btn_menu_perfil.winfo_rootx(), btn_menu_perfil.winfo_rooty() + btn_menu_perfil.winfo_height())

    # Este botón sustituye al botón soso de "Cerrar Sesión" que tenías a la derecha
    btn_menu_perfil = tk.Button(frame_header, text="Configuración ⚙️", command=mostrar_menu, bg="#34495e", fg="white",font=("Arial", 9, "bold"))
    btn_menu_perfil.pack(side="right", padx=10, pady=10)

    avatar_canvas = tk.Canvas(frame_header, width=35, height=35, bg="#2c3e50", highlightthickness=0)
    avatar_canvas.pack(side="right", padx=15, pady=5)
    avatar_canvas.create_oval(2, 2, 33, 33, fill="#3498db", outline="")

    nombre_doc = usuario_actual.email.split('@')[0]
    avatar_canvas.create_text(18, 18, text=nombre_doc[:4].upper(), fill="white", font=("Arial", 8, "bold"))
    tk.Label(frame_header, text=f"Doctor/a: {nombre_doc}", font=("Arial", 9), fg="white", bg="#2c3e50").pack(side="right", padx=5)

    frame_form = tk.LabelFrame(root, text=" Formulario Clínico (Guardado en documento 'Pacientes') ", padx=10, pady=10)
    frame_form.pack(padx=15, pady=10, fill="x")

    tk.Label(frame_form, text="Edad:").grid(row=0, column=0, sticky="w", pady=5)
    entry_edad = tk.Entry(frame_form, width=15)
    entry_edad.grid(row=0, column=1, pady=5, padx=5, sticky="w")

    tk.Label(frame_form, text="Peso:").grid(row=0, column=2, sticky="w", pady=5, padx=15)
    entry_peso = tk.Entry(frame_form, width=15)
    entry_peso.grid(row=0, column=3, pady=5, padx=5, sticky="w")

    tk.Label(frame_form, text="ID Doctor:").grid(row=0, column=4, sticky="w", pady=5, padx=15)
    entry_doc_id = tk.Entry(frame_form, width=20)
    entry_doc_id.grid(row=0, column=5, pady=5, padx=5, sticky="w")

    # Inserta el ID numérico del doctor
    id_medico = usuario_actual.id_doctor_num if hasattr(usuario_actual, 'id_doctor_num') else "2005"
    entry_doc_id.insert(0, id_medico)
    entry_doc_id.config(state="disabled")

    tk.Label(frame_form, text="Síntoma Detectado:").grid(row=1, column=0, sticky="w", pady=5)
    entry_sintoma = tk.Entry(frame_form, width=15)
    entry_sintoma.grid(row=1, column=1, pady=5, padx=5, sticky="w")

    tk.Label(frame_form, text="Resultados Test:").grid(row=1, column=2, sticky="w",
                                                                                      pady=5, padx=15)
    entry_test = tk.Entry(frame_form, width=52)
    entry_test.grid(row=1, column=3, columnspan=3, pady=5, padx=5, sticky="w")

    tk.Label(frame_form, text="Historial General:").grid(row=2, column=0, sticky="w", pady=5)
    entry_historial = tk.Entry(frame_form, width=85)
    entry_historial.grid(row=2, column=1, columnspan=5, pady=5, padx=5, sticky="w")

    tk.Button(frame_form, text="Guardar Registro Clínico", command=agregar_desde_gui, bg="#3498db", fg="white",font=("Arial", 10, "bold")).grid(row=3, column=0, columnspan=6, pady=15, padx=10, sticky="ew")

    frame_lista = tk.LabelFrame(root, text=" Campos del documento 'Pacientes' en Tiempo Real ", padx=10, pady=10)
    frame_lista.pack(padx=15, pady=5, fill="both", expand=True)

    # Contenedor para el filtro
    frame_filtro = tk.Frame(frame_lista)
    frame_filtro.pack(fill="x", pady=5)

    tk.Label(frame_filtro, text="Filtrar por asignación:").pack(side="left", padx=5)

    global combo_filtro
    combo_filtro = ttk.Combobox(frame_filtro, values=["Todos", "Mis Pacientes"], state="readonly", width=15)
    combo_filtro.set("Todos")  # Por defecto que muestre todos
    combo_filtro.pack(side="left", padx=5)

    # Hacer que cuando cambie la opción, se refresque la tabla sola
    combo_filtro.bind("<<ComboboxSelected>>", lambda e: cargar_tabla_completa())

    columnas = ("ID", "Edad", "Peso", "Doctor", "Sintoma", "Test", "Historial")
    tree = ttk.Treeview(frame_lista, columns=columnas, show="headings", selectmode="browse")
    tree.heading("ID", text="ID Paciente")
    tree.heading("Edad", text="Edad")
    tree.heading("Peso", text="Peso")
    tree.heading("Doctor", text="ID Doctor")
    tree.heading("Sintoma", text="Síntomas Activos")
    tree.heading("Test", text="Resultados del Test")
    tree.heading("Historial", text="Historial Clínico")

    tree.column("ID", width=80, anchor="center")
    tree.column("Edad", width=70, anchor="center")
    tree.column("Peso", width=70, anchor="center")
    tree.column("Doctor", width=100, anchor="center")
    tree.column("Sintoma", width=140, anchor="center")
    tree.column("Test", width=200, anchor="center")
    tree.column("Historial", width=250, anchor='center')
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
