# archivo temporal: reset_db.py
from app import app, db

with app.app_context():
    print("Eliminando tablas...")
    db.drop_all()
    print("Creando tablas...")
    db.create_all()
    db.session.commit()
    print("Base de datos reiniciada correctamente!")