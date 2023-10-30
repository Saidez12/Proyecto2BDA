
import streamlit as st
from server import conexionbd

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
