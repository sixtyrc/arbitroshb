# SOP - Sistema de Gestión de Árbitros (ArbitrosHB)
**Fecha y Hora:** 2026-04-07 07:37:00
**Estado:** Fase 1 - Definición

## 1. Objetivo del Sistema
Centralizar la gestión del Colegio de Árbitros de Handball de Chaco en una plataforma 100% móvil, rápida y moderna. El enfoque es facilitar la comunicación bidireccional entre la administración y los árbitros a través de notificaciones push y correos electrónicos.

## 2. Arquitectura Técnica (Versiones Estables)
- **Backend:** Python + Django + Django Rest Framework (DRF).
- **Frontend:** React (Vite) - PWA Mobile-First.
- **Base de Datos:** PostgreSQL.
- **Estilos:** Vanilla CSS moderno (Tokens, Variables, Flex/Grid). **Sin frameworks pesados** para máximo rendimiento.
- **Email:** Resend (Notificaciones de sistema y respaldos).
- **Notificaciones Push:** Web Push API / Service Workers (Compatibilidad Android/iOS).
- **Dominio:** `arbitroshb.ctsoft.com.ar`

## 3. Requerimientos de Diseño & UX
- **Look & Feel:** Deportivo, premium, moderno (Look "WÓW").
- **Performance:** Carga ultrarrápida. Animaciones fluidas pero ligeras.
- **Footer Obligatorio:** "© Todos los derechos reservados... Desarrollado por [CTSoft](https://ctsoft.com.ar)".

## 4. Flujos Clave & Notificaciones
### A. Designación de Árbitro
1. El admin asigna un árbitro a un partido.
2. El sistema dispara:
   - **Notificación WEB PUSH** instantánea al móvil del árbitro.
   - **Email vía Resend** como respaldo.

### B. Gestión de Disponibilidad
1. El árbitro marca sus días/horas libres desde el celular.
2. El sistema actualiza la base de datos para que el admin solo pueda asignar partidos en horarios válidos.

### C. Liquidación de Pagos
1. El sistema calcula comisiones y pagos basados en partidos dirigidos.

## 5. Restricciones y Trampas Conocidas
- **Notificaciones en iOS:** El usuario DEBE "Agregar a inicio" para recibir Push. Informar este paso en el primer inicio de sesión.
- **Estabilidad:** Solo usar versiones LTS (Long Term Support) de Django y bibliotecas de React.
- **Entorno Windows:** Se cambió `psycopg2` por `psycopg[binary]` (v3) debido a errores de compilación de wheels en Python 3.13 local.
- **Seguridad:** JWT para comunicaciones API, asegurando persistencia correcta en PWA.

---
*Este documento se actualizará en cada fase del desarrollo.*
