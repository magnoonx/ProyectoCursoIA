// ============================================================
// LOGICA CLIENTE - ASISTENTE DE OFIMATICA IA (100% OFFLINE)
// ============================================================

document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  verificarEstadoServidor();
  cargarInfoConexionMovil();
  setInterval(verificarEstadoServidor, 10000); // Polling ligero del estado del LLM
});

// DETECCIÓN DE CONEXIÓN PARA CELULARES
async function cargarInfoConexionMovil() {
  const mobileText = document.getElementById("mobile-url-text");
  if (!mobileText) return;
  try {
    const res = await fetch("/api/conexion");
    if (!res.ok) throw new Error("Error conexion");
    const data = await res.json();
    mobileText.textContent = `Móvil: ${data.url_movil}`;
  } catch (err) {
    mobileText.textContent = `Móvil: http://${window.location.hostname}:5000`;
  }
}

// GESTIÓN DE PESTAÑAS
function initTabs() {
  const navItems = document.querySelectorAll(".nav-item");
  const moduleViews = document.querySelectorAll(".module-view");

  navItems.forEach(item => {
    item.addEventListener("click", () => {
      const targetId = item.getAttribute("data-tab");

      navItems.forEach(n => n.classList.remove("active"));
      moduleViews.forEach(v => v.classList.remove("active"));

      item.classList.add("active");
      const targetView = document.getElementById(targetId);
      if (targetView) targetView.classList.add("active");
    });
  });
}

// ESTADO DEL SERVIDOR LOCAL
async function verificarEstadoServidor() {
  const llmDot = document.getElementById("llm-dot");
  const llmText = document.getElementById("llm-status-text");

  try {
    const res = await fetch("/api/status");
    if (!res.ok) throw new Error("Offline");
    const data = await res.json();

    if (data.llm_conectado) {
      llmDot.className = "dot dot-green";
      llmText.textContent = `LLM Activo: ${data.servidor_llm}`;
    } else {
      llmDot.className = "dot dot-amber";
      llmText.textContent = "LLM: En espera (Inicie llama-server o LM Studio)";
    }
  } catch (err) {
    llmDot.className = "dot dot-amber";
    llmText.textContent = "Servidor Web Local Activo";
  }
}

// ================= MÓDULO 1: REDACCIÓN =================

function cargarEjemploRedaccion() {
  document.getElementById("redac-tipo").value = "Memorando Interno";
  document.getElementById("redac-remitente").value = "Diana Martínez - Directora de Talento Humano";
  document.getElementById("redac-destinatario").value = "Todos los líderes de área y coordinadores";
  document.getElementById("redac-tono").value = "Formal Institucional";
  document.getElementById("redac-instrucciones").value = 
    "Recordar la entrega de reportes de asistencia mensual con corte al 31 de marzo.\n" +
    "Indicar que las solicitudes de permisos de Semana Santa deben radicarse a más tardar el viernes 10.\n" +
    "Reiterar que los certificados médicos deben adjuntarse escaneados en formato PDF legible.";
}

async function ejecutarRedaccion() {
  const tipo = document.getElementById("redac-tipo").value;
  const remitente = document.getElementById("redac-remitente").value;
  const destinatario = document.getElementById("redac-destinatario").value;
  const tono = document.getElementById("redac-tono").value;
  const instrucciones = document.getElementById("redac-instrucciones").value;
  const loading = document.getElementById("loading-redac");
  const resultadoBox = document.getElementById("resultado-redac");

  if (!instrucciones.trim()) {
    alert("Por favor ingrese las instrucciones o puntos clave del documento.");
    return;
  }

  loading.style.display = "flex";
  resultadoBox.innerHTML = '<div class="result-placeholder"><span>✍️</span>Redactando comunicación oficial con el modelo local...</div>';

  try {
    const res = await fetch("/api/redactar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tipo, remitente, destinatario, tono, instrucciones })
    });

    const data = await res.json();
    if (data.error) {
      resultadoBox.textContent = `Error: ${data.error}`;
    } else {
      resultadoBox.textContent = data.contenido;
    }
  } catch (err) {
    resultadoBox.textContent = `Error de conexión: ${err.message}`;
  } finally {
    loading.style.display = "none";
  }
}

