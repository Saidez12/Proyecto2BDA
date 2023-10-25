import streamlit as st
from modulos import colaborador, admin

# Use Streamlit session state to manage state variables
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'auth_user' not in st.session_state:
    st.session_state.auth_user = None
if 'rol' not in st.session_state:
    st.session_state.rol = None
if 'registro_colaborador' not in st.session_state:
    st.session_state.registro_colaborador = False
if 'registro_admin' not in st.session_state:
    st.session_state.registro_admin = False
if 'menu' not in st.session_state:
    st.session_state.menu = False  

eleccion = st.sidebar.radio("Selecciona una página:", ("Colaborador", "Administrador", "Abrir menu"))

def main():
    if not st.session_state.authenticated:
        if eleccion == "Colaborador":
            st.session_state.rol = eleccion
            if not st.session_state.authenticated:
                st.session_state.registro_colaborador = st.checkbox("Si no tienes cuenta, regístrate como Colaborador")
                if not st.session_state.authenticated:
                    st.session_state.authenticated, st.session_state.auth_user = colaborador.inicio_sesion_colaborador()
        if eleccion == "Administrador":
            st.session_state.rol = eleccion
            if not st.session_state.authenticated:
                st.session_state.registro_admin = st.checkbox("Si no tienes cuenta, regístrate como Administrador")
                if not st.session_state.authenticated:
                    st.session_state.authenticated, st.session_state.auth_user = admin.inicio_sesion_admin()
    if st.session_state.registro_colaborador:
        colaborador.registro_colaborador()
    if st.session_state.registro_admin:
        admin.registro_admin()

    if st.session_state.authenticated and eleccion == "Abrir menu":
        st.session_state.menu = True 
        if st.session_state.rol == "Colaborador":
            colaborador.colaborador_page(st.session_state.auth_user)
        elif st.session_state.rol == "Administrador":
            admin.admin_page(st.session_state.auth_user)
    if not st.session_state.authenticated and eleccion == "Abrir menu":
        st.session_state.menu = False 
        st.warning("Debe iniciar sesión o registrarse para acceder a la aplicación.")
    if st.session_state.authenticated and (eleccion == "Colaborador" or eleccion == "Administrador") and st.session_state.menu:
        st.warning("Ya has iniciado sesión. Para cambiar de usuario, debes cerrar sesión primero.")

if __name__ == '__main__':
    main()
