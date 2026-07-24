import streamlit as st

st.set_page_config(
    page_title="Generador de Cuentas de Cobro",
    page_icon="📄"
)

st.title("📄 Generador de Cuentas de Cobro")

st.write(
    "Esta aplicación permitirá generar documentos "
    "automáticamente a partir de un archivo Word y un archivo Excel."
)

st.subheader("Archivos de entrada")

word_file = st.file_uploader(
    "Selecciona la plantilla Word",
    type=["docx"]
)

excel_file = st.file_uploader(
    "Selecciona el archivo Excel",
    type=["xlsx", "xls"]
)

if word_file:
    st.success("✓ Archivo Word seleccionado")

if excel_file:
    st.success("✓ Archivo Excel seleccionado")

if word_file and excel_file:
    st.success("✓ Ambos archivos están listos para analizar")
