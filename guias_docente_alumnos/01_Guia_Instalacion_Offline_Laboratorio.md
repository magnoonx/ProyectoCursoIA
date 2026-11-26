# Guía de Instalación y Despliegue Offline para el Docente
**Curso: Inteligencia Artificial para Asistentes Administrativos con Enfoque en Ofimática**

Esta guía proporciona el protocolo para configurar los equipos de cómputo del laboratorio sin requerir conexión a internet durante las clases.

---

## 1. Requisitos de Hardware y Software

| Componente | Requisito Mínimo | Requisito Recomendado |
| :--- | :--- | :--- |
| **Sistema Operativo** | Windows 10 (64-bit) | Windows 10 / 11 (64-bit) |
| **Procesador (CPU)** | Intel Core i3 / AMD Ryzen 3 (4 hilos) | Intel Core i5 / AMD Ryzen 5 o superior |
| **Memoria RAM** | 4 GB a 8 GB | 8 GB a 16 GB |
| **Espacio en Disco** | 8 GB libres (HDD o SSD) | 10 GB libres en unidad SSD |
| **GPU Dedicada** | No requerida (Inferencia en CPU) | Opcional (NVIDIA RTX / GTX acelera respuestas) |
| **Conexión a Internet** | **Cero (0%) durante el curso** | Solo requerida una vez para armar la USB maestra |

---

## 2. Preparación de la "Memoria USB Maestra" (Un solo equipo con Internet)

Para evitar descargar modelos en cada equipo del aula, el docente o administrador de sistemas debe preparar una memoria USB (mínimo 16 GB):

1. **Descargar los modelos una única vez:**
   * Ejecutar en el equipo con internet:
     ```bash
     python motor_llm/descargar_qwen_3b.py
     python transcriptor_whisper/transcribir.py
     ```
   * Esto descargará:
     - `motor_llm/modelos/qwen2.5-3b-instruct-q4_k_m.gguf` (~2.0 GB).
     - `transcriptor_whisper/modelos/` (carpeta del modelo `faster-whisper-base`, ~145 MB).

2. **Verificar los datos de prueba:**
   * Comprobar que en `datos_de_prueba` se encuentren las 3 carpetas con sus archivos:
     - `01_audios_reuniones`: audios `.wav` de comités y llamadas.
     - `02_documentos_pdf`: contratos, circulares y facturas.
     - `03_tablas_datos`: libros Excel y archivos `.csv`.

3. **Copiar toda la carpeta `ProyectoCursoIA` a la raíz de la memoria USB.**

---

## 3. Protocolo de Despliegue en las Máquinas de los Alumnos

1. Conecte la memoria USB en cada computadora del aula.
2. Copie la carpeta `ProyectoCursoIA` al escritorio del alumno o a la unidad `D:\` o `C:\`.
3. Abra la carpeta y ejecute el archivo:
   ```cmd
   setup_entorno.ps1
   ```
   *(Verificará la presencia de Python y las librerías preinstaladas).*
4. ¡Listo! La máquina queda lista para trabajar 100% desconectada de la red.

---

## 4. Opciones para el Motor de Inferencia LLM

El docente puede elegir entre dos modalidades según el perfil de los alumnos:

### Modalidad 1: GUI Externa (LM Studio)
* Ideal para estudiantes que desean familiarizarse con interfaces gráficas comerciales.
* **Configuración:**
  1. Abrir LM Studio sin internet.
  2. Cargar el modelo desde `motor_llm\modelos\qwen2.5-3b-instruct-q4_k_m.gguf`.
  3. Ir a la pestaña **Local Server** y hacer clic en **Start Server** (puerto `1234`).
  4. Los estudiantes pueden chatear directamente en LM Studio o usar la Interfaz Web del Curso.

### Modalidad 2: Servidor Portable Integrado (llama-server)
* Ideal si los equipos del laboratorio tienen bloqueada la instalación de programas nuevos (sin permisos de Administrador).
* **Configuración:**
  1. Ejecutar el archivo `motor_llm\iniciar_servidor_llm.bat`.
  2. Abrirá una consola ligera que sirve el modelo en `http://127.0.0.1:8080`.

---

## 5. Inicio Rápido de la Clase

Para arrancar el laboratorio al comenzar la sesión:

1. El alumno hace doble clic en el acceso directo:
   ```cmd
   00_INICIAR_LABORATORIO.bat
   ```
2. Se abrirá automáticamente el navegador web en:
   ```
   http://127.0.0.1:5000
   ```
3. La interfaz web presentará las 5 herramientas ofimáticas listas para practicar.
