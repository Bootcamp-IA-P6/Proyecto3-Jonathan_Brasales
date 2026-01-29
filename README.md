# 🕷️ Web Scraper - Django, Selenium & Docker

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-green?logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-4.0-43B02A?logo=selenium&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)

> **Proyecto de web scraping automatizado con Django, Selenium y Docker.** Extrae información de sitios web, la almacena en base de datos y mantiene los datos actualizados mediante tareas programadas.

---

## 🎯 Acerca del Proyecto

Este proyecto surge como respuesta a un reto técnico planteado para analizar el mercado tecnológico mediante técnicas de web scraping. El objetivo es validar qué información se puede extraer de sitios web y demostrar capacidades de automatización, persistencia de datos y escalabilidad.

### ¿Qué hace este scraper?

Actualmente extrae el **"Recurso del día"** de Wikipedia como prueba de concepto, demostrando que la arquitectura es extensible a otros sitios web como portales de empleo, marketplaces, o fuentes de datos públicas.

---
## 📂 Estructura del Proyecto

```
webscraper/
├── scraper/                      # Aplicación principal de scraping
│   ├── management/
│   │   └── commands/
│   │       └── scraper_wiki.py   # Comando personalizado Django
│   ├── services/
│   │   └── scrape.py             # Lógica del scraper (POO)
│   ├── models.py                 # Modelo de datos
│   ├── tests.py                  # Tests unitarios
│   └── migrations/
├── webscraper_project/           # Configuración del proyecto Django
│   ├── settings.py
│   └── urls.py
├── Dockerfile                    # Definición del contenedor
├── docker-compose.yml            # Orquestación de servicios
├── cronfile                      # Configuración de tareas programadas
├── requirements.txt              # Dependencias Python
├── manage.py                     # CLI de Django
├── db.sqlite3                    # Base de datos (generada)
└── README.md
```

**Componentes clave:**
- **`scrape.py`**: Contiene la clase del scraper con toda la lógica de extracción
- **`scraper_wiki.py`**: Comando Django que orquesta la ejecución del scraper
- **`models.py`**: Define el esquema de la base de datos
- **`cronfile`**: Programa la ejecución automática del scraper

---

## ✨ Características Principales

- **🤖 Scraping automatizado** con Selenium en modo headless
- **💾 Persistencia de datos** en base de datos SQLite con Django ORM
- **⏰ Ejecución programada** mediante Cron Jobs (cada 5 minutos en pruebas)
- **🐳 Completamente dockerizado** para facilitar despliegue y portabilidad
- **📝 Sistema de logs** para trazabilidad y debugging
- **🔒 Validación de duplicados** para mantener la integridad de datos
- **🧪 Tests unitarios** para garantizar calidad del código
- **🏗️ Arquitectura modular** basada en POO y buenas prácticas

---

## 🛠️ Tecnologías

**Backend & Framework:**
- Python 3.11
- Django 5.0
- Django ORM

**Web Scraping:**
- Selenium 4.0
- Firefox + GeckoDriver (headless)

**Base de Datos:**
- SQLite (fase inicial, migrable a PostgreSQL/MySQL)

**Automatización & Deployment:**
- Docker & Docker Compose
- Cron (dentro del contenedor)

**Control de Versiones:**
- Git / GitHub
- Gestión del proyecto: GitHub Projects

---

## 🚀 Inicio Rápido

### Prerrequisitos

- Docker y Docker Compose instalados
- Git

### Instalación y Ejecución

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Bootcamp-IA-P6/Proyecto3-Jonathan_Brasales.git
   cd webscraper
   ```

2. **Construir y levantar el contenedor**
   ```bash
   docker compose up --build -d
   ```

3. **Verificar que el contenedor está corriendo**
   ```bash
   docker ps
   ```
   
   Deberías ver un contenedor llamado `webscraper-server-1` en estado `Up`.

4. **El scraper se ejecuta automáticamente cada 5 minutos**. Para verificar su funcionamiento inmediatamente, podemos usar:
   ```bash
   docker exec -it webscraper-server-1 python manage.py scraper_wiki
   ```

### Detener el Proyecto

```bash
docker compose down
```

Para detener sin eliminar datos:
```bash
docker compose stop
```

---

## 💻 Uso y Comandos

### Ejecutar el Scraper Manualmente

```bash
docker exec -it webscraper-server-1 python manage.py scraper_wiki
```

### Ver logs del Cron

```bash
# Opción 1: Desde fuera del contenedor
docker exec -it webscraper-server-1 cat /var/log/cron.log

# Opción 2: Entrando al contenedor
docker exec -it webscraper-server-1 bash
cat /var/log/cron.log
```

---

## 🗄️ Base de Datos

Los datos extraídos se almacenan en **SQLite** con la siguiente estructura:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | Integer | ID único (Primary Key) |
| `title` | String | Título del recurso |
| `description` | Text | Descripción completa |
| `image_url` | URL | URL de la imagen asociada |
| `source` | String | Fuente del dato (ej: Wikipedia) |
| `created_at` | DateTime | Fecha y hora de extracción |

### Consultar la Base de Datos

```bash
# Acceder al contenedor
docker exec -it webscraper-server-1 bash

