# colaborador.py

import streamlit as st
from server import conexionbd

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
    st.write(f"Bienvenido, {usuario} (Colaborador)")

    st.subheader("Menú de Colaborador")
    opcion = st.selectbox("Selecciona una funcionalidad:", ["Funcionalidad A", "Funcionalidad B", "Funcionalidad C"])
    
    if opcion == "Funcionalidad A":
        st.write("Has seleccionado Funcionalidad A. ¡Realiza las acciones correspondientes aquí!")
    elif opcion == "Funcionalidad B":
        st.write("Has seleccionado Funcionalidad B. ¡Realiza las acciones correspondientes aquí!")
    elif opcion == "Funcionalidad C":
        st.write("Has seleccionado Funcionalidad C. ¡Realiza las acciones correspondientes aquí!")
