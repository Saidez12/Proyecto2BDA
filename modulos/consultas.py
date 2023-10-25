#consultas.py

import streamlit as st
from server import conexionbd

def consultar_por_destino():
    st.write("Consultar Viajes por Destino Específico")
    
    destino_seleccionado = st.text_input("Ingrese el destino específico:")
    consultar_button = st.button("Consultar")

    if consultar_button:
        viajes = conexionbd.consultar_viajes_por_destino(destino_seleccionado)

        if not viajes:
            st.write("No se encontraron viajes hacia ese destino.")
        else:
            st.write("Resultados:")
            for viaje in viajes:
                st.write(f"Colaborador: {viaje['nombre_completo_colaborador']}")
                st.write(f"Fecha de inicio: {viaje['fecha_inicio']}")
                st.write(f"Motivo: {viaje['motivo']}")
                st.write("---")

def consultar_viajes_internacionales():
    st.write("Consultar Viajes Internacionales por Trimestre y Año")
    
    # Collect user input for quarter and year
    trimestre = st.selectbox("Selecciona el trimestre:", ["1", "2", "3", "4"])
    año = st.number_input("Selecciona el año:", min_value=2000, max_value=3000, step=1)
    
    consultar_button = st.button("Consultar")

    if consultar_button:

        viajes = conexionbd.viajes_internacionales(trimestre, año)

        if not viajes:
            st.write("No se encontraron viajes internacionales en el trimestre y año seleccionados.")
        else:
            st.write("Resultados:")
            for viaje in viajes:
                colaborador_nombre = viaje['nombre_completo_colaborador']
                destino_pais = viaje['pais_destino']
                st.write(f"Colaborador(a): {colaborador_nombre}")
                st.write(f"País de Destino: {destino_pais}")
                st.write("---")
