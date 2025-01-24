from db_manager import get_db_instance, Query, get_next_id

# Modelo base
class BaseModel:
    def __init__(self, table_name):
        self.db = get_db_instance(table_name)
        self.query = Query()
        self.table_name = table_name
    
    def create(self, data):
        """Crea un nuevo registro con ID autoincremental."""
        data['id'] = get_next_id(self.table_name)  # Obtener el próximo ID autoincremental
        return self.db.insert(data)
    
    def read_all(self):
        """Obtiene todos los registros."""
        return self.db.all()
    
    def read_by_id(self, record_id):
        """Obtiene un registro por ID."""
        return self.db.get(self.query.id == record_id)
    
    def read_by_name(self, kind, name):  
        """Obtiene un registro por Tipo y Nombre."""  
        return self.db.search((self.query.tipo == kind) & (self.query.nombre == name))
    
    def update(self, record_id, updates):
        """Actualiza un registro por ID."""
        return self.db.update(updates, self.query.id == record_id)
    
    def delete(self, record_id):
        """Elimina un registro por ID."""
        return self.db.remove(self.query.id == record_id)

# Modelo Bebidas
class BebidasModel(BaseModel):
    def __init__(self):
        super().__init__('bebidas')

# Modelo Tragos
class TragosModel(BaseModel):
    def __init__(self):
        super().__init__('tragos')

# Modelo Postres
class PostresModel(BaseModel):
    def __init__(self):
        super().__init__('postres')

# Modelo Presupuesto Bebida
class PresupuestoBebidaModel(BaseModel):
    def __init__(self):
        super().__init__('presupuesto_bebida')

# Modelo Presupuesto Postre
class PresupuestoPostreModel(BaseModel):
    def __init__(self):
        super().__init__('presupuesto_postre')

# Modelo Presupuesto General
class PresupuestoGeneralModel(BaseModel):
    def __init__(self):
        super().__init__('presupuesto_general')