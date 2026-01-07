# Guía de Despliegue - WSPython

## Backend en Render

### 1. Configuración del Servicio
- **New Web Service** → Conecta tu repositorio de GitHub
- **Root Directory**: `.` (raíz del proyecto)
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn backend:app --bind 0.0.0.0:$PORT`

### 2. Variables de Entorno (Environment Variables)
Añade estas variables en Render → Settings → Environment:
```
MONGO_URI=mongodb+srv://oop:oop@cluster0.9knxc.mongodb.net/oop?retryWrites=true&w=majority&appName=Cluster0
MONGO_DB=oop
MONGO_COLLECTION=Customers
```

### 3. MongoDB Atlas
- Ve a Network Access en MongoDB Atlas
- Añade la IP de Render o permite `0.0.0.0/0` (todas las IPs)

### 4. Verificación
- Abre: `https://wspython-1.onrender.com/api/items`
- Debe retornar JSON con tus datos

---

## Frontend en Vercel

### 1. Configuración del Proyecto
- **New Project** → Importa tu repositorio
- **Framework Preset**: Vite
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`

### 2. Variables de Entorno (Environment Variables)
Añade en Vercel → Settings → Environment Variables:
```
VITE_API_BASE=https://wspython-1.onrender.com
```

### 3. Deploy
- Vercel desplegará automáticamente
- URL final: `https://tu-proyecto.vercel.app`

### 4. Verificación
- Abre tu URL de Vercel
- Debe mostrar la tabla con datos de MongoDB

---

## Comandos para Subir Cambios

```bash
git add .
git commit -m "Ready for deployment"
git push
```

Render y Vercel redesplegarán automáticamente al detectar cambios en GitHub.

---

## Prueba Local

**Backend:**
```bash
C:/Users/USER/Desktop/WSPython/.venv/Scripts/python.exe backend.py
```
Abre: http://localhost:4010/api/items

**Frontend:**
```bash
cd frontend
npm run dev
```
Abre: http://localhost:5173

---

## Arquitectura

```
┌─────────────┐
│   Vercel    │  Frontend React (puerto 5173 local)
│  (Frontend) │  https://tu-proyecto.vercel.app
└──────┬──────┘
       │ fetch(VITE_API_BASE/api/items)
       ↓
┌─────────────┐
│   Render    │  Backend Flask (puerto 4010)
│  (Backend)  │  https://wspython-1.onrender.com
└──────┬──────┘
       │ MongoDB Driver (PyMongo)
       ↓
┌─────────────┐
│ MongoDB     │  Base de datos en la nube
│   Atlas     │  Colección: Customers
└─────────────┘
```

---

## Solución de Problemas

### Render muestra "ModuleNotFoundError: No module named 'app'"
- Verifica que el Start Command sea: `gunicorn backend:app --bind 0.0.0.0:$PORT`
- Asegúrate que `backend.py` tenga la línea: `app = create_app()`

### Frontend muestra "Failed to fetch"
- Verifica que `VITE_API_BASE` esté configurado en Vercel
- Verifica que el backend esté corriendo en Render
- Revisa que CORS esté habilitado en Flask

### MongoDB connection error
- Verifica que `MONGO_URI` esté correctamente configurado
- Añade la IP de Render en MongoDB Atlas Network Access
- Verifica usuario/contraseña de MongoDB
