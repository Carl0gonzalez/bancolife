from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy.orm import Session
from db import get_db, create_tables, Cliente, Cuenta, Transferencia
from models import ClienteCreate, CuentaCreate, TransferenciaCreate
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)  # Habilitar CORS para el frontend

# Crear tablas al iniciar la aplicación
def setup_database():
    create_tables()

# Endpoints para Clientes
@app.route('/clientes', methods=['GET'])
def get_clientes():
    """Obtener todos los clientes"""
    try:
        db = next(get_db())
        clientes = db.query(Cliente).all()
        return jsonify([
            {
                'id': cliente.id,
                'nombre': cliente.nombre,
                'correo': cliente.correo
            } for cliente in clientes
        ]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clientes', methods=['POST'])
def crear_cliente():
    """Crear un nuevo cliente"""
    try:
        data = request.get_json()
        db = next(get_db())
        
        # Validar datos requeridos
        if not data or 'nombre' not in data or 'correo' not in data:
            return jsonify({'error': 'Nombre y correo son requeridos'}), 400
        
        # Verificar si el correo ya existe
        cliente_existente = db.query(Cliente).filter(Cliente.correo == data['correo']).first()
        if cliente_existente:
            return jsonify({'error': 'El correo ya está registrado'}), 400
        
        # Crear nuevo cliente
        nuevo_cliente = Cliente(
            nombre=data['nombre'],
            correo=data['correo']
        )
        db.add(nuevo_cliente)
        db.commit()
        db.refresh(nuevo_cliente)
        
        return jsonify({
            'id': nuevo_cliente.id,
            'nombre': nuevo_cliente.nombre,
            'correo': nuevo_cliente.correo,
            'mensaje': 'Cliente creado exitosamente'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clientes/<int:cliente_id>', methods=['GET'])
def get_cliente(cliente_id):
    """Obtener un cliente específico"""
    try:
        db = next(get_db())
        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        
        if not cliente:
            return jsonify({'error': 'Cliente no encontrado'}), 404
        
        return jsonify({
            'id': cliente.id,
            'nombre': cliente.nombre,
            'correo': cliente.correo
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoints para Cuentas
@app.route('/cuentas', methods=['GET'])
def get_cuentas():
    """Obtener todas las cuentas"""
    try:
        db = next(get_db())
        cuentas = db.query(Cuenta).all()
        return jsonify([
            {
                'id': cuenta.id,
                'cliente_id': cuenta.cliente_id,
                'saldo': cuenta.saldo
            } for cuenta in cuentas
        ]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cuentas', methods=['POST'])
def crear_cuenta():
    """Crear una nueva cuenta"""
    try:
        data = request.get_json()
        db = next(get_db())
        
        # Validar datos requeridos
        if not data or 'cliente_id' not in data:
            return jsonify({'error': 'cliente_id es requerido'}), 400
        
        # Verificar que el cliente existe
        cliente = db.query(Cliente).filter(Cliente.id == data['cliente_id']).first()
        if not cliente:
            return jsonify({'error': 'Cliente no encontrado'}), 404
        
        # Crear nueva cuenta
        nueva_cuenta = Cuenta(
            cliente_id=data['cliente_id'],
            saldo=data.get('saldo', 0.0)
        )
        db.add(nueva_cuenta)
        db.commit()
        db.refresh(nueva_cuenta)
        
        return jsonify({
            'id': nueva_cuenta.id,
            'cliente_id': nueva_cuenta.cliente_id,
            'saldo': nueva_cuenta.saldo,
            'mensaje': 'Cuenta creada exitosamente'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cuentas/<int:cuenta_id>', methods=['GET'])
def get_cuenta(cuenta_id):
    """Obtener una cuenta específica"""
    try:
        db = next(get_db())
        cuenta = db.query(Cuenta).filter(Cuenta.id == cuenta_id).first()
        
        if not cuenta:
            return jsonify({'error': 'Cuenta no encontrada'}), 404
        
        return jsonify({
            'id': cuenta.id,
            'cliente_id': cuenta.cliente_id,
            'saldo': cuenta.saldo
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para Transferencias
@app.route('/transferencias', methods=['POST'])
def realizar_transferencia():
    """Realizar una transferencia entre cuentas"""
    try:
        data = request.get_json()
        db = next(get_db())
        
        # Validar datos requeridos
        if not data or 'cuenta_origen' not in data or 'cuenta_destino' not in data or 'monto' not in data:
            return jsonify({'error': 'cuenta_origen, cuenta_destino y monto son requeridos'}), 400
        
        cuenta_origen_id = data['cuenta_origen']
        cuenta_destino_id = data['cuenta_destino']
        monto = float(data['monto'])
        
        # Validar que el monto sea positivo
        if monto <= 0:
            return jsonify({'error': 'El monto debe ser mayor a 0'}), 400
        
        # Verificar que las cuentas existen
        cuenta_origen = db.query(Cuenta).filter(Cuenta.id == cuenta_origen_id).first()
        cuenta_destino = db.query(Cuenta).filter(Cuenta.id == cuenta_destino_id).first()
        
        if not cuenta_origen:
            return jsonify({'error': 'Cuenta origen no encontrada'}), 404
        if not cuenta_destino:
            return jsonify({'error': 'Cuenta destino no encontrada'}), 404
        
        # Verificar que no sea la misma cuenta
        if cuenta_origen_id == cuenta_destino_id:
            return jsonify({'error': 'No se puede transferir a la misma cuenta'}), 400
        
        # Verificar saldo suficiente
        if cuenta_origen.saldo < monto:
            return jsonify({'error': 'Saldo insuficiente'}), 400
        
        # Realizar la transferencia
        cuenta_origen.saldo -= monto
        cuenta_destino.saldo += monto
        
        # Crear registro de transferencia
        nueva_transferencia = Transferencia(
            cuenta_origen=cuenta_origen_id,
            cuenta_destino=cuenta_destino_id,
            monto=monto
        )
        
        db.add(nueva_transferencia)
        db.commit()
        db.refresh(nueva_transferencia)
        
        return jsonify({
            'id': nueva_transferencia.id,
            'cuenta_origen': nueva_transferencia.cuenta_origen,
            'cuenta_destino': nueva_transferencia.cuenta_destino,
            'monto': nueva_transferencia.monto,
            'fecha': nueva_transferencia.fecha.isoformat(),
            'mensaje': 'Transferencia realizada exitosamente'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/transferencias', methods=['GET'])
def get_transferencias():
    """Obtener todas las transferencias"""
    try:
        db = next(get_db())
        transferencias = db.query(Transferencia).all()
        return jsonify([
            {
                'id': transferencia.id,
                'cuenta_origen': transferencia.cuenta_origen,
                'cuenta_destino': transferencia.cuenta_destino,
                'monto': transferencia.monto,
                'fecha': transferencia.fecha.isoformat()
            } for transferencia in transferencias
        ]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint de salud
@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar el estado de la aplicación"""
    return jsonify({
        'status': 'OK',
        'message': 'BancoLite API funcionando correctamente'
    }), 200

if __name__ == '__main__':
    setup_database()
    app.run(host='0.0.0.0', port=5000, debug=True) 