# ============================================================
# DASHBOARD DE REPASO DE PRUEBAS ESTADÍSTICAS EN PSICOLOGÍA
# ============================================================

import streamlit as st
import pandas as pd
import io
import requests

# ------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ------------------------------------------------------------
st.set_page_config(page_title="Repaso de Pruebas Estadísticas", page_icon="📊", layout="centered")

st.title("📊 Repaso de Pruebas Estadísticas en Psicología")
st.markdown("""
Selecciona la **prueba estadística correcta** para cada caso.  
Recibirás retroalimentación inmediata y al final verás tu puntaje total.
""")

# ------------------------------------------------------------
# OPCIÓN A: DATOS LOCALES (segura y por defecto)
# ------------------------------------------------------------
csv_data = """id,caso,opciones,respuesta_correcta,justificacion_correcta,justificacion_incorrecta1,justificacion_incorrecta2
1,"Una psicóloga comparó los puntajes de ansiedad de 20 pacientes antes y después de terapia cognitivo-conductual.","ANOVA | t de Student para muestras relacionadas | Pearson","t de Student para muestras relacionadas","Correcta: mide dos muestras relacionadas con datos normales.","Incorrecta: ANOVA compara tres o más grupos.","Incorrecta: Pearson mide correlación, no diferencias."
2,"Una investigadora evalúa la autoestima de 40 estudiantes (20 hombres, 20 mujeres) con datos no normales.","t de Student | Mann-Whitney | Wilcoxon","Mann-Whitney","Correcta: compara dos grupos independientes no normales.","Incorrecta: t de Student requiere normalidad.","Incorrecta: Wilcoxon es para muestras relacionadas."
3,"Se mide el estrés antes y después de un programa de yoga (ordinal).","ANOVA | Wilcoxon | Mann-Whitney","Wilcoxon","Correcta: dos mediciones relacionadas no normales.","Incorrecta: ANOVA requiere normalidad.","Incorrecta: Mann-Whitney es para grupos independientes."
4,"Relación entre horas de sueño y ansiedad (ambas continuas normales).","Pearson | Spearman | ANOVA","Pearson","Correcta: correlación lineal entre variables continuas normales.","Incorrecta: Spearman es para datos no paramétricos.","Incorrecta: ANOVA compara medias, no correlaciones."
5,"Nivel socioeconómico (bajo, medio, alto) y satisfacción vital (1-5).","Pearson | Spearman | t de Student","Spearman","Correcta: correlación ordinal/no paramétrica.","Incorrecta: Pearson requiere variables continuas.","Incorrecta: t de Student compara medias, no relaciones."
6,"Comparación de tres terapias para depresión (cognitiva, humanista, control).","t de Student | ANOVA | Spearman","ANOVA","Correcta: compara tres medias paramétricas.","Incorrecta: t de Student es solo para dos grupos.","Incorrecta: Spearman mide correlación, no diferencias."
7,"Impulsividad antes y después de taller (no normal).","t de Student | Mann-Whitney | Wilcoxon","Wilcoxon","Correcta: muestra relacionada no normal.","Incorrecta: t de Student requiere normalidad.","Incorrecta: Mann-Whitney es para grupos independientes."
8,"Empatía en 25 psicólogos clínicos y 25 educativos (normal).","t de Student independiente | Wilcoxon | ANOVA","t de Student independiente","Correcta: dos grupos independientes normales.","Incorrecta: Wilcoxon es para muestras relacionadas.","Incorrecta: ANOVA compara tres o más grupos."
9,"Estrés laboral y satisfacción con la vida (no normal).","Pearson | Spearman | ANOVA","Spearman","Correcta: correlación no paramétrica.","Incorrecta: Pearson requiere normalidad.","Incorrecta: ANOVA compara medias, no correlaciones."
10,"Puntaje de atención en jóvenes, adultos y adultos mayores (no normal).","ANOVA | t de Student | Kruskal-Wallis","Kruskal-Wallis","Correcta: tres grupos independientes no normales.","Incorrecta: ANOVA requiere normalidad.","Incorrecta: t de Student es para dos grupos."
"""
df = pd.read_csv(io.StringIO(csv_data))

# ------------------------------------------------------------
# OPCIÓN B: ACTIVAR CARGA DESDE GITHUB (descomenta si lo deseas)
# ------------------------------------------------------------
"""
url_github = "https://raw.githubusercontent.com/tuusuario/tu_repo/main/preguntas_psicologia.csv"
try:
    contenido = requests.get(url_github).content
    df = pd.read_csv(io.StringIO(contenido.decode('utf-8')))
except Exception:
    st.warning("⚠️ No se pudo cargar desde GitHub, usando datos locales.")
"""

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
    if st.session_state.indice >= len(df):
        st.session_state.finalizado = True
        st.experimental_rerun()
        return

    fila = df.iloc[st.session_state.indice]
    st.markdown(f"### 🧩 Caso {int(fila['id'])}")
    st.write(f"**Situación:** {fila['caso']}")
    opciones = [op.strip() for op in fila["opciones"].split("|")]
    opcion = st.radio("Selecciona la respuesta correcta:", opciones, key=f"pregunta_{fila['id']}")

    if st.button("Responder", key=f"btn_{fila['id']}") and not st.session_state.respondido:
        st.session_state.respondido = True
        correcta = fila["respuesta_correcta"].strip()
        if opcion == correcta:
            st.success(f"✅ ¡Correcto! {fila['justificacion_correcta']}")
            st.session_state.puntaje += 1
        else:
            st.error(f"❌ Incorrecto. {fila['justificacion_incorrecta1']}")

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
    st.success(f"Tu puntuación: **{score}/{total}** ({porcentaje:.1f}%)")

    if porcentaje >= 80:
        st.balloons()
        st.markdown("🥳 ¡Excelente dominio de las pruebas estadísticas!")
    elif porcentaje >= 60:
        st.info("💪 Buen desempeño, pero puedes reforzar algunos temas.")
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

st.write("---")
st.caption("Desarrollado con ❤️ en Streamlit · Curso de Estadística en Psicología (2025)")
