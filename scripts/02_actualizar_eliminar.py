from datetime import datetime
from pymongo import MongoClient

URI = "mongodb+srv://ilustre01net_db_user:UkHsZ7OpB078tNmo@cluster0.m87yrxz.mongodb.net/"
client = MongoClient(URI)
db = client["agro_uraba_db"]

# 0. Insertar registro temporal de prueba para CRUD
finca_ref = db.fincas.find_one({"codigo_finca": "FIN-001"})
doc_prueba = {
    "finca_id": finca_ref["_id"],
    "codigo_lote": "LOT-2026-CRUD",
    "variedad": "Banano Cavendish",
    "cajas": 500,
    "peso_total_kg": 9070.0,
    "estado_fitosanitario": "En revisión",
    "fecha_cosecha": datetime(2026, 11, 20),
    "calidad": {"calibre_mm": 40, "grado_madurez": "Verde exportación"}
}
id_prueba = db.lotes_cosecha.insert_one(doc_prueba).inserted_id
print("Registro de prueba creado:", db.lotes_cosecha.find_one(
    {"_id": id_prueba}, {"_id": 0, "codigo_lote": 1, "cajas": 1, "estado_fitosanitario": 1}
))

# 1. ACTUALIZACIÓN (update_one con operador $set)
res_update = db.lotes_cosecha.update_one(
    {"_id": id_prueba},
    {"$set": {"cajas": 880, "estado_fitosanitario": "Aprobado ICA"}}
)
print("\n[UPDATE] Documentos modificados:", res_update.modified_count)
print("Documento actualizado:", db.lotes_cosecha.find_one(
    {"_id": id_prueba}, {"_id": 0, "codigo_lote": 1, "cajas": 1, "estado_fitosanitario": 1}
))

# 2. ELIMINACIÓN (delete_one) y conteo final
res_delete = db.lotes_cosecha.delete_one({"_id": id_prueba})
print("\n[DELETE] Documentos eliminados:", res_delete.deleted_count)
print("Total final en lotes_cosecha:", db.lotes_cosecha.count_documents({}))
