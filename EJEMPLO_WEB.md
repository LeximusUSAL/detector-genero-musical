# 🌐 Ejemplo de Web Interactiva Generada

Este documento muestra cómo se ve la **web interactiva automática** generada por el script.

---

## 📸 Capturas de Pantalla

### 1. Vista General - Header y Estadísticas

El header muestra el título del proyecto con gradiente púrpura y 4 tarjetas estadísticas principales:

```
┌─────────────────────────────────────────────────────────────┐
│   🎵 Análisis de Género en Personas Musicales              │
│   Proyecto LexiMus - Universidad de Salamanca              │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│     👨       │  │     👩       │  │     📊       │  │     📄       │
│   12,458     │  │     701      │  │  17.78:1     │  │     523      │
│  Masculinas  │  │  Femeninas   │  │Ratio Sesgo   │  │   Archivos   │
│   (94.7%)    │  │    (5.3%)    │  │  Masc:Fem    │  │  Analizados  │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

**Características:**
- Cards con efecto hover (elevación al pasar mouse)
- Colores codificados: Azul (masculino), Rosa (femenino), Naranja (ratio)
- Porcentajes calculados automáticamente

---

### 2. Panel de Interpretación Contextual

Caja coloreada según la severidad del sesgo:

```
┌─────────────────────────────────────────────────────────────┐
│ 📈 Interpretación del Sesgo de Género                       │
│                                                              │
│ ❌ Sesgo extremo detectado. La dominancia masculina es      │
│    severa (17.78:1), indicando una representación casi      │
│    exclusiva de hombres en el corpus analizado.             │
│                                                              │
│ Contexto: En el proyecto LexiMus, el análisis de 25.8       │
│ millones de palabras en prensa musical española (1842-2024) │
│ reveló un ratio de 17.8:1, evidenciando dominancia          │
│ masculina histórica en el periodismo musical.               │
└─────────────────────────────────────────────────────────────┘
```

**Códigos de color:**
- 🔴 Rojo: Sesgo extremo (>10:1)
- 🟡 Amarillo: Sesgo alto (5-10:1)
- 🔵 Azul: Sesgo moderado (2-5:1)
- 🟢 Verde: Equilibrado (<2:1)

---

### 3. Gráfico de Pastel (Chart.js)

Visualización circular interactiva de la distribución:

```
        Distribución General por Género

                  5.3%
                  [Rosa]

              ╱────────╲
            ╱            ╲
          ╱                ╲
        ╱       94.7%        ╲
       │       [Azul]         │
        ╲                    ╱
          ╲                ╱
            ╲────────────╱

         ○ Masculino   ○ Femenino
```

**Interactividad:**
- Tooltip al hover: "Masculino: 12,458 (94.7%)"
- Click en leyenda para ocultar/mostrar
- Animación al cargar la página

---

### 4. Gráfico de Barras Comparativo

Comparación por archivo (top 20):

```
📈 Comparativa por Archivo (Top 20)

Menciones
   │
100│     ██
 90│ ██  ██  ██
 80│ ██  ██  ██  ██
 70│ ██  ██  ██  ██  ██
 60│ ██  ██  ██  ██  ██  ██
 50│ ██  ██  ██  ██  ██  ██  ██
 40│ ██  ██  ██  ██  ██  ██  ██  ██
 30│ ██  ██  ██  ██  ██  ██  ██  ██  ██
 20│ ██  ██  ██  ██  ██  ██  ██  ██  ██  ██
 10│ ██  ██  ██  ██  ██  ██  ██  ██  ██  ██
  0└───┴───┴───┴───┴───┴───┴───┴───┴───┴───
    archivo1  archivo2  archivo3  ...

    ■ Masculinas  ■ Femeninas
```

**Características:**
- Barras agrupadas (no apiladas) para comparación directa
- Tooltip muestra ratio de cada archivo
- Etiquetas rotadas 45° para legibilidad
- Top 20 archivos con mayor actividad

---

### 5. Rankings de Nombres

Dos columnas con los nombres más mencionados:

```
┌─────────────────────────────┐  ┌─────────────────────────────┐
│ 👨 Top 10 Masculinos        │  │ 👩 Top 10 Femeninos         │
├─────────────────────────────┤  ├─────────────────────────────┤
│ Manuel          156 menc.   │  │ María           89 menc.    │
│ José            142 menc.   │  │ Carmen          67 menc.    │
│ Antonio         128 menc.   │  │ Dolores         45 menc.    │
│ Francisco       115 menc.   │  │ Isabel          38 menc.    │
│ Juan            98 menc.    │  │ Teresa          32 menc.    │
│ Pedro           87 menc.    │  │ Rosa            28 menc.    │
│ Carlos          76 menc.    │  │ Ana             25 menc.    │
│ Miguel          65 menc.    │  │ Mercedes        22 menc.    │
│ Rafael          54 menc.    │  │ Pilar           19 menc.    │
│ Luis            48 menc.    │  │ Concepción      17 menc.    │
└─────────────────────────────┘  └─────────────────────────────┘
```

**Características:**
- Cards individuales con sombra
- Nombres capitalizados automáticamente
- Conteo de menciones totales
- Fondo gris claro para contraste

---

### 6. Metadata del Análisis

Información técnica en grid responsive:

```
ℹ️ Información del Análisis

