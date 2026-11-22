from datetime import datetime
from pymongo import MongoClient

URI = "mongodb+srv://ilustre01net_db_user:UkHsZ7OpB078tNmo@cluster0.m87yrxz.mongodb.net/"

client = MongoClient(URI)

# Eliminar la base de datos anterior para mantener el entorno limpio
client.drop_database("comercio_local_db")

# Crear y usar la nueva base de datos
db = client["agro_uraba_db"]

# Limpiar colecciones si se vuelve a ejecutar
db.fincas.drop()
db.lotes_cosecha.drop()
db.despachos_puerto.drop()

# 1) Insertar 6 fincas
fincas_data = [
    {
        "codigo_finca": "FIN-001",
        "nombre_finca": "Finca La Esperanza",
        "municipio": "Apartadó",
        "vereda": "Río Grande",
        "hectareas": 45.0,
        "certificacion": "GlobalG.A.P.",
        "activa": True,
        "contacto": {
            "productor": "Carlos Mendoza",
            "telefono": "3104501101",
            "correo": "esperanza@agrouraba.co"
        }
    },
    {
        "codigo_finca": "FIN-002",
        "nombre_finca": "Finca Brisas del Atrato",
        "municipio": "Turbo",
        "vereda": "Nueva Colonia",
        "hectareas": 62.5,
        "certificacion": "Rainforest Alliance",
        "activa": True,
        "contacto": {
            "productor": "María José Arrieta",
            "telefono": "3104501102",
            "correo": "brisas@agrouraba.co"
        }
    },
    {
        "codigo_finca": "FIN-003",
        "nombre_finca": "Finca El Paraíso",
        "municipio": "Carepa",
        "vereda": "Zungo Embarcadero",
        "hectareas": 38.0,
        "certificacion": "GlobalG.A.P.",
        "activa": True,
        "contacto": {
            "productor": "Jorge Luis Palacio",
            "telefono": "3104501103",
            "correo": "paraiso@agrouraba.co"
        }
    },
    {
        "codigo_finca": "FIN-004",
        "nombre_finca": "Finca San Isidro",
        "municipio": "Chigorodó",
        "vereda": "El Caucho",
        "hectareas": 54.0,
        "certificacion": "Orgánica",
        "activa": True,
        "contacto": {
            "productor": "Ana Sofía Córdoba",
            "telefono": "3104501104",
            "correo": "sanisidro@agrouraba.co"
        }
    },
    {
        "codigo_finca": "FIN-005",
        "nombre_finca": "Finca Palmar Central",
        "municipio": "Turbo",
        "vereda": "Currulao",
        "hectareas": 30.0,
        "certificacion": "Rainforest Alliance",
        "activa": False,
        "contacto": {
            "productor": "Luis Fernando Perea",
            "telefono": "3104501105",
            "correo": "palmar@agrouraba.co"
        }
    },
    {
        "codigo_finca": "FIN-006",
        "nombre_finca": "Finca Vista Hermosa",
        "municipio": "Apartadó",
        "vereda": "San José de Apartadó",
        "hectareas": 48.5,
        "certificacion": "GlobalG.A.P.",
        "activa": True,
        "contacto": {
            "productor": "Diana Marcela Ospina",
            "telefono": "3104501106",
            "correo": "vistahermosa@agrouraba.co"
        }
    }
]
finca_ids = db.fincas.insert_many(fincas_data).inserted_ids

# 2) Insertar 64 lotes de cosecha
variedades = ["Banano Cavendish", "Plátano Hartón", "Banano Orito"]
estados_fitosanitarios = ["Aprobado ICA", "En revisión", "Observación"]
lotes_docs = []

for i in range(1, 65):
    cajas = 300 + ((i * 45) % 900)
    peso_caja_kg = 18.14 if (i % 3 != 1) else 22.0
    lotes_docs.append({
        "finca_id": finca_ids[(i - 1) % len(finca_ids)],
        "codigo_lote": f"LOT-2026-{i:04d}",
        "variedad": variedades[i % len(variedades)],
        "cajas": cajas,
        "peso_total_kg": round(cajas * peso_caja_kg, 2),
        "estado_fitosanitario": estados_fitosanitarios[i % len(estados_fitosanitarios)],
        "fecha_cosecha": datetime(2026, 10, (i % 28) + 1),
        "calidad": {
            "calibre_mm": 38 + (i % 6),
            "grado_madurez": "Verde exportación" if i % 2 == 0 else "Pre-maduración"
        }
    })
lote_ids = db.lotes_cosecha.insert_many(lotes_docs).inserted_ids

# 3) Insertar 50 despachos a puerto (Total: 6 + 64 + 50 = 120 documentos)
puertos_destino = ["Rotterdam", "Amberes", "Miami", "Algeciras"]
estados_despacho = ["En tránsito", "Embarcado", "En puerto origen", "Entregado"]
despachos_docs = []

for j in range(1, 51):
    cajas_despachadas = 400 + ((j * 35) % 800)
    valor_usd_caja = 12.5 + ((j % 5) * 0.8)
    despachos_docs.append({
        "finca_id": finca_ids[(j - 1) % len(finca_ids)],
        "lote_id": lote_ids[(j - 1) % len(lote_ids)],
        "codigo_contenedor": f"MRKU-{780000 + j}",
        "puerto_destino": puertos_destino[j % len(puertos_destino)],
        "cajas_despachadas": cajas_despachadas,
        "valor_usd_total": round(cajas_despachadas * valor_usd_caja, 2),
        "temperatura_c": round(13.2 + ((j % 4) * 0.3), 1),
        "estado": estados_despacho[j % len(estados_despacho)],
        "fecha_zarpe": datetime(2026, 11, (j % 19) + 1)
    })
db.despachos_puerto.insert_many(despachos_docs)

# 4) Verificación final
f_count = db.fincas.count_documents({})
l_count = db.lotes_cosecha.count_documents({})
d_count = db.despachos_puerto.count_documents({})

print("Fincas:", f_count)
print("Lotes de cosecha:", l_count)
print("Despachos a puerto:", d_count)
print("Total documentos insertados:", f_count + l_count + d_count)
