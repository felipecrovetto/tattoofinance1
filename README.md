# TattooFi - Sistema de Gestión Financiera para Estudio de Tatuajes

## 🎨 Descripción
TattooFi es una aplicación web moderna diseñada específicamente para la gestión financiera de estudios de tatuajes. Con un diseño futurista/callejero y funcionalidades completas de seguimiento de ingresos y gastos.

## ✨ Características Principales

### 🔐 Autenticación
- Sistema de login seguro
- Usuario demo: `tito` / Contraseña: `titotito`

### 📊 Dashboard Interactivo
- Gráficos en tiempo real con Chart.js
- Filtros por período (día/mes/año)
- KPIs visuales: ingresos, gastos, beneficio neto
- Gráfico de barras: ingresos vs gastos
- Gráfico circular: distribución de gastos por categoría

### 💰 Gestión de Transacciones
- Formulario para agregar ingresos/gastos/mixtos
- Tipos de transacción:
  - **Ingreso**: 100% ingreso
  - **Gasto**: 100% gasto  
  - **Mixto**: % configurable entre ingreso/gasto
- Categorías dinámicas personalizables
- Historial de transacciones recientes

### 🎯 Lógica de Negocio
- Configuración de porcentajes para trabajos colaborativos
- Seguimiento de ingresos por tatuador vs estudio
- Categorización flexible de gastos e ingresos

### 🚀 Tecnologías
- **Backend**: Flask + SQLAlchemy + PostgreSQL
- **Frontend**: HTML5 + CSS3 + JavaScript + Chart.js
- **Diseño**: Futurista/callejero con efectos neón
- **Autenticación**: Flask-Login + WTForms
- **Base de Datos**: PostgreSQL en la nube

## 🛠️ Instalación Local

1. **Clonar y configurar entorno:**
```bash
cd /home/ubuntu/tattoo_finance_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Configurar variables de entorno:**
```bash
# El archivo .env ya está configurado con la base de datos PostgreSQL
```

3. **Ejecutar la aplicación:**
```bash
python app.py
```

4. **Acceder a la aplicación:**
- URL: http://localhost:5000
- Usuario: `tito`
- Contraseña: `titotito`

## 🌐 Despliegue en Render

### Archivos de Configuración Incluidos:
- `render.yaml` - Configuración de servicio
- `Procfile` - Comando de inicio
- `requirements.txt` - Dependencias Python
- `runtime.txt` - Versión de Python

### Pasos para Desplegar:
1. Crear cuenta en Render.com
2. Conectar repositorio GitHub
3. Render detectará automáticamente la configuración
4. Configurar variables de entorno en Render Dashboard

## 📱 Características del Diseño

### Paleta de Colores Cyber-Punk:
- **Fondo**: Negro carbón (#121212)
- **Componentes**: Gris oscuro (#1E1E1E) 
- **Acento**: Magenta neón (#F900F9)
- **Éxito**: Verde neón (#39FF14)
- **Error**: Rojo neón (#FF073A)

### Efectos Visuales:
- Animaciones CSS fluidas
- Efectos hover con brillos neón
- Conteo animado en KPIs
- Transiciones suaves
- Botón flotante (FAB) para acciones rápidas

### Responsive Design:
- Diseño mobile-first
- Sidebar colapsable en móviles
- Grids adaptables
- Componentes flexibles

## 🗃️ Estructura de Base de Datos

### Tablas:
- **User**: Usuarios del sistema
- **Category**: Categorías de transacciones
- **Transaction**: Registros de ingresos/gastos

### Datos de Ejemplo:
- 50+ transacciones de prueba
- 9 categorías predefinidas
- Datos distribuidos en los últimos 30 días

## 🔧 Configuración de Producción

### Variables de Entorno Requeridas:
- `DATABASE_URL`: URL de PostgreSQL
- `SECRET_KEY`: Clave secreta de Flask
- `FLASK_ENV`: production

### Características de Seguridad:
- Protección CSRF con Flask-WTF
- Hashing seguro de contraseñas
- Sesiones encriptadas
- Rutas protegidas con autenticación

## 📈 Funcionalidades API

### Endpoints Disponibles:
- `GET /api/dashboard_data?filter=day|month|year`
- `POST /api/add_transaction`
- `POST /api/add_category` 
- `GET /api/get_categories`

## 🎮 Demo y Pruebas

La aplicación incluye:
- Usuario demo pre-configurado
- Datos de ejemplo representativos
- Categorías iniciales del negocio
- Transacciones variadas para probar filtros

## 📞 Soporte

Para soporte técnico o consultas sobre personalización, contacta al desarrollador.

---
**TattooFi** - Gestión Financiera Profesional para tu Estudio 🎨⚡
