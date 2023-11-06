import streamlit as st
from server import conexionbd,solicitudesCrudServer


def agregar_solicitudUI(usuario):
    st.title("Agregar Nueva Solicitud")

    nuevo_datos = {}

    nuevo_datos['nombre_completo_colaborador'] = st.text_input("Nombre Completo del Colaborador", key="nombre_completo")
    nuevo_datos['correo'] = usuario
    nuevo_datos['departamento'] = st.text_input("Departamento", key="departamento")
    nuevo_datos['internacional'] = st.checkbox("Internacional")
    nuevo_datos['pais_destino'] = st.text_input("País de Destino" if nuevo_datos['internacional'] else "Ciudad Local", key="destino")
    nuevo_datos['motivo'] = st.text_input("Motivo", key="motivo")
    fecha_inicio = st.date_input("Fecha de Inicio")
    fecha_finalizacion = st.date_input("Fecha de Finalización")

    st.subheader("Vuelos")
    nuevo_datos['vuelos'] = []

    vuelo_index = 1  # Contador para generar claves únicas

    while True:
        aerolinea = st.text_input(f"Aerolínea {vuelo_index}", key=f"aerolinea_{vuelo_index}")
        precio_boletos = st.number_input(f"Precio de Boletos en dólares {vuelo_index}", key=f"precio_{vuelo_index}")

        # Validaciones de vuelos
        if precio_boletos <= 0:
            st.warning("El precio de los boletos debe ser un valor positivo.")
            precio_boletos = 0  # Establecer el precio a 0 si es negativo
        nuevo_datos['vuelos'].append({"aerolinea": aerolinea, "precio_boletos": precio_boletos})

        add_another = st.checkbox(f"Agregar otro vuelo ({vuelo_index})", key=f"add_another_{vuelo_index}")  # Agregar un número único a la etiqueta del checkbox

        if not add_another:
            break

        vuelo_index += 1

    nuevo_datos['alojamiento'] = st.text_input("Alojamiento", key="alojamiento")
    nuevo_datos['requiere_transporte'] = st.checkbox("Requiere Transporte")

    agregar_button = st.button("Agregar Solicitud", key="agregar_button")

    if agregar_button:
        if (
            nuevo_datos['nombre_completo_colaborador']
            and nuevo_datos['departamento']
            and nuevo_datos['motivo']
            and nuevo_datos['pais_destino']
            and nuevo_datos['alojamiento']
            and nuevo_datos['vuelos'][0]['aerolinea']  # Verifica al menos un vuelo
            and nuevo_datos['vuelos'][0]['precio_boletos'] > 0  # Validación para precio de boletos positivo
        ):
            # Validación de fechas
            if fecha_inicio < fecha_finalizacion:
                # Convierte las fechas de tipo date a cadenas de texto
                nuevo_datos['fecha_inicio'] = fecha_inicio.strftime("%Y-%m-%d")
                nuevo_datos['fecha_finalizacion'] = fecha_finalizacion.strftime("%Y-%m-%d")
                nuevo_datos['estado'] = "pendiente"  # Estado en minúsculas
                
                if solicitudesCrudServer.agregar_solicitud(nuevo_datos):
                    st.success("Solicitud agregada con éxito.")
                else:
                    st.error("No se pudo agregar la solicitud.")
            else:
                st.warning("La 'Fecha de Inicio' debe ser anterior a la 'Fecha de Finalización'.")
        else:
            st.warning("Por favor, completa todos los campos obligatorios y asegúrate de que los datos sean válidos.")









# Función para mostrar las solicitudes
def mostrar_solicitudes(usuario):
    solicitudes = conexionbd.solicitudes_colaborador(usuario)
    st.title("Solicitudes Registradas")
    consultar_button = st.button("Consultar")

    if consultar_button:
        for solicitud in solicitudes:
            st.subheader(f"Solicitud de {solicitud['nombre_completo_colaborador']}")
            st.write(f"Departamento: {solicitud['departamento']}")
            st.write(f"Destino: {solicitud['pais_destino']}")
            st.write(f"Motivo: {solicitud['motivo']}")
            st.write(f"Fecha de inicio: {solicitud['fecha_inicio']}")
            st.write(f"Fecha de finalización: {solicitud['fecha_finalizacion']}")
            st.write(f"Alojamiento: {solicitud['alojamiento']}")
            st.write(f"Estado: {solicitud['estado']}")
            st.write("---")