# Instalar SQLite (si no está instalado)
apt-get update && apt-get install -y sqlite3

# Abrir la base de datos
sqlite3 db.sqlite3

# Comandos útiles dentro de SQLite
.tables                           # Ver tablas
SELECT * FROM scraper_scrapeddata; # Consultar datos
.exit                             # Salir
```

---

## 🧪 Testing

### Ejecutar Tests

```bash
docker exec -it webscraper-server-1 python manage.py test
```

### Cobertura de Tests

Los tests verifican:
- ✅ Inserción correcta de datos en la base de datos
- ✅ Validación de duplicados
- ✅ Ejecución del comando de scraping sin errores

Django crea una base de datos temporal durante los tests, por lo que no afecta los datos reales.

---

## ⏱️ Automatización

El scraper se ejecuta automáticamente mediante **Cron Jobs** configurados dentro del contenedor Docker.

### Configuración Actual

```cron
*/5 * * * * /usr/local/bin/python /app/manage.py scraper_wiki >> /var/log/cron.log 2>&1
```

**Traducción:** Cada 5 minutos ejecuta el scraper y registra la salida en `/var/log/cron.log`.

### Modificar la Frecuencia

Edita el archivo `cronfile` antes de construir el contenedor:

```cron
# Cada hora
0 * * * * /usr/local/bin/python /app/manage.py scraper_wiki >> /var/log/cron.log 2>&1

# Cada día a las 2 AM
0 2 * * * /usr/local/bin/python /app/manage.py scraper_wiki >> /var/log/cron.log 2>&1

# Cada lunes a las 9 AM
0 9 * * 1 /usr/local/bin/python /app/manage.py scraper_wiki >> /var/log/cron.log 2>&1
```

Después de modificar, reconstruye el contenedor:
```bash
docker compose up --build -d
```

### Verificar que Cron está Activo

```bash
docker exec -it webscraper-server-1 bash
ps aux | grep cron
```

---

## 🚀 Próximos Pasos

- [ ] **Frontend interactivo** para visualizar datos en tiempo real
  - Tecnologías candidatas: Django Templates, Chart.js, o React
- [ ] **Despliegue público** en servidor accesible
  - Opciones: AWS, DigitalOcean, Heroku, Railway
- [ ] **Integración con múltiples sitios web** (portales de empleo, marketplaces)
- [ ] **Migración a PostgreSQL** para mayor escalabilidad
- [ ] **API REST** para consumir los datos desde aplicaciones externas
- [ ] **Sistema de notificaciones** cuando se detecten cambios relevantes

---

## 🤝 Contribuciones

Aunque este es un proyecto individual, las contribuciones son bienvenidas. Si encuentras un bug o tienes una sugerencia:

1. **Abre un Issue** describiendo el problema o la mejora
2. **Fork** el repositorio
3. **Crea una rama** para tu feature (`git checkout -b feature/nueva-funcionalidad`)
4. **Commit** tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
5. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
6. **Abre un Pull Request**

### Áreas donde Puedes Contribuir

- 🧪 Ampliar la suite de tests
- 🎨 Desarrollar el frontend
- 📊 Crear visualizaciones de datos
- 🌐 Añadir scrapers para otros sitios web
- 📖 Mejorar la documentación
- 🐛 Reportar y corregir bugs

---

## 📄 Licencia

Este proyecto se desarrolla con fines educativos como parte de un reto técnico de web scraping y automatización.

**Consideraciones éticas:**
- ✅ Se respeta el archivo `robots.txt` de los sitios web
- ✅ El scraping se realiza a intervalos razonables para no sobrecargar servidores
- ✅ Los datos se utilizan exclusivamente con fines de aprendizaje y análisis técnico
- ✅ No se distribuyen datos sensibles o con copyright

---

## 👤 Autor

**Desarrollador:** Jonathan Brasales
**Proyecto:** Reto técnico de Web Scraping
**Contacto:** 
- 💼 LinkedIn: [jbrasales](https://www.linkedin.com/in/jbrasales/)
- 🐙 GitHub: [@tu-usuario](https://github.com/tu-usuario)

**Tablero del Proyecto:** [GitHub Projects](https://github.com/orgs/Bootcamp-IA-P6/projects/12)

---

## 🙏 Agradecimientos

- **Factoría F5** por los recursos y materiales de referencia
- Comunidad de **Django** y **Selenium** por la documentación
- **XYZ Corp** por plantear el reto técnico

---

<div align="center">
  
**⭐ Si este proyecto te resulta útil, considera darle una estrella ⭐**

Hecho con ❤️ usando Python, Django y Docker

</div>
