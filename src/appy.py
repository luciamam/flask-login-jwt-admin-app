from flask import Flask ,render_template,request,redirect,url_for

app=Flask(__name__)



@app.route('/',methods=['GET'])
def inicio():
        return render_template('login.html')


@app.route('/login',methods=['POST'])
def login():
        email=request.form['email']
        password=request.form['password']
        print(email,password)
        ## consultare la base de datos  si este usuario existe 
        return "datos insertados"



@app.route('/registrarse',methods=['GET','POST'])
def registro():
    if request.method=='POST':
        nombre=request.form['nombre']
        apellidos=request.form['apellidos']
        email=request.form['email']
        password=request.form['password']

        print(nombre,apellidos,email,password)

        #lo guardare en la base de datos  estos datos que recoja de  aqui  
    
         # return "metodo post " esta es la respuesta tipica de flask pero ahora nosotros le queremos  a enviar a una ruta perfil 
         
        return redirect(url_for('perfil',nombre=nombre))
    else:
        return render_template('Registrarse.html')
        
   

@app.route('/perfil/<string:nombre>',methods=['GET'])
def perfil(nombre):
    return render_template('Perfil.html',nombre=nombre)


if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=3000)