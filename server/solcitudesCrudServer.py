
from server import conexionbd


# Función para actualizar una solicitud
def actualizar_solicitud(usuario, solicitud_id, nuevos_datos):
    db = conexionbd.conectar_a_couchdb()
    colaboradores_doc = db.get("colaboradores")
    nombreColaborador = None

    if colaboradores_doc:
        colaboradores_lista = colaboradores_doc.get("colaboradores", [])

        for colaborador in colaboradores_lista:
            if usuario == colaborador.get("correo_electronico"):
                nombreColaborador = colaborador.get("nombre", None)
                break
    solicitudes = db.get("solicitudes")  # Obtén el documento de solicitudes

    if solicitudes:
        solicitudes_registradas = solicitudes.get('solicitudes', [])

        for solicitud in solicitudes_registradas:
            if solicitud.get('identificador') == solicitud_id and solicitud.get('nombre_completo_colaborador') == nombreColaborador:
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
    colaboradores_doc = db.get("colaboradores")
    nombreColaborador = None

    if colaboradores_doc:
        colaboradores_lista = colaboradores_doc.get("colaboradores", [])

        for colaborador in colaboradores_lista:
            if usuario == colaborador.get("correo_electronico"):
                nombreColaborador = colaborador.get("nombre", None)
                break
    solicitudes = db.get("solicitudes")  # Obtén el documento de solicitudes

    if solicitudes:
        solicitudes_registradas = solicitudes.get('solicitudes', [])

        for solicitud in solicitudes_registradas:
            if solicitud.get('identificador') == solicitud_id and solicitud.get('nombre_completo_colaborador') == nombreColaborador:
                # Elimina la solicitud de la lista
                solicitudes_registradas.remove(solicitud)
                
                # Actualiza el documento de solicitudes
                db['solicitudes'] = solicitudes
                return True

    return False  # No se encontró la solicitud o no tiene permiso para eliminarla
