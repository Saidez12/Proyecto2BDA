import streamlit as st
from server import conexionbd,solicitudesCrudServer

def mostrar_solicitudesPendientes():

    solicitudes=solicitudesCrudServer.mostrar_solicitudes_Pendientes()
    st.title("Solicitudes Pendientes")
    consultar_button = st.button("Consultar")


    if consultar_button:
        # Itera sobre las solicitudes y muéstralas
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

def cambiar_estadoSolicitud():
    solicitudes = solicitudesCrudServer.mostrar_solicitudes_Pendientes()
    listaId = [solicitud['identificador'] for solicitud in solicitudes]
    
    # Agregar un widget selectbox para que el usuario seleccione un ID
    idSeleccionado = st.selectbox("Selecciona un ID de Solicitud", listaId)
    
    # Buscar la solicitud seleccionada por ID
    solicitud_seleccionada = None
    for solicitud in solicitudes:
        if solicitud['identificador'] == idSeleccionado:
            solicitud_seleccionada = solicitud
    if solicitud_seleccionada:
        actualizar_button = st.button("Aprobar")
        rechazar_buton=st.button("Rechazar")
        if actualizar_button:
            if solicitudesCrudServer.cambiar_estadoSolicitud( idSeleccionado):
                st.success("Solicitud aprobada con éxito.")
            else:
                st.error("No se pudo actualizar el estado de la solicitud.")
        if rechazar_buton:
            if solicitudesCrudServer.rechazar_estadoSolicitud( idSeleccionado):
                st.success("Solicitud rechazada con éxito.")
            else:
                st.error("No se pudo rechazar la solicitud.")
    else:
        st.warning("Selecciona un ID válido de solicitud")
