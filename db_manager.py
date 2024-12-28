from tinydb import TinyDB, Query

# Conexión a las bases de datos
db_bebidas = TinyDB('db/bebidas.json')
db_tragos = TinyDB('db/tragos.json')
db_postres = TinyDB('db/postres.json')
db_presupuesto_bebida = TinyDB('db/presupuesto_bebida.json')
db_presupuesto_postre = TinyDB('db/presupuesto_postre.json')
db_presupuesto_general = TinyDB('db/presupuesto_general.json')

db_counters = TinyDB('db/counters.json')  # Tabla para los contadores

# Inicializar contadores
def initialize_counters():
    """Inicializa contadores para tablas si no existen."""
    for table in ['bebidas', 'tragos', 'postres', 'presupuesto_bebida', 'presupuesto_postre', 'presupuesto_general']:
        if not db_counters.search(Query().table == table):
            db_counters.insert({"table": table, "last_id": 0})

# Obtener el próximo ID autoincremental
def get_next_id(table_name):
    """Obtiene el próximo ID para una tabla específica."""
    result = db_counters.get(Query().table == table_name)
    if result:
        next_id = result['last_id'] + 1
        db_counters.update({'last_id': next_id}, Query().table == table_name)
        return next_id
    return 1


# Inicialización con datos de ejemplo
def initialize_databases():
    if len(db_bebidas) == 0:
        db_bebidas.insert({"id": 1, "tipo": "vodka", "nombre": "Smirnoff", "presentacion": 700, "precio_compra": 6090.0, "precio_venta": 9000.0})
        db_bebidas.insert({"id": 2, "tipo": "piña colada", "nombre": "American Club", "presentacion": 750, "precio_compra": 5591.0, "precio_venta": 9000.0})
        db_bebidas.insert({"id": 3, "tipo": "Licor de Menta", "nombre": "Cusenier", "presentacion": 700, "precio_compra": 4082.0, "precio_venta": 9000.0})
        db_bebidas.insert({"id": 4, "tipo": "Blue Curacao", "nombre": "Cusenier", "presentacion": 700, "precio_compra": 4985.0, "precio_venta": 9000.0})
        db_bebidas.insert({"id": 5, "tipo": "Licor de Frutilla", "nombre": "Cusenier", "presentacion": 700, "precio_compra": 4082.0, "precio_venta": 9000.0})
        db_bebidas.insert({"id": 6, "tipo": "Licor de Durazno", "nombre": "Cusenier", "presentacion": 700, "precio_compra": 4082.0, "precio_venta": 9000.0})
        db_bebidas.insert({"id": 7, "tipo": "Licor de Chocolate", "nombre": "Cusenier", "presentacion": 700, "precio_compra": 4082.0, "precio_venta": 9000.0})
        db_bebidas.insert({"id": 8, "tipo": "Licor de Huevo", "nombre": "Cusenier", "presentacion": 700, "precio_compra": 4082.0, "precio_venta": 9000.0})
        db_bebidas.insert({"id": 9, "tipo": "Licor de Kiwi", "nombre": "La Trastienda", "presentacion": 950, "precio_compra": 4930.0, "precio_venta": 9000.0})
        db_bebidas.insert({"id": 10, "tipo": "Granadina", "nombre": "Cusenier", "presentacion": 750, "precio_compra": 4249.0, "precio_venta": 9000.0})
        db_bebidas.insert({"id": 11, "tipo": "Gaseosa Limón", "nombre": "Baggio", "presentacion": 1000, "precio_compra": 1000.0, "precio_venta": 3000.0})
        db_bebidas.insert({"id": 12, "tipo": "Jugo de Naranja", "nombre": "BioFrut", "presentacion": 1000, "precio_compra": 1575.0, "precio_venta": 4500.0})
        db_bebidas.insert({"id": 13, "tipo": "Tequila", "nombre": "Sol Azteca", "presentacion": 1000, "precio_compra": 5500.0, "precio_venta": 15000.0})
        db_bebidas.insert({"id": 14, "tipo": "Whisky", "nombre": "White Horse", "presentacion": 750, "precio_compra": 12405.0, "precio_venta": 20000.0})
        db_bebidas.insert({"id": 15, "tipo": "Whisky", "nombre": "Old Smuggler", "presentacion": 750, "precio_compra": 7622.0, "precio_venta": 15000.0})

    
    if len(db_tragos) == 0:
        db_tragos.insert({"id": 1, "nombre": "Criptonita", "cantidad_ingredientes": 3, "ingredientes": [
            {"tipo": "vodka", "nombre": "Smirnoff", "cantidad": 50},
            {"tipo": "piña colada", "nombre": "American Club", "cantidad": 35},
            {"tipo": "Licor de Menta", "nombre": "Cusenier", "cantidad": 15}
            ]})
        db_tragos.insert({"id": 2, "nombre": "Cielito lindo", "cantidad_ingredientes": 3, "ingredientes": [
            {"tipo": "vodka", "nombre": "Smirnoff", "cantidad": 50},
            {"tipo": "piña colada", "nombre": "American Club", "cantidad": 35},
            {"tipo": "Blue Curacao", "nombre": "Cusenier", "cantidad": 15}
            ]})
        db_tragos.insert({"id": 3, "nombre": "Pantera Rosa", "cantidad_ingredientes": 3, "ingredientes": [
            {"tipo": "vodka", "nombre": "Smirnoff", "cantidad": 50},
            {"tipo": "piña colada", "nombre": "American Club", "cantidad": 35},
            {"tipo": "Granadina", "nombre": "Cusenier", "cantidad": 15}
            ]})
        db_tragos.insert({"id": 4, "nombre": "Piel de Iguana", "cantidad_ingredientes": 3, "ingredientes": [
            {"tipo": "vodka", "nombre": "Smirnoff", "cantidad": 50},
            {"tipo": "Licor de Kiwi", "nombre": "La Trastienda", "cantidad": 30},
            {"tipo": "Gaseosa Limón", "nombre": "Baggio", "cantidad": 20}
            ]})
        db_tragos.insert({"id": 5, "nombre": "Tequila Sunrise", "cantidad_ingredientes": 2, "ingredientes": [
            {"tipo": "Tequila", "nombre": "Sol Azteca", "cantidad": 50},
            {"tipo": "Jugo de Naranja", "nombre": "BioFrut", "cantidad": 50}
            ]})
        db_tragos.insert({"id": 6, "nombre": "Sex on the beach", "cantidad_ingredientes": 4, "ingredientes": [
            {"tipo": "vodka", "nombre": "Smirnoff", "cantidad": 30},
            {"tipo": "Licor de Durazno", "nombre": "Cusenier", "cantidad": 10},
            {"tipo": "Jugo de Naranja", "nombre": "BioFrut", "cantidad": 30},
            {"tipo": "Granadina", "nombre": "Cusenier", "cantidad": 30}
            ]})
    
    if len(db_postres) == 0:
        db_postres.insert({"id": 1, "tipo": "Tarta", "nombre": "Cheesecake", "precio_costo": 20.0, "precio_venta": 35.0, "presentacion": "Porción"})
    
    if len(db_presupuesto_bebida) == 0:
        db_presupuesto_bebida.insert({"id": 1, "detalle": "Presupuesto inicial bebida", "total": 100.0})
    
    if len(db_presupuesto_postre) == 0:
        db_presupuesto_postre.insert({"id": 1, "detalle": "Presupuesto inicial postre", "total": 50.0})
    
    if len(db_presupuesto_general) == 0:
        db_presupuesto_general.insert({"id": 1, "detalle": "Presupuesto general", "total": 150.0})

# Funciones comunes para la base de datos
def get_db_instance(table_name):
    """Devuelve la instancia correcta de la base de datos."""
    db_map = {
        "bebidas": db_bebidas,
        "tragos": db_tragos,
        "postres": db_postres,
        "presupuesto_bebida": db_presupuesto_bebida,
        "presupuesto_postre": db_presupuesto_postre,
        "presupuesto_general": db_presupuesto_general
    }
    return db_map.get(table_name)

# Inicializar bases de datos si están vacías
initialize_databases()

# Inicializar contadores si están vacíos
initialize_counters()
