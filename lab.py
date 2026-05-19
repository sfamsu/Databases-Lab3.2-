import hashlib # Para poder tener seguridad en la contraseña
import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import datetime, timezone
import random

try:
    cred = credentials.Certificate('credentials/serviceAccountKey.json')
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    print(" Conexión a Firestore y Auth establecida correctamente.")
except Exception as e:
    db = None
    print(f" Error al conectar a Firebase: {e}")

# --- AUTENTICACIÓN: DOCTORES DENTRO DEL DOCUMENTO 'DOCTORES' ---

def registrar_usuario_email(email, password):
    if db is None:
        raise Exception("No hay conexión con el servidor.")
    try:
        user = auth.create_user(email=email, password=password)
        nombre_doctor = email.split('@')[0]

        # Generamos un ID numérico único para este doctor
        id_doctor_numerico = random.randint(2000, 2999)

        # Encriptamos la contraseña antes de guardarla para que nadie pueda verla en la base de datos
        password_encriptada = hashlib.sha256(password.encode()).hexdigest()

        doc_ref = db.collection('Personal').document('Doctores')
        doc_ref.update({
            user.uid: {
                'id_doctor': id_doctor_numerico,
                'nombre': str(nombre_doctor),
                'correo': email,
                'password_hash': password_encriptada,
                'fecha_alta': datetime.now(timezone.utc)
            }
        })
        return user
    except Exception as e:
        raise Exception(f"No se pudo registrar: {e}")


def iniciar_sesion_simulado(email, password):
    if db is None:
        raise Exception("No hay conexión con el servidor.")
    try:
        # Verificamos primero si el correo existe en Firebase Auth
        user = auth.get_user_by_email(email)

        # Buscamos los datos de este doctor en Firestore
        doc_ref = db.collection('Personal').document('Doctores').get()
        if not doc_ref.exists:
            raise Exception("Error interno: No se encuentra el registro de doctores.")

        datos_doctores = doc_ref.to_dict() or {}
        datos_mi_perfil = datos_doctores.get(user.uid, {})

        # Encriptamos la contraseña introducida para compararla
        hash_introducido = hashlib.sha256(password.encode()).hexdigest()
        hash_guardado = datos_mi_perfil.get('password_hash', '')

        # Comprobamos si las contraseñas coinciden de verdad
        if hash_introducido != hash_guardado:
            raise Exception("Contraseña incorrecta.")

        # Rescatamos su ID de doctor como hacíamos ayer
        user.id_doctor_num = datos_mi_perfil.get('id_doctor', '9999')

        return user
    except Exception as e:
        # Ponemos un mensaje genérico para no dar pistas a los hackers
        raise Exception("Usuario o contraseña incorrectos.")

# --- CRUD CORREGIDO: NUEVO CAMPO DENTRO DEL DOCUMENTO 'Pacientes' DE LA COLECCIÓN 'Clientes' ---

def agregar_datos_clinicos(doctor_id, edad, historial, peso, descripcion_sintoma, resultado_test):
    if db is None:
        raise Exception("No hay conexión con la base de datos.")
    try:
        # Generamos un ID aleatorio para el paciente (ej: "4015")
        id_nuevo_paciente = str(random.randint(4000, 4999))

        # Referencias a las rutas exactas en tu Firebase
        ref_datos = db.collection('Clientes').document('Pacientes').collection('Seguimiento paciente').document('Datos_Generales')
        ref_sintomas = db.collection('Clientes').document('Pacientes').collection('Seguimiento paciente').document('Sintomas')
        ref_test = db.collection('Clientes').document('Pacientes').collection('Seguimiento paciente').document('test')

        # Preparar los bloques de datos con el ID del nuevo paciente como clave
        nuevos_datos = {
            id_nuevo_paciente: {
                'Edad': int(edad),
                'Doctor': str(doctor_id),
                'Historial': historial,
                'Peso': float(peso)
            }
        }

        nuevos_sintomas = {
            id_nuevo_paciente: {
                'ID_Sintomas': random.randint(1, 99),
                'Descripción': descripcion_sintoma,
                'Intensidad': random.randint(1, 5)
            }
        }

        nuevos_test = {
            id_nuevo_paciente: {
                'ID_Test': random.randint(1, 99),
                'Fecha_test': datetime.now(timezone.utc),
                'Results': resultado_test
            }
        }

        # Usamos .set con merge=True para crear o actualizar automáticamente sin romper nada
        ref_datos.set(nuevos_datos, merge=True)
        ref_sintomas.set(nuevos_sintomas, merge=True)
        ref_test.set(nuevos_test, merge=True)

        return id_nuevo_paciente
    except ValueError:
        raise Exception("La edad debe ser un entero y el peso un decimal.")
    except Exception as e:
        raise Exception(f"Error al guardar en la estructura de Firestore: {e}")


