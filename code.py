# ============================================================
# DASHBOARD DE REPASO DE PRUEBAS ESTADÍSTICAS EN PSICOLOGÍA
# ============================================================

import streamlit as st
import pandas as pd
import requests
import io

# ------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ------------------------------------------------------------
st.set_page_config(
    page_title="Repaso de Pruebas Estadísticas",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Repaso de Pruebas Estadísticas en Psicología")
st.markdown(
    """
    Responde cada caso seleccionando la **prueba estadística correcta**.
    Obtendrás retroalimentación inmediata y un resultado final al concluir.
    """
)

# ------------------------------------------------------------
# CARGA DE DATOS DESDE GITHUB
# ------------------------------------------------------------
# 🔧 Cambia esta URL a la de tu CSV en GitHub (usa el enlace RAW)
url_github = "https://raw.githubusercontent.com/tuusuario/tu_repo/main/preguntas_psicologia.csv"

@st.cache_data
def cargar_datos():
    """Carga el CSV desde GitHub"""
    try:
        contenido = requests.get(url_github).content
        df = pd.read_csv(io.StringIO(contenido.decode('utf-8')))
        return df
    except Exception as e:
        st.error("❌ Error al cargar el archivo. Verifica la URL RAW y el formato CSV.")
        st.stop()

df = cargar_datos()

# ------------------------------------------------------------
# VARIABLES DE SESIÓN
# ------------------------------------------------------------
if "indice" not in st.session_state:
    st.session_state.indice = 0
if "puntaje" not in st.session_state:
    st.session_state.puntaje = 0
if "respondido" not in st.session_state:
    st.session_state.respondido = False
if "finalizado" not in st.session_state:
    st.session_state.finalizado = False

# ------------------------------------------------------------
# FUNCIÓN PARA MOSTRAR UNA PREGUNTA
# ------------------------------------------------------------
def mostrar_pregunta():
    # Validar que el índice no se salga del rango
    if st.session_state.indice >= len(df):
        st.session_state.finalizado = True
        return

    fila = df.iloc[st.session_state.indice]
    st.markdown(f"### 🧩 Caso {int(fila['id'])}")
    st.write(f"**Situación:** {fila['caso']}")

    # Separar opciones
    opciones = [op.strip() for op in fila["opciones"].split("|")]
    opcion = st.radio(
        "Selecciona la prueba estadística correcta:",
        opciones,
        key=f"pregunta_{fila['id']}"
    )

    # Botón de respuesta
    if st.button("Responder", key=f"btn_{fila['id']}") and not st.session_state.respondido:
        st.session_state.respondido = True
        correcta = fila["respuesta_correcta"].strip()

        if opcion == correcta:
            st.success(f"✅ ¡Correcto! {fila['justificacion_correcta']}")
            st.session_state.puntaje += 1
        else:
            st.error(f"❌ Incorrecto. {fila['justificacion_incorrecta1']}")

    # Botón siguiente
    if st.session_state.respondido:
        if st.session_state.indice < len(df) - 1:
            if st.button("➡️ Siguiente pregunta"):
                st.session_state.indice += 1
                st.session_state.respondido = False
                st.experimental_rerun()
        else:
            if st.button("🎯 Ver resultado final"):
                st.session_state.finalizado = True
                st.experimental_rerun()

# ------------------------------------------------------------
# FUNCIÓN PARA MOSTRAR RESULTADOS
# ------------------------------------------------------------
def mostrar_resultado():
    total = len(df)
    score = st.session_state.puntaje
    porcentaje = (score / total) * 100

    st.subheader("🎯 Resultado Final")
    st.success(f"Tu puntuación es **{score}/{total}** ({porcentaje:.1f}%)")

    if porcentaje >= 80:
        st.balloons()
        st.markdown("🥳 **¡Excelente dominio de las pruebas estadísticas!**")
    elif porcentaje >= 60:
        st.info("💪 Buen desempeño, pero puedes repasar algunos conceptos.")
    else:
        st.warning("📘 Te recomiendo repasar las diferencias entre pruebas paramétricas y no paramétricas.")

    if st.button("🔁 Reiniciar cuestionario"):
        st.session_state.indice = 0
        st.session_state.puntaje = 0
        st.session_state.respondido = False
        st.session_state.finalizado = False
        st.experimental_rerun()

# ------------------------------------------------------------
# CONTROL DE FLUJO
# ------------------------------------------------------------
if not st.session_state.finalizado:
    mostrar_pregunta()
else:
    mostrar_resultado()

# ------------------------------------------------------------
# PIE DE PÁGINA
# ------------------------------------------------------------
st.write("---")
st.caption("Desarrollado con ❤️ en Streamlit · Curso de Estadística en Psicología (2025)")
