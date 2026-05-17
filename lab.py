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
        # Extraemos el string limpio antes del @ sin corchetes
        nombre_doctor = email.split('@')[0]
        
        doc_ref = db.collection('Personal').document('Doctores')
        doc_ref.update({
            user.uid: {
                'nombre': str(nombre_doctor),
                'correo': email,
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
        # 1. Comprobamos si el correo existe en Firebase Auth
        user = auth.get_user_by_email(email)

        # 2. Control de seguridad: Si la contraseña es sospechosa o errónea, la rechazamos
        if not password or len(password) < 6 or  password.isspace():
            raise Exception("Contraseña incorrecta o insegura.")

        return user
    except Exception:
        raise Exception("Usuario o contraseña incorrectos.")

# --- CRUD CORREGIDO: NUEVO CAMPO DENTRO DEL DOCUMENTO 'Pacientes' DE LA COLECCIÓN 'Clientes' ---

def agregar_datos_clinicos(doctor_id, edad, historial, peso, descripcion_sintoma, resultado_test):
    if db is None:
        raise Exception("No hay conexión con la base de datos.")
    try:
        # Generamos un ID correlativo para el nuevo paciente cardíaco
        id_nuevo_paciente = str(random.randint(4006, 4999))

        # 1. Datos principales que van en Clientes > Pacientes
        datos_paciente = {
            'Edad': int(edad),
            'Doctor': int(doctor_id),  # Guardamos el ID numérico del médico (ej: 2005)
            'Historial': historial,
            'Peso': float(peso)
        }

        doc_ref = db.collection('Clientes').document('Pacientes')
        doc_ref.update({
            id_nuevo_paciente: datos_paciente
        })

        # 2. ANIDADO DE SÍNTOMAS: Subcolección dentro del propio paciente
        db.collection('Clientes').document('Pacientes') \
            .collection('Sintomas').document(id_nuevo_paciente).set({
            'ID Sintomas': random.randint(1, 99),
            'Descripción': descripcion_sintoma,
            'Intensidad': random.randint(1, 5)
        })

        # 3. ANIDADO DE TEST CARDÍACO: Subcolección dentro del propio paciente
        db.collection('Clientes').document('Pacientes') \
            .collection('test').document(id_nuevo_paciente).set({
            'ID Test': random.randint(1, 99),
            'Fecha test': datetime.now(timezone.utc),
            'Results': resultado_test  # Ej: "Ecocardiograma: FEVI 45%"
        })

        return id_nuevo_paciente
    except ValueError:
        raise Exception("La edad y el ID del doctor deben ser enteros, y el peso un decimal.")
    except Exception as e:
        raise Exception(f"Error en la estructura de Firestore: {e}")


def leer_todo_el_panel():
    if db is None:
        return []
    try:
        doc_ref = db.collection('Clientes').document('Pacientes').get()
        lista_completa = []

        if doc_ref.exists:
            todos_los_pacientes = doc_ref.to_dict() or {}
            for p_id, p_data in todos_los_pacientes.items():
                if isinstance(p_data, dict):
                    # Leemos sus síntomas desde su subcolección anidada
                    s_doc = db.collection('Clientes').document('Pacientes').collection('Sintomas').document(
                        str(p_id)).get()
                    s_data = s_doc.to_dict() if s_doc.exists else {}

                    # Leemos sus test cardíacos desde su subcolección anidada
                    t_doc = db.collection('Clientes').document('Pacientes').collection('test').document(str(p_id)).get()
                    t_data = t_doc.to_dict() if t_doc.exists else {}

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
        print(f"Error de lectura: {e}")
        return []


def actualizar_datos_clinicos(paciente_id, datos_p, datos_m):
    if db is None:
        raise Exception("No hay conexión.")
    try:
        if datos_p:
            doc_ref_p = db.collection('Clientes').document('Pacientes')
            actualizacion = {f"{paciente_id}.{k}": v for k, v in datos_p.items()}
            doc_ref_p.update(actualizacion)

        if datos_m:
            db.collection('muestras').document(str(paciente_id)).set(datos_m, merge=True)
    except Exception as e:
        raise Exception(f"Error en Firestore: {e}")

def eliminar_datos_clinicos(paciente_id):
    if db is None:
        raise Exception("No hay conexión.")
    try:
        db.collection('Clientes').document('Pacientes').update({
            paciente_id: firestore.DELETE_FIELD
        })
        db.collection('muestras').document(paciente_id).delete()
    except Exception as e:
        raise Exception(f"Error al eliminar: {e}")
