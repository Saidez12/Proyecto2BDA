# admin.py

import streamlit as st
from server import conexionbd

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
    st.write(f"Bienvenido, {usuario} (Admin)")

    st.subheader("Menú de Administrador")
    opcion = st.selectbox("Selecciona una funcionalidad:", ["Funcionalidad 1", "Funcionalidad 2", "Funcionalidad 3"])
    
    if opcion == "Funcionalidad 1":
        st.write("Has seleccionado Funcionalidad 1. ¡Realiza las acciones correspondientes aquí!")
    elif opcion == "Funcionalidad 2":
        st.write("Has seleccionado Funcionalidad 2. ¡Realiza las acciones correspondientes aquí!")
    elif opcion == "Funcionalidad 3":
        st.write("Has seleccionado Funcionalidad 3. ¡Realiza las acciones correspondientes aquí!")
