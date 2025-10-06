# ============================================================
# DASHBOARD DE REPASO DE PRUEBAS ESTADÍSTICAS EN PSICOLOGÍA
# Autor: ChatGPT (GPT-5)
# Fecha: Octubre 2025
# Descripción:
# Muestra un caso a la vez, permite responder, da retroalimentación inmediata
# y muestra el puntaje final al concluir todas las preguntas.
# ============================================================

import streamlit as st
import pandas as pd
import requests

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
    Este dashboard interactivo te permitirá practicar la selección de la **prueba estadística correcta** 
    según diferentes casos aplicados a la psicología.  
    Responde cada caso, recibe retroalimentación inmediata y observa tu resultado final al completar el cuestionario.
    """
)

# ------------------------------------------------------------
# CARGA DE DATOS DESDE GITHUB
# ------------------------------------------------------------
# 🔧 Reemplaza esta URL con la de tu archivo CSV en GitHub (usa el enlace RAW)
url_github = "https://raw.githubusercontent.com/tuusuario/tu_repo/main/preguntas_psicologia.csv"

@st.cache_data
def cargar_datos():
    """Carga el archivo CSV con las preguntas desde GitHub"""
    contenido = requests.get(url_github).content
    df = pd.read_csv(pd.io.common.StringIO(contenido.decode('utf-8')))
    return df

try:
    df = cargar_datos()
except Exception as e:
    st.error("⚠️ No se pudo cargar el archivo desde GitHub. Verifica la URL RAW del CSV.")
    st.stop()

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
# FUNCIÓN PRINCIPAL PARA MOSTRAR CADA PREGUNTA
# ------------------------------------------------------------
def mostrar_pregunta():
    fila = df.iloc[st.session_state.indice]
    st.markdown(f"### 🧩 Caso {int(fila['id'])}")
    st.write(f"**Situación:** {fila['caso']}")

    # Opciones separadas por "|"
    opciones = [op.strip() for op in fila["opciones"].split("|")]
    opcion = st.radio(
        "Selecciona la prueba estadística correcta:",
        opciones,
        key=f"pregunta_{fila['id']}"
    )

    # Botón de respuesta
    if st.button("Responder", key=f"boton_{fila['id']}") and not st.session_state.respondido:
        st.session_state.respondido = True

        # Evaluación
        if opcion == fila["respuesta_correcta"]:
            st.success(f"✅ ¡Correcto! {fila['justificacion_correcta']}")
            st.session_state.puntaje += 1
        else:
            # Mostrar justificación incorrecta correspondiente
            opciones_sin_espacios = [op.strip() for op in fila["opciones"].split("|")]
            idx = opciones_sin_espacios.index(opcion)
            if idx == 0:
                st.error(f"❌ Incorrecto. {fila['justificacion_incorrecta1']}")
            else:
                st.error(f"❌ Incorrecto. {fila['justificacion_incorrecta2']}")

    # Avanzar
    if st.session_state.respondido:
        if st.session_state.indice < len(df) - 1:
            if st.button("➡️ Siguiente pregunta"):
                st.session_state.indice += 1
                st.session_state.respondido = False
                st.experimental_rerun()
        else:
            st.session_state.finalizado = True

# ------------------------------------------------------------
# MOSTRAR PREGUNTAS O RESULTADOS
# ------------------------------------------------------------
if not st.session_state.finalizado:
    mostrar_pregunta()
else:
    st.subheader("🎯 Resultados Finales")
    total = len(df)
    score = st.session_state.puntaje
    porcentaje = (score / total) * 100

    st.success(f"Tu puntuación final es **{score}/{total}** ({porcentaje:.1f}%)")

    if porcentaje >= 80:
        st.balloons()
        st.markdown("🥳 ¡Excelente dominio de las pruebas estadísticas!")
    elif porcentaje >= 60:
        st.info("💪 Buen desempeño, pero puedes repasar algunos conceptos.")
    else:
        st.warning("📘 Te recomiendo repasar las diferencias entre pruebas paramétricas y no paramétricas.")

    # Reiniciar
    if st.button("🔁 Reiniciar cuestionario"):
        st.session_state.indice = 0
        st.session_state.puntaje = 0
        st.session_state.respondido = False
        st.session_state.finalizado = False
        st.experimental_rerun()

# ------------------------------------------------------------
# PIE DE PÁGINA
# ------------------------------------------------------------
st.write("---")
st.caption("Desarrollado con ❤️ en Streamlit · Curso de Estadística en Psicología (2025)")
