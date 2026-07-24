import streamlit as st
import pandas as pd
from docx import Document
import re


# ==========================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ==========================================

st.set_page_config(
    page_title="Generador de Cuentas de Cobro",
    page_icon="📄"
)

st.title("📄 Generador de Cuentas de Cobro")

st.write(
    "Sube una plantilla Word y un archivo Excel "
    "para analizar si los campos coinciden."
)


# ==========================================
# CARGAR ARCHIVOS
# ==========================================

st.subheader("1. Seleccionar archivos")

word_file = st.file_uploader(
    "Selecciona la plantilla Word",
    type=["docx"]
)

excel_file = st.file_uploader(
    "Selecciona el archivo Excel",
    type=["xlsx", "xls"]
)


# ==========================================
# PROCESAR ARCHIVOS
# ==========================================

if word_file and excel_file:

    st.success("✓ Word y Excel cargados correctamente")

    if st.button("🔍 Analizar archivos"):

        # ----------------------------------
        # LEER EXCEL
        # ----------------------------------

        try:

            df = pd.read_excel(excel_file)

            st.subheader("📊 Información del Excel")

            st.write(
                f"Filas encontradas: **{len(df)}**"
            )

            st.write("Columnas encontradas:")

            for columna in df.columns:
                st.write(f"✓ {columna}")

        except Exception as e:

            st.error(
                f"Error al leer el Excel: {e}"
            )


        # ----------------------------------
        # LEER WORD
        # ----------------------------------

        try:

            documento = Document(word_file)

            texto_completo = "\n".join(
                parrafo.text
                for parrafo in documento.paragraphs
            )

            campos = re.findall(
                r"\((.*?)\)",
                texto_completo
            )

            # Eliminar campos repetidos
            campos = list(
                dict.fromkeys(campos)
            )

            st.subheader(
                "📄 Campos encontrados en Word"
            )

            for campo in campos:

                st.write(
                    f"✓ ({campo})"
                )

        except Exception as e:

            st.error(
                f"Error al leer el Word: {e}"
            )


        # ----------------------------------
        # COMPARAR WORD Y EXCEL
        # ----------------------------------

        columnas_excel = set(
            str(columna)
            .strip()
            .upper()
            for columna in df.columns
        )

        campos_word = set(
            campo
            .strip()
            .upper()
            for campo in campos
        )


        # Campo especial
        campos_especiales = {
            "VALOR LETRAS"
        }


        # Campos que deben existir
        campos_requeridos = (
            campos_word
            - campos_especiales
        )


        # Coincidencias
        coincidencias = (
            campos_requeridos
            .intersection(
                columnas_excel
            )
        )


        # Faltantes
        faltantes = (
            campos_requeridos
            - columnas_excel
        )


        # ----------------------------------
        # RESULTADOS
        # ----------------------------------

        st.subheader(
            "🔎 Resultado de la validación"
        )


        st.write(
            f"Campos coincidentes: "
            f"**{len(coincidencias)}**"
        )


        for campo in sorted(
            coincidencias
        ):

            st.success(
                f"✓ {campo}"
            )


        # ----------------------------------
        # CAMPOS ESPECIALES
        # ----------------------------------

        if (
            "VALOR LETRAS"
            in campos_word
        ):

            st.info(
                "ℹ️ VALOR LETRAS → "
                "Campo calculado automáticamente"
            )


        # ----------------------------------
        # CAMPOS FALTANTES
        # ----------------------------------

        if faltantes:

            st.warning(
                "⚠️ Faltan estos campos "
                "en el Excel:"
            )

            for campo in sorted(
                faltantes
            ):

                st.error(
                    f"✗ {campo}"
                )

        else:

            st.success(
                "✅ VALIDACIÓN EXITOSA"
            )
