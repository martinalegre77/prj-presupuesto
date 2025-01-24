from tinydb import TinyDB, Query

# Creación de las tablas de la bases de datos
db_bebidas = TinyDB('db/bebidas.json')
db_tragos = TinyDB('db/tragos.json')
db_postres = TinyDB('db/postres.json')
db_presupuesto_bebida = TinyDB('db/presupuesto_bebida.json')
db_presupuesto_postre = TinyDB('db/presupuesto_postre.json')
db_presupuesto_general = TinyDB('db/presupuesto_general.json')

db_counters = TinyDB('db/counters.json')  # Tabla para los contadores


# Inicializador de contadores
def initialize_counters():
    """Inicializa contadores para tablas si no existen."""
    for table in ['bebidas', 'tragos', 'postres', 'presupuesto_bebida', 'presupuesto_postre', 'presupuesto_general']:
        if not db_counters.search(Query().table == table):
            db_counters.insert({"table": table, "last_id": 0})


# Obtención del próximo ID autoincremental
def get_next_id(table_name):
    """Obtiene el próximo ID para una tabla específica."""
    result = db_counters.get(Query().table == table_name)
    if result:
        next_id = result['last_id'] + 1
        db_counters.update({'last_id': next_id}, Query().table == table_name)
        return next_id
    return 1


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


# Inicializar contadores si están vacíos
initialize_counters()


# Inicialización con datos de ejemplo
def initialize_databases():
    if len(db_bebidas) == 0:
        db_bebidas.insert({"id": get_next_id("bebidas"), "tipo": "vodka", "nombre": "smirnoff", "presentacion": 700, "precio_compra": 6090.0, "precio_venta": 9000.0})
        db_bebidas.insert({"id": get_next_id("bebidas"), "tipo": "piña colada", "nombre": "american club", "presentacion": 750, "precio_compra": 5591.0, "precio_venta": 9000.0})
        db_bebidas.insert({"id": get_next_id("bebidas"), "tipo": "licor de menta", "nombre": "cusenier", "presentacion": 700, "precio_compra": 4082.0, "precio_venta": 9000.0})
        db_bebidas.insert({"id": get_next_id("bebidas"), "tipo": "blue curacao", "nombre": "cusenier", "presentacion": 700, "precio_compra": 4985.0, "precio_venta": 9000.0})
        db_bebidas.insert({"id": get_next_id("bebidas"), "tipo": "licor de frutilla", "nombre": "cusenier", "presentacion": 700, "precio_compra": 4082.0, "precio_venta": 9000.0})
        db_bebidas.insert({"id": get_next_id("bebidas"), "tipo": "licor de durazno", "nombre": "cusenier", "presentacion": 700, "precio_compra": 4082.0, "precio_venta": 9000.0})
        db_bebidas.insert({"id": get_next_id("bebidas"), "tipo": "licor de chocolate", "nombre": "cusenier", "presentacion": 700, "precio_compra": 4082.0, "precio_venta": 9000.0})
        db_bebidas.insert({"id": get_next_id("bebidas"), "tipo": "licor de huevo", "nombre": "cusenier", "presentacion": 700, "precio_compra": 4082.0, "precio_venta": 9000.0})
        db_bebidas.insert({"id": get_next_id("bebidas"), "tipo": "licor de kiwi", "nombre": "la trastienda", "presentacion": 950, "precio_compra": 4930.0, "precio_venta": 9000.0})
        db_bebidas.insert({"id": get_next_id("bebidas"), "tipo": "granadina", "nombre": "cusenier", "presentacion": 750, "precio_compra": 4249.0, "precio_venta": 9000.0})
        db_bebidas.insert({"id": get_next_id("bebidas"), "tipo": "gaseosa limón", "nombre": "baggio", "presentacion": 1000, "precio_compra": 1000.0, "precio_venta": 3000.0})
        db_bebidas.insert({"id": get_next_id("bebidas"), "tipo": "jugo de naranja", "nombre": "bio frut", "presentacion": 1000, "precio_compra": 1575.0, "precio_venta": 4500.0})
        db_bebidas.insert({"id": get_next_id("bebidas"), "tipo": "tequila", "nombre": "sol azteca", "presentacion": 1000, "precio_compra": 5500.0, "precio_venta": 15000.0})
        db_bebidas.insert({"id": get_next_id("bebidas"), "tipo": "whisky", "nombre": "white horse", "presentacion": 750, "precio_compra": 12405.0, "precio_venta": 20000.0})
        db_bebidas.insert({"id": get_next_id("bebidas"), "tipo": "whisky", "nombre": "old smuggler", "presentacion": 750, "precio_compra": 7622.0, "precio_venta": 15000.0})

    
    if len(db_tragos) == 0:
        db_tragos.insert({"id": get_next_id("tragos"), "nombre": "criptonita", "cantidad_ingredientes": 3, "ingredientes": [
            {"bebida_id": 1, "cantidad": 50},
            {"bebida_id": 2, "cantidad": 35},
            {"bebida_id": 3, "cantidad": 15}
            ]})
        db_tragos.insert({"id": get_next_id("tragos"), "nombre": "cielito lindo", "cantidad_ingredientes": 3, "ingredientes": [
            {"bebida_id": 1, "cantidad": 50},
            {"bebida_id": 2, "cantidad": 35},
            {"bebida_id": 4, "cantidad": 15}
            ]})
        db_tragos.insert({"id": get_next_id("tragos"), "nombre": "pantera rosa", "cantidad_ingredientes": 3, "ingredientes": [
            {"bebida_id": 1, "cantidad": 50},
            {"bebida_id": 2, "cantidad": 35},
            {"bebida_id": 10, "cantidad": 15}
            ]})
        db_tragos.insert({"id": get_next_id("tragos"), "nombre": "piel de iguana", "cantidad_ingredientes": 3, "ingredientes": [
            {"bebida_id": 1, "cantidad": 50},
            {"bebida_id": 9, "cantidad": 30},
            {"bebida_id": 11, "cantidad": 20}
            ]})
        db_tragos.insert({"id": get_next_id("tragos"), "nombre": "tequila sunrise", "cantidad_ingredientes": 2, "ingredientes": [
            {"bebida_id": 13, "cantidad": 50},
            {"bebida_id": 12, "cantidad": 50}
            ]})
        db_tragos.insert({"id": get_next_id("tragos"), "nombre": "sex on the beach", "cantidad_ingredientes": 4, "ingredientes": [
            {"bebida_id": 1, "cantidad": 30},
            {"bebida_id": 6, "cantidad": 10},
            {"bebida_id": 12, "cantidad": 30},
            {"bebida_id": 10, "cantidad": 30}
            ]})
    
    if len(db_postres) == 0:
        db_postres.insert({"id": get_next_id("postres"), "tipo": "tarta", "nombre": "cheesecake", "precio_costo": 20.0, "precio_venta": 35.0, "presentacion": "Porción"})
    
    if len(db_presupuesto_bebida) == 0:
        db_presupuesto_bebida.insert({"id": get_next_id("presupuesto_bebida"), "detalle": "Presupuesto inicial bebida", "total": 100.0})
    
    if len(db_presupuesto_postre) == 0:
        db_presupuesto_postre.insert({"id": get_next_id("presupuesto_postre"), "detalle": "Presupuesto inicial postre", "total": 50.0})
    
    if len(db_presupuesto_general) == 0:
        db_presupuesto_general.insert({"id": get_next_id("presupuesto_general"), "detalle": "Presupuesto general", "total": 150.0})


initialize_databases()