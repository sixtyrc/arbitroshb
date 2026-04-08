# Directiva: Gestión de Árbitros de Handball (ArbitrosHB)
Fecha de creación: 2026-04-07 08:30
Última actualización: 2026-04-08 18:55

## Objetivo del Proyecto
Crear una PWA moderna enfocada en el Colegio de Árbitros de Handball de Chaco para centralizar la disponibilidad, designaciones y gestión de pagos (honorarios).

---

## 📊 Estado del Proyecto: **98% Completado (Hito 1)**

### 1. Tareas Finalizadas ✅
*   **07:30** - Arquitectura de modelos consolidada (CustomUser, Arbitro, Partido, Disponibilidad, Designacion).
*   **07:45** - Implementación de **Honorarios (Aranceles)**: Grupos de Pago con precios diferenciados.
*   **08:00** - Configuración de **Autenticación JWT** segura para la PWA.
*   **08:15** - Frontend: Sistema de Diseño "WOW" implementado en `index.css` (Glassmorphism, Sporty UI).
*   **08:30** - Frontend: Vista de Login funcional integrada con la API.
*   **08:40** - Frontend: **Dashboard del Árbitro** con partidos y honorarios calculados.
*   **08:50** - Frontend: Módulo de **Carga de Disponibilidad** 100% interactivo.
*   **08:55** - Notificaciones: Sistema de Emails (Resend) habilitado mediante Django Signals.
*   **08:57** - Service Worker (Push) configurado y llaves VAPID generadas.
*   **(2026-04-08 18:55)** - **Web Push completo**: Modelo `PushSubscription` creado y migrado. Endpoints `/push/vapid-key/` y `/push/subscribe/` registrados. `Perfil.jsx` actualizado con flujo real (obtiene llave del backend, registra suscripción).
*   **(2026-04-08 18:55)** - **Perfil de Árbitro**: CBU/Alias editable y guardable correctamente desde frontend.
*   **(2026-04-08 18:55)** - **Liquidaciones Excel**: Export automático con filtro por mes disponible en `/api/liquidaciones/excel/`.
*   **(2026-04-08 18:56)** - **Envío del Push**: Señales en `signals.py` configuradas usando `pywebpush` para mandar alerta en tiempo real al asignar una designación.

*   **(2026-04-08 19:22)** - **Administrador Full React (Fase 2)**: Reconstrucción total de los crudos base en React. Creadas `/admin` (Dashboard), `/admin/partidos` (CRUD de juegos), `/admin/designaciones` (asignaciones con cruce de disponibilidad en vivo), y `/admin/liquidaciones`.

### 2. Tareas Pendientes 🛠️
*   **Optimizaciones y Mantenimiento:** Estabilización de flujos y refactorización a futuro (Fase 3).

---

## 🏗️ Estructura Técnica Consolidada

- **Frontend:** React + Vite + PWA Plugin (Mobile-First).
- **Backend:** Django REST Framework + JWT Auth + PostgreSQL.
- **Notificaciones:** Resend (Email) + Service Worker (Web Push API).
- **Diseño:** Vanilla CSS puro con variables dinámicas de diseño.

## ⚠️ Trampas Conocidas (LECCIONES APRENDIDAS)
- **Path en Scripts:** Al ejecutar scripts en `scripts/`, siempre añadir el path manual al sistema para evitar `ModuleNotFoundError`.
- **JWT Persistence:** El token se almacena en `localStorage`. Si el usuario no lo limpia, la app "mantiene" la sesión de forma persistente como una app nativa.
- **Mesa de Control:** La lógica de pagos se maneja por `CategoriaGrupo`. Si dos categorías cobran distinto, DEBEN pertenecer a grupos distintos en el Panel Admin.

## 🔑 Archivos Críticos
- `backend/settings.py`: Configuración maestra.
- `gestion/models.py`: Motor de lógica de honorarios.
- `frontend/src/views/Dashboard.jsx`: Interfaz principal del árbitro.
- `docs/Pass.md`: Credenciales (Ignorado por Git).

---
**Nota Final:** El sistema es totalmente utilizable hoy. El administrador puede empezar a cargar datos y el árbitro ya verá su dinero ganado y su disponibilidad reflejada.
