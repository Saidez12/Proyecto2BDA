# main.py
import streamlit as st
from modulos import colaborador, admin

# Variable global para el estado de la sesión y el usuario autenticado
authenticated = False
auth_user = None

# Variable para representar la página actual
current_page = "Inicio"  # Página de inicio

def main():
    global authenticated, auth_user, current_page
    st.title("Aplicación de Viajes Corporativos")

    if not authenticated:
        st.warning("Debe iniciar sesión o registrarse para acceder a la aplicación.")

        opcion = st.radio("Selecciona tu rol:", ("Colaborador", "Admin"))

        if opcion == "Colaborador":
            if not authenticated:
                authenticated, auth_user = colaborador.inicio_sesion_colaborador()
                if not authenticated:
                    colaborador.registro_colaborador()

        elif opcion == "Admin":
            if not authenticated:
                authenticated, auth_user = admin.inicio_sesion_admin()
                if not authenticated:
                    admin.registro_admin()

    if authenticated:
        current_page = st.selectbox("Selecciona una funcionalidad:", ["Inicio", "Colaborador", "Admin"])
        if current_page == "Inicio":
            st.empty()  # Borra la vista principal
        if current_page == "Colaborador":
            colaborador.menu_colaborador(auth_user)
        if current_page == "Admin":
            admin.menu_admin(auth_user)

if __name__ == '__main__':
    main()
