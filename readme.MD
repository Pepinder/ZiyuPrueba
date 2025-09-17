# Prueba Técnica Ziyu

Este repositorio contiene una API RESTful robusta para una empresa de jardinería, desarrollada con Django y Django Rest Framework.

## Logica principal

- **Arquitectura de Perfiles de Usuario:** Se utiliza el sistema de autenticación de Django, extendido con perfiles `Cliente` y `Jardinero`.
- **Autenticación por Tokens (JWT):** La API está securizada mediante JSON Web Tokens, el estándar moderno para APIs sin estado.
- **API Basada en Roles:** La lógica de negocio está claramente separada por roles:
  - **Clientes:** Crean y gestionan sus propias solicitudes.
  - **Jardineros:** Ven las solicitudes disponibles y pueden auto-asignarse a los trabajos.
  - **Administradores:** Tienen visibilidad total y control administrativo.
- **Documentación Autogenerada (Swagger/OpenAPI):** Se ha integrado `drf-yasg` para ofrecer una documentación de API interactiva y siempre actualizada.
- **Endpoints de Registro y Login:** La API permite la creación de nuevos usuarios y la obtención de tokens de autenticación sin necesidad de acceder al panel de administración.

## Instalación y Ejecución

**Requisitos:**

- Python 3.8+
- Git

**Pasos:**

1.  **Clonar el repositorio:**

    ```bash
    git clone https://github.com/Pepinder/ZiyuPrueba
    cd ziyuPrueba
    ```

2.  **Crear y activar un entorno virtual:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instalar dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Aplicar las migraciones de la base de datos:**

    ```bash
    python manage.py migrate
    ```

5.  **(Opcional) Crear un superusuario para el panel de Admin:**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Iniciar el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```

## Endpoints y Flujo de Trabajo

El servidor estará corriendo en `http://127.0.0.1:8000/`.

- **Documentación Interactiva (Swagger):** `http://127.0.0.1:8000/swagger/`
- **Documentación Estándar (ReDoc):** `http://127.0.0.1:8000/redoc/`
- **Panel de Administración:** `http://127.0.0.1:8000/admin/`

### Flujo de API Recomendado (Usando Postman o Swagger)

1.  **Registrar un Cliente:**

    - `POST` a `/api/v1/register/`
    - Body: `{ "username": "cliente1", "password": "...", "rol": "cliente" }`

2.  **Registrar un Jardinero:**

    - `POST` a `/api/v1/register/`
    - Body: `{ "username": "jardinero1", "password": "...", "rol": "jardinero" }`

3.  **Obtener Token de Autenticación (Login):**

    - `POST` a `/api/token/`
    - Body: `{ "username": "cliente1", "password": "..." }`
    - **Copia el `access_token` de la respuesta.**

4.  **Crear una Solicitud (como Cliente):**

    - `POST` a `/api/v1/solicitudes/`
    - **Authorization Header:** `Bearer <TU_ACCESS_TOKEN_CLIENTE>`
    - Body: `{ "direccion": "...", "tipo_servicio": "...", ... }`

5.  **Aceptar Servicio (como Jardinero):**
    - Obtén el token para el usuario jardinero.
    - `POST` a `/api/v1/solicitudes/{id}/aceptar-servicio/`
    - **Authorization Header:** `Bearer <TU_ACCESS_TOKEN_JARDINERO>`
