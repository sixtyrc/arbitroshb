# Guía de Deploy Paso a Paso (Para Windows Server)
Fecha: 2026-04-08

Esta guía abarca todo el proceso desde cero para montar en producción **ArbitrosHB** (Frontend en React/Vite + Backend en Django) utilizando **Caddy Server** para Reverse Proxy / HTTPS y **NSSM** para mantener tu API viva como un servicio de Windows.

## 1. Requisitos Previos (En el Servidor)

Descarga e instala lo siguiente:
- **Python 3.10+**: Al instalar, marca la casilla "Add Python to PATH".
- **Node.js (LTS)**: Por ej. v20+. Asegúrate de agregarlo al PATH.
- **PostgreSQL**: Asegúrate de acordarte la contraseña del usuario `postgres`.
- **NSSM**: Descargalo (el .zip), extrae la versión `win64`, y copia `nssm.exe` en `C:\Windows\System32` (para que puedas usarlo directo desde consola).
- **Caddy Server**: Descarga la versión de Windows, pon el ejecutable `caddy.exe` en una carpeta como `C:\caddy\` y añadila al PATH del sistema. Opcionalmente créalo como servicio NSSM luego.

---

## 2. Preparar la Base de Datos (PostgreSQL)

1. Abre **pgAdmin** o la consola `psql` e ingresa.
2. Crea una base de datos exclusiva:
   ```sql
   CREATE DATABASE arbitrosdb;
   ```
3. Anota tu URL de conexión, que será algo así como: `postgres://postgres:TU_CONTRASEÑA@localhost:5432/arbitrosdb`

---

## 3. Clonar y Configurar el Backend (Django)

Abre **PowerShell** y ve a tu carpeta de producción (ej. `C:\Proyectos\Arbitros`):

```powershell
git clone <TU_REPOSITORIO> C:\Proyectos\Arbitros
cd C:\Proyectos\Arbitros
```

### A. Crear y activar Entorno Virtual
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### B. Instalar Dependencias del Backend
Asegúrate de instalar waitress, que actuará como el servidor de producción (reemplazando al runserver):
```powershell
pip install -r requirements.txt
pip install waitress
```

### C. Archivo `.env` (CRÍTICO: Incluidas llaves VAPID)
Crea o copia tu archivo `.env` en `C:\Proyectos\Arbitros\.env`
Asegúrate de configurarlo **MUY BIEN**. Aquí deberás generar nuevamente las llaves VAPID o pegar las mismas del desarrollo, pero ¡NO pierdas las del servidor porque los usuarios suscritos tendrían invalidada la sesión Push!:

**Ejemplo ideal de `.env`**:
```ini
DEBUG=False
SECRET_KEY=Una_Clave_Larga_Y_Segura_Sin_Espacios
DATABASE_URL=postgres://postgres:TuPassword@localhost:5432/arbitrosdb

# --- CONFIGURACIÓN DE NOTIFICACIONES PUSH (VAPID) ---
# Importante: Estas llaves validan quién sos ante el navegador de los usuarios.
# Podés generarlas con el comando:
# python scripts/gen_vapid_crypto.py
VAPID_PUBLIC_KEY=tu_public_key_generada_aqui
VAPID_PRIVATE_KEY=tu_private_key_generada_aqui
# Debe ser un mail con un dominio controlable por vos si es posible, ideal admin@tudominio.com
VAPID_ADMIN_EMAIL=admin@tuservidor.com

# --- (Opcional si usas los Emails) ---
EMAIL_HOST=smtp.resend.com
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_HOST_USER=resend
EMAIL_HOST_PASSWORD=tu_clave_de_resend
DEFAULT_FROM_EMAIL=Notificaciones ArbitrosHB <notificaciones@tubackend.com.ar>
```

