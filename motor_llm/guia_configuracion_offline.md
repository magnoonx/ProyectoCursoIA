# Guía de Configuración Offline del Motor de Inferencia LLM
**Curso de Inteligencia Artificial para Asistentes Administrativos y Ofimática**

Este documento detalla la puesta a punto del motor de inferencia local para garantizar que los equipos del laboratorio funcionen de manera fluida, segura y **sin conexión a internet**.

---

## 1. Especificaciones del Modelo Seleccionado

* **Modelo:** `Qwen 2.5 3B Instruct`
* **Formato:** GGUF (`qwen2.5-3b-instruct-q4_k_m.gguf`)
* **Tamaño en disco:** ~2.0 GB
* **Consumo de memoria RAM:** ~2.8 GB a 3.5 GB (muy eficiente para equipos escolares y corporativos de 8 GB o incluso 4 GB de RAM)
* **¿Por qué Qwen 2.5 3B para Ofimática?**
  1. **Excelente fluidez en español:** Comprende modismos, lenguaje formal de negocios y términos jurídicos/administrativos.
  2. **Capacidad de razonamiento estructurado:** Sigue formatos de salida estrictos (minutas de reunión, tablas markdown, extracciones JSON).
  3. **Alta velocidad de generación en CPU:** Supera a modelos de 7B u 8B en procesadores Intel Core i3/i5 o AMD Ryzen estándar de laboratorio.

---

## 2. Opción A: Configuración en LM Studio (Recomendada con GUI amigable)

LM Studio es una de las interfaces gráficas más intuitivas para los estudiantes.

### Paso 1: Instalación Offline
1. Descargue el instalador de LM Studio (`LM-Studio-Setup-...exe`) en un equipo con internet y guárdelo en la memoria USB del laboratorio.
2. Ejecute el instalador en cada equipo.

### Paso 2: Desactivar Verificación de Red y Telemetría
1. Abra LM Studio.
2. Vaya a **Settings** (ícono de engranaje en la esquina inferior izquierda).
3. En la sección **Application**:
   * Desmarque: `Check for updates on launch` (Buscar actualizaciones al iniciar).
   * Desmarque: `Send anonymous telemetry` (Enviar datos de diagnóstico).
4. En **Model Directory**: configure la ruta hacia la carpeta compartida o local:
   `D:\MEGA_FOLDER\Proyectos_desarrollo\Python\ProyectoCursoIA\motor_llm\modelos`

### Paso 3: Carga y Ajustes del Modelo
1. Haga clic en la pestaña **Chat** (ícono de globo de conversación).
2. En el desplegable superior, seleccione `qwen2.5-3b-instruct-q4_k_m.gguf`.
3. En el panel derecho de configuración (**Parameters**):
   * **Context Length (`n_ctx`):** `4096` tokens (suficiente para documentos administrativos completos y actas).
   * **Temperature:** `0.3` (valores bajos garantizan precisión, seriedad y cero alucinaciones en redacción corporativa).
   * **Repeat Penalty:** `1.1`
   * **CPU Threads:** Ajustar al número de núcleos físicos del equipo (típicamente `4`).
   * **GPU Offload:** Si el equipo dispone de tarjeta gráfica dedicada (NVIDIA/AMD), mover a `Max` o `28 layers`; si es solo CPU, dejar en `0`.

### Paso 4: Habilitar el Servidor Local (Para conectar con la Interfaz Web del Curso)
1. En el menú lateral izquierdo de LM Studio, haga clic en el ícono **Developer / Local Server** (`<->`).
2. Verifique que el puerto sea `1234` y el host `127.0.0.1`.
3. Haga clic en el botón verde **Start Server**.
4. ¡Listo! Cualquier aplicación local puede consumir el modelo vía API compatible con OpenAI en:
   `http://127.0.0.1:1234/v1/chat/completions`

---

## 3. Opción B: Configuración en GPT4All

GPT4All es una alternativa ultra ligera y de código abierto.

### Paso 1: Instalación
1. Copie el instalador offline de GPT4All a cada equipo.
2. Instálelo normalmente.

### Paso 2: Configurar Carpeta de Modelos
1. Abra GPT4All y vaya a **Settings** -> **Application**.
2. En **Download Path / Model Directory**, seleccione la carpeta:
   `...\ProyectoCursoIA\motor_llm\modelos`
3. Desactive la opción de `Network Usage Statistics` y `Enable crash reporter`.

