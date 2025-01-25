from flask import Flask ,render_template,request,redirect,url_for

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
            password=request.form['password']
            print(email,password) 

            #siempre a la conexion  a la base de datos usar el try 
            try:
                cur=mysql.connection.cursor()
                print("dentro del trai",email,password)
                cur.execute('SELECT * FROM usuarios WHERE email=%s and password=%s',(email,password))
                user=cur.fetchone()
                #print("usuario",user[0])
            
                if user:
                    return redirect(url_for('miperfil'))
                else:
                    return "usuario no valido "
                
            except Exception as e:
                return f"ha ocurrido {e}"  
        else:
            #no quiero salirme de la ruta 
            return render_template('login.html')



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
        #creamos la conexion con la base de datos 
        cur=mysql.connection.cursor()
        cur.execute('Insert into usuarios(nombre,apellidos,email,password) values (%s,%s,%s,%s)',(nombre,apellidos,email,password))
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