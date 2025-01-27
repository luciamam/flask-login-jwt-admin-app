from flask import Flask ,render_template,request,redirect,url_for

#para el hahsin de las contraseñas en la base datos 
from werkzeug.security import generate_password_hash ,check_password_hash

#para usar mysql y os 
from flask_mysqldb import   MySQL
from dotenv import load_dotenv
from os import getenv
import os

load_dotenv



app=Flask(__name__)

#esto tiene que estar aqui siempre 
app.config['MYSQL_HOST']=getenv('MYSQL_HOST')
app.config['MYSQL_USER']=getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD']=getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB']=getenv('MYSQL_DB')
app.secret_key=os.getenv('SECRET_KEY')


#esto indica que aplicacion flask usara mysql 
mysql=MySQL(app)




#RUTA RAIZ noa tiene que tiene que redigir a la ruta login de alli usamos el redirect 
@app.route('/',methods=['GET'])
def inicio():
        return redirect(url_for('login'))




#la ruta /login nos muestra el formulario (renderiza el template .Login) y a la vez procesamos los datos este template 
# por eso usamos los dos metodos  GET Y POST 
@app.route('/login',methods=['GET','POST'])
def login():
        #para recoger datos del formaulario 
        if request.method=='POST':
            email=request.form['email']
            password_in=request.form['password']
            ##voy conectar la base de datos 
            try:
                cur=mysql.connection.cursor()
                #hacemos una consulta  y asi obtenemos el usuaroio 
                cur.execute('SELECT * FROM usuarios WHERE email=%s',(email,))
                user=cur.fetchone()

                #siempre asegurarnos de que el usuario no sea NONE
                if not user:
                    return "no existe el usuario "
                

                #ahora vamos a recueperar la contraseña haseada del usuario 
                hashed_password=user[4]

                #condicion para saber si la contraña resupera hasheada es igual a la que se introduce ahora 
                if check_password_hash(hashed_password,password_in):
                    return redirect(url_for('miperfil'))
                else:
                    return "constresña invalida"

            except Exception as e:
                return "ha ocurrido un error, {}".format(e)
            

            finally:
                cur.close()
        

        else:
            return  render_template('login.html')







#ruta registrarse 
@app.route('/registrarse',methods=['GET','POST'])
def registro():
    #si el metodo es POST insertamos datos los datos en la base de datos 
    if request.method=='POST':
        nombre=request.form['nombre']
        apellidos=request.form['apellidos']
        email=request.form['email']
        password=request.form['password']
        #print(nombre,apellidos,email,password)

        #****************encripatr una contraseña
        #vamos a hashear la base de datos en que caso de ataque a mi base datos
        hash_password=generate_password_hash(password,salt_length=16)
        cur=mysql.connection.cursor()
        cur.execute('Insert into usuarios(nombre,apellidos,email,password) values (%s,%s,%s,%s)',(nombre,apellidos,email,hash_password))
        mysql.connection.commit()

        return redirect(url_for('perfil',nombre=nombre))
    else:
        return render_template('Registrarse.html')



#ruta perfil 
@app.route('/miperfil')
def miperfil():
    return render_template ('Miperfil.html')


#ruta 
@app.route('/perfil/<string:nombre>',methods=['GET'])
def perfil(nombre):
    return render_template('Perfil.html',nombre=nombre)


if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=3000)