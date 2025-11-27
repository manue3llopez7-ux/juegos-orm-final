# Sistema de Gestión de Videojuegos con Flask

Una aplicación web robusta desarrollada en Python utilizando el framework Flask. Permite la gestión completa (CRUD) de un catálogo de videojuegos, cuenta con un sistema seguro de autenticación de usuarios, una API RESTful integrada y monitoreo de errores en tiempo real.

## Características Principales

* **Gestión de Juegos (CRUD):** Crear, Leer, Actualizar y Eliminar videojuegos (usando PyMySQL para consultas directas y eficientes).
* **Autenticación Segura:**
    * Registro e Inicio de Sesión de usuarios.
    * Gestión de sesiones con **Flask-Login**.
    * Contraseñas encriptadas con **Werkzeug**.
    * Protección de rutas (solo usuarios logueados pueden editar/eliminar).
* **API RESTful:** Endpoints JSON para interactuar con los datos externamente (usando **Flask-RESTful**).
* **Manejo de Errores:**
    * Páginas personalizadas para errores 400, 404, 405 y 500.
    * Registro de errores locales en `errors.log`.
    * Monitoreo de errores en la nube con **Sentry**.
* **Seguridad:** Protección CSRF en formularios (Flask-WTF) y cookies seguras.
* **Testing:** Pruebas unitarias integradas para validar rutas, modelos y API.

## Tecnologías Utilizadas

* **Python 3.13**
* **Flask** (Framework Web)
* **MySQL / MariaDB** (Base de datos)
* **PyMySQL** (Conector de base de datos)
* **Flask-Login** (Gestión de sesiones)
* **Flask-WTF** (Formularios y validación)
* **Flask-RESTful** (Creación de API)
* **Sentry SDK** (Monitoreo)
* **Unittest** (Pruebas automatizadas)
* **Bulma CSS** (Estilos frontend)

## Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone [https://github.com/tu-usuario/nombre-repo.git](https://github.com/tu-usuario/nombre-repo.git)
cd juegos_orm_final