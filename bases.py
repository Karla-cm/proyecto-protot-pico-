
import streamlit as st
import pandas as pd
import folium
import geopandas as gpd
from matplotlib.colors import rgb2hex
import matplotlib.cm
from streamlit_folium import folium_static
import numpy as np # For checking NaN values more broadly if needed
import plotly.express as px # For charts in SocioScram
import re # For URL analysis in SocioScram
import altair as alt # For Scrambuster 60+ charts
import pydeck as pydeck # For Scrambuster 60+ map
# Configuración inicial de la página
st.set_page_config(page_title="Curso: Prevención del Ciberfraude y Phishing", layout="wide")

# --- Inyección de CSS Personalizado ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Lato:wght@400;700&family=Open+Sans:wght@400;700&display=swap');

body {
    font-family: 'Lato', 'Open Sans', sans-serif; /* Nueva fuente para el cuerpo */
    background-color: #98FB98; /* Tono de verde menta */
    color: #263238; /* Color de texto principal más oscuro */
    line-height: 1.6;
}

/* Contenedor principal de la aplicación (excluyendo la barra lateral) */
[data-testid="stAppViewContainer"] {
    background-color: rgba(255, 255, 255, 0.8); /* Fondo blanco semi-transparente para el contenido */
    backdrop-filter: blur(5px); /* Efecto de desenfoque para el fondo del contenedor */
    border-radius: 10px; /* Bordes redondeados para el contenedor principal */
    margin: 10px; /* Pequeño margen alrededor del contenedor principal */
    padding: 20px; /* Padding interno */
}

h1 { /* st.title */
    font-family: 'Montserrat', 'Roboto', sans-serif; /* Nueva fuente para títulos */
    color: #00796b; /* Verde azulado oscuro para títulos */
    font-weight: 700;
    border-bottom: 3px solid #004d40; /* Acento verde más oscuro */
    padding-bottom: 0.3em;
    margin-bottom: 0.7em;
}

h2 { /* st.header */
    font-family: 'Montserrat', 'Roboto', sans-serif; /* Nueva fuente para encabezados */
    color: #00897b; /* Verde azulado para encabezados */
    font-weight: 700;
    margin-top: 1.5em;
    margin-bottom: 0.6em;
}

h3 { /* st.subheader */
    font-family: 'Montserrat', 'Roboto', sans-serif; /* Nueva fuente para subencabezados */
    color: #26a69a; /* Verde azulado más claro para subencabezados */
    font-weight: 400;
    margin-top: 1.2em;
    margin-bottom: 0.5em;
}

p, li {
    font-size: 1.05em; /* Ligeramente más grande para mejorar legibilidad */
    color: #37474f; /* Gris azulado oscuro para párrafos y listas */
}

