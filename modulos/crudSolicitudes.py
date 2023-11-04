
import streamlit as st
from server import conexionbd,solcitudesCrudServer


# Función para mostrar las solicitudes
def mostrar_solicitudes(usuario):

    solicitudes=conexionbd.solicitudes_colaborador(usuario)
    st.title("Solicitudes Registradas")
    consultar_button = st.button("Consultar")


    if consultar_button:
        # Itera sobre las solicitudes y muéstralas
        for solicitud in solicitudes:
            st.subheader(f"Solicitud de {solicitud['nombre_completo_colaborador']}")
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
            if solcitudesCrudServer.actualizar_solicitud(usuario, idSeleccionado, nuevos_datos):
                st.success("Solicitud actualizada con éxito.")
            else:
                st.error("No se pudo actualizar la solicitud.")
    else:
        st.warning("Selecciona un ID válido de solicitud")