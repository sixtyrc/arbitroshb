# Directiva: Panel Administrador Full React (ArbitrosHB - Fase 2)
Fecha: 2026-04-08 19:10

## Objetivo
Refactorizar el actual panel de administración (`/admin` por defecto de Django) y construir una vista Premium basada en **React** que permita a las autoridades (Tesoreros, Asignadores) gestionar a los árbitros, crear partidos y manejar liquidaciones con la estética "Sporty UI / Glassmorphism" del sistema actual.

## Entradas y Dependencias
1. Perfil del usuario logueado con rol `'ADMIN'`.
2. El enrutamiento actual del frontend en `App.jsx` debe proteger estas nuevas vistas `AdminDashboard`, `AdminPartidos`, `AdminDesignaciones` asegurando que solo usuarios con `role === 'ADMIN'` puedan ingresar.
3. Se consumirán los endpoints existentes de `gestionViewSet` (ya creados en `views.py`):
   - `GET /api/users/`, `/api/arbitros/`, `/api/partidos/`, `/api/disponibilidades/`, `/api/designaciones/`
   - `POST / PATCH / DELETE` correspondientes.

## Entregables (Salidas)
1. **Vista `AdminDashboard.jsx`**: Resumen general con estadísticas (Partidos en curso, Total liquidaciones).
2. **Vista `AdminPartidos.jsx`**: CRUD para configurar partidos de cada fin de semana.
3. **Vista `AdminDesignaciones.jsx`**: Panel donde el asignador ve disponibilidades y vincula a Árbitros con Partidos.
4. **Vista `AdminLiquidaciones.jsx`**: Exportación avanzada de Excel de honorarios, permitiendo filtrar dinámicamente por Rango de Fechas (semanal/quincenal), por Mes, y opcionalmente por un Partido específico.

## Restricciones y Casos Borde (Trampas Conocidas)
- **Seguridad (Frontend vs Backend)**: No alcanza con ocultar el botón en React. Si el JWT token del usuario NO tiene los permisos (`IsAdminUser`), el backend rechazará peticiones.
- **Autenticación (API)**: El frontend debe diferenciar post-login a dónde dirige (`/dashboard` normal vs `/admin`).
- **Diseño**: No usar librerías UI pesadas (ej: Material UI). Apegarse estrictamente a las variables CSS en `index.css` para mantener la estética rápida de la PWA.

## Protocolo de Acción Operativa
1. **Delegación a Scripts Python**: En vez de escribir los componentes manualmente en la terminal, se utilizará un script de Python en `scripts/build_admin_ui.py` que se encargará de generar la estructura base de las vistas.
2. Actualizar el enrutador en `App.jsx` para integrar las nuevas páginas condicionalmente.
