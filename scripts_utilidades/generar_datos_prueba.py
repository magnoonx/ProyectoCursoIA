"""
Generador de Datos de Prueba para el Curso de IA en Ofimática
Genera documentos PDF realistas, hojas de cálculo Excel/CSV y audios de reuniones en español.
"""
import os
import csv
import datetime
import pandas as pd
import numpy as np
from fpdf import FPDF
import pyttsx3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS_DIR = os.path.join(BASE_DIR, "datos_de_prueba")
AUDIOS_DIR = os.path.join(DATOS_DIR, "01_audios_reuniones")
PDFS_DIR = os.path.join(DATOS_DIR, "02_documentos_pdf")
TABLAS_DIR = os.path.join(DATOS_DIR, "03_tablas_datos")

for d in [AUDIOS_DIR, PDFS_DIR, TABLAS_DIR]:
    os.makedirs(d, exist_ok=True)

# ==========================================
# 1. GENERACIÓN DE TABLAS DE DATOS EXCEL/CSV
# ==========================================
def generar_tablas():
    print("-> Generando hojas de calculo y tablas de prueba...")
    
    # A) Control de Asistencia
    empleados = [
        ("EMP001", "Ana Gomez", "Administracion", "Asistente Ejecutiva"),
        ("EMP002", "Carlos Rodriguez", "Contabilidad", "Analista Contable"),
        ("EMP003", "Diana Martinez", "Talento Humano", "Coordinadora RRHH"),
        ("EMP004", "Eduardo Lopez", "Operaciones", "Auxiliar de Logistica"),
        ("EMP005", "Fernanda Ortiz", "Ventas", "Ejecutiva Comercial"),
        ("EMP006", "Gustavo Silva", "Tecnologia", "Soporte Tecnico"),
        ("EMP007", "Helena Castro", "Administracion", "Recepcionista"),
        ("EMP008", "Ivan Duque", "Contabilidad", "Auxiliar de Facturacion"),
        ("EMP009", "Julia Romero", "Ventas", "Coordinadora Comercial"),
        ("EMP010", "Luis Morales", "Operaciones", "Jefe de Bodega")
    ]
    
    filas_asistencia = []
    fecha_base = datetime.date(2026, 3, 2)  # Lunes
    for dia_idx in range(10): # 2 semanas laborales (lunes a viernes)
        dia_actual = fecha_base + datetime.timedelta(days=(dia_idx // 5)*7 + (dia_idx % 5))
        if dia_actual.weekday() >= 5:
            continue
            
        for emp_id, nombre, depto, cargo in empleados:
            # Simulacion de eventos realistas
            rand = np.random.RandomState(abs(hash(f"{emp_id}-{dia_idx}")) % (2**31))
            val = rand.rand()
            
            if val < 0.05:
                estado = "Permiso Medico"
                hora_in = "--"
                hora_out = "--"
                min_retardo = 0
                horas_extra = 0
            elif val < 0.10:
                estado = "Retardo Injustificado"
                hora_in = f"08:{rand.randint(16, 45):02d}"
                hora_out = "17:00"
                min_retardo = int(hora_in.split(":")[1])
                horas_extra = 0
            elif val < 0.25:
                estado = "Jornada Extendida"
                hora_in = "07:55"
                hora_out = f"19:{rand.randint(0, 30):02d}"
                min_retardo = 0
                horas_extra = 2.0
            else:
                estado = "Presente a Tiempo"
                hora_in = f"07:{rand.randint(45, 59):02d}"
                hora_out = "17:00"
                min_retardo = 0
                horas_extra = 0
                
            filas_asistencia.append({
                "Fecha": dia_actual.strftime("%Y-%m-%d"),
                "Codigo": emp_id,
                "Colaborador": nombre,
                "Departamento": depto,
                "Cargo": cargo,
                "Hora_Entrada": hora_in,
                "Hora_Salida": hora_out,
                "Minutos_Retardo": min_retardo,
                "Horas_Extra": horas_extra,
                "Estado": estado
            })
            
    df_asistencia = pd.DataFrame(filas_asistencia)
    path_asistencia = os.path.join(TABLAS_DIR, "control_asistencia_personal_marzo_2026.xlsx")
    with pd.ExcelWriter(path_asistencia, engine="openpyxl") as writer:
        df_asistencia.to_excel(writer, sheet_name="Asistencia", index=False)
    print(f"   [OK] {path_asistencia}")

    # B) Inventario de Suministros de Oficina
    suministros = [
        ("SUM-001", "Resmas de Papel Carta (500 hojas)", "Papeleria", 85, 20, 4.50, "Papeles Andinos S.A."),
        ("SUM-002", "Resmas de Papel Oficio (500 hojas)", "Papeleria", 12, 25, 5.20, "Papeles Andinos S.A."),
        ("SUM-003", "Boligrafos Tinta Negra (Caja x 50)", "Papeleria", 18, 15, 8.90, "Distribuidora Escolar"),
        ("SUM-004", "Boligrafos Tinta Azul (Caja x 50)", "Papeleria", 5, 15, 8.90, "Distribuidora Escolar"),
        ("SUM-005", "Toner Impresora HP LaserJet Pro M404", "Tecnologia", 2, 4, 65.00, "Sistemas & Copias Ltda."),
        ("SUM-006", "Cartucho Tinta Epson T544 Negro", "Tecnologia", 8, 5, 14.50, "Sistemas & Copias Ltda."),
        ("SUM-007", "Carpetas Colgantes Carta (Caja x 25)", "Archivo", 14, 10, 12.00, "Archivo Total S.A.S."),
        ("SUM-008", "Grapas Estandar 26/6 (Caja x 5000)", "Papeleria", 30, 10, 2.80, "Distribuidora Escolar"),
        ("SUM-009", "Clips Metalicos No. 2 (Caja x 100)", "Papeleria", 45, 20, 1.50, "Distribuidora Escolar"),
        ("SUM-010", "Cafe Molido Especial 500g", "Cafeteria", 6, 12, 7.50, "Tostadora Gourmet"),
        ("SUM-011", "Azucar Morena 1 Kg", "Cafeteria", 4, 8, 2.20, "Supermercado Mayorista"),
        ("SUM-012", "Vasos Biodegradables 7oz (Paquete x 100)", "Cafeteria", 3, 10, 4.10, "EcoEmpaques del Sur"),
        ("SUM-013", "Alcohol Antiseptico 70% 1L", "Limpieza", 15, 10, 3.80, "Quimicos Industriales"),
        ("SUM-014", "Toallas de Mano Dobladas (Fardo x 2000)", "Limpieza", 7, 12, 19.50, "Higiene Corporativa"),
        ("SUM-015", "Pilas Alcalinas AA (Paquete x 4)", "Tecnologia", 9, 10, 3.90, "ElectroPlus")
    ]
    
    filas_inv = []
    for cod, desc, cat, stock, stock_min, costo, prov in suministros:
        alerta = "ALERTA: REORDEN URGENTE" if stock <= stock_min else "STOCK NORMAL"
        valor_total = round(stock * costo, 2)
        filas_inv.append({
            "Codigo_SKU": cod,
            "Descripcion_Articulo": desc,
            "Categoria": cat,
            "Stock_Actual": stock,
            "Stock_Minimo": stock_min,
            "Costo_Unitario_USD": costo,
            "Valor_Total_Stock_USD": valor_total,
            "Proveedor_Habitual": prov,
            "Estado_Inventario": alerta
        })
        
    df_inv = pd.DataFrame(filas_inv)
    path_inv = os.path.join(TABLAS_DIR, "inventario_suministros_oficina.xlsx")
    with pd.ExcelWriter(path_inv, engine="openpyxl") as writer:
        df_inv.to_excel(writer, sheet_name="Inventario_Actual", index=False)
    print(f"   [OK] {path_inv}")

    # C) Rendición de Cuentas y Viáticos (CSV)
    viaticos = [
        {"ID_Gasto": "VT-101", "Fecha": "2026-03-05", "Funcionario": "Carlos Rodriguez", "Depto": "Contabilidad", "Destino": "Medellin", "Concepto": "Tiquete Aereo", "No_Factura": "LATAM-9921", "Monto_USD": 145.00, "Estado_Aprobacion": "Aprobado"},
        {"ID_Gasto": "VT-102", "Fecha": "2026-03-05", "Funcionario": "Carlos Rodriguez", "Depto": "Contabilidad", "Destino": "Medellin", "Concepto": "Hospedaje Hotel Dan", "No_Factura": "H-33214", "Monto_USD": 85.00, "Estado_Aprobacion": "Aprobado"},
        {"ID_Gasto": "VT-103", "Fecha": "2026-03-06", "Funcionario": "Carlos Rodriguez", "Depto": "Contabilidad", "Destino": "Medellin", "Concepto": "Alimentacion Clientes", "No_Factura": "REST-441", "Monto_USD": 62.50, "Estado_Aprobacion": "Pendiente Auditoria"},
        {"ID_Gasto": "VT-104", "Fecha": "2026-03-06", "Funcionario": "Carlos Rodriguez", "Depto": "Contabilidad", "Destino": "Medellin", "Concepto": "Taxi Aeropuerto", "No_Factura": "TX-008", "Monto_USD": 25.00, "Estado_Aprobacion": "Aprobado"},
        {"ID_Gasto": "VT-105", "Fecha": "2026-03-08", "Funcionario": "Fernanda Ortiz", "Depto": "Ventas", "Destino": "Cali", "Concepto": "Combustible Vehiculo", "No_Factura": "EST-8812", "Monto_USD": 45.00, "Estado_Aprobacion": "Aprobado"},
        {"ID_Gasto": "VT-106", "Fecha": "2026-03-08", "Funcionario": "Fernanda Ortiz", "Depto": "Ventas", "Destino": "Cali", "Concepto": "Peajes Ruta Sur", "No_Factura": "PEA-552", "Monto_USD": 18.00, "Estado_Aprobacion": "Aprobado"},
        {"ID_Gasto": "VT-107", "Fecha": "2026-03-09", "Funcionario": "Fernanda Ortiz", "Depto": "Ventas", "Destino": "Cali", "Concepto": "Cena Representacion", "No_Factura": "REST-901", "Monto_USD": 110.00, "Estado_Aprobacion": "Rechazado (Supera Limite Politica)"},
        {"ID_Gasto": "VT-108", "Fecha": "2026-03-12", "Funcionario": "Diana Martinez", "Depto": "Talento Humano", "Destino": "Bogota", "Concepto": "Inscripcion Seminario Gestion", "No_Factura": "SEM-2026", "Monto_USD": 210.00, "Estado_Aprobacion": "Aprobado"},
        {"ID_Gasto": "VT-109", "Fecha": "2026-03-12", "Funcionario": "Diana Martinez", "Depto": "Talento Humano", "Destino": "Bogota", "Concepto": "Transporte Urbano", "No_Factura": "UB-4411", "Monto_USD": 30.00, "Estado_Aprobacion": "Aprobado"}
    ]
    df_viaticos = pd.DataFrame(viaticos)
    path_viaticos = os.path.join(TABLAS_DIR, "rendicion_cuentas_viaticos.csv")
    df_viaticos.to_csv(path_viaticos, index=False, encoding="utf-8-sig")
    print(f"   [OK] {path_viaticos}")

    # D) Registro de PQRS (Atención al Cliente)
    pqrs = [
        {"Ticket": "PQR-2026-001", "Fecha_Ingreso": "2026-03-01", "Cliente": "Distribuidora El Triunfo", "Canal": "Correo Electronico", "Tipo": "Reclamo", "Asunto": "Retraso en entrega de pedido No. 4410", "Prioridad": "Alta", "Dias_Abierto": 5, "Responsable": "Ana Gomez", "Estado": "En Tramite"},
        {"Ticket": "PQR-2026-002", "Fecha_Ingreso": "2026-03-02", "Cliente": "Inversiones del Caribe", "Canal": "Telefono", "Tipo": "Queja", "Asunto": "Atencion descortes en mesa de ayuda", "Prioridad": "Media", "Dias_Abierto": 4, "Responsable": "Diana Martinez", "Estado": "Cerrado Satisfactorio"},
        {"Ticket": "PQR-2026-003", "Fecha_Ingreso": "2026-03-03", "Cliente": "Colegio Santa Maria", "Canal": "Web Portal", "Tipo": "Peticion", "Asunto": "Solicitud copia de certificado tributario 2025", "Prioridad": "Baja", "Dias_Abierto": 1, "Responsable": "Carlos Rodriguez", "Estado": "Resuelto"},
        {"Ticket": "PQR-2026-004", "Fecha_Ingreso": "2026-03-04", "Cliente": "Transportes Rápidos Ltda.", "Canal": "Correo Electronico", "Tipo": "Reclamo", "Asunto": "Inconsistencia en valor de factura 9821", "Prioridad": "Alta", "Dias_Abierto": 3, "Responsable": "Ivan Duque", "Estado": "Escalado a Gerencia"},
        {"Ticket": "PQR-2026-005", "Fecha_Ingreso": "2026-03-05", "Cliente": "Supermercado Mayorista", "Canal": "Presencial", "Tipo": "Sugerencia", "Asunto": "Habilitar recepcion de documentos en formato digital", "Prioridad": "Baja", "Dias_Abierto": 2, "Responsable": "Ana Gomez", "Estado": "Cerrado"}
    ]
    df_pqrs = pd.DataFrame(pqrs)
    path_pqrs = os.path.join(TABLAS_DIR, "registro_solicitudes_pqrs.xlsx")
    with pd.ExcelWriter(path_pqrs, engine="openpyxl") as writer:
        df_pqrs.to_excel(writer, sheet_name="PQRS_Marzo", index=False)
    print(f"   [OK] {path_pqrs}")

# ==========================================
# 2. GENERACIÓN DE DOCUMENTOS PDF
# ==========================================
class CorporatePDF(FPDF):
    def __init__(self, title_text, doc_ref):
        super().__init__()
        self.title_text = title_text
        self.doc_ref = doc_ref

    def header(self):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(30, 41, 59)
        self.cell(0, 8, "CORPORACION EMPRESARIAL ANDINA S.A.S.", ln=1, align="L")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(100, 116, 139)
        self.cell(0, 5, f"Sistema de Gestion Documental e Institucional | Ref: {self.doc_ref}", ln=1, align="L")
        self.set_draw_color(203, 213, 225)
        self.set_line_width(0.5)
        self.line(10, 24, 200, 24)
        self.ln(6)

    def footer(self):
        self.set_y(-18)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 8, f"Documento confidencial para uso exclusivo academico y administrativo - Pagina {self.page_no()}/{{nb}}", align="C")

def generar_pdfs():
    print("-> Generando documentos administrativos en PDF...")
    
    # PDF 1: Contrato de Prestacion de Servicios
    pdf1 = CorporatePDF("CONTRATO DE PRESTACION DE SERVICIOS", "CTO-2026-402")
    pdf1.alias_nb_pages()
    pdf1.add_page()
    
    pdf1.set_font("Helvetica", "B", 14)
    pdf1.set_text_color(15, 23, 42)
    pdf1.cell(0, 10, "CONTRATO DE PRESTACION DE SERVICIOS PROFESIONALES NO. 402", ln=1, align="C")
    pdf1.ln(3)
    
    pdf1.set_font("Helvetica", "", 10)
    pdf1.set_text_color(51, 65, 85)
    
    p1 = ("Entre los suscritos a saber: de una parte, CARLOS EDUARDO MENDOZA, identificado con cedula de ciudadania "
          "No. 79.452.110 de Bogota, en calidad de Representante Legal de INNOVACIONES EMPRESARIALES S.A.S. con NIT 900.842.119-3, "
          "quien en adelante se denominara EL CONTRATANTE; y de la otra parte, SOFIA VALENCIA JARAMILLO, mayor de edad, "
          "identificada con cedula No. 52.883.940, actuando a nombre propio, quien en adelante se denominara LA CONTRATISTA, "
          "se ha convenido celebrar el presente contrato regido por las siguientes clausulas:")
    pdf1.multi_cell(0, 5, p1)
    pdf1.ln(4)
    
    clausulas = [
        ("CLAUSULA PRIMERA - OBJETO:", 
         "LA CONTRATISTA se obliga para con EL CONTRATANTE a prestar de manera autonoma sus servicios profesionales "
         "de consultoria en optimizacion de procesos ofimaticos, digitalizacion documental y capacitacion del personal secretarial."),
        ("CLAUSULA SEGUNDA - VALOR Y FORMA DE PAGO:", 
         "El valor total pactado del presente contrato es la suma de DIEZ MILLONES QUINIENTOS MIL PESOS M/CTE ($10.500.000 COP), "
         "pagaderos en tres (3) cuotas mensuales iguales de $3.500.000 COP, previa presentacion de la cuenta de cobro, informe de "
         "actividades aprobado por la supervision y certificacion de aportes al Sistema General de Seguridad Social."),
        ("CLAUSULA TERCERA - PLAZO DE EJECUCION:", 
         "El plazo de ejecucion del contrato sera de noventa (90) dias calendario, contados a partir del 1 de abril de 2026 y "
         "hasta el 30 de junio de 2026."),
        ("CLAUSULA CUARTA - CONFIDENCIALIDAD:", 
         "LA CONTRATISTA se compromete a guardar estricta reserva sobre toda la informacion financiera, estrategica y datos personales "
         "a los que tenga acceso durante la ejecucion de sus labores, bajo penalidad civil y penal segun la Ley 1581 de 2012."),
        ("CLAUSULA QUINTA - SUPERVISION:", 
         "La supervision y vigilancia del contrato estara a cargo de la Coordinadora de Talento Humano, Sra. Diana Martinez, "
         "quien certificara el cumplimiento de los entregables acordados.")
    ]
    
    for titulo, desc in clausulas:
        pdf1.set_font("Helvetica", "B", 10)
        pdf1.cell(0, 6, titulo, ln=1)
        pdf1.set_font("Helvetica", "", 10)
        pdf1.multi_cell(0, 5, desc)
        pdf1.ln(3)
        
    pdf1.ln(6)
    pdf1.cell(90, 6, "_____________________________", ln=0)
    pdf1.cell(90, 6, "_____________________________", ln=1)
    pdf1.set_font("Helvetica", "B", 9)
    pdf1.cell(90, 5, "CARLOS EDUARDO MENDOZA", ln=0)
    pdf1.cell(90, 5, "SOFIA VALENCIA JARAMILLO", ln=1)
    pdf1.set_font("Helvetica", "", 8)
    pdf1.cell(90, 4, "Representante Legal - Contratante", ln=0)
    pdf1.cell(90, 4, "Consultora Especializada - Contratista", ln=1)
    
    path_pdf1 = os.path.join(PDFS_DIR, "Contrato_Prestacion_Servicios_No_402.pdf")
    pdf1.output(path_pdf1)
    print(f"   [OK] {path_pdf1}")

    # PDF 2: Circular Interna de Horarios y Modalidades
    pdf2 = CorporatePDF("CIRCULAR INFORMATIVA INSTITUCIONAL", "CIR-2026-012")
    pdf2.alias_nb_pages()
    pdf2.add_page()
    
    pdf2.set_font("Helvetica", "B", 14)
    pdf2.cell(0, 10, "CIRCULAR INFORMATIVA NO. 012 - RECTORIA Y RRHH", ln=1, align="C")
    pdf2.ln(2)
    
    pdf2.set_font("Helvetica", "B", 10)
    pdf2.cell(30, 6, "PARA:", ln=0)
    pdf2.set_font("Helvetica", "", 10)
    pdf2.cell(0, 6, "Todo el Personal Administrativo, Secretarial y Operativo", ln=1)
    
    pdf2.set_font("Helvetica", "B", 10)
    pdf2.cell(30, 6, "DE:", ln=0)
    pdf2.set_font("Helvetica", "", 10)
    pdf2.cell(0, 6, "Direccion de Talento Humano y Gestion Corporativa", ln=1)
    
    pdf2.set_font("Helvetica", "B", 10)
    pdf2.cell(30, 6, "FECHA:", ln=0)
    pdf2.set_font("Helvetica", "", 10)
    pdf2.cell(0, 6, "15 de marzo de 2026", ln=1)
    
    pdf2.set_font("Helvetica", "B", 10)
    pdf2.cell(30, 6, "ASUNTO:", ln=0)
    pdf2.set_font("Helvetica", "B", 10)
    pdf2.cell(0, 6, "Actualizacion de Politicas de Asistencia, Trabajo Remoto y Registro de Horas", ln=1)
    pdf2.ln(4)
    
    cuerpo_circular = (
        "Estimado equipo de colaboradores:\n\n"
        "En concordancia con el plan de modernizacion y bienestar corporativo, nos permitimos informar las nuevas "
        "directrices operativas vigentes a partir del proximo 1 de abril de 2026:\n\n"
        "1. JORNADA LABORAL Y PUNTUALIDAD: El horario oficial de atencion en sede central sera de 08:00 a 17:00 horas, "
        "con una hora reglamentaria para el almuerzo (13:00 a 14:00 horas). Se establece una tolerancia maxima de 10 minutos. "
        "Los retardos superiores a 15 minutos deberan contar con debida justificacion ante la jefatura inmediata.\n\n"
        "2. ESQUEMA DE TRABAJO HIBRIDO: Aquellos cargos administrativos autorizados podran ejercer trabajo remoto hasta "
        "dos (2) dias a la semana (martes y jueves). Para acceder al beneficio, el funcionario debera mantener conectividad activa "
        "y responder a requerimientos en un lapso no superior a 30 minutos dentro del horario laboral.\n\n"
        "3. AUTORIZACION DE HORAS EXTRAORDINARIAS: Ninguna hora extra podra ser liquidada sin la aprobacion previa y por "
        "escrito de la Gerencia de Operaciones con al menos 24 horas de anticipacion.\n\n"
        "4. CANAL DE RADICACION DE NOVEDADES: Todos los certificados de incapacidad medica EPS y permisos especiales deberan "
        "ser remitidos escaneados en formato PDF al correo talento.humano@corporacionandina.com dentro de los dos (2) dias habiles "
        "siguientes a la ausencia.\n\n"
        "Agradecemos su compromiso constante con la excelencia organizacional."
    )
    pdf2.set_font("Helvetica", "", 10)
    pdf2.multi_cell(0, 5.5, cuerpo_circular)
    pdf2.ln(6)
    pdf2.set_font("Helvetica", "B", 10)
    pdf2.cell(0, 6, "DIANA MARCELA MARTINEZ", ln=1)
    pdf2.set_font("Helvetica", "", 9)
    pdf2.cell(0, 5, "Directora de Gestion de Talento Humano", ln=1)
    
    path_pdf2 = os.path.join(PDFS_DIR, "Circular_Interna_012_Politica_Horarios.pdf")
    pdf2.output(path_pdf2)
    print(f"   [OK] {path_pdf2}")

    # PDF 3: Factura Comercial de Servicios IT
    pdf3 = CorporatePDF("FACTURA ELECTRONICA DE VENTA", "FAC-IT-9821")
    pdf3.alias_nb_pages()
    pdf3.add_page()
    
    pdf3.set_font("Helvetica", "B", 14)
    pdf3.cell(0, 10, "FACTURA ELECTRONICA DE VENTA NO. 9821", ln=1, align="C")
    pdf3.ln(2)
    
    # Datos emisor y cliente
    pdf3.set_font("Helvetica", "B", 9)
    pdf3.cell(95, 5, "EMISOR: SISTEMAS & COPIAS LTDA.", ln=0)
    pdf3.cell(95, 5, "CLIENTE: CORPORACION EMPRESARIAL ANDINA S.A.S.", ln=1)
    pdf3.set_font("Helvetica", "", 9)
    pdf3.cell(95, 5, "NIT: 860.512.930-1 | Regimen Comun", ln=0)
    pdf3.cell(95, 5, "NIT: 900.842.119-3", ln=1)
    pdf3.cell(95, 5, "Dir: Calle 72 # 11-40, Bogota D.C.", ln=0)
    pdf3.cell(95, 5, "Dir: Carrera 15 # 93-60, Piso 4, Bogota", ln=1)
    pdf3.cell(95, 5, "Fecha Emision: 10/03/2026 | Vencimiento: 10/04/2026", ln=0)
    pdf3.cell(95, 5, "Orden de Compra No.: OC-2026-88", ln=1)
    pdf3.ln(4)
    
    # Tabla de items
    pdf3.set_fill_color(241, 245, 249)
    pdf3.set_font("Helvetica", "B", 9)
    pdf3.cell(20, 7, "Item", 1, 0, "C", fill=True)
    pdf3.cell(95, 7, "Descripcion del Servicio / Suministro", 1, 0, "L", fill=True)
    pdf3.cell(20, 7, "Cant.", 1, 0, "C", fill=True)
    pdf3.cell(25, 7, "V. Unitario", 1, 0, "R", fill=True)
    pdf3.cell(30, 7, "Total", 1, 1, "R", fill=True)
    
    items_fac = [
        ("01", "Mantenimiento Preventivo Mensual Servidores y Red", 1, 1200000, 1200000),
        ("02", "Licenciamiento Microsoft 365 Business (Pack 15 Lic)", 15, 68000, 1020000),
        ("03", "Toner Original HP LaserJet Pro M404 Negro", 4, 260000, 1040000),
        ("04", "Soporte Tecnico Presencial y Remoto Mesa de Ayuda", 40, 35000, 1400000)
    ]
    
    pdf3.set_font("Helvetica", "", 9)
    subtotal = 0
    for it, desc, cant, vu, tot in items_fac:
        subtotal += tot
        pdf3.cell(20, 6, it, 1, 0, "C")
        pdf3.cell(95, 6, desc, 1, 0, "L")
        pdf3.cell(20, 6, str(cant), 1, 0, "C")
        pdf3.cell(25, 6, f"${vu:,.0f}", 1, 0, "R")
        pdf3.cell(30, 6, f"${tot:,.0f}", 1, 1, "R")
        
    iva = subtotal * 0.19
    retefuente = subtotal * 0.04
    total_neto = subtotal + iva - retefuente
    
    pdf3.ln(2)
    pdf3.set_font("Helvetica", "B", 9)
    pdf3.cell(135, 6, "SUBTOTAL BRUTO:", 0, 0, "R")
    pdf3.cell(55, 6, f"${subtotal:,.0f} COP", 1, 1, "R")
    pdf3.cell(135, 6, "IVA (19%):", 0, 0, "R")
    pdf3.cell(55, 6, f"${iva:,.0f} COP", 1, 1, "R")
    pdf3.cell(135, 6, "Menos Retencion en la Fuente (4%):", 0, 0, "R")
    pdf3.cell(55, 6, f"-${retefuente:,.0f} COP", 1, 1, "R")
    pdf3.set_fill_color(226, 232, 240)
    pdf3.cell(135, 7, "VALOR NETO A TRANSFERIR:", 0, 0, "R")
    pdf3.cell(55, 7, f"${total_neto:,.0f} COP", 1, 1, "R", fill=True)
    
    pdf3.ln(5)
    pdf3.set_font("Helvetica", "I", 8)
    pdf3.multi_cell(0, 4, "Favor consignar a la Cuenta de Ahorros Bancolombia No. 441-098231-11 a nombre de Sistemas & Copias Ltda. Remitir comprobante a facturacion@sistemasycopias.com")
    
    path_pdf3 = os.path.join(PDFS_DIR, "Factura_Comercial_Servicios_IT_9821.pdf")
    pdf3.output(path_pdf3)
    print(f"   [OK] {path_pdf3}")

    # PDF 4: Acta de Sesión Anterior
    pdf4 = CorporatePDF("ACTA DE JUNTA Y COMITE", "ACTA-2026-004")
    pdf4.alias_nb_pages()
    pdf4.add_page()
    
    pdf4.set_font("Helvetica", "B", 13)
    pdf4.cell(0, 8, "ACTA DE REUNION ORDINARIA DEL COMITE DIRECTIVO", ln=1, align="C")
    pdf4.set_font("Helvetica", "I", 10)
    pdf4.cell(0, 6, "Sesion del 25 de Febrero de 2026 - Hora: 09:00 a 11:30", ln=1, align="C")
    pdf4.ln(4)
    
    secciones_acta = [
        ("1. ASISTENTES:", 
         "- Carlos Eduardo Mendoza (Gerente General)\n"
         "- Diana Marcela Martinez (Directora de RRHH)\n"
         "- Carlos Rodriguez (Analista Financiero)\n"
         "- Ana Gomez (Secretaria de Gerencia / Actuaria)"),
        ("2. ORDEN DEL DIA:", 
         "1. Verificacion de quorum.\n"
         "2. Revision de ejecucion presupuestal enero-febrero 2026.\n"
         "3. Adquisicion del nuevo mobiliario de recepcion y equipos de computo.\n"
         "4. Proposiciones y varios."),
        ("3. DESARROLLO Y ACUERDOS PRINCIPALES:", 
         "La Gerencia aprobo por unanimidad la partida presupuestal de $15.000.000 COP para renovacion de equipos portatiles. "
         "Se encarga a la Sra. Ana Gomez solicitar tres (3) cotizaciones antes del 15 de marzo de 2026.\n"
         "Respecto al informe de viaticos, se recordo que ningun consumo de licores ni propinas voluntarias seran reembolsadas."),
        ("4. COMPROMISOS Y TAREAS PENDIENTES:", 
         "- Ana Gomez: Consolidar cotizaciones de portatiles (Plazo: 15 de marzo).\n"
         "- Carlos Rodriguez: Presentar balance contable con corte a 28 de febrero (Plazo: 10 de marzo).\n"
         "- Diana Martinez: Publicar circular de politicas de horarios (Plazo: 15 de marzo).")
    ]
    
    for tit, cont in secciones_acta:
        pdf4.set_font("Helvetica", "B", 10)
        pdf4.cell(0, 6, tit, ln=1)
        pdf4.set_font("Helvetica", "", 10)
        pdf4.multi_cell(0, 5, cont)
        pdf4.ln(3)
        
    path_pdf4 = os.path.join(PDFS_DIR, "Acta_Sesion_Anterior_Comite_Directivo.pdf")
    pdf4.output(path_pdf4)
    print(f"   [OK] {path_pdf4}")

# ==========================================
# 3. GENERACIÓN DE AUDIOS REALISTAS
# ==========================================
def generar_audios():
    print("-> Generando audios de reuniones simuladas...")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    # Seleccionar voz en español si existe
    voz_espanol = None
    for v in voices:
        if "spanish" in v.name.lower() or "helena" in v.name.lower() or "sabina" in v.name.lower() or "es-es" in v.id.lower() or "es-mx" in v.id.lower():
            voz_espanol = v.id
            break
            
    if voz_espanol:
        engine.setProperty('voice', voz_espanol)
    engine.setProperty('rate', 150) # Tono natural de conversación

    guiones = [
        ("reunion_presupuesto_suministros.wav", (
            "Buenos días equipo. Damos inicio a la reunión extraordinaria del comité de compras y suministros. "
            "El objetivo principal es revisar las solicitudes de papelería y cafetería para el segundo trimestre del año. "
            "Revisando el inventario actual, la secretaria ejecutiva Ana Gómez nos alerta que estamos al límite crítico "
            "con las resmas de papel tamaño oficio, quedando únicamente doce unidades cuando el mínimo de seguridad es veinticinco. "
            "Adicionalmente, se requiere comprar cuatro cartuchos de tinta negra y dos cajas de bolígrafos azules. "
            "El presupuesto máximo autorizado para esta orden de compra es de tres millones ochocientos mil pesos. "
            "Acuerdos tomados: Primero, Ana Gómez emitirá la orden de compra al proveedor habitual Papeles Andinos antes de este viernes. "
            "Segundo, el contador Carlos Rodríguez verificará la factura y aplicará la retención del cuatro por ciento. "
            "Tercero, todo el material deberá ser recibido en bodega por Luis Morales el próximo martes a primera hora. "
            "Sin más temas que tratar, se levanta la sesión a las diez y cuarenta y cinco de la mañana."
        )),
        ("reunion_coordinacion_semanal.wav", (
            "Buenos días a todos. En esta reunión de coordinación semanal del equipo administrativo, vamos a revisar los entregables prioritarios. "
            "Punto número uno: La auditoría interna de calidad se llevará a cabo el día veinte de abril. Para esa fecha, todos los contratos "
            "de prestación de servicios de este año deben estar escaneados y cargados en el repositorio digital en formato PDF con sus pólizas. "
            "Diana Martínez estará a cargo de verificar que los expedientes del personal tengan las certificaciones de seguridad social al día. "
            "Punto número dos: Se ha detectado un incremento en los minutos de retardo durante los días lunes y viernes. "
            "Recordamos que la circular doce ya fue publicada y la tolerancia es de diez minutos. "
            "Compromisos: Cada área enviará el viernes a las cuatro de la tarde su reporte de tareas completadas. "
            "Muchísimas gracias por su puntualidad y que tengan una excelente semana laboral."
        )),
        ("llamada_cliente_reclamo_garantia.wav", (
            "Buenos días, Corporación Andina, le atiende Ana Gómez del área de atención y quejas, ¿con quién tengo el gusto? "
            "Buenos días señorita, habla Fernando Torres de Transportes Rápidos. Llamo sumamente preocupado porque en la factura "
            "noventa y ocho veintiuno nos están cobrando cuarenta horas de soporte técnico por valor de un millón cuatrocientos mil pesos, "
            "cuando según nuestro contrato de mantenimiento solo correspondían veinticinco horas en este periodo. "
            "Entiendo perfectamente su molestia señor Torres y le ofrezco disculpas por el inconveniente. Permítame tomar atenta nota. "
            "He verificado su expediente y efectivamente existe una discrepancia con las horas registradas por el técnico asignado. "
            "Voy a generar de inmediato el radicado de reclamación PQR dos mil veintiséis cero cero cuatro con prioridad alta. "
            "El analista contable Iván Duque revisará las planillas de soporte y emitiremos una nota crédito por la diferencia en un plazo "
            "máximo de veinticuatro horas hábiles a su correo electrónico. ¿Le parece adecuada esta solución? "
            "Muchas gracias Ana, quedo atento al correo con la nota crédito. Hasta luego."
        ))
    ]

    for archivo_nombre, texto in guiones:
        path_salida = os.path.join(AUDIOS_DIR, archivo_nombre)
        print(f"   -> Sintetizando audio: {archivo_nombre}...")
        engine.save_to_file(texto, path_salida)
        engine.runAndWait()
        print(f"   [OK] {path_salida}")

if __name__ == "__main__":
    print("=== INICIANDO GENERACIÓN DE RECURSOS DE PRUEBA ===")
    generar_tablas()
    generar_pdfs()
    generar_audios()
    print("=== TODOS LOS RECURSOS DE PRUEBA FUERON GENERADOS CON ÉXITO ===")
