import firebase_admin
from firebase_admin import credentials, firestore

# 1. Configuración de la llave y conexión
# Asegúrate de que la ruta coincida con tu carpeta y archivo
cred = credentials.Certificate("credentials/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


# 2. Funciones para manejar los datos
def crear_muestra(datos):
    doc_ref = db.collection('muestras').add(datos)
    print(f"✔️ Muestra creada con éxito.")


def leer_muestras():
    docs = db.collection('muestras').stream()
    print("\n--- Listado de Muestras ---")
    for doc in docs:
        print(f"ID: {doc.id} => {doc.to_dict()}")


def actualizar_muestra(doc_id, nuevos_datos):
    db.collection('muestras').document(doc_id).update(nuevos_datos)
    print(f"✔️ Muestra {doc_id} actualizada.")


def eliminar_muestra(doc_id):
    db.collection('muestras').document(doc_id).delete()
    print(f" Muestra {doc_id} eliminada.")


# 3. El Menú (Aquí es donde completamos el reto)
def menu():
    while True:
        print("\n--- GESTIÓN DE LABORATORIO FIREBASE ---")
        print("1. Insertar muestra")
        print("2. Ver todas las muestras")
        print("3. Actualizar estado de muestra")
        print("4. Eliminar muestra")
        print("5. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            tipo = input("Tipo de muestra: ")
            estado = "pendiente"
            crear_muestra({'tipo': tipo, 'estado': estado})

        elif opcion == "2":
            leer_muestras()

        elif opcion == "3":
            leer_muestras()  # Para que veas los IDs
            doc_id = input("\nCopia y pega el ID de la muestra: ").strip()
            # RETO COMPLETADO: Pedimos el estado al usuario
            nuevo_estado = input("Ingrese el nuevo estado (ej: procesada, rechazada): ")
            actualizar_muestra(doc_id, {'estado': nuevo_estado})

        elif opcion == "4":
            leer_muestras()
            doc_id = input("\nID de la muestra a eliminar: ")
            eliminar_muestra(doc_id)

        elif opcion == "5":
            break


if __name__ == "__main__":
    menu()
