# 🏦 BancoLite - Sistema Bancario Simple

Una aplicación fullstack que simula las operaciones básicas de un banco, construida con Flask, PostgreSQL y JavaScript vanilla.

## 📋 Características

- **Gestión de Clientes**: CRUD completo para clientes bancarios
- **Gestión de Cuentas**: Crear y gestionar cuentas bancarias
- **Transferencias**: Realizar transferencias entre cuentas
- **Interfaz Web**: Frontend moderno y responsivo
- **API REST**: Backend con endpoints JSON
- **Base de Datos**: PostgreSQL con persistencia de datos

## 🏗️ Arquitectura

```
banco-lite/
├── backend/          # API Flask + SQLAlchemy
├── frontend/         # HTML + JavaScript + CSS
├── docker-compose.yml # Orquestación de servicios
└── .env             # Variables de entorno
```

## 🚀 Instalación y Ejecución

### Prerrequisitos

- Docker y Docker Compose
- Python 3.11+ (para desarrollo local)

### Ejecución con Docker (Recomendado)

1. **Clonar el repositorio:**

   ```bash
   git clone <url-del-repositorio>
   cd bancolife
   ```

2. **Configurar variables de entorno:**

   ```bash
   # El archivo .env ya está configurado con valores por defecto
   # Puedes modificarlo según tus necesidades
   ```

3. **Ejecutar la aplicación:**

   ```bash
   docker-compose up --build
   ```

4. **Acceder a la aplicación:**
   - Frontend: http://localhost
   - Backend API: http://localhost:5000
   - Base de datos: localhost:5432

### Desarrollo Local

1. **Crear ambiente virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. **Instalar dependencias:**

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configurar base de datos PostgreSQL:**

   - Instalar PostgreSQL
   - Crear base de datos `banco_lite`
   - Configurar variables de entorno en `.env`

4. **Ejecutar backend:**

   ```bash
   cd backend
   python app.py
   ```

5. **Ejecutar frontend:**
   ```bash
   cd frontend
   python -m http.server 8000
   ```

## 📚 API Endpoints

### Clientes

- `GET /clientes` - Obtener todos los clientes
- `POST /clientes` - Crear nuevo cliente
- `GET /clientes/{id}` - Obtener cliente específico

### Cuentas

- `GET /cuentas` - Obtener todas las cuentas
- `POST /cuentas` - Crear nueva cuenta
- `GET /cuentas/{id}` - Obtener cuenta específica

### Transferencias

- `GET /transferencias` - Obtener todas las transferencias
- `POST /transferencias` - Realizar transferencia

### Salud

- `GET /health` - Verificar estado de la API

## 🗄️ Base de Datos

### Tablas

**clientes**

- `id` (Primary Key)
- `nombre` (String)
- `correo` (String, Unique)

**cuentas**

- `id` (Primary Key)
- `cliente_id` (Foreign Key)
- `saldo` (Float)

**transferencias**

- `id` (Primary Key)
- `cuenta_origen` (Foreign Key)
- `cuenta_destino` (Foreign Key)
- `monto` (Float)
- `fecha` (DateTime)

## 🔧 Variables de Entorno

```env
POSTGRES_USER=banco_user
POSTGRES_PASSWORD=banco_password
POSTGRES_DB=banco_lite
DB_HOST=db
DB_PORT=5432
FLASK_ENV=development
FLASK_DEBUG=1
```

## 🐳 Comandos Docker Útiles

```bash
# Construir y ejecutar
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Eliminar volúmenes (cuidado: borra datos)
docker-compose down -v

# Reconstruir un servicio específico
docker-compose up --build backend
```

## 🧪 Pruebas

### Crear un Cliente

```bash
curl -X POST http://localhost:5000/clientes \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Juan Pérez", "correo": "juan@email.com"}'
```

### Crear una Cuenta

```bash
curl -X POST http://localhost:5000/cuentas \
  -H "Content-Type: application/json" \
  -d '{"cliente_id": 1, "saldo": 1000.00}'
```

### Realizar Transferencia

```bash
curl -X POST http://localhost:5000/transferencias \
  -H "Content-Type: application/json" \
  -d '{"cuenta_origen": 1, "cuenta_destino": 2, "monto": 500.00}'
```

## 🛠️ Tecnologías Utilizadas

- **Backend**: Flask, SQLAlchemy, PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Base de Datos**: PostgreSQL
- **Contenedores**: Docker, Docker Compose
- **Servidor Web**: Nginx

## 📝 Notas de Desarrollo

- La aplicación está diseñada para ser simple y educativa
- No incluye autenticación ni autorización (para simplicidad)
- Los datos se persisten en un volumen de Docker
- CORS está habilitado para desarrollo local
- El frontend se comunica con el backend vía fetch API

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🆘 Soporte

Si encuentras algún problema o tienes preguntas:

1. Revisa los logs: `docker-compose logs`
2. Verifica la conectividad de la base de datos
3. Asegúrate de que los puertos 80, 5000 y 5432 estén disponibles
4. Revisa que Docker esté ejecutándose correctamente

---

**¡Disfruta usando BancoLite! 🏦✨**
