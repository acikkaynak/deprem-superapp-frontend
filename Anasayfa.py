from helpers.streamlit_helpers import streamlit_helper as sh, streamlit_events as se, \
    streamlit_session_helper as session_helper
import streamlit as st
from streamlit_folium import folium_static
from dotenv import load_dotenv
from models import GLOBALS

load_dotenv()

payload = {}


def InitComponents():
    sh.SetInitialStreamlitStates(sections=["global", "first_page"])
    st.set_page_config(layout="wide")

InitComponents()


def first_page():
    st.header("Yardım Çağrısında Bulun!")

    folium_static(fig=session_helper.get_session("first_page_map"), width=1400, height=600)

    payload["il"] = st.sidebar.selectbox(
        label="İl [ZORUNLU]", options=session_helper.get_session("province_list"), key="first_page_province",
        on_change=se.first_page_province_changed, index=session_helper.get_session("first_page_province_index"),
    )

    payload["ilce"] = st.sidebar.selectbox(
        label="İlçe [ZORUNLU]", options=session_helper.get_session("first_page_selectable_districts"),
        index=session_helper.get_session("first_page_district_index"),
        key="first_page_district", on_change=se.first_page_district_changed
    )

    payload["gereksinimler"] = st.sidebar.multiselect(
        'Neye İhtiyacınız Var?',
        GLOBALS.NEEDS,
        GLOBALS.NEEDS[0])

    payload["adres"] = st.sidebar.text_area(
        label="Adres [ZORUNLU]", key='first_page_address', on_change=se.first_page_address_changed
    )

    st.sidebar.checkbox(label="Adresi benim için otomatik doldur", key="first_page_is_address_autofill", value=True)

    payload["isim"] = st.sidebar.text_input(
        label="İsim [ZORUNLU]"
    )

    payload["telefon"] = st.sidebar.text_input(
        label="Telefon numarası [OPSİYONEL]"
    )

    payload["notlar"] = st.sidebar.text_area(
        label="NOT [OPSİYONEL]"
    )
    st.sidebar.button("Gönder", key="first_page_submit_button", on_click=se.first_page_on_submit_button_click, args=(payload,))

    if session_helper.get_session("first_page_is_success"):
        st.sidebar.success('Mesajınız alındı!', icon="✅")
    if session_helper.get_session("first_page_is_error"):
        st.sidebar.error(session_helper.get_session("first_page_error_message"), icon="🚨")


first_page()