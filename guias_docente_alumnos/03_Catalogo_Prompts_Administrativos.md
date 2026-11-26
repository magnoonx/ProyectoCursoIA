# Catálogo de Prompts para Asistentes Administrativos y Ofimática
**Optimizado para el modelo local Qwen 2.5 3B Instruct**

Este catálogo contiene plantillas de instrucciones estructuradas listas para copiar, rellenar y ejecutar en LM Studio, GPT4All o en la Interfaz Web del laboratorio.

---

## Bloque 1: Correspondencia y Redacción Ejecutiva

### Prompt 1.1: Memorando de Cumplimiento Normativo
```text
Actúa como Asistente Ejecutivo de Gerencia. Redacta un memorando formal con las siguientes características:
- De: [Tu Nombre / Cargo]
- Para: [Departamento o Personal Destinatario]
- Asunto: [Tema, ej: Cumplimiento en el registro de horas de entrada]
- Puntos clave:
  1. Recordar la hora oficial de ingreso ([Hora]).
  2. Mencionar que la tolerancia es de [X] minutos.
  3. Indicar que retardos reiterados requieren justificación por escrito ante RRHH.
- Tono: Formal, respetuoso, sobrio e institucional.
- Incluye: Lugar y fecha actual, encabezado numerado y espacio para firmas.
```

### Prompt 1.2: Circular Informativa de Cambio de Procedimiento
```text
Redacta una Circular Informativa para todo el personal de la empresa sobre la actualización del procedimiento de [Nombre del Procedimiento, ej: Solicitud de Viáticos y Reembolso de Gastos].
Detalles:
- Vigencia: A partir del [Fecha de inicio].
- Requisito obligatorio: Todos los soportes y facturas deben adjuntarse escaneados en formato PDF con el RUT del proveedor.
- Plazo máximo de radicación: 3 días hábiles posteriores al viaje.
- Correo de contacto para dudas: [Correo].
Usa viñetas para enumerar los 4 pasos del nuevo trámite de forma clara.
```

### Prompt 1.3: Convocatoria Formal a Sesión de Junta Directiva
```text
Elabora una convocatoria oficial a la sesión ordinaria de Junta Directiva / Comité Operativo.
- Fecha y hora: [Día, Hora de inicio y fin].
- Lugar / Modalidad: [Sala de Juntas Piso 3 / Enlace Microsoft Teams].
- Orden del día a incluir:
  1. Verificación de quórum.
  2. Lectura y aprobación del acta anterior.
  3. Informe de avance de proyectos del trimestre.
  4. Revisión del presupuesto de suministros.
  5. Proposiciones y varios.
- Solicitud de confirmación de asistencia con al menos 24 horas de antelación.
```

---

## Bloque 2: Actas, Minutas y Gestión de Reuniones

### Prompt 2.1: Estructuración de Acta Ejecutiva desde Notas en Borrador
```text
A partir del siguiente texto desordenado tomado durante una reunión de equipo, genera un ACTA DE REUNIÓN formal y ejecutiva.

NOTAS DEL ASISTENTE:
"[Pega aquí las notas o transcripción de Whisper]"

ESTRUCTURA REQUERIDA:
1. INFORMACIÓN BÁSICA: Título, fecha, hora y asistentes identificados.
2. OBJETIVO PRINCIPAL DE LA REUNIÓN.
3. SÍNTESIS DE TEMAS TRATADOS (Dividido por temas con viñetas).
4. ACUERDOS Y RESOLUCIONES FINALES.
5. TABLA DE COMPROMISOS (Formato Markdown con columnas: Responsable | Tarea Concreta | Fecha de Entrega).
```

### Prompt 2.2: Resumen Ejecutivo en 1 Párrafo para la Gerencia General
```text
Sintetiza la siguiente transcripción de reunión en un único párrafo de máximo 5 líneas orientado al Gerente General. Resalta únicamente: la decisión principal tomada, el impacto en el presupuesto y la fecha del próximo entregable.

TEXTO:
"[Pega aquí la transcripción]"
```

---

## Bloque 3: Gestión Financiera, Facturación y Cobranzas

