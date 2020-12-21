from flask import Flask, render_template, request ,url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required,logout_user
from datetime import date
from datetime import datetime
from datetime import timedelta  




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key="secret123"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

#classes (user,doctor,patient,nurse,appointment,depratment,pharmacist)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True,)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, name,username,password):
        self.name=name
        self.username=username
        self.password=password
  
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True,)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), unique=True, nullable=False)
    adress = db.Column(db.String(120), nullable=False)
    specialty = db.Column(db.String(120), nullable=False)     
    tel = db.Column(db.String(8), nullable=False)

    def __init__(self,first_name,last_name,adress,specialty,tel):
        self.first_name=first_name
        self.last_name=last_name
        self.adress=adress
        self.specialty=specialty
        self.tel=tel

class Nurse(db.Model):
    id = db.Column(db.Integer, primary_key=True,)
    first_name_N = db.Column(db.String(120), nullable=False)
    last_name_N = db.Column(db.String(120), unique=True, nullable=False)
    adress_N = db.Column(db.String(120), nullable=False)
    tel_N = db.Column(db.String(8), nullable=False)
    def __init__(self,first_name_N,last_name_N,adress_N,tel_N):
        self.first_name_N=first_name_N
        self.last_name_N=last_name_N
        self.adress_N=adress_N
        self.tel_N=tel_N

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True,)
    first_name_p = db.Column(db.String(120), nullable=False)
    last_name_p = db.Column(db.String(120), unique=True, nullable=False)
    age_p= db.Column(db.Integer, nullable=False)     
    genre_p = db.Column(db.String(50), nullable=False)
    adress_p= db.Column(db.String(120), nullable=False)
    tel_p= db.Column(db.String(8), nullable=False)

    def __init__(self,first_name_p,last_name_p,age_p,genre_p,adress_p,tel_p):
        self.first_name_p=first_name_p
        self.last_name_p=last_name_p
        self.age_p=age_p
        self.genre_p=genre_p
        self.adress_p=adress_p
        self.tel_p=tel_p

class Pharmacist(db.Model):
    id = db.Column(db.Integer, primary_key=True,)
    first_name_ph = db.Column(db.String(120), nullable=False)
    last_name_ph = db.Column(db.String(120), unique=True, nullable=False)
    adress_ph= db.Column(db.String(120), nullable=False)
    genre_ph = db.Column(db.String(50), nullable=False)
    tel_p= db.Column(db.String(8), nullable=False)

    def __init__(self,first_name_ph,last_name_ph,adress_ph,genre_ph,tel_p):
        self.first_name_ph=first_name_ph
        self.last_name_ph=last_name_ph
        self.adress_ph=adress_ph
        self.genre_ph=genre_ph
        self.tel_p=tel_p

class Depratment(db.Model):
    id = db.Column(db.Integer, primary_key=True,)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)
    status = db.Column(db.String(120), nullable=False)

    def __init__(self,name,description,status):
        self.name=name
        self.description=description
        self.status=status

class Appointment(db.Model):
    code= db.Column(db.Integer,primary_key=True)
    name_doctor = db.Column(db.String(120), nullable=False)
    name_patient = db.Column(db.String(120), unique=True, nullable=False)
    date= db.Column(db.DateTime(), nullable=False) 
    id_patient = db.Column(db.Integer)
    id_doctor = db.Column(db.Integer)
    def __init__(self,name_doctor,name_patient,date,id_patient,id_doctor):
        self.name_doctor=name_doctor
        self.name_patient=name_patient
        self.date=date
        self.id_patient=id_patient
        self.id_doctor=id_doctor
       
@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

# Index route log infro
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/login',methods = ['GET','POST'])
def log():
    if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user= User.query.filter_by(username=username,password=password).first()

            if user is not None:
                return redirect(url_for("home"))
            else:
                flash("Password or Username is invalid !","danger")
                return redirect(url_for("index"))