/* Estilo para los contenedores usados como tarjetas en la página de Inicio */
/* Se dirige a la estructura específica creada por st.columns y st.container(border=True) */
div[data-testid="stVerticalBlock"] div[data-testid="stHorizontalBlock"] div[data-testid="stVerticalBlock"] > div[data-testid="stStyledFullScreenFrame"] {
    background-color: #ffffff; /* Fondo blanco para las tarjetas */
    border: 1px solid #dfe6e9; /* Borde suave */
    border-radius: 10px; /* Bordes más redondeados */
    box-shadow: 0 2px 5px rgba(0,0,0,0.08);
    padding: 1.3em !important; /* Aumentar padding, !important si es necesario */
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

div[data-testid="stVerticalBlock"] div[data-testid="stHorizontalBlock"] div[data-testid="stVerticalBlock"] > div[data-testid="stStyledFullScreenFrame"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 10px rgba(0,0,0,0.12);
}

/* Estilo para los encabezados de los st.expander */
[data-testid="stExpander"] summary {
    font-size: 1.1em; /* Un poco más grande */
    font-weight: bold;
    background-color: #B4E1FF; /* Azul claro pastel para expanders */
    color: #ffffff; /* Texto blanco */
    border: none;
    border-radius: 8px; /* Bordes más redondeados */
    padding: 0.7em 1.2em;
    margin-bottom: 0.2em; /* Pequeño espacio antes del contenido */
    transition: background-color 0.2s ease;
}
[data-testid="stExpander"] summary:hover {
    background-color: #ADD8E6; /* Azul claro al pasar el cursor */
}

/* Estilo para el contenido dentro de los st.expander */
[data-testid="stExpander"] [data-testid="stVerticalBlock"] {
    background-color: #e8f5e9; /* Fondo verde muy claro para el contenido del expander */
    padding: 1.2em;
    border: 1px solid #c8e6c9; /* Borde verde sutil */
    border-top: none; /* El summary ya crea una separación visual */
    border-radius: 0 0 6px 6px; /* Redondear esquinas inferiores */
}

/* --- Estilos Opcionales para la Barra Lateral --- */
/* [data-testid="stSidebar"] {
    background-color: #2c3e50; 
}
[data-testid="stSidebar"] .st-emotion-cache-16txtl3 { 
    color: #ecf0f1 !important;
    font-size: 1.05em;
}
[data-testid="stSidebar"] .st-emotion-cache-16txtl3:hover {
    color: #ffffff !important;
}
[data-testid="stSidebar"] h1 { 
    color: #ffffff;
    font-size: 1.5em;
    text-align: center;
    border-bottom: none;
    margin-bottom: 1em;
} */

/* Estilo para st.info */
div[data-testid="stInfo"] {
    background-color: #e0f2f1; /* Verde azulado muy claro */
    border-left: 5px solid #00796b; /* Borde izquierdo verde azulado */
    color: #004d40; /* Texto verde azulado oscuro */
    padding: 1em;
    border-radius: 4px;
}

/* Estilo para st.success */
div[data-testid="stSuccess"] {
    background-color: #dcedc8; /* Verde claro */
    border-left: 5px solid #689f38; /* Borde izquierdo verde medio */
    color: #33691e; /* Texto verde oscuro */
    padding: 1em;
    border-radius: 4px;
}

/* Estilo para st.error */
div[data-testid="stError"] {
    background-color: #ffcdd2; /* Rojo muy claro */
    border-left: 5px solid #d32f2f; /* Borde izquierdo rojo */
    color: #b71c1c; /* Texto rojo oscuro */
    padding: 1em;
    border-radius: 4px;
}

/* Estilo para st.warning */
div[data-testid="stWarning"] {
    background-color: #fff9c4; /* Amarillo muy claro */
    border-left: 5px solid #fbc02d; /* Borde izquierdo amarillo */
    color: #f57f17; /* Texto amarillo oscuro/naranja */
    padding: 1em;
    border-radius: 4px;
}

/* Estilo para botones */
button[data-testid="baseButton-secondary"] { /* Botón por defecto de Streamlit */
    background-color: #00796b; /* Verde azulado para botones */
    color: white;
    border: none;
    border-radius: 5px;
    padding: 0.6em 1.2em;
    font-weight: bold;
    transition: background-color 0.2s ease, transform 0.1s ease;
}
button[data-testid="baseButton-secondary"]:hover {
    background-color: #004d40; /* Verde más oscuro al pasar el cursor */
    transform: translateY(-1px);
}
button[data-testid="baseButton-secondary"]:active {
    transform: translateY(0px);
}

</style>
""", unsafe_allow_html=True)

# --- Funciones para mostrar cada página/módulo ---

def display_inicio():
    st.title("🔐Curso: Prevención del Ciberfraude y Phishing🔐")
    st.divider()
    st.markdown("""
    🧠Bienvenido al curso interactivo sobre cómo protegerte del ciberfraude y el phishing🧠.

    📌En la era digital, los adultos mayores se han convertido en un grupo especialmente vulnerable ante el creciente fenómeno del fraude a través de dispositivos móviles. Este problema no solo representa un desafío tecnológico, sino también social, psicológico y ético, ya que afecta directamente su seguridad económica, su confianza en las herramientas digitales y su bienestar emocional. En muchos casos, esta población carece de las habilidades necesarias para identificar y evitar estafas en línea.
    El fraude digital contra la tercera edad no puede abordarse desde una sola perspectiva. Por un lado, existe un componente tecnológico: los delincuentes aprovechan la falta de familiaridad de los adultos mayores con aplicaciones, mensajes de phishing o enlaces maliciosos. Por otro, hay un factor social: muchos ancianos viven solos o tienen redes de apoyo limitadas, lo que los hace más susceptibles a engaños. Además, el impacto psicológico es significativo, ya que, tras ser víctimas de fraude, pueden desarrollar desconfianza hacia la tecnología o incluso aislarse por miedo a nuevos ataques.
    """)
    st.divider()
    st.subheader("🔍 En este curso aprenderás a:")

    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.markdown("##### ✅ Reconocer Señales de Alerta")
            st.markdown("En correos, mensajes y sitios web.")
    with col2:
        with st.container(border=True):
            st.markdown("##### ❌ Evitar Fraudes Comunes")
            st.markdown("Especialmente en redes sociales.")
    with col3:
        with st.container(border=True):
            st.markdown("##### 🔒 Proteger tu Información")
            st.markdown("Mantén seguros tus datos personales en línea.")

    st.divider()
    st.markdown("""
   📋 Usa el menú lateral para navegar por los módulos.
    """)

def display_modulo1():
    st.header("🧩Módulo 1: ¿Qué es el Ciberfraude?👨‍💻 / 👩‍💻")
    st.markdown("""
    El ciberfraude es un tipo de delito cometido a través de Internet o medios digitales, donde los ciberdelincuentes utilizan técnicas engañosas para obtener beneficios económicos, robar información personal o financiera, o causar daños a las víctimas.
    """)
    st.divider()
    st.subheader("Modalidades Comunes de Ciberfraude:")
    st.markdown("""
    *   **⚠️ Phishing:** Suplantación de identidad de instituciones financieras o empresas para robar datos bancarios mediante correos o mensajes falsos.
    *   **⚠️ Smishing:** Uso de mensajes SMS con enlaces fraudulentos que dirigen a páginas falsas.
    *   **⚠️ Pharming:** Redirección a sitios web falsos para capturar información confidencial.
    *   **⚠️ Vishing:** Llamadas telefónicas simulando ser empleados de bancos para obtener datos.
    *   **⚠️ Malware:** Software malicioso (como ransomware) que infecta dispositivos para extorsionar o robar información.
    *   **⚠️ Ofertas engañosas:** Promociones falsas en redes sociales o tiendas en línea que buscan estafar con pagos anticipados.
    """)

def display_modulo2():
    st.header("🧩Módulo 2: ¿Qué es el Phishing?")
    st.markdown("""
    🖥️El phishing es un tipo de ciberfraude que busca engañar a las personas para que revelen información personal, como contraseñas o datos bancarios. Los atacantes se hacen pasar por entidades de confianza (bancos, empresas, instituciones públicas) a través de correos electrónicos, mensajes de texto, llamadas telefónicas o sitios web falsos
    """)
    st.divider()

    st.subheader("📲 Características del Phishing")
    st.markdown("""
    *   **📟 Suplantación de identidad:** Los ciberdelincuentes imitan marcas legítimas (ej. Amazon, PayPal, bancos) usando logos y diseños similares para parecer auténticos.
    *   **👩‍💻 Tácticas de urgencia o miedo:** Mensajes alarmantes como "¡Tu cuenta será bloqueada!" o "¡Actúa ahora!" para manipular emocionalmente a la víctima.
    *   **🌐 Enlaces o archivos maliciosos:** Incluyen links a páginas falsas que imitan sitios reales (ej. una copia de la web de BBVA) o adjuntos infectados con malware.
    """)

    st.subheader("📱 Tipos Comunes de Phishing")
    st.markdown("""
    *   **📤 Phishing masivo:** Correos genéricos enviados a miles de personas, esperando que algunos caigan.
    *   **👫 Spear phishing:** Ataques personalizados con información específica de la víctima (ej. nombre, cargo laboral).
    *   **📞 Smishing y Vishing:** Usan SMS o llamadas telefónicas para robar datos.
    *   **📶 Whaling:** Dirigido a ejecutivos de alto nivel para fraudes financieros.
    *   **🛜 Pharming:** Redirige a sitios falsos incluso si la víctima escribe la URL correcta.
    """)

def display_modulo3():
    st.header("🧩Módulo 3: ¿Por qué los Adultos Mayores son Vulnerables?")
    st.markdown("""
    Los adultos mayores enfrentan una situación de vulnerabilidad debido a la convergencia de múltiples factores que dificultan su adaptación a una sociedad en constante evolución. Esta vulnerabilidad surge principalmente por barreras tecnológicas, sociales y psicológicas, las cuales se interrelacionan y generan exclusión, dependencia y riesgos para su calidad de vida.
    """)
    st.divider()

    with st.expander("💻 Factores Tecnológicos", expanded=True):
        st.markdown("""
        La **brecha digital** es uno de los mayores obstáculos, ya que muchos adultos mayores no tuvieron contacto temprano con tecnologías modernas como smartphones, computadoras o internet. Esto les dificulta realizar trámites en línea, acceder a servicios digitales o incluso comunicarse con familiares a través de plataformas virtuales.
        *   Dificultades de aprendizaje debido a la rápida evolución tecnológica.
        *   Falta de acceso económico a dispositivos o conexiones estables.
        *   Temor a fraudes digitales (como phishing o estafas), lo que incrementa su marginación.
        """)

    with st.expander("🤝 Factores Sociales"):
        st.markdown("""
        El **aislamiento social** es un problema recurrente, agravado por la jubilación, la pérdida de pareja o amigos, y la movilidad reducida. Esto limita sus interacciones y puede llevar a soledad crónica.
        *   Estereotipos sociales que los presentan como incapaces de aprender o participar activamente.
        *   Dependencia económica, con pensiones a menudo insuficientes.
        *   Falta de políticas públicas que promuevan su inclusión.
        """)

    with st.expander("🧠 Factores Psicológicos"):
        st.markdown("""
        La **resistencia al cambio** es común, pues muchos prefieren métodos tradicionales y experimentan ansiedad ante lo nuevo.
        *   El deterioro cognitivo asociado a la edad (como demencia o Alzheimer) puede dificultar la adaptación.
        *   Baja autoeficacia (falta de confianza en sus propias habilidades para aprender).
        *   Problemas de salud mental como depresión o ansiedad, que pueden generar sentimientos de inutilidad.
        """)

def display_modulo4():
    st.header("🧩Módulo 4: Señales de Alerta") # Corregido para consistencia de mayúsculas
    st.markdown("""
    Los adultos mayores son especialmente vulnerables a los ciberfraudes y phishing debido a factores como la brecha digital, la confianza excesiva y el desconocimiento de las tácticas utilizadas por los delincuentes. A continuación, se detallan las señales de alerta más comunes y cómo identificarlas para protegerte:
    """)
    st.divider()

    with st.expander("🚩 En Correos Electrónicos y Mensajes (SMS/WhatsApp)", expanded=True):
        st.markdown("""
        *   **Remitentes desconocidos o sospechosos:** Si no reconoces la dirección de correo o el número de teléfono, desconfía. Presta atención a direcciones que intentan imitar a empresas conocidas pero tienen ligeras variaciones (ej. `soporte@banco-confirmacion.com` en lugar de `soporte@banco.com`).
        *   **Asuntos alarmistas o demasiado buenos para ser verdad:** Frases como "¡Urgente! Su cuenta ha sido bloqueada", "Ha ganado un premio millonario" o "Problema con su envío" buscan generar una reacción inmediata sin pensar.
        *   **Errores gramaticales y ortográficos:** Los mensajes fraudulentos suelen contener errores de redacción, mala puntuación o traducciones extrañas. Las empresas serias cuidan mucho su comunicación.
        *   **Solicitud de información personal o financiera:** Ninguna entidad legítima (bancos, gobierno, etc.) te pedirá contraseñas, números de tarjeta completos, códigos de seguridad o datos sensibles por correo o mensaje.
        *   **Enlaces o botones sospechosos:** Antes de hacer clic, pasa el cursor sobre el enlace (sin hacer clic) para ver la dirección web real a la que te dirige. Si parece extraña o no coincide con la empresa que dice ser, no hagas clic. En el móvil, mantén presionado el enlace para ver la URL.
        *   **Archivos adjuntos inesperados:** No descargues ni abras archivos adjuntos que no esperabas, especialmente si son de remitentes desconocidos o tienen extensiones como `.exe`, `.zip` (si no esperas un comprimido) o `.scr`.
        *   **Saludos genéricos:** Desconfía de correos que comiencen con "Estimado cliente" o "Apreciado usuario" en lugar de tu nombre, especialmente si supuestamente provienen de una entidad con la que tienes una cuenta.
        """)

    with st.expander("🚩 En Sitios Web"):
        st.markdown("""
        *   **URL extraña o sin "https":** Verifica que la dirección del sitio web comience con `https://` (la "s" indica seguridad) y que el nombre de dominio sea el correcto. Los sitios fraudulentos pueden tener URLs muy largas, con guiones o números extraños, o dominios diferentes (ej. `bbva-seguridad.net` en lugar de `bbva.mx`).
        *   **Diseño de baja calidad o diferente al habitual:** Si el sitio web se ve poco profesional, con imágenes de mala calidad, colores distintos o una estructura diferente a la que conoces de esa empresa, podría ser falso.
        *   **Ventanas emergentes (pop-ups) pidiendo datos:** Desconfía de las ventanas emergentes que te piden información personal o te instan a descargar software.
        *   **Ofertas demasiado buenas para ser verdad:** Precios increíblemente bajos o promociones exageradas pueden ser un gancho para estafarte.
        """)

    with st.expander("🚩 En Llamadas Telefónicas (Vishing)"):
        st.markdown("""
        *   **Llamadas inesperadas de supuestos bancos o instituciones:** Si te llaman para "verificar tu cuenta", "confirmar una transacción sospechosa" o "actualizar tus datos", cuelga.
        *   **Presión para actuar de inmediato:** Los estafadores intentarán que no tengas tiempo de pensar, amenazando con consecuencias graves si no proporcionas la información al instante.
        *   **Solicitud de claves, contraseñas o códigos de verificación:** Nunca compartas esta información por teléfono. Tu banco nunca te la pedirá.
        *   **Petición de instalar software o dar acceso remoto a tu computadora/móvil:** Esto es una táctica común para tomar control de tus dispositivos.
        """)

def display_modulo5():
    st.header("🧩Módulo 5: Casos Reales y Estadísticas con Mapa Interactivo")
    st.markdown("""
    Explora las denuncias de manera interactiva en el mapa. Utiliza los filtros para analizar patrones y tendencias en la Ciudad de México.
    """)
    st.divider()

    # --- Carga de datos ---
    @st.cache_data # Cache data for performance
    def load_data():
        try:
            df_denuncias = pd.read_csv("denuncias_filtrado.csv")
            geojson_path = "limite-de-las-alcaldas(1).json" 
            alcaldias_gdf = gpd.read_file(geojson_path)
            return df_denuncias, alcaldias_gdf
        except FileNotFoundError as e:
            st.error(f"Error al cargar archivos de datos: {e}. Asegúrate de que 'denuncias_filtrado.csv' y 'limite-de-las-alcaldas.json' estén en el directorio correcto.")
            return None, None

    df_denuncias, alcaldias_gdf = load_data()

    if df_denuncias is None or alcaldias_gdf is None:
        return # Stop execution if data loading failed

    # Preprocesamiento inicial
    alcaldias_gdf['alcaldia'] = alcaldias_gdf['NOMGEO'].str.upper()
    if 'alcaldia_hecho' in df_denuncias.columns:
        df_denuncias['alcaldia_hecho'] = df_denuncias['alcaldia_hecho'].str.upper()
    else:
        st.warning("La columna 'alcaldia_hecho' no se encuentra en 'denuncias_filtrado.csv'. Algunas funcionalidades del mapa pueden no estar disponibles.")

    # --- Filtros interactivos ---
    st.subheader("Filtros del Mapa")
    
    # Check for necessary columns before creating filters
    available_years = []
    if 'anio_hecho' in df_denuncias.columns and len(df_denuncias['anio_hecho'].dropna().unique()) > 0:
        available_years = sorted(df_denuncias['anio_hecho'].dropna().astype(int).unique())
    
    available_delitos = []
    if 'delito' in df_denuncias.columns and len(df_denuncias['delito'].dropna().unique()) > 0:
        available_delitos = sorted(df_denuncias['delito'].dropna().unique())

    año_selected = st.selectbox("Selecciona el año:", available_years, key="map_year_filter") if available_years else None
    
    col1_filter, col2_filter, col3_filter = st.columns(3)
    with col1_filter:
        delitos_selected = st.multiselect("Selecciona delitos:", available_delitos, default=[], key="map_delitos_filter") if available_delitos else []
    with col2_filter:
        dias_semana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dias_selected = st.multiselect("Selecciona días de la semana:", dias_semana, default=[], key="map_dias_filter") if 'dia_semana' in df_denuncias.columns else []
    with col3_filter:
        franjas_horarias = ['Madrugada', 'Mañana', 'Tarde', 'Noche']
        franjas_selected = st.multiselect("Selecciona franja horaria:", franjas_horarias, default=[], key="map_franjas_filter") if 'franja_horaria' in df_denuncias.columns else []

    # --- Aplicar filtros ---
    df_filtrado = df_denuncias.copy()
    if año_selected and 'anio_hecho' in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado['anio_hecho'] == año_selected]
    if delitos_selected and 'delito' in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado['delito'].isin(delitos_selected)]
    if dias_selected and 'dia_semana' in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado['dia_semana'].isin(dias_selected)]
    if franjas_selected and 'franja_horaria' in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado['franja_horaria'].isin(franjas_selected)]

    # Limpiar coordenadas
    if 'latitud' in df_filtrado.columns and 'longitud' in df_filtrado.columns:
        df_filtrado = df_filtrado.dropna(subset=['latitud', 'longitud'])
    else:
        st.error("Las columnas 'latitud' o 'longitud' no se encuentran en los datos. No se pueden mostrar los marcadores de denuncias.")
        return

    if df_filtrado.empty:
        st.warning("No hay datos para mostrar con los filtros seleccionados.")
        return

    # --- Clasificación adulto mayor (simulada) ---
    df_filtrado['grupo_poblacional'] = 'General'
    if 'alcaldia_hecho' in df_filtrado.columns:
        for alcaldia_val in df_filtrado['alcaldia_hecho'].dropna().unique():
            indices = df_filtrado[df_filtrado['alcaldia_hecho'] == alcaldia_val].sample(frac=0.3, random_state=42).index
            df_filtrado.loc[indices, 'grupo_poblacional'] = 'Adulto mayor'

    # --- Mapa base ---
    m = folium.Map(location=[19.4326, -99.1332], zoom_start=10, tiles='CartoDB positron')

    # Agregar denuncias por alcaldía (coropleta)
    if 'alcaldia_hecho' in df_filtrado.columns:
        denuncias_por_alcaldia = df_filtrado['alcaldia_hecho'].value_counts().reset_index()
        denuncias_por_alcaldia.columns = ['alcaldia', 'denuncias']
        alcaldias_mapa_data = alcaldias_gdf.merge(denuncias_por_alcaldia, on='alcaldia', how='left')
        alcaldias_mapa_data['denuncias'] = alcaldias_mapa_data['denuncias'].fillna(0)

        unique_alcaldias_map = alcaldias_mapa_data['alcaldia'].dropna().unique()
        if len(unique_alcaldias_map) > 0:
            cmap = matplotlib.cm.get_cmap('viridis', len(unique_alcaldias_map)) # Using viridis colormap
            colors_rgba = [cmap(i) for i in range(len(unique_alcaldias_map))]
            color_dict = {alcaldia: rgb2hex(colors_rgba[i]) for i, alcaldia in enumerate(unique_alcaldias_map)}

            def style_function(feature):
                alcaldia_feat = feature['properties']['alcaldia']
                return {
                    'fillColor': color_dict.get(alcaldia_feat, '#lightgray'), # Default color
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.7
                }
            folium.GeoJson(
                alcaldias_mapa_data,
                name='Alcaldías por número de denuncias',
                style_function=style_function,
                tooltip=folium.GeoJsonTooltip(fields=['NOMGEO', 'denuncias'], aliases=['Alcaldía:', 'Denuncias:'])
            ).add_to(m)

    # --- Agregar marcadores de denuncias individuales ---
    color_marker = {'Adulto mayor': 'blue', 'General': 'red'}
    if 'grupo_poblacional' in df_filtrado.columns:
        for grupo in df_filtrado['grupo_poblacional'].dropna().unique():
            capa_grupo = folium.FeatureGroup(name=f"Población: {grupo}")
            df_grupo_data = df_filtrado[df_filtrado['grupo_poblacional'] == grupo]
            for _, row in df_grupo_data.iterrows():
                popup_html = f"<b>Delito:</b> {row.get('delito', 'N/A')}<br><b>Alcaldía:</b> {row.get('alcaldia_hecho', 'N/A')}<br><b>Hora:</b> {row.get('hora_hecho', 'N/A')}"
                folium.CircleMarker(
                    location=[row['latitud'], row['longitud']],
                    radius=4, # Slightly larger markers
                    color=color_marker.get(grupo, 'gray'),
                    fill=True,
                    fill_color=color_marker.get(grupo, 'gray'),
                    fill_opacity=0.6,
                    popup=folium.Popup(popup_html, max_width=300)
                ).add_to(capa_grupo)
            capa_grupo.add_to(m)

    # --- Mostrar mapa ---
    folium.LayerControl().add_to(m)
    with st.container(): # Use a container for better layout control if needed
        folium_static(m, width=None, height=600) # Width=None makes it responsive

def display_modulo6():
    st.header("🧩Módulo 6: Buenas Prácticas para Protegerte") # Corregido para consistencia de mayúsculas
    st.markdown("""
    Adoptar hábitos seguros en línea es tu mejor defensa contra el ciberfraude y el phishing. Aquí te presentamos algunas prácticas esenciales:
    """)
    st.divider()

    with st.expander("🔑 Gestión de Contraseñas", expanded=True):
        st.markdown("""
        *   **Usa contraseñas seguras y únicas:** Combina letras mayúsculas, minúsculas, números y símbolos. Evita usar la misma contraseña para múltiples cuentas. Considera un gestor de contraseñas para ayudarte.
        *   **Cámbialas periódicamente:** Especialmente las de tus cuentas más importantes (banco, correo electrónico).
        *   **No las compartas con nadie:** Ni siquiera con amigos o familiares.
        """)

    with st.expander("🛡️ Protección de Dispositivos y Conexiones"):
        st.markdown("""
        *   **Mantén tu software actualizado:** Esto incluye tu sistema operativo (Windows, Android, iOS), navegador web y antivirus. Las actualizaciones suelen corregir fallos de seguridad.
        *   **Usa un antivirus y firewall confiables:** Asegúrate de que estén activos y actualizados.
        *   **Desconfía de redes Wi-Fi públicas:** Evita realizar transacciones bancarias o ingresar información sensible cuando estés conectado a redes Wi-Fi abiertas (aeropuertos, cafeterías). Si es necesario, usa una VPN (Red Privada Virtual).
        *   **Cierra sesión** en tus cuentas cuando termines de usarlas, especialmente en computadoras compartidas.
        """)

    with st.expander("🧐 Navegación y Comunicación Segura"):
        st.markdown("""
        *   **Verifica enlaces antes de hacer clic:** Como aprendiste en el módulo de señales de alerta, revisa siempre la URL.
        *   **No confíes ciegamente en correos o mensajes:** Aplica el escepticismo. Si algo parece sospechoso, probablemente lo sea.
        *   **Activa la autenticación de dos factores (2FA) siempre que sea posible:** Esto añade una capa extra de seguridad, ya que además de tu contraseña, necesitarás un segundo código (generalmente enviado a tu móvil) para acceder a tu cuenta.
        *   **Nunca compartas información sensible por mensaje, correo o llamada no solicitada:** Los bancos y empresas serias no te pedirán datos confidenciales de esta forma.
        *   **Ten cuidado con lo que descargas:** Descarga aplicaciones y archivos solo de fuentes oficiales y confiables.
        *   **Configura la privacidad en tus redes sociales:** Limita quién puede ver tu información personal.
        """)

    with st.expander("🧠 Educación y Prevención Continua"):
        st.markdown("""
        *   **Mantente informado:** Las tácticas de los ciberdelincuentes cambian. Infórmate sobre las nuevas modalidades de fraude.
        *   **Desconfía de ofertas demasiado buenas:** Si algo suena increíble, probablemente no sea real.
        *   **Pide ayuda si tienes dudas:** Si no estás seguro sobre un correo, mensaje o sitio web, pregunta a alguien de confianza o contacta directamente a la entidad involucrada por un canal oficial.
        *   **Reporta los intentos de fraude:** Ayuda a proteger a otros reportando correos de phishing o sitios fraudulentos a las autoridades competentes o a las empresas suplantadas.
        """)

def display_aviso_privacidad():
    st.header("📜 Aviso de Privacidad")
    st.markdown("""
    En **Scrambuster 60+**, la privacidad de tus datos es fundamental. A continuación, te explicamos cómo manejamos la información que pudieras proporcionarnos:
    """)
    with st.container(border=True):
        st.markdown("""
    
Scrambuster 60+ informa que los datos personales recabados a través de esta plataforma se utilizan únicamente con fines académicos, de investigación y concientización social sobre la prevención del fraude digital en personas adultas mayores.

Nuestro proyecto no tiene fines de lucro, no comercializa los datos personales y no los comparte con terceros sin consentimiento previo y explícito.

El tratamiento de los datos se rige bajo los principios establecidos en la LFPDPPP, en particular:

Artículo 1°: Objeto de la Ley (proteger los datos personales en posesión de particulares).

Artículo 3° (Principios): Licitud, consentimiento, información, calidad, finalidad, lealtad, proporcionalidad y responsabilidad.

Artículo 8°: El consentimiento debe ser expreso y previo, salvo excepciones legales.

Artículo 15°: Limitación del uso de datos a las finalidades especificadas en el aviso de privacidad.

Artículo 16:° Prohibición de transferencia de datos sin consentimiento, salvo excepciones previstas en la ley.

Los titulares de los datos pueden ejercer sus derechos ARCO (Acceso, Rectificación, Cancelación y Oposición) o revocar su consentimiento, conforme a los Artículos 22 al 30 de la LFPDPPP.
        """)

def display_evaluacion_final():
    st.header("📝 Evaluación Final") # Corregido para consistencia de mayúsculas
    st.markdown("Es hora de poner a prueba tus conocimientos. Responde las siguientes preguntas para ver cuánto has aprendido sobre la prevención del ciberfraude y phishing.")
    st.divider()
    st.subheader("💡 Ponte a Prueba")
    
    # Pregunta 1
    q1_respuesta = st.radio(
        "¿Cuál de las siguientes acciones es MÁS SEGURA al recibir un correo electrónico inesperado de tu banco?",
        options=[
            "Hacer clic en el enlace del correo para verificar tu cuenta rápidamente.",
            "Llamar al número de teléfono proporcionado en el correo electrónico.",
            "Ignorar el correo y visitar el sitio web oficial del banco escribiendo la URL directamente en el navegador o usando un marcador guardado.",
            "Responder al correo con tu número de cuenta para que puedan verificarlo."
        ],
        index=None, # Para que no haya ninguna opción seleccionada por defecto
        key="q1"
    )

    # Pregunta 2
    q2_respuesta = st.radio(
        "Si recibes un mensaje de texto (SMS) que dice ser de un servicio de paquetería, indicando que tienes un paquete retenido y debes pagar una pequeña tarifa haciendo clic en un enlace, ¿qué deberías hacer?",
        options=[
            "Pagar la tarifa inmediatamente para recibir tu paquete.",
            "Hacer clic en el enlace para ver más detalles sobre el paquete.",
            "Ignorar el mensaje y, si esperas un paquete, rastrearlo directamente en el sitio web oficial de la paquetería.",
            "Llamar al número que envió el SMS para preguntar."
        ],
        index=None,
        key="q2"
    )

    # Pregunta 3
    q3_respuesta = st.radio(
        "¿Qué es la autenticación de dos factores (2FA)?",
        options=[
            "Usar dos contraseñas diferentes para la misma cuenta.",
            "Un método de seguridad que requiere dos formas distintas de verificación para acceder a una cuenta (ej. contraseña y un código enviado a tu teléfono).",
            "Un software antivirus que revisa tus archivos dos veces.",
            "Una forma de verificar tu identidad en dos sitios web diferentes."
        ],
        index=None,
        key="q3"
    )

    st.divider()

    if st.button("Verificar Respuestas"):
        correctas = 0
        total_preguntas = 3

        # Verificar Pregunta 1
        if q1_respuesta and "visitar el sitio web oficial del banco escribiendo la URL directamente" in q1_respuesta:
            st.success("Pregunta 1: ¡Correcto! ✅ Visitar el sitio oficial directamente es la acción más segura.")
            correctas += 1
        elif q1_respuesta:
            st.error("Pregunta 1: Incorrecto. ❌ La opción más segura es ir directamente al sitio oficial del banco.")
        
        # Verificar Pregunta 2
        if q2_respuesta and "Ignorar el mensaje y, si esperas un paquete, rastrearlo directamente en el sitio web oficial" in q2_respuesta:
            st.success("Pregunta 2: ¡Correcto! ✅ Siempre verifica directamente con la fuente oficial.")
            correctas += 1
        elif q2_respuesta:
            st.error("Pregunta 2: Incorrecto. ❌ Hacer clic en enlaces de SMS sospechosos es peligroso.")

        # Verificar Pregunta 3
        if q3_respuesta and "Un método de seguridad que requiere dos formas distintas de verificación" in q3_respuesta:
            st.success("Pregunta 3: ¡Correcto! ✅ La 2FA añade una capa crucial de seguridad.")
            correctas += 1
        elif q3_respuesta:
            st.error("Pregunta 3: Incorrecto. ❌ Revisa la definición de autenticación de dos factores.")

        if not (q1_respuesta and q2_respuesta and q3_respuesta):
            st.warning("Por favor, responde todas las preguntas antes de verificar.")
        else:
            st.subheader(f"Resultado: {correctas} de {total_preguntas} respuestas correctas.")
            if correctas == total_preguntas:
                st.balloons()
                st.markdown("🎉 ¡Felicidades! Has dominado los conceptos clave. 🎉")
            else:
                st.info("Sigue repasando los módulos para mejorar tu conocimiento. ¡Tú puedes!")

def display_socio_scram():
    st.header("🚀 +SocioScram: Tu Aliado Interactivo")
    st.markdown("Herramientas y juegos para fortalecer tu conocimiento y protegerte mejor contra el ciberfraude.")
    st.divider()

    # --- Scrambuster 60+ Session State Initializations (moved here) ---
    if "scrambuster_mensaje_guardado" not in st.session_state:
        st.session_state["scrambuster_mensaje_guardado"] = ""
    if "scrambuster_pregunta_actual" not in st.session_state:
        st.session_state.scrambuster_pregunta_actual = 0
    if "scrambuster_juego_puntaje" not in st.session_state:
        st.session_state.scrambuster_juego_puntaje = 0

    # --- Carga de datos (reutilizando la función de Módulo 5 o una similar) ---
    @st.cache_data
    def load_data_socio():
        try:
            df_denuncias_socio = pd.read_csv("denuncias_filtrado.csv")
            # Asegúrate que el nombre del archivo geojson sea el correcto
            geojson_path_socio = "limite-de-las-alcaldas(1).json" 
            alcaldias_gdf_socio = gpd.read_file(geojson_path_socio)
            
            # Preprocesamiento básico
            if 'NOMGEO' in alcaldias_gdf_socio.columns:
                alcaldias_gdf_socio['alcaldia'] = alcaldias_gdf_socio['NOMGEO'].str.upper()
            if 'alcaldia_hecho' in df_denuncias_socio.columns:
                 df_denuncias_socio['alcaldia_hecho'] = df_denuncias_socio['alcaldia_hecho'].astype(str).str.upper()

            return df_denuncias_socio, alcaldias_gdf_socio
        except FileNotFoundError as e:
            st.error(f"Error al cargar archivos de datos para SocioScram: {e}. Verifica las rutas.")
            return None, None

    df_denuncias, alcaldias_gdf = load_data_socio()

    # --- Sección 1: Detector de URLs Sospechosas (Educativo) ---
    st.subheader("🔍 Detector de URLs Sospechosas (Educativo)")
    st.markdown("Ingresa una URL para identificar posibles señales de alerta. Esta herramienta es para fines educativos y no garantiza la detección de todas las URLs maliciosas.")

    url_input = st.text_input("URL a analizar:", key="socio_url_input")
    if st.button("Analizar URL", key="socio_url_button"):
        if url_input:
            st.markdown("--- \n**Análisis de la URL:**")
            warnings_url = []
            recommendations_url = [
                "**Siempre verifica el candado (HTTPS):** Asegúrate de que la conexión sea segura.",
                "**Revisa el dominio principal:** ¿Es el sitio oficial que esperas?",
                "**Cuidado con errores ortográficos:** En el nombre del dominio o en el contenido.",
                "**Desconfía de URLs acortadas en contextos inesperados.**",
                "**No ingreses datos sensibles si tienes dudas:** Contacta a la entidad por un medio oficial."
            ]

            if "http://" in url_input and "https://" not in url_input:
                warnings_url.append("⚠️ **Conexión no segura (HTTP):** Evita ingresar información sensible.")
            if "https://" not in url_input:
                 warnings_url.append("ℹ️ **Verifica HTTPS:** Asegúrate de que la URL final muestre 'https://'.")

            suspicious_tlds = [".xyz", ".tk", ".top", ".loan", ".club", ".info", ".biz"]
            for tld in suspicious_tlds:
                if url_input.endswith(tld) or tld+"/" in url_input or tld+"?" in url_input:
                    warnings_url.append(f"⚠️ **Dominio ({tld}) a menudo usado para spam/phishing:** Procede con cautela.")
                    break
            
            try:
                domain_part_match = re.search(r'(?:https?://)?([^/]+)', url_input)
                if domain_part_match:
                    domain_part = domain_part_match.group(1)
                    if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain_part):
                        warnings_url.append("⚠️ **Uso de Dirección IP en lugar de Nombre de Dominio:** Puede ser una señal de alerta.")
                    if domain_part.count('.') > 3:
                        warnings_url.append("⚠️ **Múltiples Subdominios:** Revisa cuidadosamente el dominio principal.")
            except Exception:
                pass # Silently ignore regex errors for malformed URLs

            if not warnings_url:
                st.success("✅ No se detectaron señales de alerta obvias con estas comprobaciones básicas. ¡Sigue vigilante!")
            else:
                for warning_msg in warnings_url:
                    st.warning(warning_msg)
            
            st.markdown("--- \n**Recomendaciones Generales al Navegar:**")
            for rec_msg in recommendations_url:
                st.markdown(f"- {rec_msg}")
        else:
            st.info("Por favor, ingresa una URL para analizar.")
    st.markdown("---")

    # # --- Sección 2: Juego Interactivo ---
    # st.subheader("🎮 Juego Interactivo: ¡Detecta el Engaño!")
    # phishing_scenarios_game = [
    #     {"id": "sg1", "scenario": "Email: '¡URGENTE! Actividad sospechosa en su cuenta Netflix. Haga clic aquí: netflix-support-logins.com para verificar.'", "q": "¿Es phishing?", "ans": "Sí", "exp": "Dominio falso y urgencia son señales."},
    #     {"id": "sg2", "scenario": "SMS: 'BBVA: Compra aprobada por $5,800. Si no la reconoce, llame al 55-1234-5678.'", "q": "¿Qué harías?", "ans": "No llamar, verificar en la app oficial del banco.", "exp": "No confíes en números de SMS; ve a fuentes oficiales."}
    # ]
    # for item in phishing_scenarios_game:
    #     st.markdown(f"**Escenario:** {item['scenario']}")
    #     user_choice = st.radio(item["q"], ["Sí", "No", "No llamar, verificar en la app oficial del banco."], key=item["id"], index=None)
    #     if st.button("Verificar", key=f"b_{item['id']}"):
    #         if user_choice == item["ans"]:
    #             st.success(f"¡Correcto! {item['exp']}")
    #         elif user_choice is not None:
    #             st.error(f"Incorrecto. La mejor acción es: {item['ans']}. {item['exp']}")
    #         else:
    #             st.warning("Selecciona una opción.")
    # st.markdown("---")

    # # --- Sección 3: "Modelo de Probabilidad" (Análisis de Frecuencias Históricas) ---
    # st.subheader("📊 ¿Cuándo y Dónde? Patrones de Fraude (Basado en Datos Históricos)")
    # st.markdown("Este análisis muestra tendencias basadas en datos históricos de denuncias y no son predicciones exactas.")
    # if df_denuncias is not None:
    #     # Análisis por Hora
    #     if 'hora_hecho' in df_denuncias.columns:
    #         df_denuncias['hora_simple'] = pd.to_datetime(df_denuncias['hora_hecho'], format='%H:%M:%S', errors='coerce').dt.hour
    #         hourly_risk = df_denuncias['hora_simple'].value_counts().sort_index().reset_index()
    #         hourly_risk.columns = ['Hora', 'Número de Denuncias']
    #         if not hourly_risk.empty:
    #             fig_hora_socio = px.bar(hourly_risk, x='Hora', y='Número de Denuncias', title="Distribución de Denuncias por Hora")
    #             st.plotly_chart(fig_hora_socio, use_container_width=True)

    #     # Análisis por Alcaldía
    #     if 'alcaldia_hecho' in df_denuncias.columns:
    #         alcaldia_risk = df_denuncias['alcaldia_hecho'].value_counts().reset_index()
    #         alcaldia_risk.columns = ['Alcaldía', 'Número de Denuncias']
    #         if not alcaldia_risk.empty:
    #             fig_alcaldia_socio = px.bar(alcaldia_risk.head(10), x='Alcaldía', y='Número de Denuncias', title="Top 10 Alcaldías por Denuncias")
    #             st.plotly_chart(fig_alcaldia_socio, use_container_width=True)
    # else:
    #     st.warning("Datos de denuncias no disponibles para el análisis de patrones.")
    # st.markdown("---")

    # # --- Sección 4: Mapa Interactivo de Alcaldías Afectadas ---
    # st.subheader("🗺️ Mapa de Incidencia General de Fraudes por Alcaldía")
    # if df_denuncias is not None and alcaldias_gdf is not None and 'alcaldia_hecho' in df_denuncias.columns and 'alcaldia' in alcaldias_gdf.columns:
    #     denuncias_agg_map = df_denuncias['alcaldia_hecho'].value_counts().reset_index()
    #     denuncias_agg_map.columns = ['alcaldia', 'total_denuncias']
        
    #     map_data_socio = alcaldias_gdf.merge(denuncias_agg_map, on='alcaldia', how='left')
    #     map_data_socio['total_denuncias'] = map_data_socio['total_denuncias'].fillna(0)

    #     m_socio = folium.Map(location=[19.4326, -99.1332], zoom_start=10, tiles='CartoDB positron')
        
    #     if not map_data_socio.empty and 'total_denuncias' in map_data_socio.columns:
    #         folium.Choropleth(
    #             geo_data=map_data_socio.to_json(), # Convert GeoDataFrame to GeoJSON string
    #             name='Choropleth',
    #             data=map_data_socio,
    #             columns=['alcaldia', 'total_denuncias'],
    #             key_on='feature.properties.alcaldia',
    #             fill_color='YlOrRd',
    #             fill_opacity=0.7,
    #             line_opacity=0.2,
    #             legend_name='Total de Denuncias Reportadas Históricamente'
    #         ).add_to(m_socio)
    #         folium.LayerControl().add_to(m_socio)
    #         folium_static(m_socio, width=None, height=500)
    #     else:
    #         st.warning("No hay suficientes datos para generar el mapa coroplético.")
    # else:
    #     st.warning("Datos no disponibles para generar el mapa interactivo de SocioScram.")

    # --- Contenido de Scrambuster 60+ integrado en SocioScram ---
    st.divider()
    st.subheader("🛡️ Scrambuster 60+: Detector de Mensajes Sospechosos")
    st.markdown("Copia aquí el mensaje que recibiste y lo analizaremos por ti.")
    
    palabras_peligrosas = [
        "urgente", "clic aquí", "premio", "cuenta bloqueada", "verifica", "regalo",
        "bonificación", "transferencia", "datos personales", "confirmar tu identidad",
        "has sido seleccionado", "seguridad bancaria", "problemas con tu cuenta"
    ]

    mensaje_sb = st.text_area("✉️ Escribe o pega el mensaje aquí (Scrambuster):", value=st.session_state["scrambuster_mensaje_guardado"], height=150, key="scrambuster_text_area")

    col1_sb, col2_sb = st.columns(2)
    with col1_sb:
        analizar_sb = st.button("🔍 Analizar mensaje (Scrambuster)", key="scrambuster_analizar_button")
    with col2_sb:
        limpiar_sb = st.button("🧹 Limpiar mensaje (Scrambuster)", key="scrambuster_limpiar_button")

    if analizar_sb:
        st.session_state["scrambuster_mensaje_guardado"] = mensaje_sb
        if mensaje_sb.strip() == "":
            st.warning("⚠️ Por favor, escribe o pega un mensaje para analizar.")
        else:
            es_malicioso_sb = any(p in mensaje_sb.lower() for p in palabras_peligrosas)
            if es_malicioso_sb:
                st.markdown("""
                <div style='padding:15px; background-color:#ffe6e6; border-radius:10px'>
                    <h4 style='color:#b30000'>🚨 ¡Alerta! Mensaje posiblemente malicioso (Scrambuster)</h4>
                    <p>No hagas clic en enlaces ni compartas datos personales.</p>
                    <ul>
                        <li>✅ No respondas al mensaje.</li>
                        <li>🔒 Cambia tus contraseñas si ya diste información.</li>
                        <li>📞 Reporta el incidente a tu banco o institución correspondiente.</li>
                        <li>🛡️ Considera instalar herramientas de seguridad digital.</li>
                        <li>📚 Infórmate más en este curso para prevenir fraudes futuros.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='padding:15px; background-color:#e6ffe6; border-radius:10px'>
                    <h4 style='color:#267326'>✅ Este mensaje parece confiable (Scrambuster)</h4>
                    <p>Aun así, actúa con precaución.</p>
                </div>
                """, unsafe_allow_html=True)

    if limpiar_sb:
        st.session_state["scrambuster_mensaje_guardado"] = ""
        st.info("🧹 El mensaje ha sido borrado. Puedes escribir uno nuevo.")
        st.rerun() # Ensure text area updates immediately

    st.markdown("---")
    st.markdown("##### 🎮 Juego Scrambuster: ¿Este mensaje es malicioso?")
    mensajes_juego_sb = [
        ("Has ganado un premio, haz clic aquí para reclamar.", "Malicioso"),
        ("Hola, ¿quieres salir a caminar hoy?", "No malicioso"),
        ("Verifica tu cuenta para evitar bloqueos.", "Malicioso"),
        ("Te espero a las 5 en el parque.", "No malicioso")
    ]

    if st.session_state.scrambuster_pregunta_actual < len(mensajes_juego_sb):
        mensaje_j_sb, respuesta_correcta_sb = mensajes_juego_sb[st.session_state.scrambuster_pregunta_actual]
        st.markdown(f"**Mensaje (Juego Scrambuster):** {mensaje_j_sb}")
        col_j1_sb, col_j2_sb = st.columns(2)
        with col_j1_sb:
            if st.button("🚨 Malicioso", key="scrambuster_juego_malicioso_button"):
                if respuesta_correcta_sb == "Malicioso":
                    st.success("✅ Correcto")
                    st.session_state.scrambuster_juego_puntaje += 1
                else:
                    st.error("❌ Incorrecto")
        with col_j2_sb:
            if st.button("✅ No malicioso", key="scrambuster_juego_no_malicioso_button"):
                if respuesta_correcta_sb == "No malicioso":
                    st.success("✅ Correcto")
                    st.session_state.scrambuster_juego_puntaje += 1
                else:
                    st.error("❌ Incorrecto")
        
        if st.button("Siguiente pregunta", key="scrambuster_juego_siguiente_button"):
            st.session_state.scrambuster_pregunta_actual += 1
            st.rerun()
    else:
        st.success(f"🎉 Juego Scrambuster terminado. Puntaje: {st.session_state.scrambuster_juego_puntaje}/{len(mensajes_juego_sb)}")
        if st.button("Reiniciar juego", key="scrambuster_juego_reiniciar_button"):
            st.session_state.scrambuster_pregunta_actual = 0
            st.session_state.scrambuster_juego_puntaje = 0
            st.rerun()

    st.markdown("---")
    st.markdown("##### 📍 Predicción de fraude por alcaldía (Scrambuster)")
    alcaldias_posibles = [
        'CUAUHTEMOC', 'LA MAGDALENA CONTRERAS', 'BENITO JUAREZ', 'IZTAPALAPA', 
        'GUSTAVO A. MADERO', 'MIGUEL HIDALGO', 'COYOACAN', 'TLAHUAC', 
        'CUAJIMALPA DE MORELOS', 'TLALPAN', 'MILPA ALTA', 'VENUSTIANO CARRANZA', 
        'AZCAPOTZALCO', 'ALVARO OBREGON', 'XOCHIMILCO', 'CDMX'
    ]
    horas_numericas = list(range(0, 24))
    hora_dict = {f"{h:02d}:00": h for h in horas_numericas}
    
    alcaldia_select_sb = st.selectbox("Selecciona una alcaldía (Scrambuster):", alcaldias_posibles, key="scrambuster_alcaldia_selectbox")
    hora_select_sb = st.selectbox("Selecciona una hora (Scrambuster):", list(hora_dict.keys()), key="scrambuster_hora_selectbox")
    
    np.random.seed(42)
    data_simulada_sb = pd.DataFrame({
        "alcaldia_hecho": np.random.choice(alcaldias_posibles, 5000),
        "hora": np.random.choice(horas_numericas, 5000),
        "fraude_ocurrido": np.random.binomial(1, 0.2, 5000)
    })
    filtrado_data_sb = data_simulada_sb[(data_simulada_sb["alcaldia_hecho"] == alcaldia_select_sb) & (data_simulada_sb["hora"] == hora_dict[hora_select_sb])]
    probabilidad_calculada_sb = filtrado_data_sb["fraude_ocurrido"].mean() if not filtrado_data_sb.empty else 0
    st.metric("Probabilidad estimada de fraude (Scrambuster)", f"{probabilidad_calculada_sb*100:.1f}%")
    
    def explicar_prediccion_scrambuster(filtrado_local, probabilidad_local):
        total = len(filtrado_local)
        casos_fraude = filtrado_local["fraude_ocurrido"].sum()
        return f"<div style='background-color:#f9f9f9; padding:10px; border-radius:10px; border-left:5px solid #4CAF50;'><b>¿Cómo se calcula?</b><br>De un total de <b>{total}</b> reportes simulados para esa alcaldía y hora, <b>{casos_fraude}</b> fueron fraudes reales.<br>Esto da una estimación de <b>{probabilidad_local*100:.1f}%</b>.</div>"
    st.markdown(explicar_prediccion_scrambuster(filtrado_data_sb, probabilidad_calculada_sb), unsafe_allow_html=True)
    
    conteo_fraude_sb = data_simulada_sb.groupby("alcaldia_hecho")["fraude_ocurrido"].mean().reset_index()
    conteo_fraude_sb.columns = ["Alcaldía", "Probabilidad"]
    chart_altair_sb = alt.Chart(conteo_fraude_sb).mark_bar().encode(x=alt.X("Alcaldía", sort="-y"), y=alt.Y("Probabilidad", title="Probabilidad de fraude"), color="Probabilidad", tooltip=["Alcaldía", "Probabilidad"]).properties(height=400, title="Probabilidad promedio de fraude por alcaldía (Scrambuster)")
    st.altair_chart(chart_altair_sb, use_container_width=True)
    
    # La sección del mapa de reportes de Scrambuster ha sido eliminada.
    st.markdown("---")
    st.markdown("> Esta aplicación tiene fines **educativos y sin fines de lucro**. Los mensajes ingresados no se almacenan ni se comparten públicamente. Scrambuster 60+ protege tu privacidad y no expone tus datos.")
    st.caption("🔐 Scrambuster 60+ | Prevención de fraudes digitales para adultos mayores")
    # --- Fin del contenido de Scrambuster 60+ integrado ---

# --- Configuración del Menú y Mapeo a Funciones ---
PAGE_CONFIG = {
    "🏠Inicio": display_inicio,
    "🧩Módulo 1: ¿Qué es el ciberfraude?": display_modulo1,
    "🧩Módulo 2: ¿Qué es el phishing?": display_modulo2,
    "🧩Módulo 3: ¿Por qué los adultos mayores son vulnerables?": display_modulo3,
    "🧩Módulo 4: Señales de alerta": display_modulo4,
    "🧩Módulo 5: Casos reales y estadísticas": display_modulo5,
    "🧩Módulo 6: Buenas prácticas para protegerte": display_modulo6,
    "🧩Evaluación final": display_evaluacion_final,
    "+SocioScram": display_socio_scram,
    "Aviso de privacidad": display_aviso_privacidad
}

# --- Barra Lateral (Sidebar) ---
st.sidebar.title("Navegación del Curso")
# Descomenta la siguiente línea y reemplaza "path/to/your/logo.png" con la ruta a tu imagen de logo si tienes una:
# st.sidebar.image("path/to/your/logo.png", width=100) 

menu_selection = st.sidebar.radio("Elige una sección:", list(PAGE_CONFIG.keys()))

# --- Mostrar Contenido de la Página Seleccionada ---
if menu_selection in PAGE_CONFIG:
    PAGE_CONFIG[menu_selection]()
else:
    st.error("Página no encontrada. Por favor, selecciona una opción válida del menú.")
