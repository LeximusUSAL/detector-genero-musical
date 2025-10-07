# 🎵 Detector Automático de Género en Personas Musicales

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

**Herramienta de análisis lingüístico-computacional para detectar sesgo de género en prensa musical histórica y contemporánea.**

---

## 📖 Descripción

Este proyecto proporciona un **script en Python** que analiza automáticamente textos musicales (revistas, prensa, críticas) para identificar y cuantificar menciones de **hombres y mujeres** relacionados con la música.

### Características principales

✅ **Detección automática** de nombres propios masculinos/femeninos (80+ nombres históricos)
✅ **Análisis de tratamientos formales** (Don/Doña, Sr./Sra., Maestro/Maestra)
✅ **Profesiones musicales** con marcadores de género (40+ términos)
✅ **Cálculo de ratios de sesgo** (ej: 17.8:1 masculino:femenino)
✅ **Web interactiva automática** con gráficos Chart.js (NUEVO 🌐)
✅ **Exportación JSON** para visualización de datos
✅ **Reporte en texto plano** legible para investigadores
✅ **Adaptable a diferentes épocas** (1842-2024)

---

## 🎯 Contexto Académico

**Proyecto:** [LexiMus: Léxico y ontología de la música en español]([https://leximususal.github.io/inicio/])
**Instituciones:** Universidad de Salamanca, Instituto Complutense de Ciencias Musicales, Universidad de La Rioja
**Financiación:** PID2022-139589NB-C33

### Hallazgos del proyecto LexiMus

Análisis de **25.8 millones de palabras** en prensa musical española (1842-2024):

- **Ratio de sesgo general:** 17.8:1 (masculino:femenino)
- **Menciones profesionales:** 166.8:1 dominancia masculina
- **Corpus analizado:** 3,238 archivos de 19 revistas musicales

Este script permite **replicar y extender** estos análisis en otros corpus.

---

## 🚀 Inicio Rápido

### 1. Requisitos

- Python 3.7 o superior
- Solo bibliotecas estándar (no requiere `pip install`)

### 2. Instalación

```bash
# Clonar el repositorio
git clone https://github.com/LeximusUSAL/detector-genero-musical.git
cd detector-genero-musical

# Dar permisos de ejecución
chmod +x detector_genero_musical.py
```

### 3. Uso básico

```bash
# Editar la ruta del directorio en línea 450 del script
nano detector_genero_musical.py

# Modificar esta línea:
directorio_base = "/ruta/a/tus/archivos/txt"

# Ejecutar
python3 detector_genero_musical.py
```

### 4. Resultados

El script genera automáticamente **3 archivos**:

- **`analisis_genero.html`** - 🌐 **Web interactiva con gráficos** (Chart.js)
- **`resultados_deteccion_genero.json`** - Datos completos estructurados
- **`reporte_genero.txt`** - Resumen legible con interpretación

**Ejemplo de salida:**

```
================================================================================
✅ ANÁLISIS COMPLETADO
================================================================================
👨 Menciones masculinas: 12,458
👩 Menciones femeninas: 701
📊 Ratio de sesgo: 17.78:1

📁 Archivos generados:
   - resultados_deteccion_genero.json (datos completos)
   - reporte_genero.txt (resumen legible)
   - analisis_genero.html (web interactiva)

🌐 Abre 'analisis_genero.html' en tu navegador para ver los resultados interactivos
```

### 5. Ver resultados en web

Abre el archivo `analisis_genero.html` en cualquier navegador:

```bash
# Mac
open analisis_genero.html

# Linux
xdg-open analisis_genero.html

# Windows
start analisis_genero.html
```

**La web incluye:**
- 📊 Gráfico de pastel interactivo (distribución masculino/femenino)
- 📈 Gráfico de barras comparativo (top 20 archivos)
- 👥 Rankings de nombres más mencionados (top 10 de cada género)
- 🎨 Diseño responsive y profesional con gradientes
- 📱 Compatible con móviles y tablets
- 🔗 Enlaces a datos JSON y repositorio GitHub

---

## 📚 Documentación Completa

**[📖 TUTORIAL COMPLETO](./TUTORIAL_DETECTOR_GENERO.md)** - Guía paso a paso con:

- Instalación detallada

**[🌐 EJEMPLO WEB INTERACTIVA](./EJEMPLO_WEB.md)** - Capturas visuales de la interfaz generada:

- ASCII art de cada sección
- Paleta de colores y diseño responsive
- Casos de uso y comparación de formatos
- Configuración avanzada (agregar nombres, profesiones)
- Adaptación a diferentes épocas (s. XIX, XX, XXI)
- Casos de uso académicos
- Interpretación de resultados
- Solución de problemas

---

## 🔍 ¿Qué Detecta?

### 1. Nombres propios

**Masculinos:** Manuel, Antonio, José, Francisco, Juan, Carlos, Miguel, Pablo...
**Femeninos:** María, Carmen, Dolores, Pilar, Teresa, Ana, Rosa, Mercedes...

### 2. Tratamientos formales

| Masculino | Femenino |
|-----------|----------|
| Don, D. | Doña, Dª, Dña. |
| Sr., Señor | Sra., Señora |
| Maestro, Mtro. | Maestra, Mtra. |

### 3. Profesiones musicales

| Masculino | Femenino |
|-----------|----------|
| Compositor, director, tenor, barítono | Compositora, directora, soprano, contralto |
| Pianista, violinista, guitarrista | Pianista, violinista, guitarrista |
| Crítico, musicólogo, virtuoso | Crítica, musicóloga, virtuosa |

### 4. Métricas calculadas

- **Totales:** Menciones masculinas vs. femeninas por archivo y globales
- **Ratio de sesgo:** Proporción masculino:femenino (ej: 17.8:1)
- **Porcentajes:** Representación relativa (ej: 94.7% masculino, 5.3% femenino)
- **Top 10 archivos** con mayor sesgo

---

## 🛠️ Personalización

### Agregar nombres específicos

Edita las líneas 30-65 del script:

```python
self.nombres_masculinos.update({
    'albéniz', 'granados', 'falla', 'turina',  # Compositores españoles
    'pau', 'jordi', 'quim',                    # Nombres catalanes
})

self.nombres_femeninos.update({
    'montserrat', 'mercè', 'núria',            # Nombres catalanes
    'rosalía', 'emilia', 'consuelo',           # Cantantes históricas
})
```

### Agregar profesiones

Edita las líneas 90-120:

```python
self.profesiones_masculinas.extend([
    'jazzista', 'tocaor', 'rockero', 'dj'
])

self.profesiones_femeninas.extend([
    'jazzista', 'cantaora', 'bailaora', 'rockera', 'dj'
])
```

---

## 📊 Casos de Uso

### 1. Análisis de revista específica

```python
detector = DetectorGeneroMusical("/corpus/Revista-Musical-Bilbao-1909-1913")
resultados = detector.analizar_directorio()
```

**Pregunta:** ¿Hubo cambios en representación femenina entre 1909-1913?

### 2. Comparación temporal

```bash
python3 detector_genero_musical.py --dir="/corpus/1920-1930"
python3 detector_genero_musical.py --dir="/corpus/2010-2020"
```

**Pregunta:** ¿Evolucionó el sesgo de género en 100 años?

### 3. Análisis por género periodístico

```python
detector_criticas = DetectorGeneroMusical("/corpus/criticas")
detector_entrevistas = DetectorGeneroMusical("/corpus/entrevistas")
```

**Pregunta:** ¿Difiere el sesgo en críticas vs. entrevistas?

---

## 📈 Interpretación de Resultados

| Ratio | Interpretación |
|-------|---------------|
| **1:1** | Paridad perfecta (ideal) |
| **2:1 a 5:1** | Sesgo moderado |
| **5:1 a 10:1** | Sesgo alto |
| **10:1 a 20:1** | Sesgo extremo (común en prensa musical histórica) |
| **>20:1** | Exclusión sistemática de mujeres |

**Ejemplo del proyecto LexiMus:**
Ratio **17.8:1** en corpus completo → **Dominancia masculina severa** en periodismo musical español (1842-2024).

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas!

1. **Fork** del repositorio
2. Crea una rama: `git checkout -b mejora-deteccion-flamenco`
3. Commit: `git commit -m "Agregar términos de flamenco"`
4. Push: `git push origin mejora-deteccion-flamenco`
5. Abre un **Pull Request**

### Ideas para contribuir

- Agregar nombres de músicos/as de otras regiones (Cataluña, País Vasco, Galicia)
- Expandir profesiones (jazz, flamenco, rock, electrónica)
- Mejorar algoritmos de detección contextual
- Agregar soporte para otros idiomas (catalán, gallego, euskera)

---

## 📄 Licencia

**MIT License** - Uso libre para investigación académica.

```
Copyright (c) 2025 Proyecto LexiMus - Universidad de Salamanca

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

Ver [LICENSE](./LICENSE) para más detalles.

---

## 📚 Citar este trabajo

Si utilizas esta herramienta en tu investigación, cita:

```bibtex
@software{detector_genero_musical_2025,
  author = {Proyecto LexiMus},
  title = {Detector Automático de Género en Personas Musicales},
  year = {2025},
  publisher = {Universidad de Salamanca},
  url = {https://github.com/LeximusUSAL/detector-genero-musical},
  note = {Herramienta de análisis de sesgo de género en prensa musical}
}
```

---

## 📧 Contacto

**Proyecto LexiMus**
Universidad de Salamanca
Instituto Complutense de Ciencias Musicales
Universidad de La Rioja

**Financiación:** Proyecto PID2022-139589NB-C33
**GitHub:** [https://github.com/LeximusUSAL](https://github.com/LeximusUSAL)

---

## 🙏 Agradecimientos

- **Claude Code** - Generación del código y documentación
- **Proyecto LexiMus** - Contexto académico y datos de validación
- Comunidad de investigadores en Humanidades Digitales Musicales

---

## 🔗 Enlaces Relacionados

- [Tutorial completo](./TUTORIAL_DETECTOR_GENERO.md)
- [Proyecto LexiMus principal](https://github.com/LeximusUSAL)
- [Corpus Ópera Iberia 1842](https://github.com/LeximusUSAL/opera-corpus-iberia-1842)

---

**Última actualización:** Octubre 2025
**Versión:** 1.0.0
