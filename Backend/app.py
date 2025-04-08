from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://Citas_Medicas:123@JHOSSUA/Citas_Medicas_T03?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelos
class Paciente(db.Model):
    __tablename__ = 'Pacientes'
    id_paciente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    direccion = db.Column(db.String(255), nullable=False)
    
    # Relación con citas
    citas = db.relationship('Cita', back_populates='paciente')

class Doctor(db.Model):
    __tablename__ = 'Doctores'
    id_doctor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    horario = db.Column(db.String(50), nullable=True)
    
    # Relación con citas
    citas = db.relationship('Cita', back_populates='doctor')

class Cita(db.Model):
    __tablename__ = 'Citas'
    id_cita = db.Column(db.Integer, primary_key=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey('Pacientes.id_paciente'))
    id_doctor = db.Column(db.Integer, db.ForeignKey('Doctores.id_doctor'))
    fecha_hora = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='Pendiente')
    
    # Relaciones
    paciente = db.relationship('Paciente', back_populates='citas')
    doctor = db.relationship('Doctor', back_populates='citas')

# Rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pacientes', methods=['GET', 'POST'])
def listar_pacientes():
    if request.method == 'POST':
        try:
            nuevo_paciente = Paciente(
                nombre=request.form['nombre'],
                edad=request.form.get('edad', None),
                telefono=request.form.get('telefono', None),
                direccion=request.form['direccion']
            )
            db.session.add(nuevo_paciente)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error al guardar paciente: {e}")
        
        return redirect(url_for('listar_pacientes'))
    
    pacientes = Paciente.query.order_by(Paciente.nombre).all()
    return render_template('pacientes.html', pacientes=pacientes)

@app.route('/doctores', methods=['GET', 'POST'])
def gestion_doctores():
    if request.method == 'POST':
        try:
            doctor = Doctor(
                nombre=request.form['nombre'],
                especialidad=request.form['especialidad'],
                telefono=request.form.get('telefono', None),
                horario=request.form.get('horario', None)
            )
            db.session.add(doctor)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error al guardar doctor: {e}")
        
        return redirect(url_for('gestion_doctores'))
    
    doctores = Doctor.query.order_by(Doctor.nombre).all()
    return render_template('doctores.html', doctores=doctores)

@app.route('/citas', methods=['GET', 'POST'])
def gestion_citas():
    if request.method == 'POST':
        try:
            cita = Cita(
                id_paciente=request.form['paciente_id'],
                id_doctor=request.form['doctor_id'],
                fecha_hora=datetime.strptime(request.form['fecha_hora'], '%Y-%m-%dT%H:%M'),
                estado='Pendiente'
            )
            db.session.add(cita)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear cita: {str(e)}")
        
        return redirect(url_for('gestion_citas'))
    
    pacientes = Paciente.query.all()
    doctores = Doctor.query.all()
    return render_template('citas.html', pacientes=pacientes, doctores=doctores)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)