# Register route sign up
@app.route('/register', methods=['GET','POST'])
def register():
        if request.method == 'POST':
            name = request.form['name']
            username = request.form['username']
            password = request.form['password']
            user= User.query.filter_by(username=username).first()
            if user is not None:
                flash("Username is already exist !","danger")
                return redirect(url_for("register"))
            else:
                my_data = User(name, username, password)  
                db.session.add(my_data)
                db.session.commit()  
                flash('Your accout is created',"success")
                return redirect(url_for("index"))
        else:
            return render_template("register.html")
# home route 
@app.route('/home/')
def home():
    today = datetime.today().strftime('%Y-%m-%d-%H:%M')
    nbr_doctors = Doctor.query.count()
    nbr_patients = Patient.query.count()
    nbr_nurses = Nurse.query.count()
    nbr_app = Appointment.query.count()
    nbr_dept=Depratment.query.count()
    nbr_pharmacists = Pharmacist.query.count()
    return render_template("home.html",nbd=nbr_doctors,nbp=nbr_patients, nbn=nbr_nurses,nba=nbr_app,td=today,nbph=nbr_pharmacists,nb_d=nbr_dept)
@app.route('/home/profile')
def profile():
    return render_template("profile.html")
# Patients CRUD 
@app.route('/home/add_patient', methods=['GET','POST'])

def add_patient():
    if request.method =='POST':
        firstnamep = request.form['firstname']
        lastnamep = request.form['lastname']
        agep = request.form['age']
        genrep = request.form['sex']
        adressp = request.form['adress']
        telp = request.form['tel']
        data_patient = Patient(firstnamep, lastnamep, agep, genrep, adressp, telp)
        db.session.add(data_patient)
        db.session.commit()  
        flash("Patient added successeflly","success")
        return redirect(url_for("list_patients"))

@app.route('/home/list_patients/<id>/',methods=['GET','POST'])

def delete_patient(id):
    patient_data= Patient.query.get(id)
    db.session.delete(patient_data)
    db.session.commit()
    flash("Patient deleted successeflly","success")
    return redirect(url_for("list_patients"))

@app.route('/home/update_patient',methods=['GET','POST'])

def update_patient():
    if request.method=='POST':
         x= request.form['id']
         data_patient = Patient.query.get(x)
         data_appoinement = Appointment.query.filter_by(id_patient=x).first()
         data_patient.first_name_p= request.form['firstname']
         data_patient.last_name_p= request.form['lastname']
         data_patient.age_p= request.form['age']
         data_patient.genre_p= request.form['sex']
         data_patient.adress_p= request.form['adress']
         data_patient.tel_p= request.form['tel']
         data_appoinement.name_patient= request.form['lastname']
         list_patients= Patient.query.get(id)
         
         
         db.session.commit()
         flash("Patient updated successeflly","success")
         return redirect(url_for("list_patients"))

@app.route('/home/list_patients')

def list_patients():
    list_patients = Patient.query.all()
    return render_template("listpatients.html", patients=list_patients)

# Doctor crud
@app.route('/home/add_doctor', methods=['GET','POST'])

def add_doctor():  
    if request.method =='POST':
        firstname=request.form['first_name']
        lastname=request.form['last_name']
        adress=request.form['adress']
        specialty=request.form['specialty']
        tel=request.form['tel']
        data_doctor=Doctor(firstname,lastname,adress,specialty,tel)
        db.session.add(data_doctor)
        db.session.commit()
        flash('Doctor added successeflly','success')
        return redirect(url_for("list_doctors"))

@app.route('/home/list_doctors/<id>/',methods=['GET','POST'])

def delete_doctor(id):
    doctor_data= Doctor.query.get(id)
    db.session.delete(doctor_data)
    db.session.commit()
    flash("Doctor deleted successeflly","success")
    return redirect(url_for("list_doctors"))


@app.route('/home/update_doctor',methods=['GET','POST'])

