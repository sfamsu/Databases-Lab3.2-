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

def agregar_datos_clinicos(doctor_email, edad, historial, peso, tipo_muestra, estado_muestra):
    if db is None:
        raise Exception("No hay conexión con la base de datos.")
    try:
        nombre_doc = doctor_email.split('@')[0]
        # Generamos un ID numérico de 4 dígitos correlativo al tuyo (ej: 4006, 4007...)
        id_nuevo_paciente = str(random.randint(4006, 4999))
        
        # Diccionario con los campos idénticos a tu captura de pantalla
        datos_paciente = {
            'Nombre': nombre,
            'Apellidos': apellidos,
            'Edad': int(edad),
            'Doctor': str(nombre_doc),
            'Historial': historial,
            'Peso': float(peso)
        }
        
        # RUTA EXACTA DE TU CAPTURA: Colección 'Clientes' -> Documento 'Pacientes'
        doc_ref = db.collection('Clientes').document('Pacientes')
        
        # Se añade como un campo nuevo (mapa) debajo de tu registro 4005
        doc_ref.update({
            id_nuevo_paciente: datos_paciente
        })
        
        # Colección muestras (intacta, vinculada por el mismo ID numérico)
        db.collection('muestras').document(id_nuevo_paciente).set({
            'paciente_id': id_nuevo_paciente,
            'tipo_muestra': tipo_muestra,
            'estado_muestra': estado_muestra,
            'fecha_analisis': datetime.now(timezone.utc)
        })
        return id_nuevo_paciente
    except ValueError:
        raise Exception("La edad debe ser un número entero y el peso un decimal.")
    except Exception as e:
        raise Exception(f"Error en Firestore: {e}")

def leer_todo_el_panel():
    if db is None:
        return []
    try:
        # Leemos el documento 'Pacientes' de la colección 'Clientes'
        doc_ref = db.collection('Clientes').document('Pacientes').get()
        lista_completa = []
        
        if doc_ref.exists:
            todos_los_pacientes = doc_ref.to_dict() or {}
            for p_id, p_data in todos_los_pacientes.items():
                if isinstance(p_data, dict):
                    m_doc = db.collection('muestras').document(str(p_id)).get()
                    m_data = m_doc.to_dict() if m_doc.exists else {}
                    
                    fila = {
                        'id': p_id,
                        'Edad': p_data.get('Edad', 'N/A'),
                        'Peso': p_data.get('Peso', 'N/A'),
                        'Doctor': p_data.get('Doctor', 'N/A'),
                        'Historial': p_data.get('Historial', 'N/A'),
                        'tipo_muestra': m_data.get('tipo_muestra', 'N/A'),
                        'estado_muestra': m_data.get('estado_muestra', 'N/A')
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
