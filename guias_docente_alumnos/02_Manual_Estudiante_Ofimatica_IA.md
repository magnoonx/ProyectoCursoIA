# Manual del Estudiante: Talleres Prácticos de IA en Ofimática
**Curso: Herramientas de Inteligencia Artificial para Asistentes Administrativos y Secretariado**

¡Bienvenido al laboratorio práctico! Durante este curso aprenderás a utilizar modelos de lenguaje y procesamiento de audio locales como tu asistente personal de oficina, optimizando tu tiempo y aumentando la calidad de tus entregables.

---

## Taller 1: Redacción Inteligente de Comunicaciones Oficiales
**Objetivo:** Redactar y transformar comunicaciones administrativas respetando la jerarquía, el protocolo formal y los lineamientos corporativos.

### Ejercicio 1.1: Memorando de Cierre de Mes
1. En la aplicación web del curso, dirígete a la pestaña **✍️ Redactor Ejecutivo**.
2. Configura los siguientes parámetros:
   * **Tipo:** `Memorando Interno`
   * **Remitente:** `Diana Martínez - Directora de Talento Humano`
   * **Destinatario:** `Líderes de Departamento y Coordinadores`
   * **Tono:** `Formal Institucional`
   * **Instrucciones:** *Recordar que el 31 de marzo vence el plazo para radicar planillas de asistencia y horas extras. Indicar que permisos para festivos deben tramitarse antes del día 15 con el formato F-TH-02.*
3. Presiona **Generar Documento con IA**.
4. **Análisis crítico del estudiante:**
   * ¿El saludo y la despedida son acordes a la etiqueta empresarial?
   * ¿Las fechas y los plazos quedaron resaltados con claridad?
   * Modifica el tono a *Ejecutivo y Conciso* y compara las diferencias de estilo.

### Ejercicio 1.2: Carta de Respuesta a una PQR
1. Selecciona el tipo **Respuesta Formal a Reclamo de Cliente (PQR)**.
2. Carga una situación real: Un cliente reclama por cobro indebido en la factura No. 9821.
3. Elige el tono **Cordial y Empático**.
4. Evalúa cómo la IA estructura las disculpas institucionales sin comprometer legalmente a la empresa y ofreciendo una solución concreta en 24 horas.

---

## Taller 2: Transcripción de Audio y Minutas de Reunión con Whisper
**Objetivo:** Convertir el contenido de reuniones presenciales o virtuales en actas ejecutivas formales sin necesidad de transcribir palabra por palabra a mano.

### Ejercicio 2.1: Comité Extraordinario de Compras
1. Ve a la pestaña **🎙️ Actas con Whisper**.
2. En el menú desplegable de muestras, selecciona:
   `reunion_presupuesto_suministros.wav`
3. Asegúrate de que esté marcada la casilla *Generar automáticamente el Acta Oficial con Qwen 2.5 3B*.
4. Haz clic en **Procesar y Transcribir Audio**.
5. Observa el resultado generado en menos de 5 segundos:
   * **Transcripción continua:** Revisa la precisión de los números ($3.800.000 COP, 12 resmas de papel).
   * **Marcas de tiempo:** Permiten ubicar el segundo exacto donde se dijo cada frase.
   * **Acta ejecutiva estructurada:** Revisa la tabla de compromisos:
     - ¿Quién es el responsable de emitir la orden de compra? (Ana Gómez).
     - ¿Quién verifica la retención en la fuente? (Carlos Rodríguez).
     - ¿Cuándo y quién recibe en bodega? (Luis Morales, martes a primera hora).

---

## Taller 3: Extracción y Auditoría de Documentos PDF
**Objetivo:** Extraer información crítica de contratos comerciales y circulares institucionales para evitar lecturas tediosas de decenas de páginas.

### Ejercicio 3.1: Auditoría del Contrato No. 402
1. Dirígete a la pestaña **📄 Lector de PDFs**.
2. En el selector de muestras, elige:
   `Contrato_Prestacion_Servicios_No_402.pdf`
3. En el campo de consulta, escribe:
   ```text
   Extrae en una tabla los siguientes datos:
   - Partes contratantes (Nombre y NIT/Cédula)
   - Objeto del contrato
   - Valor total y forma de pago
   - Plazo de ejecución (Fecha inicio y fin)
   - Nombre de la supervisora designada
   ```
4. Presiona **Analizar Documento PDF**.
5. Verifica si el modelo extrajo fielmente el valor de $10.500.000 COP y las 3 cuotas mensuales de $3.500.000 COP sin inventar datos.

---

## Taller 4: Análisis de Hojas de Cálculo con Lenguaje Natural
**Objetivo:** Explorar tablas de datos y obtener resúmenes cuantitativos sin necesidad de formular tablas dinámicas complejas.

### Ejercicio 4.1: Diagnóstico de Inventario de Suministros
1. Abre la pestaña **📊 Analista de Tablas**.
2. Selecciona la muestra:
   `inventario_suministros_oficina.xlsx`
3. En la instrucción, escribe:
   ```text
   ¿Cuáles artículos se encuentran en estado de REORDEN URGENTE?
   Calcula la cantidad de unidades que faltan para alcanzar el stock mínimo y formula un plan de compra prioritario.
   ```
4. Presiona **Analizar Datos con IA**.
5. Examina los resultados numéricos:
   * La IA identificará artículos como las *Resmas de papel oficio* (Stock: 12, Mínimo: 25) y los *Bolígrafos tinta azul*.
   * Te entregará una justificación para presentar al jefe de compras.

### Ejercicio 4.2: Control de Asistencia y Puntualidad
1. Carga la tabla:
   `control_asistencia_personal_marzo_2026.xlsx`
2. Pregunta:
   ```text
   ¿Cuáles colaboradores tienen mayor cantidad de minutos acumulados en retardos y en qué departamento se concentra el problema?
   ```
3. Comprueba cómo el asistente cruza los datos de las columnas *Minutos_Retardo* y *Departamento* para darte un reporte listo para RRHH.

---

## Taller 5: Privacidad, Seguridad y Regla de Oro "Antialucinación"

1. **Privacidad de Datos Offline:**
   * En este laboratorio, tus datos **NUNCA viajan a la nube ni a servidores extranjeros**.
   * Esto permite procesar nombres de clientes, cédulas y datos financieros cumpliendo estrictamente con las leyes de protección de datos personales.

2. **La Regla de Oro del Asistente Administrativo:**
   * La IA es un **copiloto**, no el firmante responsable.
   * Siempre debes hacer una revisión final (proofreading) de cifras, nombres propios y fechas antes de enviar cualquier documento formal a gerencia.
