import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DB_USER = os.getenv('POSTGRES_USER', 'banco_user')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'banco_password')
DB_NAME = os.getenv('POSTGRES_DB', 'banco_lite')
DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = os.getenv('DB_PORT', '5432')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear engine de SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Modelo Cliente
class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)
    
    # Relación con cuentas
    cuentas = relationship("Cuenta", back_populates="cliente")

# Modelo Cuenta
class Cuenta(Base):
    __tablename__ = "cuentas"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    saldo = Column(Float, default=0.0, nullable=False)
    
    # Relaciones
    cliente = relationship("Cliente", back_populates="cuentas")
    transferencias_origen = relationship("Transferencia", foreign_keys="Transferencia.cuenta_origen")
    transferencias_destino = relationship("Transferencia", foreign_keys="Transferencia.cuenta_destino")

# Modelo Transferencia
class Transferencia(Base):
    __tablename__ = "transferencias"
    
    id = Column(Integer, primary_key=True, index=True)
    cuenta_origen = Column(Integer, ForeignKey("cuentas.id"), nullable=False)
    cuenta_destino = Column(Integer, ForeignKey("cuentas.id"), nullable=False)
    monto = Column(Float, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)

# Función para obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para crear todas las tablas
def create_tables():
    Base.metadata.create_all(bind=engine) 