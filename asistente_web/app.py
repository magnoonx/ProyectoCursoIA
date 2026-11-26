"""
Servidor Web Local - Asistente de IA para Ofimática y Gestión Administrativa
Entorno 100% Offline para el Laboratorio de Capacitación
"""
import os
import sys
import json
import re
import time
import socket
import requests
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_from_directory
from pypdf import PdfReader
def obtener_ip_local():
    """Detecta la IP local de este equipo en la red WiFi/LAN del aula."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


# Importar transcriptor local de Whisper
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from transcriptor_whisper.transcribir import TranscriptorOficina

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS_DIR = os.path.join(BASE_DIR, "datos_de_prueba")
AUDIOS_DIR = os.path.join(DATOS_DIR, "01_audios_reuniones")
PDFS_DIR = os.path.join(DATOS_DIR, "02_documentos_pdf")
TABLAS_DIR = os.path.join(DATOS_DIR, "03_tablas_datos")
UPLOADS_DIR = os.path.join(BASE_DIR, "asistente_web", "uploads")

os.makedirs(UPLOADS_DIR, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOADS_DIR
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

# Instancia global de Whisper (carga bajo demanda)
transcriptor_global = None

def get_transcriptor():
    global transcriptor_global
    if transcriptor_global is None:
        transcriptor_global = TranscriptorOficina(model_size="base")
    return transcriptor_global

# Endpoints de LLM configurables (llama-server o LM Studio)
LLM_SERVERS = [
    {"nombre": "llama-server (Puerto 8081)", "url": "http://127.0.0.1:8081/v1/chat/completions"},
    {"nombre": "LM Studio (Puerto 1234)", "url": "http://127.0.0.1:1234/v1/chat/completions"},
    {"nombre": "Ollama (Puerto 11434)", "url": "http://127.0.0.1:11434/v1/chat/completions"}
]

def detectar_servidor_activo():
    """Detecta rápidamente cuál servidor LLM está encendido y el modelo cargado."""
    for srv in LLM_SERVERS:
        try:
            r = requests.get(srv["url"].replace("/chat/completions", "/models"), timeout=1.2)
            if r.status_code == 200:
                srv_copy = dict(srv)
                # Obtener el id del modelo cargado dinámicamente
                try:
                    data = r.json()
                    modelos = data.get("data", [])
                    if modelos and isinstance(modelos, list):
                        srv_copy["modelo_id"] = modelos[0].get("id", "default")
                    else:
                        srv_copy["modelo_id"] = "qwen2.5-3b-instruct"
                except Exception:
                    srv_copy["modelo_id"] = "qwen2.5-3b-instruct"
                return srv_copy
        except Exception:
            continue
    return None

def limpiar_pensamiento(texto):
    """
    Elimina bloques de pensamiento interno (<think>...</think> o <thought>...</thought>)
    típicos de modelos de razonamiento (DeepSeek-R1, QwQ, etc.) para entregar una respuesta
    ejecutiva limpia, directa e instantánea.
    """
    if not texto:
        return ""
    # Eliminar bloques cerrados de razonamiento
    limpio = re.sub(r'<(think|thought)>.*?</\1>', '', texto, flags=re.DOTALL).strip()
    # Si quedó alguna etiqueta huérfana
    if '<think>' in limpio or '<thought>' in limpio:
        limpio = re.sub(r'</?(think|thought)>', '', limpio).strip()
    return limpio


def llamar_llm(mensajes, temperatura=0.3, max_tokens=500):
    """
    Intenta comunicarse con el servidor local de LLM activo.
    Detecta primero el servidor disponible para evitar falsos negativos.
    """
    srv_activo = detectar_servidor_activo()
    if not srv_activo:
        return {
            "exito": False,
            "contenido": (
                "[AVISO: Servidor LLM no detectado]\n\n"
                "El servidor local de Qwen 2.5 3B no está respondiendo en los puertos 8080 (llama.cpp) ni 1234 (LM Studio).\n\n"
                "Para activar las respuestas con IA real:\n"
                "1. Inicie 'motor_llm\\iniciar_servidor_llm.bat', o\n"
                "2. Abra LM Studio y haga clic en 'Start Local Server' en el puerto 1234.\n\n"
                "A continuación se presenta una estructura base de demostración para su requerimiento:\n\n"
                "--------------------------------------------------\n"
                "DOCUMENTO MODELO PRECONFIGURADO:\n"
                "1. Destinatario: Dirección Ejecutiva\n"
                "2. Asunto: Gestión y Seguimiento de Tareas Ofimáticas\n"
                "3. Contenido: Se remite la información requerida con estricto apego a las políticas institucionales.\n"
                "4. Compromisos: Entrega de soportes antes del cierre de la jornada laboral."
            ),
            "servidor_usado": "Simulador Offline (Servidor LLM apagado)"
        }

    # Suprimir modo razonamiento (<think>) para agilizar la generación en CPU
    mensajes_optimizados = []
    directiva_no_think = "\n\n[DIRECTIVA: Responde directamente de forma ejecutiva y concisa. NO uses modo razonamiento interno ni generes etiquetas <think>.]"
    tiene_sistema = False
    for m in mensajes:
        m_copy = dict(m)
        if m_copy.get("role") == "system":
            m_copy["content"] = m_copy.get("content", "") + directiva_no_think
            tiene_sistema = True
        mensajes_optimizados.append(m_copy)
    if not tiene_sistema and mensajes_optimizados:
        mensajes_optimizados.insert(0, {"role": "system", "content": directiva_no_think.strip()})

    modelo_a_usar = srv_activo.get("modelo_id", "qwen2.5-3b-instruct")
    payload = {
        "model": modelo_a_usar,
        "messages": mensajes_optimizados,
        "temperature": temperatura,
        "max_tokens": max_tokens,
        "stream": False
    }

    try:
        resp = requests.post(srv_activo["url"], json=payload, timeout=180)
        if resp.status_code == 200:
            data = resp.json()
            contenido_raw = data["choices"][0]["message"]["content"]
            contenido = limpiar_pensamiento(contenido_raw)
            return {
                "exito": True,
                "contenido": contenido,
                "servidor_usado": srv_activo["nombre"]
            }
        else:
            return {
                "exito": False,
                "contenido": f"[Error {resp.status_code} desde {srv_activo['nombre']}]: {resp.text}",
                "servidor_usado": srv_activo["nombre"]
            }
    except requests.exceptions.Timeout:
        return {
            "exito": False,
            "contenido": (
                f"[AVISO: Tiempo de espera agotado]\n\n"
                f"El servidor {srv_activo['nombre']} está activo pero tardó más de 180s en generar la respuesta completa en CPU.\n\n"
                "Sugerencia: Para acelerar la inferencia en CPU, prueba con un texto de audio o documento más breve, "
                "o ajusta el número de hilos en 'iniciar_servidor_llm.bat'."
            ),
            "servidor_usado": "Timeout en CPU"
        }
    except Exception as e:
        return {
            "exito": False,
            "contenido": f"[Error de comunicación con {srv_activo['nombre']}]: {str(e)}",
            "servidor_usado": srv_activo["nombre"]
        }

# ================= RUTAS PRINCIPALES =================

@app.route('/api/conexion')
def api_conexion():
    """Devuelve la IP local del servidor para instrucciones de conexion movil."""
    ip = obtener_ip_local()
    return jsonify({
        "ip_local": ip,
        "url_movil": f"http://{ip}:5000",
        "modo": "Red Local (Accesible desde celulares en la misma WiFi)"
    })


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    """Verifica el estado del motor LLM, Whisper y archivos de prueba"""
    srv = detectar_servidor_activo()
    llm_activo = srv is not None
    if srv:
        m_id = srv.get("modelo_id", "")
        if "/" in m_id:
            m_id = m_id.split("/")[-1]
        servidor_detectado = f"{srv['nombre']} [{m_id}]" if m_id else srv["nombre"]
    else:
        servidor_detectado = None

    whisper_listo = os.path.exists(os.path.join(BASE_DIR, "transcriptor_whisper", "modelos"))
    
    # Conteo de archivos de prueba
    audios = len(os.listdir(AUDIOS_DIR)) if os.path.exists(AUDIOS_DIR) else 0
    pdfs = len(os.listdir(PDFS_DIR)) if os.path.exists(PDFS_DIR) else 0
    tablas = len(os.listdir(TABLAS_DIR)) if os.path.exists(TABLAS_DIR) else 0

    return jsonify({
        "llm_conectado": llm_activo,
        "servidor_llm": servidor_detectado or "Desconectado (Inicie LM Studio o llama-server)",
        "whisper_disponible": whisper_listo,
        "modelo_sugerido": "Qwen 2.5 3B Instruct (Q4_K_M)",
        "archivos_prueba": {
            "audios": audios,
            "pdfs": pdfs,
            "tablas": tablas
        }
    })

@app.route('/api/datos_prueba/listar')
def listar_datos_prueba():
    """Lista todos los archivos de prueba disponibles para carga en un clic"""
    audios = [f for f in os.listdir(AUDIOS_DIR) if f.endswith(('.wav', '.mp3'))] if os.path.exists(AUDIOS_DIR) else []
    pdfs = [f for f in os.listdir(PDFS_DIR) if f.endswith('.pdf')] if os.path.exists(PDFS_DIR) else []
    tablas = [f for f in os.listdir(TABLAS_DIR) if f.endswith(('.xlsx', '.csv'))] if os.path.exists(TABLAS_DIR) else []
    
    return jsonify({
        "audios": audios,
        "pdfs": pdfs,
        "tablas": tablas
    })

@app.route('/api/datos_prueba/cargar/<tipo>/<filename>')
def cargar_dato_prueba(tipo, filename):
    """Permite descargar o inspeccionar un archivo de prueba"""
    if tipo == "audios":
        carpeta = AUDIOS_DIR
    elif tipo == "pdfs":
        carpeta = PDFS_DIR
    elif tipo == "tablas":
        carpeta = TABLAS_DIR
    else:
        return jsonify({"error": "Tipo no válido"}), 400
        
    return send_from_directory(carpeta, filename)

# ================= MÓDULO 1: REDACCIÓN EJECUTIVA =================

@app.route('/api/redactar', methods=['POST'])
def redactar_documento():
    data = request.json or {}
    tipo_doc = data.get("tipo", "Memorando Interno")
    destinatario = data.get("destinatario", "Equipo de Trabajo")
    remitente = data.get("remitente", "Coordinación Administrativa")
    tono = data.get("tono", "Formal Institucional")
    instrucciones = data.get("instrucciones", "")

    if not instrucciones.strip():
        return jsonify({"error": "Debe proporcionar los puntos clave o instrucciones del documento."}), 400

    prompt_sistema = (
        "Eres un asistente ejecutivo de alta dirección y redactor corporativo experto en ofimática. "
        "Tu misión es redactar comunicaciones institucionales impecables en español, utilizando estructura formal, "
        "ortografía perfecta, claridad y cortesía profesional."
    )

    prompt_usuario = (
        f"Por favor redacta un(a) {tipo_doc} oficial con las siguientes especificaciones:\n"
        f"- Remitente: {remitente}\n"
        f"- Destinatario: {destinatario}\n"
        f"- Tono de comunicación: {tono}\n"
        f"- Puntos clave e instrucciones:\n{instrucciones}\n\n"
        f"Estructura requerida:\n"
        f"1. Encabezado institucional completo (Lugar, Fecha, Para, De, Asunto).\n"
        f"2. Saludo protocolario.\n"
        f"3. Cuerpo del mensaje dividido en párrafos claros o viñetas numeradas.\n"
        f"4. Llamado a la acción o compromisos esperados con plazos.\n"
        f"5. Despedida formal y espacio de firma."
    )

    mensajes = [
        {"role": "system", "content": prompt_sistema},
        {"role": "user", "content": prompt_usuario}
    ]

    res = llamar_llm(mensajes, temperatura=0.25)
    return jsonify(res)

# ================= MÓDULO 2: TRANSCRIPCIÓN Y ACTAS DE REUNIÓN =================

@app.route('/api/transcribir_audio', methods=['POST'])
def procesar_audio():
    archivo = request.files.get('audio')
    audio_muestra = request.form.get('audio_muestra')
    generar_acta = request.form.get('generar_acta', 'true').lower() == 'true'

    ruta_audio = None
    if archivo and archivo.filename:
        ruta_audio = os.path.join(UPLOADS_DIR, archivo.filename)
        archivo.save(ruta_audio)
    elif audio_muestra:
        ruta_audio = os.path.join(AUDIOS_DIR, audio_muestra)

    if not ruta_audio or not os.path.exists(ruta_audio):
        return jsonify({"error": "No se recibió ningún archivo de audio válido."}), 400

    objetivo = request.form.get('objetivo', 'acta_completa')

    try:
        ts = get_transcriptor()
        res_transcripcion = ts.transcribir_archivo(ruta_audio)
        texto_transcrito = res_transcripcion["transcripcion_continua"]

        resultado_ia = None
        if texto_transcrito and objetivo != "solo_texto":
            if objetivo == "correo_formal":
                prompt_sistema = (
                    "Eres un asistente ejecutivo de alta dirección. Tu tarea es transformar notas de voz o dictados orales "
                    "en un correo electrónico corporativo formal, elegante, sin rodeos y listo para enviar."
                )
                prompt_usuario = (
                    "A partir de la siguiente nota de voz, redacta un CORREO ELECTRÓNICO FORMAL DE NEGOCIOS:\n\n"
                    "- Asunto sugerido conciso y profesional.\n"
                    "- Saludo formal.\n"
                    "- Cuerpo del mensaje bien estructurado, eliminando titubeos o expresiones informales.\n"
                    "- Compromisos, peticiones o plazos claros.\n"
                    "- Despedida formal y firma.\n\n"
                    f"--- NOTA DE VOZ TRANSCRITA ---\n{texto_transcrito}"
                )
            elif objetivo == "resumen_tareas":
                prompt_sistema = (
                    "Eres un coordinador administrativo experto en gestión de tareas. "
                    "Extraes instrucciones operativas de notas de voz y las organizas en una lista de tareas estructurada."
                )
                prompt_usuario = (
                    "A partir de la siguiente nota de voz, extrae una LISTA DE TAREAS Y ACCIONES PRIORITARIAS:\n\n"
                    "1. Resumen de la instrucción en 1 frase.\n"
                    "2. Lista de Tareas Clave (Checklist):\n"
                    "   - [ ] Tarea / Responsable / Fecha límite mencionada\n"
                    "3. Personas o áreas involucradas.\n\n"
                    f"--- NOTA DE VOZ TRANSCRITA ---\n{texto_transcrito}"
                )
            else: # acta_completa por defecto
                prompt_sistema = (
                    "Eres un secretario general y experto en actas de junta corporativa. "
                    "Transformas transcripciones de reuniones orales en actas de reunión estructuradas, precisas y ejecutivas."
                )
                prompt_usuario = (
                    "A partir de la siguiente transcripción de una reunión de oficina o nota de voz, genera un ACTA OFICIAL con el siguiente formato:\n\n"
                    "1. INFORMACIÓN GENERAL: Título de la reunión, fecha estimada, objetivo principal.\n"
                    "2. PARTICIPANTES DETECTADOS: Lista de personas mencionadas y sus roles.\n"
                    "3. TEMAS Y DISCUSIONES: Resumen de los puntos tratados.\n"
                    "4. ACUERDOS Y DECISIONES TOMADAS: Resoluciones acordadas.\n"
                    "5. TABLA DE COMPROMISOS (Markdown):\n"
                    "| Responsable | Tarea / Compromiso | Plazo / Fecha Límite |\n\n"
                    f"--- NOTA DE VOZ / REUNIÓN TRANSCRITA ---\n{texto_transcrito}"
                )

            tokens_limite = 500
            if objetivo == "correo_formal":
                tokens_limite = 350
            elif objetivo == "resumen_tareas":
                tokens_limite = 350

            mensajes = [
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario}
            ]

            resultado_ia = llamar_llm(mensajes, temperatura=0.2, max_tokens=tokens_limite)

        return jsonify({
            "exito": True,
            "transcripcion": res_transcripcion,
            "acta": resultado_ia,
            "objetivo": objetivo
        })
    except Exception as e:
        return jsonify({"error": f"Error procesando audio: {str(e)}"}), 500

# ================= MÓDULO 3: ANÁLISIS DE DOCUMENTOS (PDF) =================

@app.route('/api/analizar_pdf', methods=['POST'])
def analizar_pdf():
    archivo = request.files.get('pdf')
    pdf_muestra = request.form.get('pdf_muestra')
    consulta = request.form.get('consulta', 'Extrae los puntos clave, obligaciones y montos de este documento.')

    ruta_pdf = None
    if archivo and archivo.filename:
        ruta_pdf = os.path.join(UPLOADS_DIR, archivo.filename)
        archivo.save(ruta_pdf)
    elif pdf_muestra:
        ruta_pdf = os.path.join(PDFS_DIR, pdf_muestra)

    if not ruta_pdf or not os.path.exists(ruta_pdf):
        return jsonify({"error": "No se encontró el documento PDF especificado."}), 400

    try:
        # Extraer texto con pypdf
        reader = PdfReader(ruta_pdf)
        texto_completo = []
        for i, page in enumerate(reader.pages):
            t = page.extract_text()
            if t:
                texto_completo.append(f"--- PÁGINA {i+1} ---\n{t}")
        
        texto_doc = "\n\n".join(texto_completo)
        if not texto_doc.strip():
            return jsonify({"error": "No se pudo extraer texto del documento PDF."}), 400

        # Enviar a Qwen 2.5
        prompt_sistema = (
            "Eres un analista de gestión documental y legal administrativo. "
            "Examinas documentos oficiales, contratos, resoluciones y facturas, respondiendo con rigor y exactitud a las consultas."
        )
        prompt_usuario = (
            f"Analiza el siguiente documento administrativo y responde a la consulta del usuario.\n\n"
            f"DOCUMENTO COMPLETO:\n{texto_doc[:8000]}\n\n"
            f"CONSULTA DEL ASISTENTE ADMINISTRATIVO:\n{consulta}"
        )
        mensajes = [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ]
        res_llm = llamar_llm(mensajes, temperatura=0.2)

        return jsonify({
            "exito": True,
            "total_paginas": len(reader.pages),
            "texto_extraido_muestra": texto_doc[:500] + ("..." if len(texto_doc) > 500 else ""),
            "respuesta": res_llm
        })
    except Exception as e:
        return jsonify({"error": f"Error al procesar el PDF: {str(e)}"}), 500

# ================= MÓDULO 4: ANÁLISIS DE HOJAS DE CÁLCULO (EXCEL / CSV) =================

@app.route('/api/analizar_tabla', methods=['POST'])
def analizar_tabla():
    archivo = request.files.get('tabla')
    tabla_muestra = request.form.get('tabla_muestra')
    pregunta = request.form.get('pregunta', 'Realiza un diagnóstico ejecutivo y resume los principales hallazgos de esta tabla.')

    ruta_tabla = None
    if archivo and archivo.filename:
        ruta_tabla = os.path.join(UPLOADS_DIR, archivo.filename)
        archivo.save(ruta_tabla)
    elif tabla_muestra:
        ruta_tabla = os.path.join(TABLAS_DIR, tabla_muestra)

    if not ruta_tabla or not os.path.exists(ruta_tabla):
        return jsonify({"error": "No se encontró el archivo de datos especificado."}), 400

    try:
        # Cargar con Pandas
        if ruta_tabla.endswith('.csv'):
            df = pd.read_csv(ruta_tabla)
        else:
            df = pd.read_excel(ruta_tabla)

        total_filas, total_cols = df.shape
        columnas = list(df.columns)
        
        # Muestra de las primeras 8 filas en formato dict para la tabla web
        vista_previa = df.head(8).to_dict(orient="records")
        
        # Resumen estadístico numérico si existe
        desc_num = ""
        cols_num = df.select_dtypes(include=['number']).columns.tolist()
        if cols_num:
            desc_num = df[cols_num].describe().round(2).to_string()

        # Enviar información estructurada al LLM
        prompt_sistema = (
            "Eres un consultor experto en análisis de datos empresariales y ofimática (Excel, reportería financiera y administrativa). "
            "Generas resúmenes ejecutivos comprensibles para secretarias, jefaturas y asistentes administrativos."
        )
        prompt_usuario = (
            f"Se ha cargado una hoja de cálculo con {total_filas} registros y {total_cols} columnas.\n"
            f"Columnas presentes: {', '.join(columnas)}\n\n"
            f"Resumen estadístico de variables numéricas:\n{desc_num}\n\n"
            f"Muestra de los primeros registros:\n{df.head(5).to_string()}\n\n"
            f"REQUERIMIENTO DEL ASISTENTE:\n{pregunta}\n\n"
            f"Por favor responde estructurando:\n"
            f"1. Resumen Ejecutivo (¿Qué datos contiene esta tabla?).\n"
            f"2. Hallazgos Relevantes y Alertas (totales, valores atípicos, promedios, situaciones de atención).\n"
            f"3. Recomendaciones Administrativas Prácticas."
        )
        mensajes = [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ]
        res_llm = llamar_llm(mensajes, temperatura=0.25)

        return jsonify({
            "exito": True,
            "total_filas": total_filas,
            "total_columnas": total_cols,
            "columnas": columnas,
            "vista_previa": vista_previa,
            "analisis": res_llm
        })
    except Exception as e:
        return jsonify({"error": f"Error al procesar la tabla: {str(e)}"}), 500

# ================= MÓDULO 5: CHAT GENERAL =================

@app.route('/api/chat', methods=['POST'])
def chat_asistencial():
    data = request.json or {}
    historial = data.get("mensajes", [])
    rol = data.get("rol", "Asistente Ejecutivo General")

    roles_sistema = {
        "Asistente Ejecutivo General": "Eres un asistente virtual de gerencia, experto en ofimática, etiqueta corporativa y redacción en español.",
        "Experto en Ortografía y Redacción": "Eres un corrector de estilo y editor senior especializado en cartas institucionales y comunicados corporativos.",
        "Analista Contable y de Facturación": "Eres un especialista en revisión de facturas, cuentas de cobro, viáticos e impuestos comerciales.",
        "Gestor de Talento Humano": "Eres un profesional en RRHH, redacción de memorandos disciplinarios, circulares y gestión de bienestar laboral."
    }

    mensaje_sistema = {
        "role": "system",
        "content": roles_sistema.get(rol, roles_sistema["Asistente Ejecutivo General"])
    }

    mensajes_completos = [mensaje_sistema] + historial
    res = llamar_llm(mensajes_completos, temperatura=0.3)
    return jsonify(res)

if __name__ == '__main__':
    puerto = 5000
    ip_local = obtener_ip_local()
    print("=" * 65)
    print(" ASISTENTE DE IA PARA OFIMATICA Y ADMINISTRACION")
    print(" Modo: Red Local del Aula (Acceso desde PC y Celulares)")
    print("=" * 65)
    print(f" Servidor web iniciado en:")
    print(f"   > Desde esta PC:    http://127.0.0.1:{puerto}")
    print(f"   > Desde celulares:  http://{ip_local}:{puerto}")
    print()
    print(f" Los alumnos deben conectar su celular a la misma red WiFi")
    print(f" del aula y abrir en el navegador:")
    print()
    print(f"     >>> http://{ip_local}:{puerto} <<<")
    print()
    print("=" * 65)
    app.run(host='0.0.0.0', port=puerto, debug=False)
