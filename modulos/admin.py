# admin.py

import streamlit as st
from server import conexionbd
from modulos import consultas,aprobarSolicitud
#pip install streamlit-option-menu
from streamlit_option_menu import option_menu

def registro_admin():
    st.subheader("Registro de Administrador")
    correo = st.text_input("Usuario", key="usuario_admin")
    contrasena = st.text_input("Contraseña", type="password", key="contrasena_admin")

    if st.button("Registrarse"):
        registrado = conexionbd.registrar_admin(correo, contrasena)
        if registrado:
            st.success("Registro de administrador exitoso. Puedes iniciar sesión ahora.")
        else:
            st.error("El administrador ya existe. Por favor, inicie sesión.")


def inicio_sesion_admin():
    st.subheader("Inicio de Sesión de Administrador")
    correo = st.text_input("Usuario")
    contrasena = st.text_input("Contraseña", type="password")

    if st.button("Iniciar Sesión"):
        autenticado = conexionbd.autenticar_admin(correo, contrasena)
        if autenticado:
            st.success("Inicio de sesión de administrador exitoso.")
            return True, correo  # Devuelve el estado autenticado y el correo
        else:
            st.error("Credenciales incorrectas. Por favor, inténtalo de nuevo.")
    return False, None  # Devuelve el estado no autenticado


def admin_page(usuario):
    st.sidebar.title(f"Bienvenido, {usuario} (Admin)")
    st.title(f"Bienvenido, {usuario} (Admin)")

    st.subheader("Menú de Administrador")


    selected=option_menu(
        menu_title="Menú de Administrador",
        options=["Valorar solicitud", "Consultar viajes programados", "Consultar viajes internacionales", "Consultar por destino específico"],
        orientation="horizontal",
    )
    if selected=="Valorar solicitud":
        aprobarSolicitud.mostrar_solicitudesPendientes()
        aprobarSolicitud.cambiar_estadoSolicitud()
    if selected=="Consultar viajes programados":
        consultas.consultar_viajes_programados()
    if selected=="Consultar viajes internacionales":
        consultas.consultar_viajes_internacionales()
    if selected=="Consultar por destino específico":
        consultas.consultar_por_destino()
    # "Logout" 
    if st.button("Logout"):
        # Reset the authentication state
        st.session_state.authenticated = False
        st.experimental_rerun()