def update_doctor():
    if request.method=='POST':
         y = request.form['id']
         data_doctor = Doctor.query.get(y)
         data_doctor.first_name= request.form['first_name']
         data_doctor.last_name= request.form['last_name']
         data_doctor.adress= request.form['adress']
         data_doctor.specialty= request.form['specialty']
         data_doctor.tel= request.form['tel']
         list_doctors= Doctor.query.get(id)
         db.session.commit()
         flash("Doctor updated successeflly","success")
         return redirect(url_for("list_doctors"))
    


@app.route('/home/list_doctors')
def list_doctors():
    list_doctors = Doctor.query.all()    
    list_departements = Depratment.query.filter_by(status="active").all()
    return render_template("listdoctors.html", doctors=list_doctors,departments=list_departements)


# Nurse crud
@app.route('/home/add_nurse', methods=['GET','POST'])
def add_nurse():  
    if request.method =='POST':
        firstname=request.form['first_name']
        lastname=request.form['last_name']
        adress=request.form['adress']
        tel=request.form['tel']
        data_nurse=Nurse(firstname,lastname,adress,tel)
        db.session.add(data_nurse)
        db.session.commit()
        flash('Nurse added successeflly','success')
        return redirect(url_for("list_nurses"))

@app.route('/home/list_nurses/<id>/',methods=['GET','POST'])
def delete_nurse(id):
    nurse_data= Nurse.query.get(id)
    db.session.delete(nurse_data)
    db.session.commit()
    flash("Nurse deleted successeflly","success")
    return redirect(url_for("list_nurses"))

@app.route('/home/update_nurse',methods=['GET','POST'])
def update_nurse():
    if request.method=='POST':
         data_nurse = Nurse.query.get(request.form['id'])
         data_nurse.first_name_N= request.form['firstname']
         data_nurse.last_name_N= request.form['lastname']
         data_nurse.age_N= request.form['adress']
         data_nurse.tel_N= request.form['tel']
         list_nurses= Nurse.query.get(id)
         db.session.commit()
         flash("Nurse updated successeflly","success")
         return redirect(url_for("list_nurses"))

@app.route('/home/list_nurses')
def list_nurses():
    list_nurses = Nurse.query.all()
    return render_template("listnurses.html", nurses=list_nurses)

# PharmacistsCrud
@app.route('/home/add_pharmacist', methods=['GET','POST'])
def add_pharmacist():  
    if request.method =='POST':
        firstname_ph=request.form['first_name']
        lastname_ph=request.form['last_name']
        adress_ph=request.form['adress_ph']
        genre_ph=request.form['sex_ph']
        tel_ph=request.form['tel_ph']

        data_ph=Pharmacist(firstname_ph,lastname_ph,adress_ph,genre_ph,tel_ph)
        db.session.add(data_ph)
        db.session.commit()
        flash('Pharmacist added successeflly','success')
        return redirect(url_for("list_pharmacist"))


@app.route('/home/list_pharmacist/<id>/',methods=['GET','POST'])

def delete_phar(id):
    phar_data= Pharmacist.query.get(id)
    db.session.delete(phar_data)
    db.session.commit()
    flash("Pharmacist deleted successeflly","success")
    return redirect(url_for("list_pharmacist"))

@app.route('/home/update_pharmacist',methods=['GET','POST'])
def update_pharmacist():
    if request.method=='POST':
         data_ph = Pharmacist.query.get(request.form['id'])
         data_ph.first_name_ph= request.form['first_name_ph']
         data_ph.last_name_ph= request.form['last_name_ph']
         data_ph.adress_ph= request.form['adress_ph']
         data_ph.genre_ph= request.form['sex_ph']
         data_ph.tel_p= request.form['tel_ph']
         list_pharmacist= Pharmacist.query.get(id)
         db.session.commit()
         flash("Pharmacist updated successeflly","success")
         return redirect(url_for("list_pharmacist"))

@app.route('/home/list_pharmacist')
def list_pharmacist():
    list_pharmacist = Pharmacist.query.all()
    return render_template("listpharmacist.html", pharmacists=list_pharmacist)

