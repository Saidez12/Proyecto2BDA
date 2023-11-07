
from server import conexionbd

def agregar_solicitud(datos):
    db = conexionbd.conectar_a_couchdb()

    solicitudes = db.get("solicitudes")
    solicitudes_registradas = []

    if solicitudes:
        solicitudes_registradas = solicitudes.get('solicitudes', [])

    nuevo_id = len(solicitudes_registradas) + 1

    nueva_solicitud = {
        "identificador": nuevo_id,
        **datos
    }

    solicitudes_registradas.append(nueva_solicitud)
    solicitudes["solicitudes"] = solicitudes_registradas

    db.save(solicitudes)
    return True


# Función para actualizar una solicitud
def actualizar_solicitud(usuario, solicitud_id, nuevos_datos):
    db = conexionbd.conectar_a_couchdb()

    solicitudes = db.get("solicitudes")  # Obtén el documento de solicitudes

    if solicitudes:
        solicitudes_registradas = solicitudes.get('solicitudes', [])

        for solicitud in solicitudes_registradas:
            if solicitud.get('identificador') == solicitud_id and solicitud.get('correo') == usuario:
                # Actualiza los datos de la solicitud con los nuevos datos
                for key, value in nuevos_datos.items():
                    solicitud[key] = value

                # Actualiza la solicitud en la lista
                db['solicitudes'] = solicitudes
                return True

    return False  # No se encontró la solicitud o no tiene permiso para actualizarla

# Función para eliminar una solicitud por ID
def eliminar_solicitud(usuario, solicitud_id):
    db = conexionbd.conectar_a_couchdb()
    solicitudes = db.get("solicitudes")  # Obtén el documento de solicitudes

    if solicitudes:
        solicitudes_registradas = solicitudes.get('solicitudes', [])

        for solicitud in solicitudes_registradas:
            if solicitud.get('identificador') == solicitud_id and solicitud.get('correo') == usuario:
                # Elimina la solicitud de la lista
                solicitudes_registradas.remove(solicitud)
                
                # Actualiza el documento de solicitudes
                db['solicitudes'] = solicitudes
                return True

    return False  # No se encontró la solicitud o no tiene permiso para eliminarla

def mostrar_solicitudes_Pendientes():
    db = conexionbd.conectar_a_couchdb()

    db_solicitudes = db.get("solicitudes")

    if db_solicitudes:
        solicitudes_registradas = db_solicitudes.get("solicitudes", [])
        listaSolicitudes = []

        for solicitud in solicitudes_registradas:
            estado = solicitud.get("estado")
            if estado and estado.lower() == "pendiente":
                listaSolicitudes.append(solicitud)
            
        return listaSolicitudes
    else:
        return []

    
def cambiar_estadoSolicitud(id_solicitud):
    db = conexionbd.conectar_a_couchdb()
    solicitudes = db.get("solicitudes")  # Obtén el documento de solicitudes

    if solicitudes:
        solicitudes_registradas = solicitudes.get('solicitudes', [])

        for solicitud in solicitudes_registradas:
            if solicitud.get('identificador') == id_solicitud:
                # Actualiza el estado de la solicitud a "aceptada"
                solicitud['estado'] = "aprobada"

                # Actualiza la solicitud en la lista
                db['solicitudes'] = solicitudes
                return True

    return False  # No se encontró la solicitud o no tiene permiso para actualizarla

def rechazar_estadoSolicitud(id_solicitud):
    db = conexionbd.conectar_a_couchdb()
    solicitudes = db.get("solicitudes")  # Obtén el documento de solicitudes

    if solicitudes:
        solicitudes_registradas = solicitudes.get('solicitudes', [])

        for solicitud in solicitudes_registradas:
            if solicitud.get('identificador') == id_solicitud:
                # Actualiza el estado de la solicitud a "aceptada"
                solicitud['estado'] = "rechazada"

                # Actualiza la solicitud en la lista
                db['solicitudes'] = solicitudes
                return True

    return False  # No se encontró la solicitud o no tiene permiso para actualizarla

