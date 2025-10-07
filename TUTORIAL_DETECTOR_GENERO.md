# Tutorial: Detector Automático de Género en Personas Musicales

**Proyecto:** LexiMus - Universidad de Salamanca
**Herramienta:** `detector_genero_musical.py`
**Versión:** 1.0
**Licencia:** MIT

---

## 📋 Índice

1. [Introducción](#introducción)
2. [Instalación](#instalación)
3. [Uso Básico](#uso-básico)
4. [Configuración Avanzada](#configuración-avanzada)
5. [Adaptación a Diferentes Épocas](#adaptación-a-diferentes-épocas)
6. [Interpretación de Resultados](#interpretación-de-resultados)
7. [Casos de Uso](#casos-de-uso)
8. [Solución de Problemas](#solución-de-problemas)

---

## 🎯 Introducción

Este script detecta **automáticamente** menciones de hombres y mujeres relacionados con la música en textos históricos (prensa, revistas musicales, críticas). Utiliza:

- ✅ **Listas de nombres** españoles históricos y actuales
- ✅ **Tratamientos formales** (Don/Doña, Sr./Sra., Maestro/Maestra)
- ✅ **Profesiones musicales** con marcadores de género
- ✅ **Análisis estadístico** con ratios de sesgo de género

### Características principales

| Característica | Descripción |
|---------------|-------------|
| **Detección automática** | No requiere anotación manual |
| **Perspectiva histórica** | Adaptable a diferentes épocas (1842-2024) |
| **Análisis cuantitativo** | Ratios, porcentajes, comparativas |
| **Exportación JSON** | Datos estructurados para visualización |
| **Reporte texto plano** | Legible para investigadores |

---

## 🔧 Instalación

### Requisitos previos

- **Python 3.7 o superior**
- **Bibliotecas estándar** (no requiere instalación adicional)

### Verificar instalación

```bash
python3 --version
```

Debe mostrar `Python 3.7.0` o superior.

### Descargar el script

```bash
# Opción 1: Clonar repositorio completo
git clone https://github.com/tu-usuario/LexiMusUSAL.git
cd LexiMusUSAL

# Opción 2: Descargar solo el script
curl -O https://raw.githubusercontent.com/tu-usuario/LexiMusUSAL/main/detector_genero_musical.py
```

### Dar permisos de ejecución

```bash
chmod +x detector_genero_musical.py
```

---

## 🚀 Uso Básico

### 1. Preparar tus archivos de texto

Organiza tus archivos `.txt` en un directorio:

```
/mi_proyecto/
  ├── revista_1842_01.txt
  ├── revista_1842_02.txt
  └── revista_1843_01.txt
```

### 2. Modificar la ruta en el script

Abre `detector_genero_musical.py` y modifica la línea 450:

```python
# ANTES
directorio_base = "/Users/maria/Desktop/REVISTAS TXT PARA WEBS ESTADÍSTICAS"

# DESPUÉS
directorio_base = "/ruta/a/tu/proyecto/textos"
```

### 3. Ejecutar el análisis

```bash
python3 detector_genero_musical.py
```

### 4. Revisar los resultados

El script genera dos archivos:

1. **`resultados_deteccion_genero.json`** - Datos completos en formato JSON
2. **`reporte_genero.txt`** - Resumen legible

**Ejemplo de salida en consola:**

```
🎵 DETECTOR AUTOMÁTICO DE GÉNERO EN PERSONAS MUSICALES
================================================================================
📂 Directorio: /mi_proyecto/textos

📂 Analizando directorio: /mi_proyecto/textos
📄 Encontrados 523 archivos TXT
⚙️  Procesando 1/523: revista_1842_01.txt
⚙️  Procesando 2/523: revista_1842_02.txt
...

================================================================================
✅ ANÁLISIS COMPLETADO
================================================================================
👨 Menciones masculinas: 12,458
👩 Menciones femeninas: 701
📊 Ratio de sesgo: 17.78:1

📁 Archivos generados:
   - resultados_deteccion_genero.json (datos completos)
   - reporte_genero.txt (resumen legible)
```

---

## ⚙️ Configuración Avanzada

### Agregar nombres específicos de tu corpus

Si tus textos mencionan músicos/as específicos frecuentemente, agrégalos:

#### Editar la clase (líneas 30-65):

```python
# NOMBRES MASCULINOS
self.nombres_masculinos = {
    # Clásicos existentes...
    'manuel', 'antonio', 'josé',

    # 🆕 AGREGAR TUS NOMBRES ESPECÍFICOS:
    'albéniz', 'granados', 'falla', 'turina',  # Compositores españoles
    'pau', 'jordi', 'quim',                    # Nombres catalanes
    'mikel', 'iker', 'aitor',                  # Nombres vascos
}

# NOMBRES FEMENINOS
self.nombres_femeninos = {
    # Clásicas existentes...
    'maría', 'carmen', 'dolores',

    # 🆕 AGREGAR TUS NOMBRES ESPECÍFICOS:
    'emilia', 'rosalía', 'montserrat',        # Cantantes históricas
    'mercè', 'núria', 'roser',                # Nombres catalanes
    'aitana', 'nerea', 'irati',               # Nombres vascos
}
```

### Ajustar profesiones musicales

Si trabajas con géneros específicos (jazz, flamenco, rock), agrega términos:

#### Editar líneas 90-120:

```python
# PROFESIONES MASCULINAS
self.profesiones_masculinas = [
    # Existentes...
    'compositor', 'pianista', 'violinista',

    # 🆕 AGREGAR ESPECIALIZADAS:
    'jazzista', 'saxofonista', 'baterista',   # Jazz
    'tocaor', 'guitarrista flamenco',         # Flamenco
    'rockero', 'bajista', 'batería',          # Rock/Pop
]

# PROFESIONES FEMENINAS
self.profesiones_femeninas = [
    # Existentes...
    'compositora', 'pianista', 'violinista',

    # 🆕 AGREGAR ESPECIALIZADAS:
    'jazzista', 'saxofonista', 'baterista',   # Jazz
    'cantaora', 'bailaora', 'palmera',        # Flamenco
    'rockera', 'bajista', 'vocalista',        # Rock/Pop
]
```

---

## 📅 Adaptación a Diferentes Épocas

### Para textos del siglo XIX (1842-1900)

**Prioriza:**
- Tratamientos formales: Don/Doña, Sr./Sra.
- Profesiones: compositor, pianista, tenor, soprano
- Nombres clásicos: Manuel, José, Carmen, Dolores

**Modificación recomendada:**

```python
# Agregar nombres del Romanticismo español
self.nombres_masculinos.update({
    'isaac', 'tomás', 'ruperto', 'felipe',
    'emilio', 'baltasar', 'cristóbal'
})

self.nombres_femeninos.update({
    'paulina', 'isabella', 'adelina', 'giulia',
    'teresa', 'rosina', 'amalia'
})
```

### Para textos del siglo XX temprano (1900-1950)

**Prioriza:**
- Profesiones: director, concertista, crítico
- Nombres modernistas
- Términos como "maestro", "virtuoso"

### Para textos contemporáneos (1990-2024)

**Prioriza:**
- Profesiones: DJ, productor/a, manager
- Nombres modernos: Laura, Sara, David, Daniel
- Términos: artista, músico/a, intérprete

**Modificación recomendada:**

```python
# Agregar profesiones modernas
self.profesiones_masculinas.extend([
    'dj', 'productor', 'manager', 'promotor',
    'ingeniero de sonido', 'roadie'
])

self.profesiones_femeninas.extend([
    'dj', 'productora', 'manager', 'promotora',
    'ingeniera de sonido', 'vocalista'
])
```

---

## 📊 Interpretación de Resultados

### Estructura del JSON de salida

```json
{
  "metadata": {
    "directorio": "/ruta/al/corpus",
    "total_archivos": 523,
    "total_palabras": 2580000,
    "fecha_analisis": "2025-10-07T14:32:00"
  },
  "resumen_general": {
    "menciones_masculinas_total": 12458,
    "menciones_femeninas_total": 701,
    "ratio_sesgo_general": 17.78,
    "porcentaje_masculino": 94.67,
    "porcentaje_femenino": 5.33
  },
  "archivos": [
    {
      "archivo": "revista_1842_01.txt",
      "palabras": 4580,
      "detecciones": {
        "nombres": {
          "masculinos": {"manuel": 3, "josé": 5},
          "femeninos": {"carmen": 1},
          "total_masculinos": 8,
          "total_femeninos": 1
        },
        "tratamientos": {
          "masculinos": 12,
          "femeninos": 2
        },
        "profesiones": {
          "masculinas": {"compositor": 4, "pianista": 2},
          "femeninas": {"pianista": 1},
          "total_masculinas": 6,
          "total_femeninas": 1
        }
      },
      "totales": {
        "menciones_masculinas": 26,
        "menciones_femeninas": 4,
        "ratio_sesgo": 6.5
      }
    }
  ]
}
```

### Interpretación del ratio de sesgo

| Ratio | Interpretación |
|-------|---------------|
| **1:1** | Paridad perfecta |
| **2:1 a 5:1** | Sesgo moderado a favor de lo masculino |
| **5:1 a 10:1** | Sesgo alto |
| **10:1 a 20:1** | Sesgo extremo (caso típico prensa musical histórica) |
| **>20:1** | Exclusión sistemática de mujeres |

**Ejemplo real del proyecto LexiMus:**
- **Ratio 17.8:1** en corpus completo (1842-2024)
- **Ratio 166.8:1** en menciones profesionales
- Indica **dominancia masculina severa** en prensa musical española

---

## 🎓 Casos de Uso

### Caso 1: Análisis de una revista específica

```python
# Modificar main() para analizar solo "Revista Musical de Bilbao"
directorio_base = "/corpus/revistas/TXT-Revista-Musical-Bilbao-1909-1913"

detector = DetectorGeneroMusical(directorio_base)
resultados = detector.analizar_directorio()
```

**Pregunta de investigación:**
¿Hubo cambios en la representación de mujeres músicas entre 1909 y 1913?

### Caso 2: Comparación temporal

Ejecuta el análisis por décadas:

```bash
# Década 1920
python3 detector_genero_musical.py --dir="/corpus/1920-1930"

# Década 1980
python3 detector_genero_musical.py --dir="/corpus/1980-1990"

# Década 2010
python3 detector_genero_musical.py --dir="/corpus/2010-2020"
```

Compara los ratios de sesgo para estudiar evolución histórica.

### Caso 3: Análisis por tipo de contenido

```python
# Críticas musicales vs. Entrevistas
detector_criticas = DetectorGeneroMusical("/corpus/criticas")
detector_entrevistas = DetectorGeneroMusical("/corpus/entrevistas")

# ¿Hay diferencias en representación de género según el género periodístico?
```

---

## 🛠️ Solución de Problemas

### Problema 1: "No se encuentran archivos TXT"

**Causa:** Ruta incorrecta o archivos con otra extensión.

**Solución:**
```python
# Verificar que la ruta existe
import os
print(os.path.exists("/ruta/a/tu/directorio"))  # Debe devolver True

# Listar archivos
print(os.listdir("/ruta/a/tu/directorio"))
```

### Problema 2: "El script no detecta nombres conocidos"

**Causa:** Nombres con acentos o mayúsculas inconsistentes.

**Solución:**
```python
# Agregar variantes del nombre
self.nombres_masculinos.update({
    'tomás', 'tomas',  # Con y sin acento
    'josé', 'jose',
})
```

### Problema 3: "Ratio de sesgo es infinito (∞)"

**Causa:** No se detectaron menciones femeninas.

**Interpretación:** Exclusión total de mujeres en el corpus (hallazgo válido).

**Verificación:**
```python
# Revisar manualmente algunos textos
with open("/ruta/archivo.txt", 'r') as f:
    print(f.read()[:500])  # Primeros 500 caracteres
```

### Problema 4: "El análisis es muy lento"

**Causa:** Miles de archivos grandes.

**Solución:** Procesar por lotes
```python
# En vez de todo el directorio, analiza subdirectorios
for subdirectorio in os.listdir(base_directory):
    detector = DetectorGeneroMusical(subdirectorio)
    detector.analizar_directorio()
```

---

## 📚 Referencias Académicas

Si utilizas esta herramienta en tu investigación, cita:

```bibtex
@software{detector_genero_musical_2025,
  author = {Proyecto LexiMus},
  title = {Detector Automático de Género en Personas Musicales},
  year = {2025},
  publisher = {Universidad de Salamanca},
  url = {https://github.com/tu-usuario/LexiMusUSAL}
}
```

---

## 🤝 Contribuciones

Para agregar nombres, profesiones o mejorar el algoritmo:

1. Fork del repositorio
2. Crea una rama: `git checkout -b mejora-deteccion-flamenco`
3. Commit: `git commit -m "Agregar términos de flamenco"`
4. Push: `git push origin mejora-deteccion-flamenco`
5. Abre un Pull Request

---

## 📧 Contacto

**Proyecto:** LexiMus - Universidad de Salamanca
**Financiación:** PID2022-139589NB-C33
**GitHub:** https://github.com/tu-usuario/LexiMusUSAL

---

## 📄 Licencia

MIT License - Uso libre para investigación académica.

---

**Última actualización:** Octubre 2025
**Versión del tutorial:** 1.0
