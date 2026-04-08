# Directiva: Optimización Mobile y Navegación (Fase 3)
Fecha: 2026-04-08 19:37

## Objetivo
Implementar una barra de navegación inferior (Tab Bar) al estilo "App Nativa" (Instagram, WhatsApp) para estandarizar la usabilidad móvil de la plataforma. Evitar el "aislamiento" de las vistas y permitir cambiar rápidamente entre "Dashboard", "Disponibilidad" y "Perfil" (incluyendo un salto al "/admin" si el usuario lo necesita y tiene permisos).

## Tareas a Realizar
1. **Estilos Globales (`index.css`)**: 
   - Añadir soporte CSS para `.bottom-nav` asegurando que esté fija abajo (`position: fixed; bottom: 0;`), tenga blur por efecto glass y ocupe el ancho total.
   - Ajustar el `.app-container` para dejar un padding-bottom suficiente y evitar que el contenido sea tapado por la barra.
2. **Componente Estructural (`Layout.jsx`)**: 
   - Reemplazar el footer genérico.
   - Condicionar la renderización de la `.bottom-nav` para que **sólo** se muestre si hay sesión activa (token en localStorage).
   - Botones a incluir: 🏠 Inicio (`/dashboard`), 📅 Disp. (`/disponibilidad`), 👤 Perfil (`/perfil`).
3. **Automatización**: Se generará el script `scripts/build_mobile_nav.py` para inyectar estos componentes sin modificar a mano.

## Restricciones y Notas Operativas
- **Iconografía**: Se usarán emojis o SVGs sencillos inline para no obligar a instalar librerías pesadas como `react-icons` temporalmente.
- **Seguridad**: El botón Admin no debe estar expuesto para todos. Por ello, delegaremos el acceso Admin a un "panel lateral" o como un botón mágico dentro de la pestaña de "Perfil" (cuando el backend retorne que es ADMIN).