# Función para editar una solicitud
def editar_solicitud(usuario):
    solicitudes = conexionbd.solicitudes_colaborador(usuario)
    listaId = [solicitud['identificador'] for solicitud in solicitudes]

    # Agregar un widget selectbox para que el usuario seleccione un ID
    idSeleccionado = st.selectbox("Selecciona un ID de Solicitud", listaId)

    # Buscar la solicitud seleccionada por ID
    solicitud_seleccionada = None
    for solicitud in solicitudes:
        if solicitud['identificador'] == idSeleccionado:
            solicitud_seleccionada = solicitud

    if solicitud_seleccionada:
        st.subheader(f"Editando Solicitud - {solicitud_seleccionada['identificador']}")
        nuevos_datos = {}

        nuevos_datos['motivo'] = st.text_input("Nuevo Motivo", solicitud_seleccionada['motivo'])
        nuevos_datos['departamento'] = st.text_input("Nuevo Departamento", solicitud_seleccionada['departamento'])
        nuevos_datos['pais_destino'] = st.text_input("Nuevo País de destino", solicitud_seleccionada['pais_destino'])
        nuevos_datos['fecha_inicio'] = st.text_input("Nueva Fecha de Inicio", solicitud_seleccionada['fecha_inicio'])
        nuevos_datos['fecha_finalizacion'] = st.text_input("Nueva Fecha de Finalización", solicitud_seleccionada['fecha_finalizacion'])
        nuevos_datos['alojamiento'] = st.text_input("Nuevo Alojamiento", solicitud_seleccionada['alojamiento'])
        nuevos_datos['internacional'] = st.checkbox("Internacional", solicitud_seleccionada['internacional'])
        # Opciones para editar los vuelos
        nuevos_vuelos = []
        for vuelo in solicitud_seleccionada['vuelos']:
            aerolinea = st.text_input("Aerolínea", vuelo['aerolinea'])
            precio_boletos = st.number_input("Precio de Boletos", value=vuelo['precio_boletos'])
            nuevos_vuelos.append({"aerolinea": aerolinea, "precio_boletos": precio_boletos})
        nuevos_datos['vuelos'] = nuevos_vuelos

        actualizar_button = st.button("Actualizar")

        if actualizar_button:
            if solicitudesCrudServer.actualizar_solicitud(usuario, idSeleccionado, nuevos_datos):
                st.success("Solicitud actualizada con éxito.")
            else:
                st.error("No se pudo actualizar la solicitud.")
    else:
        st.warning("Selecciona un ID válido de solicitud")

# Función para eliminar una solicitud
def eliminarSolicitud(usuario):
    solicitudes = conexionbd.solicitudes_colaborador(usuario)
    listaId = [solicitud['identificador'] for solicitud in solicitudes]

    # Agregar un widget selectbox para que el usuario seleccione un ID
    idSeleccionado = st.selectbox("Selecciona un ID de Solicitud", listaId)
    eliminar_button = st.button("Eliminar")

    # Buscar la solicitud seleccionada por ID
    solicitud_seleccionada = None
    for solicitud in solicitudes:
        if solicitud['identificador'] == idSeleccionado:
            solicitud_seleccionada = solicitud

    if solicitud_seleccionada:
        if eliminar_button:
            if solicitudesCrudServer.eliminar_solicitud(usuario, idSeleccionado):
                st.success("Solicitud eliminada con éxito.")
            else:
                st.error("No se pudo eliminar la solicitud.")
    else:
        st.warning("Selecciona un ID válido de solicitud")