from pymongo import MongoClient

URI = "mongodb+srv://ilustre01net_db_user:UkHsZ7OpB078tNmo@cluster0.m87yrxz.mongodb.net/"
client = MongoClient(URI)
db = client["agro_uraba_db"]

pipeline = [
    {
        "$lookup": {
            "from": "fincas",
            "localField": "finca_id",
            "foreignField": "_id",
            "as": "datos_finca"
        }
    },
    {
        "$group": {
            "_id": "$estado",
            "total_despachos": {"$sum": 1},
            "total_cajas": {"$sum": "$cajas_despachadas"},
            "suma_valor_usd": {"$sum": "$valor_usd_total"},
            "promedio_valor_usd": {"$avg": "$valor_usd_total"},
            "promedio_temp_c": {"$avg": "$temperatura_c"}
        }
    },
    {"$sort": {"total_cajas": -1}}
]

for fila in db.despachos_puerto.aggregate(pipeline):
    fila["suma_valor_usd"] = round(fila["suma_valor_usd"], 2)
    fila["promedio_valor_usd"] = round(fila["promedio_valor_usd"], 2)
    fila["promedio_temp_c"] = round(fila["promedio_temp_c"], 2)
    print(fila)