┌────────────────────────────┐  ┌────────────────────────────┐
│ 📂 Directorio analizado    │  │ 📝 Total de palabras       │
│    /corpus/revistas/       │  │    2,580,000               │
└────────────────────────────┘  └────────────────────────────┘

┌────────────────────────────┐  ┌────────────────────────────┐
│ 📅 Fecha de análisis       │  │ 🔬 Metodología             │
│    2025-10-07T15:30:00     │  │    Detección lingüística   │
└────────────────────────────┘  └────────────────────────────┘
```

---

### 7. Footer con Enlaces

```
┌─────────────────────────────────────────────────────────────┐
│ Proyecto LexiMus - Universidad de Salamanca,                │
│ Instituto Complutense de Ciencias Musicales,                │
│ Universidad de La Rioja                                      │
│                                                              │
│ Financiación: PID2022-139589NB-C33                          │
│                                                              │
│ 🔗 GitHub Repository | 📊 Datos JSON                        │
│                                                              │
│ 🤖 Generado con Detector Automático de Género Musical v1.0  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 Paleta de Colores

| Elemento | Color | Uso |
|----------|-------|-----|
| **Masculino** | `#3498db` (Azul) | Cards, gráficos |
| **Femenino** | `#e91e63` (Rosa) | Cards, gráficos |
| **Ratio** | `#f39c12` (Naranja) | Card de ratio |
| **Archivos** | `#9b59b6` (Púrpura) | Card de archivos |
| **Header** | `linear-gradient(135deg, #667eea, #764ba2)` | Fondo degradado |
| **Background** | `#f8f9fa` (Gris claro) | Secciones alternas |

---

## 📱 Responsive Design

La web se adapta automáticamente a diferentes tamaños:

### Desktop (>1200px)
- Grid de 4 columnas para stats
- Gráficos a ancho completo
- Nombres en 2 columnas lado a lado

### Tablet (768px - 1200px)
- Grid de 2 columnas para stats
- Gráficos ajustados
- Nombres en 2 columnas estrechas

### Mobile (<768px)
- Cards en columna única
- Gráficos verticales
- Nombres apilados verticalmente

---

## 🔧 Tecnologías Utilizadas

| Tecnología | Versión | Uso |
|------------|---------|-----|
| **Chart.js** | 4.4.0 | Gráficos interactivos |
| **HTML5** | - | Estructura semántica |
| **CSS3** | - | Estilos y animaciones |
| **JavaScript ES6** | - | Interactividad |
| **CDN** | jsDelivr | Carga de Chart.js |

**Ventajas:**
- ✅ Sin instalación de librerías (CDN)
- ✅ Funciona offline (excepto Chart.js en primera carga)
- ✅ Compatible con todos los navegadores modernos
- ✅ Peso total: ~50 KB (sin imágenes)

---

## 💡 Casos de Uso

### 1. Presentación académica
Abrir la web durante conferencias para mostrar resultados en tiempo real.

### 2. Publicación en sitio web
Subir el HTML a un servidor para compartir públicamente.

### 3. Análisis exploratorio
Navegar interactivamente por los datos antes de escribir el artículo.

### 4. Comparación temporal
Generar múltiples HTMLs para diferentes períodos y compararlos.

---

## 🚀 Ejemplo de Ejecución

```bash
$ python3 detector_genero_musical.py

🎵 DETECTOR AUTOMÁTICO DE GÉNERO EN PERSONAS MUSICALES
================================================================================
📂 Directorio: /corpus/revistas

📂 Analizando directorio: /corpus/revistas
📄 Encontrados 523 archivos TXT
⚙️  Procesando 1/523: revista_1842_01.txt
⚙️  Procesando 2/523: revista_1842_02.txt
...
⚙️  Procesando 523/523: revista_2024_12.txt

✅ Resultados guardados en: resultados_deteccion_genero.json
✅ Reporte guardado en: reporte_genero.txt
✅ Web interactiva generada: analisis_genero.html

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

Luego simplemente:

```bash
$ open analisis_genero.html
```

¡Y la web se abre automáticamente en tu navegador predeterminado! 🎉

---

## 📊 Comparación de Formatos

| Formato | Ventajas | Limitaciones |
|---------|----------|--------------|
| **HTML (NUEVO)** | Interactivo, visual, gráficos, fácil de compartir | Requiere navegador |
| **JSON** | Máquina-legible, programable, completo | No es legible para humanos |
| **TXT** | Simple, portátil, legible | No es visual, sin gráficos |

**Recomendación:** Usa los 3 formatos según tu necesidad:
- 🌐 HTML para presentaciones y exploración
- 📊 JSON para análisis programático posterior
- 📝 TXT para referencias rápidas en terminal

---

**Última actualización:** Octubre 2025
**Versión:** 1.1 (con web interactiva)
