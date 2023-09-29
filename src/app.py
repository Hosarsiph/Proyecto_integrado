from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_login import LoginManager,login_user, logout_user, login_required
import psycopg2
from config import *
from Funciones import imp_excel

#modelos

from models.ModelUser import ModelUser # modelo de usuarios 
from models.dbModel import * # modelo de la base de datos


#entities
from models.entities.Users import User # entidad usuario

#estableciondo la conección.
def conexion():
    conn = psycopg2.connect(**db_config)
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Jvm2OrrMd4QaRNHzvtgqfxyLir8' # llave secreta
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Asea2023@localhost/siset'# conexion a la base
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db.init_app(app) # inicializacion de la base
    
login_manager_app = LoginManager(app) # Configuracion de login
login_manager_app.login_view = "login" # 

# Funcion para mantener la sesion del usuario activo
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db,id)

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User(0,request.form['username'],request.form['password'])
        logged_user = ModelUser.login(db,user)
        if logged_user != None:
            if logged_user.pswd:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Contrasena incorrecta")
                return render_template('auth/login.html')
        else:
            flash('usuario no encontrado')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('inicio/home.html')

@app.route('/ingreso/')
@login_required
def ingresos():
    ti = Tip_ing.query.all() 
    asu = Asunto.query.all() 
    mat = Materia.query.all()
    return render_template('inicio/ingreso.html',ti=ti,asu=asu,mat=mat)

@app.route('/ingreso/<materia_id>')
@login_required
def opc(materia_id):
    tramites = Tramite.query.filter_by(cvetramite = materia_id).all()
    tramites = [{'cvetramite': t.cvetramite,'cofemer':t.cofemer} for t in tramites]
    print(tramites)
    return jsonify(tramites)

@app.route('/consulta',methods=['GET','POST'])
@login_required
def consulta():
    tip_ingr = Tip_ing.query.all() # consulta a tramite
    items = Materia.query.all()# consulta a materia
    dir_gen = Dir_Gen.query.filter_by(cve_unidad=2).all()# consulta a direccion general
    return render_template('inicio/consulta.html', items=items, tip_ingr=tip_ingr, dir_gen=dir_gen)

@app.route('/tabla', methods=('GET','POST'))
@login_required
def users():
    con_tipoingreso = ""
    if request.method == 'POST':# verifica si el request es por medio de post 
        f1 = request.form['fecha_inicial']# variable de fecha inicial
        f2 = request.form['fecha_final']# variable de fecha final
        mat = request.form['materia']# variable de materia
        ti = request.form['ta']# variable con condiciones de tipo ingreso
        dg = request.form['dg']# variables con condiciones de direccion general
    conn = conexion()
    cursor = conn.cursor()
    #consulta inicial esto es para la tabla que se visualiza en html 
    con_inicial = "SELECT" + \
    " seguimiento.fsolicitud," + \
    " cat_tipo_ingreso.tipo_ingreso," + \
    "seguimiento.bitacora_expediente," + \
    " cat_materia.materia," + \
    " seguimiento.rnomrazonsolcial," + \
    " dir_gral.siglas," + \
    " cat_estatus.estatus" + \
    " FROM seguimiento" + \
    " LEFT JOIN cat_tipo_ingreso ON seguimiento.tipo_ingreso = cat_tipo_ingreso.id" + \
    " LEFT JOIN cat_tipo_asunto ON seguimiento.tipo_asunto = cat_tipo_asunto.id" + \
    " LEFT JOIN cat_descripcion ON seguimiento.descripcion = cat_descripcion.id" + \
    " LEFT JOIN cat_materia ON seguimiento.materia = cat_materia.id" + \
    " LEFT JOIN cat_tramites ON seguimiento.tramite = cat_tramites.idtram" + \
    " LEFT JOIN cat_tipoinstalacion  ON seguimiento.tipoinstalacion = cat_tipoinstalacion.id" + \
    " LEFT JOIN cat_actividad ON seguimiento.cve_actividad = cat_actividad.id" + \
    " LEFT JOIN cat_personal AS evaluador ON seguimiento.nevaluador = evaluador.idpers" + \
    " LEFT JOIN cat_personal AS aar ON seguimiento.persona_ingresa = aar.idpers" +\
    " LEFT JOIN dir_gral ON seguimiento.dirgralfirma = dir_gral.id" + \
    " LEFT JOIN cat_sitact ON seguimiento.situacionactualtram = cat_sitact.id" + \
    " LEFT JOIN cat_sentido_resolucion ON seguimiento.sentido_resolucion = cat_sentido_resolucion.id" + \
    " LEFT JOIN cat_estatus ON seguimiento.estatus_tramite = cat_estatus.id" + \
    " WHERE"

    # string con la condicion de fecha
    con_fechas = "(seguimiento.fsolicitud >= " + "'" + f1 + "'" + " and seguimiento.fsolicitud <= " + "'" + f2 + "')"
    # string con condiciones tipo de ingreso
    if ti != "":
        con_tipoingreso = ti +")"
    # string con dicion de materia
    if mat != "TODO":
        con_materia = "and cat_materia.materia ='" + mat + "'"
    else:
        con_materia = ""
    # string con las condiciones de direccion general
    if dg !="":
        con_dirgeneral =dg + ")"
    else:
        con_dirgeneral = ""
    # string con la sentencia final completa
    query = con_inicial + " " + con_fechas + " " +con_tipoingreso + " " + con_materia + " " + con_dirgeneral
    # string con condiciones para la funcion de exportar excel
    con_where = con_fechas + " " +con_tipoingreso + " " + con_materia + " " + con_dirgeneral
    # funcion para realizar una consulta y crear un archivo en excel para su descarga
    imp_excel(con_where)
    #
    cursor.execute(query)
    users = cursor.fetchall()      
    print(query)
    conn.close()
    return render_template('tablas/tabla.html', users=users)

@app.route('/download')
@login_required
def Download_File():
    #ruta para descargar el archivo
    PATH='source/Consulta.xlsx'
    return send_file(PATH,as_attachment=True,)

@app.route('/turnado')
@login_required
def turnado():
    return render_template('inicio/turnado.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html')

def status_401(error):
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(401,status_401)
    app.run()