// ================= MÓDULO 2: TRANSCRIPCIÓN Y NOTAS DE VOZ =================

let audioArchivoSubido = null;
let mediaRecorder = null;
let audioChunks = [];
let grabacionTimerInterval = null;
let segundosGrabacion = 0;

async function toggleGrabacionMic() {
  const btn = document.getElementById("btn-grabar-mic");
  const timerSpan = document.getElementById("grabando-timer");
  const micLabel = document.getElementById("mic-label");
  const micIcon = document.getElementById("mic-icon");

  if (mediaRecorder && mediaRecorder.state === "recording") {
    // DETENER GRABACIÓN
    mediaRecorder.stop();
    clearInterval(grabacionTimerInterval);
    timerSpan.style.display = "none";
    micLabel.textContent = "Grabar Dictado / Nota de Voz";
    micIcon.textContent = "🎤";
    btn.classList.remove("btn-danger");
    btn.classList.add("btn-secondary");
  } else {
    // INICIAR GRABACIÓN
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioChunks = [];
      mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = e => {
        if (e.data.size > 0) audioChunks.push(e.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
        audioArchivoSubido = new File([audioBlob], "dictado_nota_voz.webm", { type: "audio/webm" });
        document.getElementById("audio-file-name").textContent = "🎙️ Nota de voz grabada desde micrófono lista.";
        document.getElementById("audio-muestra-select").value = "";

        const player = document.getElementById("audio-player");
        player.src = URL.createObjectURL(audioBlob);
        player.style.display = "block";

        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      segundosGrabacion = 0;
      timerSpan.textContent = "🔴 00:00";
      timerSpan.style.display = "inline";
      micLabel.textContent = "Detener Grabación";
      micIcon.textContent = "⏹️";
      btn.classList.remove("btn-secondary");
      btn.classList.add("btn-danger");

      grabacionTimerInterval = setInterval(() => {
        segundosGrabacion++;
        const mins = String(Math.floor(segundosGrabacion / 60)).padStart(2, "0");
        const secs = String(segundosGrabacion % 60).padStart(2, "0");
        timerSpan.textContent = `🔴 ${mins}:${secs}`;
      }, 1000);
    } catch (err) {
      alert("No se pudo acceder al micrófono: " + err.message + "\nAsegúrate de otorgar permisos de micrófono en el navegador.");
    }
  }
}

function archivoAudioSeleccionado(input) {
  if (input.files && input.files[0]) {
    audioArchivoSubido = input.files[0];
    document.getElementById("audio-file-name").textContent = `Archivo cargado: ${audioArchivoSubido.name}`;
    document.getElementById("audio-muestra-select").value = "";

    const player = document.getElementById("audio-player");
    player.src = URL.createObjectURL(audioArchivoSubido);
    player.style.display = "block";
  }
}

function probarAudioMuestra() {
  const sel = document.getElementById("audio-muestra-select").value;
  if (!sel) return;
  audioArchivoSubido = null;
  document.getElementById("input-audio-file").value = "";
  document.getElementById("audio-file-name").textContent = `Muestra seleccionada: ${sel}`;

  const player = document.getElementById("audio-player");
  player.src = `/api/datos_prueba/cargar/audios/${sel}`;
  player.style.display = "block";
}

async function ejecutarTranscripcion() {
  const muestra = document.getElementById("audio-muestra-select").value;
  const objetivo = document.getElementById("audio-objetivo-select").value;
  const loading = document.getElementById("loading-audio");
  const resultadoBox = document.getElementById("resultado-acta");

  if (!audioArchivoSubido && !muestra) {
    alert("Por favor graba una nota de voz, selecciona un audio de prueba o sube un archivo.");
    return;
  }

  loading.style.display = "flex";
  resultadoBox.innerHTML = '<div class="result-placeholder"><span>🎧</span>Transcribiendo nota de voz con Faster-Whisper local y procesando con IA...</div>';

  const formData = new FormData();
  if (audioArchivoSubido) {
    formData.append("audio", audioArchivoSubido);
  } else {
    formData.append("audio_muestra", muestra);
  }
  formData.append("objetivo", objetivo);

  try {
    const res = await fetch("/api/transcribir_audio", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    if (data.error) {
      resultadoBox.textContent = `Error: ${data.error}`;
    } else {
      let salida = "";
      
      if (data.acta && data.acta.contenido) {
        let tituloSeccion = "RESULTADO PROCESADO CON IA";
        if (objetivo === "correo_formal") tituloSeccion = "CORREO ELECTRÓNICO FORMAL GENERADO DESDE NOTA DE VOZ";
        else if (objetivo === "resumen_tareas") tituloSeccion = "LISTA DE TAREAS Y ACCIONES PRIORITARIAS (CHECKLIST)";
        else if (objetivo === "acta_completa") tituloSeccion = "ACTA OFICIAL DE REUNIÓN";

        salida += `====================================================\n`;
        salida += `   ${tituloSeccion}   \n`;
        salida += `====================================================\n\n`;
        salida += data.acta.contenido + "\n\n";
      }

      salida += "====================================================\n";
      salida += "         TRANSCRIPCIÓN COMPLETA (WHISPER)          \n";
      salida += "====================================================\n";
      salida += `Archivo: ${data.transcripcion.archivo} | Duración: ${data.transcripcion.duracion_audio_seg}s | Procesado en: ${data.transcripcion.tiempo_procesamiento_seg}s\n\n`;
      salida += data.transcripcion.transcripcion_continua + "\n\n";
      salida += "--- SEGMENTOS CON MARCAS DE TIEMPO ---\n";
      data.transcripcion.segmentos.forEach(s => {
        salida += `${s.tiempo_formato} ${s.texto}\n`;
      });

      resultadoBox.textContent = salida;
    }
  } catch (err) {
    resultadoBox.textContent = `Error al procesar audio: ${err.message}`;
  } finally {
    loading.style.display = "none";
  }
}

// ================= MÓDULO 3: LECTOR DE PDFS =================

let pdfArchivoSubido = null;

function archivoPdfSeleccionado(input) {
  if (input.files && input.files[0]) {
    pdfArchivoSubido = input.files[0];
    document.getElementById("pdf-file-name").textContent = `PDF cargado: ${pdfArchivoSubido.name}`;
    document.getElementById("pdf-muestra-select").value = "";
  }
}

function probarPdfMuestra() {
  const sel = document.getElementById("pdf-muestra-select").value;
  if (!sel) return;
  pdfArchivoSubido = null;
  document.getElementById("input-pdf-file").value = "";
  document.getElementById("pdf-file-name").textContent = `Muestra seleccionada: ${sel}`;

  if (sel.includes("Contrato")) {
    document.getElementById("pdf-consulta").value = "¿Quiénes son las partes contratantes, cuál es el valor pactado, el plazo de ejecución y qué obligaciones de confidencialidad se establecen?";
  } else if (sel.includes("Circular")) {
    document.getElementById("pdf-consulta").value = "Resume las nuevas políticas de asistencia: horario oficial, tolerancia de retardos, condiciones del trabajo híbrido y trámite de incapacidades.";
  } else if (sel.includes("Factura")) {
    document.getElementById("pdf-consulta").value = "Extrae el número de factura, cliente, emisor, detalle de servicios facturados, IVA, retenciones y valor neto a transferir.";
  }
}

async function ejecutarAnalisisPdf() {
  const muestra = document.getElementById("pdf-muestra-select").value;
  const consulta = document.getElementById("pdf-consulta").value;
  const loading = document.getElementById("loading-pdf");
  const resultadoBox = document.getElementById("resultado-pdf");

  if (!pdfArchivoSubido && !muestra) {
    alert("Por favor seleccione un documento PDF de muestra o suba un archivo.");
    return;
  }

  loading.style.display = "flex";
  resultadoBox.innerHTML = '<div class="result-placeholder"><span>📑</span>Extrayendo texto del PDF y analizando con Qwen...</div>';

  const formData = new FormData();
  if (pdfArchivoSubido) {
    formData.append("pdf", pdfArchivoSubido);
  } else {
    formData.append("pdf_muestra", muestra);
  }
  formData.append("consulta", consulta || "Extrae los puntos clave y obligaciones de este documento.");

  try {
    const res = await fetch("/api/analizar_pdf", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    if (data.error) {
      resultadoBox.textContent = `Error: ${data.error}`;
    } else {
      let salida = "";
      salida += `=== ANÁLISIS DOCUMENTAL (Total Páginas: ${data.total_paginas}) ===\n\n`;
      salida += data.respuesta.contenido;
      resultadoBox.textContent = salida;
    }
  } catch (err) {
    resultadoBox.textContent = `Error al procesar PDF: ${err.message}`;
  } finally {
    loading.style.display = "none";
  }
}

// ================= MÓDULO 4: ANÁLISIS DE TABLAS =================

let tablaArchivoSubido = null;

function archivoTablaSeleccionado(input) {
  if (input.files && input.files[0]) {
    tablaArchivoSubido = input.files[0];
    document.getElementById("tabla-file-name").textContent = `Tabla cargada: ${tablaArchivoSubido.name}`;
    document.getElementById("tabla-muestra-select").value = "";
  }
}

function probarTablaMuestra() {
  const sel = document.getElementById("tabla-muestra-select").value;
  if (!sel) return;
  tablaArchivoSubido = null;
  document.getElementById("input-tabla-file").value = "";
  document.getElementById("tabla-file-name").textContent = `Muestra seleccionada: ${sel}`;

  if (sel.includes("inventario")) {
    document.getElementById("tabla-pregunta").value = "Identifica los artículos en estado de REORDEN URGENTE, calcula el costo total estimado para reabastecerlos hasta el stock mínimo y formula recomendaciones de compra.";
  } else if (sel.includes("asistencia")) {
    document.getElementById("tabla-pregunta").value = "¿Qué colaboradores registran más minutos de retardo? ¿Cuáles acumulan horas extras y qué departamento tiene mayor cumplimiento horario?";
  } else if (sel.includes("viaticos")) {
    document.getElementById("tabla-pregunta").value = "Analiza los viáticos por departamento: ¿cuánto se ha gastado en total? ¿Hay gastos rechazados o pendientes de auditoría y por qué motivo?";
  } else if (sel.includes("pqrs")) {
    document.getElementById("tabla-pregunta").value = "¿Cuántas solicitudes están abiertas, cuáles son de prioridad alta y qué funcionario tiene más casos asignados?";
  }
}

async function ejecutarAnalisisTabla() {
  const muestra = document.getElementById("tabla-muestra-select").value;
  const pregunta = document.getElementById("tabla-pregunta").value;
  const loading = document.getElementById("loading-tabla");
  const resultadoBox = document.getElementById("resultado-tabla");
  const contenedorPrevia = document.getElementById("contenedor-tabla-previa");
  const tablaPrevia = document.getElementById("tabla-preview-element");

  if (!tablaArchivoSubido && !muestra) {
    alert("Por favor seleccione una hoja de cálculo o suba un archivo .xlsx o .csv.");
    return;
  }

  loading.style.display = "flex";
  resultadoBox.innerHTML = '<div class="result-placeholder"><span>📊</span>Procesando datos con Pandas y elaborando diagnóstico ejecutivo...</div>';

  const formData = new FormData();
  if (tablaArchivoSubido) {
    formData.append("tabla", tablaArchivoSubido);
  } else {
    formData.append("tabla_muestra", muestra);
  }
  formData.append("pregunta", pregunta || "Realiza un diagnóstico ejecutivo de esta tabla.");

  try {
    const res = await fetch("/api/analizar_tabla", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    if (data.error) {
      resultadoBox.textContent = `Error: ${data.error}`;
      contenedorPrevia.style.display = "none";
    } else {
      document.getElementById("tabla-header-info").textContent = 
        `Diagnóstico (${data.total_filas} registros, ${data.total_columnas} columnas)`;
      resultadoBox.textContent = data.analisis.contenido;

      // Renderizar tabla previa
      if (data.vista_previa && data.vista_previa.length > 0) {
        let thHtml = "<tr>" + data.columnas.map(c => `<th>${c}</th>`).join("") + "</tr>";
        let tbHtml = data.vista_previa.map(fila => {
          return "<tr>" + data.columnas.map(c => `<td>${fila[c] !== undefined ? fila[c] : ''}</td>`).join("") + "</tr>";
        }).join("");
        tablaPrevia.innerHTML = thHtml + tbHtml;
        contenedorPrevia.style.display = "block";
      }
    }
  } catch (err) {
    resultadoBox.textContent = `Error al procesar tabla: ${err.message}`;
    contenedorPrevia.style.display = "none";
  } finally {
    loading.style.display = "none";
  }
}

// ================= MÓDULO 5: CHAT LIBRE =================

const chatHistorial = [];

async function enviarMensajeChat() {
  const input = document.getElementById("chat-user-input");
  const texto = input.value.trim();
  if (!texto) return;

  const container = document.getElementById("chat-messages-container");
  const rol = document.getElementById("chat-rol").value;

  // Añadir mensaje del usuario a la interfaz
  const bubbleUser = document.createElement("div");
  bubbleUser.className = "chat-bubble user";
  bubbleUser.textContent = texto;
  container.appendChild(bubbleUser);
  input.value = "";

  chatHistorial.push({ role: "user", content: texto });

  // Bubble de espera
  const bubbleWaiting = document.createElement("div");
  bubbleWaiting.className = "chat-bubble assistant";
  bubbleWaiting.textContent = "Pensando...";
  container.appendChild(bubbleWaiting);
  container.scrollTop = container.scrollHeight;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mensajes: chatHistorial, rol })
    });

    const data = await res.json();
    bubbleWaiting.textContent = data.contenido;
    chatHistorial.push({ role: "assistant", content: data.contenido });
  } catch (err) {
    bubbleWaiting.textContent = `Error al comunicar con el modelo: ${err.message}`;
  }
  container.scrollTop = container.scrollHeight;
}

function limpiarChat() {
  chatHistorial.length = 0;
  const container = document.getElementById("chat-messages-container");
  container.innerHTML = `
    <div class="chat-bubble assistant">
      Conversación reiniciada. ¿En qué tarea administrativa u ofimática deseas que te asista?
    </div>
  `;
}

// ================= UTILIDADES =================

function copiarAlPortapapeles(idElemento) {
  const texto = document.getElementById(idElemento).innerText;
  navigator.clipboard.writeText(texto).then(() => {
    alert("¡Contenido copiado al portapapeles exitosamente!");
  }).catch(() => {
    alert("No se pudo copiar automáticamente. Por favor seleccione y copie manualmente.");
  });
}

function descargarTxt(idElemento, nombreArchivo) {
  const texto = document.getElementById(idElemento).innerText;
  const blob = new Blob([texto], { type: "text/plain;charset=utf-8" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = nombreArchivo;
  a.click();
}
