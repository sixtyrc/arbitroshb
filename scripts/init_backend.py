import os
import subprocess
import sys

def run_command(command, description):
    print(f"Ejecutando: {description}...")
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error en {description}: {e}")
        sys.exit(1)

def main():
    # 1. Asegurar que estamos en el directorio correcto
    project_root = r"d:\Proyectos\Arbitros"
    os.chdir(project_root)

    # 2. Instalar dependencias
    run_command("pip install -r requirements.txt", "Instalación de dependencias")

    # 3. Crear proyecto Django si no existe
    if not os.path.exists("backend"):
        run_command("python -m django startproject backend .", "Creación de proyecto Django")
    
    # 4. Crear app principal si no existe
    # Usaremos 'gestion' para la lógica de árbitros
    app_path = os.path.join("backend", "gestion")
    # Nota: django-admin startapp gestion crea la carpeta en el root si usamos . en el project
    if not os.path.exists("gestion"):
        run_command("python manage.py startapp gestion", "Creación de app 'gestion'")

    print("\n[OK] Entorno de Backend inicializado correctamente.")

if __name__ == "__main__":
    main()