#DEPARTMENTS
@app.route('/home/add_departement', methods=['GET','POST'])
def add_departement():  
    if request.method =='POST':
        name_d=request.form['name']
        description=request.form['desc']
        status=request.form['status']
        data_dept=Depratment(name_d,description,status)
        db.session.add(data_dept)
        db.session.commit()
        flash('Department added successeflly','success')
        return redirect(url_for("list_departements"))

@app.route('/home/list_departements/<id>/',methods=['GET','POST'])
def delete_dept(id):
    dept_data= Depratment.query.get(id)
    db.session.delete(dept_data)
    db.session.commit()
    flash("Department deleted successeflly","success")
    return redirect(url_for("list_departements"))

@app.route('/home/update_dept',methods=['GET','POST'])
def update_dept():
    if request.method=='POST':
         data_dept = Depratment.query.get(request.form['id'])
         data_dept.name= request.form['name']
         data_dept.last_name_ph= request.form['desc']
         data_dept.adress_ph= request.form['status']
         list_departements= Depratment.query.get(id)
         db.session.commit()
         flash("Department updated successeflly","success")
         return redirect(url_for("list_departements"))


@app.route('/home/list_departements',methods=['GET','POST'])
def list_departements():
     list_departements = Depratment.query.all()
     return render_template("listdepartement.html",departments=list_departements)
#APPOINTMENTS 
@app.route('/home/add_app', methods=['GET','POST'])
def add_app():  
    if request.method =='POST':
        today = date.today()
        name_doctor=request.form['name_doctor']
        name_patient=request.form['name_patient']
        rdv_date=request.form['rdv_date']

        l= len(name_doctor)
        ll=len(name_patient)

        s=name_doctor.find(" ")
        nd=name_doctor[0:s]# lastname doctor
        ftd= name_doctor[s+1:l+1]#firstname doctor
       
    
        ss= name_patient.find(" ")
        np = name_patient[0:ss]# lastname patient
        ftp = name_patient[ss+1:ll+1]#firstname  patient
        w=str(rdv_date)+str(timedelta(minutes=60))
         
        

        docter= Doctor.query.filter_by(last_name=nd,first_name=ftd).first()
        patient = Patient.query.filter_by(last_name_p=np,first_name_p=ftp).first()
        app = Appointment.query.filter_by(id_patient=patient.id,id_doctor=docter.id,date=rdv_date).first()
        app1= Appointment.query.filter_by(date=rdv_date,id_doctor=docter.id).first()
        app2= Appointment.query.filter_by(date=rdv_date,id_patient=patient.id).first()

   
        
    

        if str(rdv_date)<str(today):
            flash("invalid date","danger")
            return redirect(url_for("list_appointments"))
        
      



        if app is not None: 
            flash("This appointment is already exist","warning")
            return redirect(url_for("list_appointments"))
        else:

            if app1 is not None:
                flash("This doctor had an appointment in the same date, Please choose an other date for an appointment ","warning")
                return redirect(url_for("list_appointments"))

            
                
            if app2 is not None:
                flash("This Patient had an appointment in the same date, Please choose an other date for an appointment ","warning")
                return redirect(url_for("list_appointments"))
            
               
            else: 
                
                data_app=Appointment(name_doctor,name_patient,rdv_date,patient.id,docter.id)  
                db.session.add(data_app)
                db.session.commit()
                flash('Appointment added successeflly','success')
                return redirect(url_for("list_appointments"))


@app.route('/home/list_appointments/<code>/',methods=['GET','POST'])
def delete_app(code):
    app_data= Appointment.query.get(code)
    db.session.delete(app_data)
    db.session.commit()
    flash("Appointment deleted successeflly","success")
    return redirect(url_for("list_appointments"))




@app.route('/home/list_appointments')
def list_appointments():     
    list_doctors=Doctor.query.all()
    list_patients = Patient.query.all()
    list_appointments = Appointment.query.all()
    return render_template("listappointments.html",doctors=list_doctors,patients=list_patients,appointments=list_appointments)



#log out
@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__=="__main__":
    app.run(debug=True)
    



    

