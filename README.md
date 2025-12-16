# 📋 Sistema de Asistencia con Código QR

Este proyecto es una aplicación web basada en **Django** que permite gestionar la asistencia de personas mediante códigos QR. Incluye un módulo para registrar usuarios y generar sus credenciales (QR), y dos métodos de lectura: uno vía web (cámara del dispositivo) y otro mediante un script de escritorio con OpenCV.

---

## 🚀 Características

1.  **Registro de Usuarios:** Formulario web para ingresar Nombre, Apellido y DNI.
2.  **Generación de QR:** Creación automática de un código QR único basado en un hash SHA256 de los datos del usuario.
3.  **Base de Datos SQLite:** Almacenamiento ligero y eficiente de los registros y estados de asistencia.
4.  **Escáner Web:** Interfaz moderna para leer QRs directamente desde el navegador (móvil o desktop).
5.  **Escáner de Escritorio:** Script en Python (`main.py`) para usar una webcam conectada al PC como lector rápido.
6.  **Control de Estados:** Detecta automáticamente si es una **Entrada** o una **Salida** y evita registros duplicados.

---

## 🛠️ Instalación y Configuración

### 1. Prerrequisitos
Asegúrate de tener Python instalado. Luego, instala las dependencias necesarias:

```bash
pip install django qrcode pillow opencv-python pyzbar
```

### 2. Estructura del Proyecto
El proyecto debe tener la siguiente estructura para funcionar correctamente:

```text
/
├── manage.py           # Gestor de Django
├── data.sqlite         # Base de datos (se crea automáticamente o se usa la existente)
├── main.py             # Script de escáner de escritorio (OpenCV)
├── asistencia_qr/      # Configuración del proyecto Django
│   ├── settings.py
│   └── urls.py
└── core/               # Aplicación principal
    ├── models.py       # Modelo de datos
    ├── views.py        # Lógica de registro y escaneo
    ├── urls.py         # Rutas de la app
    ├── forms.py        # Formulario de registro
    └── templates/core/ # Archivos HTML
        ├── registro.html
        └── lector.html
```

### 3. Inicialización de la Base de Datos
Si es la primera vez que ejecutas el proyecto, aplica las migraciones de Django:

```bash
python manage.py migrate
```

---

## ▶️ Ejecución

### Opción A: Servidor Web (Registro y Escáner Web)
Inicia el servidor de desarrollo de Django:

```bash
python manage.py runserver
```

* **Registro de Usuarios:** Abre tu navegador en `http://127.0.0.1:8000/`. Llena el formulario y descarga el QR generado.
* **Escáner Web:** Abre `http://127.0.0.1:8000/lector/`. Da permiso a la cámara y apunta al código QR.

### Opción B: Escáner de Escritorio (Script Python)
Si prefieres usar una aplicación de escritorio dedicada para escanear (más rápido para alto volumen):

1.  Asegúrate de que el servidor web (`runserver`) no es estrictamente necesario para este script, pero ambos comparten la misma base de datos `data.sqlite`.
2.  Ejecuta el script:

```bash
python main.py
```

3.  Se abrirá una ventana de cámara.
    * Presiona **'q'** para salir.
    * El sistema mostrará en pantalla "Entrada registrada", "Salida registrada" o errores si el usuario no existe.

---

## 🧩 Lógica del Sistema

### Modelo de Datos (`data` table)
| Campo      | Tipo         | Descripción |
|------------|--------------|-------------|
| `id_hash`  | VARCHAR(64)  | Hash SHA256 único del usuario (PK). |
| `time_entry`| BIGINT      | Timestamp Unix de la hora de entrada. (0 si no ha entrado) |
| `time_exit` | BIGINT      | Timestamp Unix de la hora de salida. (0 si no ha salido) |

### Flujo de Asistencia
1.  **Escaneo 1:** Si `time_entry` es 0 -> Registra **Entrada**.
2.  **Escaneo 2:** Si `time_entry` existe y `time_exit` es 0 -> Registra **Salida**.
3.  **Escaneo 3+:** Si ambos existen -> Muestra "Salida ya registrada" (Ciclo completado).


---

## 🤝 Contribuir
Si deseas mejorar el diseño o la lógica, siéntete libre de editar los archivos HTML en `core/templates/` o la lógica en `core/views.py`.