### D. Concluir Configuración:
Aplica la migración y crea tu super usuario y recopila archivos estáticos del panel de admin original:
```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

---

## 4. Crear Servicio de Windows para el Backend (con NSSM)

No usaremos `python manage.py runserver` ¡Eso es solo para desarrollar! Usaremos `waitress` encapsulado en un servicio.

1. Abre **PowerShell COMO ADMINISTRADOR**.
2. Ejecuta el gestor gráfico de NSSM:
   ```powershell
   nssm install ArbitrosBackend
   ```
3. Se abrirá una ventana, configurala así:
   - **Path**: `C:\Proyectos\Arbitros\venv\Scripts\waitress-serve.exe`
   - **Arguments**: `--port=8000 backend.wsgi:application`
   - **Directory**: `C:\Proyectos\Arbitros\` *(Tu carpeta principal donde está `manage.py`)*

4. En la pestaña **Details**, ponle Startup Type: Automatic.
5. Clickea "Install Service".
6. Luego puedes iniciarlo en la consola con:
   ```powershell
   nssm start ArbitrosBackend
   ```
*(Con esto ya tenel el Backend escuchando en localhost:8000 permanentemente)*

---

## 5. Preparar el Frontend (React/Vite)

Abre **PowerShell** (no hace falta admin). Ve a la carpeta frontend:

```powershell
cd C:\Proyectos\Arbitros\frontend
npm install
```

### Puntos a cambiar antes de compilar
Debes indicarle al código que ya NO usará `/api` directamente sino que apuntará a tu dominio base.
Por suerte, Vite con `api.js` configurado como `const API_URL = '/api';` ya debería seguir funcionando siempre y cuando Caddy dirija lo que empiece con `/api` a `localhost:8000`.

Procedemos a construir tu App React para tener código puro estático.
```powershell
npm run build
```
Esto te generará una carpeta `C:\Proyectos\Arbitros\frontend\dist`. **Esta es la carpeta mágica** que le daremos a Caddy.

---

## 6. Configurar el Proxy / HTTPS con Caddy

Caddy instalará automáticamente el SSL por ti. No necesitas Certbot. 
Sólo asegúrate de tener los DNS de tu Dominio (ej. `arbitroshb.ctsoft.com.ar`) apuntados a la IP Pública de tu Router/Windows Server y el puerto 443 liberado.

1. En tu carpeta principal del proyecto (`C:\Proyectos\Arbitros\`), crea un archivo llamado `Caddyfile` sin ninguna extensión.
2. Ábrelo con un bloc de notas y escribe tal cual esto:

```caddyfile
arbitroshb.ctsoft.com.ar {
    # 1. Servir todo el código estático de React
    root * C:\Proyectos\Arbitros\frontend\dist
    file_server

    # 2. Las rutas que empiece con /api las tiramos al backend
    handle_path /api/* {
        reverse_proxy localhost:8000
    }

    # 3. Solucionar el problema de rutas "Not Found" propio de React (React Router)
    try_files {path} /index.html
}
```

3. **Iniciando Caddy**: Puedes correrlo temporalmente para probar que funcione:
   Abre powershell en la carpeta principal de tu proyecto.
   ```powershell
   caddy run
   ```
   *Caddy solicitará un certificado a Let'sEncrypt automáticamente, ¡magia!.*

### Convertir Caddy en un servicio de Windows para el auto-start:
Para no tener que dejar la consola negra de Caddy abierta 24/7.
1. Detén el "caddy run" actual (Ctrl + C).
2. Abre **PowerShell como Administrador**.
3. ```powershell
   nssm install CaddyServer
   ```
4. - **Path**: `C:\caddy\caddy.exe` *(o donde hayas guardado tu ejecutable caddy)*
   - **Arguments**: `run --config C:\Proyectos\Arbitros\Caddyfile`
   - **Directory**: `C:\Proyectos\Arbitros\`

5. Click "Install Service" y luego: `nssm start CaddyServer`

---

## 🎉 LISTO!
Tu plataforma está online.

### Troubleshooting (Trampas Clásicas)
1. **No andan las Push Notifications**: Es muy probable que no tengas `HTTPS` oficial o estás intentando desde una red sin cifrado. La API de Push de los navegadores **exige HTTPS absoluto**. Caddy te soluciona esto, debés chequear que tengas candado de seguridad, y chequear en `.env` que `VAPID_PUBLIC_KEY` sea idéntico en BD.
2. **"No API call found" / 404 en el Frontend**: Asegurate que en el `Caddyfile` agregaste la regla de `try_files` para que index.html atrape cualquier ruteo manual. Y asegurate que la regla de proxy no borre sin querer nada antes de llamar a tu Django.
3. **Se me reinició el servidor Windows y no arranca**: Entra a "Servicios" de Windows (Services.msc) y buscá *ArbitrosBackend* y *CaddyServer*. Asegúrate que ambos tengan el Status de "Execution" y Startup "Automatic".
