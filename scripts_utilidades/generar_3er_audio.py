import pyttsx3
import os

engine = pyttsx3.init()
for v in engine.getProperty('voices'):
    if 'spanish' in v.name.lower() or 'helena' in v.name.lower():
        engine.setProperty('voice', v.id)
        break

engine.setProperty('rate', 150)
texto = (
    "Buenos días Corporación Andina, le atiende Ana Gómez del área de atención y quejas. "
    "Habla Fernando Torres de Transportes Rápidos. Llamo porque en la factura noventa y ocho veintiuno "
    "nos cobran cuarenta horas de soporte cuando correspondían veinticinco. "
    "Ana genera radicado PQR dos mil veintiséis cero cero cuatro con prioridad alta y "
    "el analista Iván Duque emitirá una nota crédito por la diferencia en veinticuatro horas hábiles."
)

ruta = os.path.join("datos_de_prueba", "01_audios_reuniones", "llamada_cliente_reclamo_garantia.wav")
engine.save_to_file(texto, ruta)
engine.runAndWait()
print(f"3er audio generado con éxito: {ruta}")