### Prompt 3.1: Correo de Cobranza Amigable (Primera Notificación)
```text
Redacta un correo electrónico cordial pero profesional dirigido al departamento de compras del cliente [Nombre del Cliente].
- Motivo: Recordatorio de factura pendiente de pago No. [Número de Factura] por valor de [Monto].
- Fecha de vencimiento: Venció hace 5 días ([Fecha]).
- Tono: Cordial, preventivo (asumiendo que pudo tratarse de un retraso administrativo).
- Adjuntar: Recordar que se envía adjunta la copia de la factura y los datos bancarios para transferencia.
```

### Prompt 3.2: Reclamo a Proveedor por Inconsistencia en Factura
```text
Elabora una carta formal dirigida al área de facturación del proveedor [Nombre del Proveedor].
- Asunto: Devolución e inconformidad con la Factura No. [Número].
- Motivo: Se cobraron [Monto facturado] correspondientes a [Concepto], cuando la Orden de Compra aprobada estipulaba un valor de [Monto convenido].
- Solicitud: Emisión de la correspondiente nota crédito o reexpedición de la factura corregida para proceder con el trámite de pago.
- Plazo de respuesta requerido: 48 horas hábiles.
```

---

## Bloque 4: Atención al Cliente y PQRS

### Prompt 4.1: Respuesta Formal a Reclamo con Solución Inmediata
```text
Eres el encargado del canal de atención al usuario. Redacta una carta de respuesta a la reclamación radicada con el número PQR-[Código].
- Cliente: [Nombre del Cliente o Empresa].
- Motivo del reclamo: Retraso de 4 días en la entrega de suministros de papelería.
- Posición de la empresa: Reconocer la anomalía logística debida a mantenimiento en flota de transporte, pedir disculpas sinceras y confirmar que el pedido fue despachado en la mañana de hoy con entrega garantizada antes de las 14:00 horas.
- Compensación: Otorgar un descuento del 5% en la siguiente orden de compra.
- Tono: Empático, transparente y altamente profesional.
```

---

## Bloque 5: Análisis Documental y Auditoría de Contratos (PDF)

### Prompt 5.1: Matriz de Riesgos y Obligaciones de un Contrato
```text
Analiza el siguiente texto extraído de un contrato de prestación de servicios y genera una tabla comparativa con las siguientes columnas:
1. Cláusula o Sección.
2. Obligación principal del contratista.
3. Penalizaciones o consecuencias por incumplimiento.
4. Plazos o fechas perentorias.

TEXTO DEL CONTRATO:
"[Pega el texto del documento]"
```

### Prompt 5.2: Verificación de Requisitos para Pago de Cuentas de Cobro
```text
A partir del informe de actividades y contrato adjunto, verifica si el contratista ha cumplido con los requisitos necesarios para autorizar el desembolso de su cuota mensual:
- ¿Entregó el informe de actividades aprobado por el supervisor?
- ¿Se adjuntó la planilla de pago de seguridad social (salud, pensión y ARL)?
- ¿El monto cobrado coincide con el valor pactado en la Cláusula Segunda?
Emite un dictamen: AUTORIZADO / PENDIENTE DE SUBSANAR, justificando la respuesta.
```

---

## Bloque 6: Análisis de Tablas de Cálculo y Hojas Excel

### Prompt 6.1: Detección de Fugas Presupuestales en Viáticos
```text
Examina los siguientes registros de gastos de viaje y viáticos de los colaboradores.
Identifica:
1. Gastos que superen los topes habituales (Alimentación > $50 USD, cenas de representación no autorizadas).
2. Gastos que carezcan de número de factura válido.
3. El departamento que ha generado el mayor porcentaje de gasto acumulado.
Presenta tus conclusiones en 3 viñetas ejecutivas con recomendaciones de control interno.
```

### Prompt 6.2: Alerta de Quiebre de Stock en Papelería
```text
A partir del listado de inventario de suministros, clasifica los productos en 3 categorías:
- CRÍTICO (Stock actual menor o igual al 50% del mínimo requerido).
- PREVENTIVO (Stock entre 51% y 100% del mínimo).
- ÓPTIMO (Stock superior al mínimo).
Calcula la inversión total necesaria para abastecer únicamente los productos en nivel CRÍTICO.
```
