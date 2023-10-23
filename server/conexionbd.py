import couchdb

# Configurar la conexión a CouchDB
def conectar_a_couchdb():
    server = couchdb.Server('http://admin:admin@localhost:5984/')
    return server['viajes_corporativos']

# Función para registrar un colaborador
def registrar_colaborador(correo, contrasena):
    db = conectar_a_couchdb()
    colaborador_data = {
        "correo_electronico": correo,
        "clave": contrasena,
        "solicitudes": []
    }

    try:
        colaboradores_doc = db.get("colaboradores")  # Obtiene el documento de colaboradores

        if colaboradores_doc is None:
            # Si no existe el documento, crea uno nuevo
            colaboradores_doc = {"colaboradores": [colaborador_data]}
            db['colaboradores'] = colaboradores_doc
            return True
        else:
            # Si el documento ya existe, agrega el nuevo colaborador si no existe
            colaboradores = colaboradores_doc.get("colaboradores", [])
            if correo not in [colaborador['correo_electronico'] for colaborador in colaboradores]:
                colaboradores.append(colaborador_data)
                colaboradores_doc['colaboradores'] = colaboradores
                db['colaboradores'] = colaboradores_doc  # Actualiza el documento de colaboradores
                return True
            else:
                return False  # El colaborador ya existe
    except couchdb.ResourceConflict:
        # Maneja el conflicto de revisión aquí, puedes implementar la lógica necesaria
        # para resolver el conflicto si es necesario
        return False  # Error de conflicto de revisión

# Función para registrar un administrador
def registrar_admin(usuario, contrasena):
    db = conectar_a_couchdb()
    admin_data = {
        "usuario": usuario,
        "clave": contrasena
    }

    try:
        admin_doc = db.get("administradores")  # Obtiene el documento de administradores

        if admin_doc is None:
            # Si no existe el documento, crea uno nuevo
            admin_doc = {"administradores": [admin_data]}
            db['administradores'] = admin_doc
            return True
        else:
            # Si el documento ya existe, agrega el nuevo administrador si no existe
            admins = admin_doc.get("administradores", [])
            if usuario not in [admin['usuario'] for admin in admins]:
                admins.append(admin_data)
                admin_doc['administradores'] = admins
                db['administradores'] = admin_doc  # Actualiza el documento de administradores
                return True
            else:
                return False  # El administrador ya existe
    except couchdb.ResourceConflict:
        # Maneja el conflicto de revisión aquí, puedes implementar la lógica necesaria
        # para resolver el conflicto si es necesario
        return False  # Error de conflicto de revisión

# Función para autenticar colaboradores
def autenticar_colaborador(correo, contrasena):
    db = conectar_a_couchdb()
    colaboradores = db['colaboradores']['colaboradores']
    
    for colaborador in colaboradores:
        if colaborador.get('correo_electronico') == correo and colaborador.get('clave') == contrasena:
            return True
    return False  # Las credenciales no coinciden

# Función para autenticar administradores
def autenticar_admin(usuario, contrasena):
    db = conectar_a_couchdb()['administradores']
    for admin in db:
        if admin['usuario'] == usuario and admin['clave'] == contrasena:
            return True
    return False  # Las credenciales no coinciden
