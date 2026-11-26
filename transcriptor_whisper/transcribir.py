"""
Módulo de Transcripción de Audio Local con Faster-Whisper
Diseñado para el Laboratorio de IA en Ofimática (Ejecución 100% Offline)
Permite transcribir reuniones, llamadas y dictados de audio a texto estructurado.
"""
import os
import sys
import json
import time
from faster_whisper import WhisperModel

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELOS_DIR = os.path.join(BASE_DIR, "transcriptor_whisper", "modelos")
AUDIOS_DIR = os.path.join(BASE_DIR, "datos_de_prueba", "01_audios_reuniones")
RESULTADOS_DIR = os.path.join(BASE_DIR, "transcriptor_whisper", "transcripciones_guardadas")

os.makedirs(MODELOS_DIR, exist_ok=True)
os.makedirs(RESULTADOS_DIR, exist_ok=True)

class TranscriptorOficina:
    def __init__(self, model_size="base", device="cpu", compute_type="int8"):
        """
        Inicializa el modelo Whisper local optimizado para CPU y bajo consumo de RAM.
        - model_size: 'tiny' (~75MB), 'base' (~145MB), o 'small' (~480MB).
        - compute_type: 'int8' para máxima velocidad en procesadores estándar de oficina.
        """
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.model = None

    def cargar_modelo(self):
        if self.model is None:
            print(f"[Whisper] Cargando modelo '{self.model_size}' en {self.device} ({self.compute_type})...")
            # Usa la carpeta local de modelos para operar offline
            self.model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type,
                download_root=MODELOS_DIR
            )
            print("[Whisper] Modelo cargado y listo para transcripción offline.")

    def transcribir_archivo(self, ruta_audio, idioma="es"):
        """
        Transcribe un archivo de audio (WAV, MP3, M4A, OGG) a texto y devuelve
        la transcripción completa y segmentos con marcas de tiempo.
        """
        if not os.path.exists(ruta_audio):
            raise FileNotFoundError(f"No se encontró el archivo de audio: {ruta_audio}")

        self.cargar_modelo()
        inicio = time.time()
        print(f"[Whisper] Procesando archivo: {os.path.basename(ruta_audio)}...")

        # VAD (Voice Activity Detection) para omitir silencios y acelerar la inferencia
        segments, info = self.model.transcribe(
            ruta_audio,
            language=idioma,
            vad_filter=True,
            beam_size=5
        )

        segmentos_lista = []
        texto_completo = []

        for seg in segments:
            min_inicio = int(seg.start // 60)
            seg_inicio = int(seg.start % 60)
            min_fin = int(seg.end // 60)
            seg_fin = int(seg.end % 60)
            tiempo_str = f"[{min_inicio:02d}:{seg_inicio:02d} -> {min_fin:02d}:{seg_fin:02d}]"
            
            texto_linea = f"{tiempo_str} {seg.text.strip()}"
            segmentos_lista.append({
                "inicio_seg": seg.start,
                "fin_seg": seg.end,
                "tiempo_formato": tiempo_str,
                "texto": seg.text.strip()
            })
            texto_completo.append(seg.text.strip())

        tiempo_total = round(time.time() - inicio, 2)
        resultado = {
            "archivo": os.path.basename(ruta_audio),
            "idioma_detectado": info.language,
            "probabilidad_idioma": round(info.language_probability, 4),
            "duracion_audio_seg": round(info.duration, 2),
            "tiempo_procesamiento_seg": tiempo_total,
            "transcripcion_continua": " ".join(texto_completo),
            "segmentos": segmentos_lista
        }

        # Guardar en archivo TXT y JSON para uso en ofimática
        nombre_base = os.path.splitext(os.path.basename(ruta_audio))[0]
        ruta_txt = os.path.join(RESULTADOS_DIR, f"{nombre_base}_transcripcion.txt")
        ruta_json = os.path.join(RESULTADOS_DIR, f"{nombre_base}_datos.json")

        with open(ruta_txt, "w", encoding="utf-8") as f:
            f.write(f"=== REPORTE DE TRANSCRIPCIÓN DE AUDIO ===\n")
            f.write(f"Archivo: {resultado['archivo']}\n")
            f.write(f"Duración: {resultado['duracion_audio_seg']} seg | Procesado en: {resultado['tiempo_procesamiento_seg']} seg\n")
            f.write(f"Idioma: {resultado['idioma_detectado']} (Confianza: {resultado['probabilidad_idioma']*100:.1f}%)\n")
            f.write("="*42 + "\n\n")
            f.write("--- TEXTO CONTINUO ---\n")
            f.write(resultado["transcripcion_continua"] + "\n\n")
            f.write("--- SEGMENTOS CON MARCAS DE TIEMPO ---\n")
            for s in segmentos_lista:
                f.write(f"{s['tiempo_formato']} {s['texto']}\n")

        with open(ruta_json, "w", encoding="utf-8") as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)

        print(f"[Whisper] Finalizado en {tiempo_total}s. Guardado en: {ruta_txt}")
        return resultado

if __name__ == "__main__":
    print("=== TRANSCRIPTOR LOCAL WHISPER PARA OFIMÁTICA ===")
    # Si se pasa un archivo como argumento, procesarlo
    if len(sys.argv) > 1:
        ruta_audio_entrada = sys.argv[1]
    else:
        # Por defecto usar el primer audio de prueba
        audios_disponibles = [f for f in os.listdir(AUDIOS_DIR) if f.endswith(".wav") or f.endswith(".mp3")]
        if audios_disponibles:
            ruta_audio_entrada = os.path.join(AUDIOS_DIR, audios_disponibles[0])
            print(f"No se especificó audio. Usando archivo de prueba: {audios_disponibles[0]}")
        else:
            print("No se encontraron audios de prueba en 'datos_de_prueba/01_audios_reuniones'.")
            sys.exit(1)

    transcriptor = TranscriptorOficina(model_size="base")
    res = transcriptor.transcribir_archivo(ruta_audio_entrada)
    print("\n[VISTA PREVIA DEL TEXTO TRANSCRITO]:")
    print(res["transcripcion_continua"])
