from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://Citas_Medicas:123@DESKTOP-VF5IOEU/Citas_Medicas_T03?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelos (simplificados)
class Paciente(db.Model):
    __tablename__ = 'Pacientes'
    id_paciente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(20), nullable=False)

class Doctor(db.Model):
    __tablename__ = 'Doctores'
    id_doctor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)

class Cita(db.Model):
    __tablename__ = 'Citas'
    id_cita = db.Column(db.Integer, primary_key=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey('Pacientes.id_paciente'))
    id_doctor = db.Column(db.Integer, db.ForeignKey('Doctores.id_doctor'))
    fecha_hora = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(20), nullable=False)

# Rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pacientes')
def listar_pacientes():
    pacientes = Paciente.query.all()
    return render_template('pacientes.html', pacientes=pacientes)

@app.route('/pacientes/nuevo', methods=['GET', 'POST'])
def nuevo_paciente():
    if request.method == 'POST':
        paciente = Paciente(
            nombre=request.form['nombre'],
            contacto=request.form['contacto']
        )
        db.session.add(paciente)
        db.session.commit()
        return redirect(url_for('listar_pacientes'))
    return render_template('nuevo_paciente.html')

@app.route('/doctores')
def listar_doctores():
    doctores = Doctor.query.all()
    return render_template('doctores.html', doctores=doctores)

@app.route('/doctores/nuevo', methods=['GET', 'POST'])
def nuevo_doctor():
    if request.method == 'POST':
        doctor = Doctor(
            nombre=request.form['nombre'],
            especialidad=request.form['especialidad']
        )
        db.session.add(doctor)
        db.session.commit()
        return redirect(url_for('listar_doctores'))
    return render_template('nuevo_doctor.html')

@app.route('/citas/nueva', methods=['GET', 'POST'])
def nueva_cita():
    if request.method == 'POST':
        cita = Cita(
            id_paciente=request.form['paciente_id'],
            id_doctor=request.form['doctor_id'],
            fecha_hora=datetime.strptime(request.form['fecha_hora'], '%Y-%m-%dT%H:%M'),
            estado='Pendiente'
        )
        db.session.add(cita)
        db.session.commit()
        return redirect(url_for('index'))
    
    pacientes = Paciente.query.all()
    doctores = Doctor.query.all()
    return render_template('nueva_cita.html', pacientes=pacientes, doctores=doctores)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea tablas si no existen
    app.run(debug=True)