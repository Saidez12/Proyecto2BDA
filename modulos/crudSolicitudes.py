import streamlit as st
from server import conexionbd,solicitudesCrudServer
import datetime

def agregar_solicitudUI(usuario):
    st.title("Agregar Nueva Solicitud")

    nuevo_datos = {}

    nuevo_datos['nombre_completo_colaborador'] = st.text_input("Nombre Completo del Colaborador")
    nuevo_datos['departamento'] = st.text_input("Departamento")
    nuevo_datos['internacional'] = st.checkbox("Internacional")

    if nuevo_datos['internacional']:
        nuevo_datos['pais_destino'] = st.text_input("País de Destino")
    else:
        nuevo_datos['pais_destino'] = st.text_input("Ciudad Local")

    nuevo_datos['motivo'] = st.text_input("Motivo")
    fecha_inicio = st.date_input("Fecha de Inicio")
    fecha_finalizacion = st.date_input("Fecha de Finalización")

    st.subheader("Vuelos")
    nuevo_datos['vuelos'] = []

    vuelo_index = 1  # Contador para generar claves únicas

    while True:
        aerolinea = st.text_input(f"Aerolínea {vuelo_index}")
        precio_boletos = st.number_input(f"Precio de Boletos {vuelo_index}")
        nuevo_datos['vuelos'].append({"aerolinea": aerolinea, "precio_boletos": precio_boletos})

        add_another = st.checkbox(f"Agregar otro vuelo ({vuelo_index})")  # Agregar un número único a la etiqueta del checkbox

        if not add_another:
            break

        vuelo_index += 1

    nuevo_datos['alojamiento'] = st.text_input("Alojamiento")
    nuevo_datos['requiere_transporte'] = st.checkbox("Requiere Transporte")

    agregar_button = st.button("Agregar Solicitud")

    if agregar_button:
        # Convierte las fechas de tipo date a cadenas de texto
        nuevo_datos['fecha_inicio'] = fecha_inicio.strftime("%Y-%m-%d")
        nuevo_datos['fecha_finalizacion'] = fecha_finalizacion.strftime("%Y-%m-%d")
        nuevo_datos['estado'] = "pendiente"  # Estado por defecto

        if solicitudesCrudServer.agregar_solicitud(usuario, nuevo_datos):
            st.success("Solicitud agregada con éxito.")
        else:
            st.error("No se pudo agregar la solicitud.")




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
            st.write(f"Requiere transporte: {solicitud['requiere_transporte']}")
            st.write(f"Es internacioal: {solicitud['internacional']}")
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