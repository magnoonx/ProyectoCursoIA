# Entorno 100% Standalone y Laboratorio Offline de IA para Ofimática
**Diseñado para Asistentes Administrativos, Secretariado Ejecutivo y Gestión Documental**
*Garantía Standalone: No requiere tener Python, pip ni ninguna librería instalada en el equipo*

---

## 🔒 Garantía "Plug & Play" (Zero Instalación)

Este proyecto ha sido empaquetado para que **funcione en cualquier computadora con Windows (10 u 11)** directamente desde una memoria USB o disco local, sin importar qué programas o librerías tenga instaladas la máquina:

1. **Intérprete Python Portable Integrado (`python_portable/`):**
   - Viene con su propio ejecutable `python.exe` y runtime aislado.
   - Incluye todas las librerías preinstaladas (`Flask`, `faster-whisper`, `ctranslate2`, `Pandas`, `Openpyxl`, `pypdf`, `fpdf2`, `pyttsx3`, `requests`, `numpy`).
   - No toca el PATH del sistema ni el registro de Windows.
   - Funciona sin permisos de Administrador.

2. **Motor LLM Nativo en C++ (`motor_llm/bin/llama-server.exe`):**
   - Binario compilado oficial de `llama.cpp` x64 AVX2 con sus DLLs (`llama.dll`, `ggml.dll`).
   - Cero dependencias externas. Arranca directamente en el puerto `8080`.

3. **Motor Whisper Local Preinstalado (`transcriptor_whisper/`):**
   - Modelo Whisper `base` alojado en disco local.
   - Transcribe audios de reuniones en español en segundos sin conexión.

4. **Lanzador de 1 Clic (`00_INICIAR_LABORATORIO.bat`):**
   - Inicia el servidor LLM, levanta el Asistente Web y abre el navegador automáticamente.

---

## 🏛️ Estructura del Entorno

```
ProyectoCursoIA/
│
├── 00_INICIAR_LABORATORIO.bat    <-- DOBLE CLIC AQUÍ para iniciar todo el laboratorio
├── setup_entorno.ps1              <-- Diagnóstico rápido del estado del laboratorio
│
├── python_portable/              <-- Intérprete Python portable 100% aislado (Zero Install)
│   ├── python.exe
│   ├── python314.dll / DLLs
│   └── Lib/site-packages/        <-- Todas las librerías preinstaladas
│
├── motor_llm/                    <-- Motor de Inferencia Offline
│   ├── bin/                      <-- llama-server.exe nativo (AVX2 x64) y DLLs
│   ├── modelos/                  <-- Destino de 'qwen2.5-3b-instruct-q4_k_m.gguf' (~2.0 GB)
│   ├── iniciar_servidor_llm.bat  <-- Arranque individual del servidor LLM
│   └── descargar_qwen_3b.py      <-- Descargador con reanudación y barra de progreso
│
├── transcriptor_whisper/         <-- Procesamiento de Audio Local
│   ├── transcribir.py            <-- Motor Whisper local con marcas de tiempo
│   ├── transcribir_audio.bat     <-- Arrastra cualquier audio aquí para transcribir
│   └── modelos/                  <-- Modelo faster-whisper base precargado
│
├── asistente_web/                <-- Interfaz Web Local Especializada (HTML5 + CSS + Flask)
│   ├── app.py                    <-- Servidor web local en puerto 5000
│   ├── templates/index.html      <-- Panel con 5 módulos ofimáticos
│   └── static/                   <-- Estilos corporativos oscuros y JS reactivo
│
├── datos_de_prueba/              <-- Material Práctico Preinstalado
│   ├── 01_audios_reuniones/      <-- Grabaciones WAV de comités de compras, coordinación y reclamos
│   ├── 02_documentos_pdf/        <-- Contratos, circulares de horarios y facturas comerciales
│   └── 03_tablas_datos/          <-- Libros Excel y CSV (asistencia, inventarios, viáticos, PQRS)
│
└── guias_docente_alumnos/        <-- Material Pedagógico Completo
    ├── 01_Guia_Instalacion_Offline_Laboratorio.md
    ├── 02_Manual_Estudiante_Ofimatica_IA.md
    ├── 03_Catalogo_Prompts_Administrativos.md
    └── 04_Plan_Estudios_Curso_Ofimatica_IA.md
```

---

## 🚀 Cómo Usarlo en Cualquier Computadora

1. Conecte la memoria USB o copie la carpeta `ProyectoCursoIA`.
2. Asegúrese de que el archivo del modelo `qwen2.5-3b-instruct-q4_k_m.gguf` esté en `motor_llm\modelos\`.
   *(Si aún no lo ha descargado, ejecute `python_portable\python.exe motor_llm\descargar_qwen_3b.py` en una máquina con internet).*
3. Haga doble clic en:
   ```cmd
   00_INICIAR_LABORATORIO.bat
   ```
4. Se abrirá automáticamente el navegador en:
   **`http://127.0.0.1:5000`**

---

## 🛠️ Los 5 Módulos de Ofimática Incluidos

* **✍️ Redactor Inteligente:** Memorandos, Circulares, Solicitudes a Proveedores y Cartas formales.
* **🎙️ Actas con Whisper:** Carga o arrastra audios de reuniones y genera el acta ejecutiva con tabla de compromisos en segundos.
* **📄 Lector de PDFs:** Auditoría y extracción de cláusulas en Contratos, Facturas y Circulares.
* **📊 Analista de Hojas de Cálculo:** Diagnóstico en lenguaje natural sobre retardos en Asistencia, stock crítico en Inventarios y Viáticos.
* **💬 Chat Asistencial:** Chat libre con perfiles ejecutivos (*Asistente de Gerencia*, *Corrector de Estilo*, *Analista Contable*).
