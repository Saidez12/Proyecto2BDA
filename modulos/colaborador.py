# colaborador.py

import streamlit as st
from server import conexionbd
#pip install streamlit-option-menu
from streamlit_option_menu import option_menu
from modulos import crudSolicitudes

def registro_colaborador():
    st.subheader("Registro de Colaborador")
    correo = st.text_input("Correo Electrónico", key="correo_colaborador")
    contrasena = st.text_input("Contraseña", type="password", key="contrasena_colaborador")

    if st.button("Registrarse"):
        registrado = conexionbd.registrar_colaborador(correo, contrasena)
        if registrado:
            st.success("Registro de colaborador exitoso. Puedes iniciar sesión ahora.")
        else:
            st.error("El colaborador ya existe. Por favor, inicie sesión.")

def inicio_sesion_colaborador():
    st.subheader("Inicio de Sesión de Colaborador")
    correo = st.text_input("Correo Electrónico")
    contrasena = st.text_input("Contraseña", type="password")

    if st.button("Iniciar Sesión"):
        autenticado = conexionbd.autenticar_colaborador(correo, contrasena)
        if autenticado:
            st.success("Inicio de sesión de colaborador exitoso.")
            return True, correo  # Devuelve el estado autenticado y el correo
        else:
            st.error("Credenciales incorrectas. Por favor, inténtalo de nuevo.")
    return False, None  # Devuelve el estado no autenticado

def colaborador_page(usuario):
    st.sidebar.title(f"Bienvenido, {usuario} (Colaborador)")
    st.title(f"Bienvenido, {usuario} (Colaborador)")

    st.subheader("Menú de Colaborador")


    selected=option_menu(
        menu_title="Menú de Colaborador",
        options=["Registro de una solicitud de viaje", "Modificar una solicitud", "Eliminar una solicitud", "Ver historial de solicitudes"],
        orientation="horizontal",
    )
    if selected=="Registro de una solicitud de viaje":
        st.write("Has seleccionado Funcionalidad 1. ¡Realiza las acciones correspondientes aquí!")
    if selected=="Modificar una solicitud":
        st.write("Has seleccionado Funcionalidad 2. ¡Realiza las acciones correspondientes aquí!")
        crudSolicitudes.editar_solicitud(usuario)
    if selected=="Eliminar una solicitud":
         st.write("Has seleccionado Funcionalidad 2. ¡Realiza las acciones correspondientes aquí!")
    if selected=="Ver historial de solicitudes":
        crudSolicitudes.mostrar_solicitudes(usuario)
    # "Logout" 
    if st.button("Logout"):
        # Reset the authentication state
        st.session_state.authenticated = False
        st.experimental_rerun()