### Paso 3: Configurar Plantilla de Prompt (ChatML para Qwen 2.5)
En **Settings** -> **Model**, seleccione el modelo Qwen y configure:
* **System Prompt:**
  ```text
  Eres un asistente virtual experto en gestión administrativa, secretariado ejecutivo y ofimática. Respondes en español con un tono altamente profesional, cortés, estructurado y preciso.
  ```
* **Prompt Template:**
  ```text
  <|im_start|>system
  %1<|im_end|>
  <|im_start|>user
  %2<|im_end|>
  <|im_start|>assistant
  ```

---

## 4. Opción C: Servidor Portable Nativo llama.cpp (Sin instalación previa)

Ideal para aulas donde los alumnos **no tienen permisos de Administrador de Windows** para instalar software o cuando no se desea abrir LM Studio.

1. Simplemente haga doble clic en el archivo:
   `motor_llm\iniciar_servidor_llm.bat`
2. **Selector de modelos interactivo:**
   * El script escanea de forma automática la carpeta `modelos/` y todas las subcarpetas organizadas por LM Studio (`bartowski/`, `lmstudio-community/`, etc.).
   * Si hay más de un modelo `.gguf`, mostrará un menú numerado para que elijas cuál cargar (o presiones Enter para el primero por defecto).
   * También puedes pasarle el número como argumento por consola: `iniciar_servidor_llm.bat 2`.
3. **Detección automática de CPU:**
   * **`bin/` (AVX2):** Para procesadores modernos (Intel Core 4ta gen en adelante, AMD Ryzen).
   * **`bin_avx/` (AVX):** Para procesadores anteriores (Intel Core 2da/3ra gen Sandy/Ivy Bridge, AMD FX).
   * **`bin_noavx/` (Universal):** Para procesadores de entrada o antiguos (Intel Celeron, Pentium, Athlon).
4. Se iniciará el servidor en:
   `http://127.0.0.1:8081`

---

## 5. Diagnóstico de Errores Comunes al Desplegar en Otras PC

### Problema: El archivo .bat se cierra de inmediato tras mostrar el encabezado
Si al ejecutar `iniciar_servidor_llm.bat` la ventana se cierra instantáneamente sin mostrar los registros del modelo:
1. **Incompatibilidad de CPU (AVX2 no soportado):**
   * El ejecutable original de llama-server requería instrucciones AVX2. Si la PC tiene un procesador más antiguo o un Pentium/Celeron, Windows cierra el proceso (`0xC000001D: Illegal Instruction`).
   * *Solución implementada:* El script ahora conmuta de forma transparente entre AVX2, AVX y NO-AVX.
2. **Falta de librerías Microsoft Visual C++ (MSVCP140.dll / VCRUNTIME140.dll):**
   * Equipos con Windows 10 recién instalado o sin paquetes de desarrollo pueden carecer de este runtime (`0xC0000135: DLL not found`).
   * *Solución implementada:* Las DLLs requeridas (`msvcp140.dll`, `vcruntime140.dll`, `vcruntime140_1.dll`, `vcomp140.dll`) ya están incluidas directamente junto a cada ejecutable en `motor_llm/bin/`, `bin_avx/` y `bin_noavx/`.
3. **Bloqueo de seguridad de Windows (SmartScreen):**
   * Si la carpeta fue copiada desde una memoria USB o red, Windows puede bloquear los ejecutables.
   * Haga clic derecho sobre la carpeta del proyecto -> **Propiedades** -> Marque la casilla **Desbloquear** si aparece disponible.

---

## 6. Acceso para Alumnos desde Celulares / Tablets (WiFi del Aula)

La aplicación web está configurada para funcionar como un **servidor centralizado en el aula**:

1. **Requisito:** La PC del profesor y los celulares de los alumnos deben estar conectados a la **misma red WiFi** (o punto de acceso local).
2. **Iniciar servicios en la PC del docente:**
   * Primero: Ejecute `motor_llm\iniciar_servidor_llm.bat`
   * Segundo: Ejecute `00_INICIAR_LABORATORIO.bat`
3. **Conexión de los alumnos:**
   * La consola negra de `00_INICIAR_LABORATORIO.bat` y el encabezado de la web mostrarán la dirección IP local del aula (por ejemplo: `http://192.168.1.103:5000`).
   * Los alumnos simplemente abren esa URL en el navegador de su teléfono (Chrome, Safari, Edge).
   * La interfaz es 100% responsive y se adapta automáticamente a pantallas de celulares.
   * Toda la inferencia pesada (Qwen 2.5 y Whisper) se procesa en la PC del profesor, permitiendo que incluso celulares de gama baja ejecuten todas las prácticas del laboratorio sin instalar nada.