def leer_todo_el_panel():
    if db is None:
        return []
    try:
        lista_completa = []

        # 1. Leemos el documento de Datos Generales
        dg_doc = db.collection('Clientes').document('Pacientes').collection('Seguimiento paciente').document('Datos_Generales').get()

        if dg_doc.exists:
            todos_los_datos = dg_doc.to_dict() or {}

            # Leemos también los documentos de síntomas y tests para cruzarlos
            sintomas_doc = db.collection('Clientes').document('Pacientes').collection('Seguimiento paciente').document('Sintomas').get()
            sintomas_todos = sintomas_doc.to_dict() if sintomas_doc.exists else {}

            test_doc = db.collection('Clientes').document('Pacientes').collection('Seguimiento paciente').document('test').get()
            test_todos = test_doc.to_dict() if test_doc.exists else {}

            # 2. Reconstruimos la ficha de cada paciente usando su ID
            for p_id, p_data in todos_los_datos.items():
                if isinstance(p_data, dict):
                    s_data = sintomas_todos.get(p_id, {})
                    t_data = test_todos.get(p_id, {})

                    fila = {
                        'id': p_id,
                        'Edad': p_data.get('Edad', 'N/A'),
                        'Peso': p_data.get('Peso', 'N/A'),
                        'Doctor': p_data.get('Doctor', 'N/A'),
                        'Historial': p_data.get('Historial', 'N/A'),
                        'sintoma': s_data.get('Descripción', 'Ninguno'),
                        'test_resultado': t_data.get('Results', 'Sin registrar')
                    }
                    lista_completa.append(fila)
        return lista_completa
    except Exception as e:
        print(f"Error al leer el panel: {e}")
        return []


def actualizar_datos_clinicos(paciente_id, datos_p, datos_m, campo_modificado=None):
    if db is None:
        raise Exception("No hay conexión.")
    try:
        paciente_id_str = str(paciente_id)
        base_ref = db.collection('Clientes').document('Pacientes').collection('Seguimiento paciente')

        # 1. Si nos piden actualizar Datos Generales (Edad, Peso, Historial)
        if datos_p:
            ref_datos = base_ref.document('Datos_Generales')
            # Preparamos la estructura: { '4005': { 'Edad': 30, 'Peso': 70.5... } }
            actualizacion = {paciente_id_str: datos_p}
            ref_datos.set(actualizacion, merge=True)

        # 2. Si nos piden actualizar Síntomas o Tests
        if datos_m:
            if campo_modificado == "sintoma":
                ref_sintomas = base_ref.document('Sintomas')
                actualizacion = {paciente_id_str: datos_m}
                ref_sintomas.set(actualizacion, merge=True)

            elif campo_modificado == "test":
                ref_test = base_ref.document('test')
                actualizacion = {paciente_id_str: datos_m}
                ref_test.set(actualizacion, merge=True)

    except Exception as e:
        raise Exception(f"Error en Firestore al actualizar: {e}")

def eliminar_datos_clinicos(paciente_id):
    if db is None:
        raise Exception("No hay conexión.")
    try:
        paciente_id_str = str(paciente_id)
        base_ref = db.collection('Clientes').document('Pacientes').collection('Seguimiento paciente')

        # Usamos la instrucción especial de Firebase para borrar un campo específico dentro de un mapa
        borrado_campo = {paciente_id_str: firestore.DELETE_FIELD}

        # Borramos el rastro del paciente en los tres documentos
        base_ref.document('Datos_Generales').update(borrado_campo)
        base_ref.document('Sintomas').update(borrado_campo)
        base_ref.document('test').update(borrado_campo)

    except Exception as e:
        raise Exception(f"Error en Firestore al eliminar: {e}")
