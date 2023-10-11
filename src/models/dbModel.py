"""Este .py contiene los modelos de las bases de datos o mas bien dicho las tablas que 
usara nuestro programa se tiene que definir con las columnas que usaremos de cada tabla
o definir toda la tabla 
nota: tiene que ser el mismo nombre de la columna de la base de datos para que pueda
realizar la sentencia SQL de manera correcta.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tip_ing(db.Model): #------------------tipo ingreso----------------------
    __tablename__ = 'cat_tipo_ingreso'
   
    id = db.Column(db.Integer, primary_key=True)
    tipo_ingreso = db.Column(db.String(255))
    
    def __init__(self,id,tipo_ingreso):
        self.id = id
        self.tipo_ingreso = tipo_ingreso

class Asunto(db.Model): #------------------tipo asunto----------------------
    __tablename__ = 'cat_tipo_asunto'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(255))
    
    def __init__(self,id,tipo):
        self.id = id
        self.tipo = tipo

class Materia(db.Model): #------------------Materia----------------------
    __tablename__ = 'cat_materia'

    id = db.Column(db.Integer, primary_key=True)
    materia = db.Column(db.String(255))
    
    def __init__(self,id,materia):
        self.id = id
        self.materia = materia

class Tramite(db.Model): #------------------Tramite----------------------
    __tablename__ = 'cat_tramites'

    idtram = db.Column(db.Integer, primary_key=True)
    cvetramite = db.Column(db.String(255))
    cofemer = db.Column(db.String(255))
    
    def __init__(self,idtram,cvetramite,cofemer):
        self.idtram = idtram
        self.cvetramite = cvetramite
        self.cofemer = cofemer

class Descripcion(db.Model): #------------------Descripcion----------------------
    __tablename__ = 'cat_descripcion'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255))

    def __init__(self,id,descripcion):
        self.id = id
        self.descripcion = descripcion

class Procedencia(db.Model): #------------------Procedencia----------------------
    __tablename__ = 'cat_procedencia'

    id = db.Column(db.Integer, primary_key=True)
    procedencia = db.Column(db.String(255))

    def __init__(self,id,procedencia):
        self.id = id
        self.procedencia = procedencia

class Cad_val(db.Model): #------------------Cadena de Valor----------------------
    __tablename__ = 'cat_cadena_valor'

    id = db.Column(db.Integer, primary_key=True)
    cadena_valor = db.Column(db.String(255))

    def __init__(self,id,cadena_valor):
        self.id = id
        self.cadena_valor = cadena_valor

class Tip_per(db.Model): #------------------Tipo persona----------------------
    __tablename__ = 'cat_tipopersona'

    idtpers = db.Column(db.Integer, primary_key=True)
    tipo_persona = db.Column(db.String(255))

    def __init__(self,idtpers,tipo_persona):
        self.idtpers = idtpers
        self.tipo_persona = tipo_persona

class Dir_Gen(db.Model): #------------------Direccion general----------------------
    __tablename__ = 'cat_dirgeneral'

    id = db.Column(db.Integer, primary_key=True)
    direccion_general = db.Column(db.String(255))
    siglas = db.Column(db.String(255))
    cve_unidad = db.Column(db.Integer)
    
    def __init__(self,id,direccion_general,siglas,cve_unidad):
        self.id = id
        self.direccion_general = direccion_general
        self.siglas = siglas
        self.cve_unidad = cve_unidad

class Personal(db.Model): #------------------Personal----------------------
    __tablename__ = 'cat_personal'

    idpers = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    active = db.Column(db.String(2))
    
    def __init__(self,idpers,nombre,active):
        self.idpers = idpers
        self.nombre = nombre
        self.active = active
               
class Seguimiento(db.Model): #------------------Seguimiento----------------------
    __tablename__ = 'seguimiento'

    bitacora_expediente = db.Column(db.String(100), primary_key=True)
    rnomrazonsolcial = db.Column(db.String(255))
    tipo_ingreso = db.Column(db.Integer)
    tramite = db.Column(db.Integer)
    materia = db.Column(db.Integer)
    turnado_da = db.Column(db.Integer)
    cve_procedencia = db.Column(db.Integer)
    cadena_valor = db.Column(db.Integer)
    tipopersonalidad = db.Column(db.Integer)
    dirgralfirma = db.Column(db.Integer)

    
    def __init__(self,bitacora_expediente,rnomrazonsolcial,tipo_ingreso,materia,
                 tramite,turnado_da,cve_procedencia,cadena_valor,
                 tipopersonalidad,dirgralfirma):

        self.bitacora_expediente = bitacora_expediente
        self.rnomrazonsolcial = rnomrazonsolcial
        self.tipo_ingreso = tipo_ingreso
        self.tramite = tramite
        self.materia = materia
        self.turnado_da = turnado_da
        self.cve_procedencia = cve_procedencia
        self.cadena_valor = cadena_valor
        self.tipopersonalidad = tipopersonalidad
        self.dirgralfirma = dirgralfirma
        self.turnado_da = turnado_da