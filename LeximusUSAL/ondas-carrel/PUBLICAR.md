# 📻 Guía de publicación del carrel ONDAS

## ✅ Estado del carrel

El carrel ONDAS ha sido generado exitosamente con:

- **276 documentos** procesados (1925-1935)
- **564,907 palabras** filtradas y analizadas
- **Estructura completa** de Distant Reader
- **Documentación en español** completa

## 📁 Estructura del carrel

```
ondas-carrel/
├── index.htm          # Página principal con visualizaciones
├── index.xhtml        # Índice bibliográfico navegable
├── index.txt          # Resumen en texto plano
├── index.json         # Datos estructurados (62KB)
├── readme.txt         # Documentación completa
├── bib/               # Metadatos bibliográficos (vacío por ahora)
├── cache/             # Archivos originales (vacío)
├── ent/               # Entidades nombradas (276 archivos)
├── etc/
│   ├── stopwords.txt  # Stopwords español (610 palabras)
│   └── carrel.txt     # Corpus completo (7.1 MB)
├── figures/           # Directorio para visualizaciones (vacío)
├── pos/               # Partes del discurso (276 archivos)
├── txt/               # Textos completos (276 archivos, 7.3 MB)
└── wrd/               # Palabras frecuentes (276 archivos)
```

**Tamaño total:** ~17 MB

## 🌐 Publicación en GitHub Pages

### Opción 1: Repositorio nuevo

```bash
cd /Users/maria/Desktop/LeximusUSAL/ondas-carrel

# Inicializar git
git init
git add .
git commit -m "Carrel ONDAS completo (1925-1935): 276 números digitalizados"

# Crear repositorio en GitHub
# https://github.com/new → Nombre: "ondas-carrel"

# Subir al repositorio
git remote add origin https://github.com/leximususal/ondas-carrel.git
git branch -M main
git push -u origin main

# Activar GitHub Pages
# Settings → Pages → Source: main branch → Save
```

La web estará disponible en: `https://leximususal.github.io/ondas-carrel/`

### Opción 2: Añadir al repositorio existente

```bash
cd /Users/maria/Desktop/LeximusUSAL

# Si ondas-carrel ya está en el repositorio
git add ondas-carrel/
git commit -m "Agregar carrel ONDAS completo con 276 documentos analizados"
git push origin main
```

## 📊 Archivos clave para análisis

### Para investigadores

1. **index.json** - Datos estructurados completos
   - Top 100 palabras, 50 bigrams
   - Entidades: personas, lugares, organizaciones
   - POS: sustantivos, verbos, adjetivos, adverbios
   - Metadata por documento

2. **etc/carrel.txt** - Corpus completo (7.1 MB)
   - Todos los textos concatenados
   - Listo para Voyant Tools, AntConc, etc.

3. **etc/stopwords.txt** - Lista de palabras vacías
   - 610 stopwords en español
   - Compatible con herramientas de análisis

### Para navegación

1. **index.htm** - Interfaz web principal
   - Visualizaciones interactivas
   - Estadísticas resumidas
   - Nubes de palabras CSS

2. **index.xhtml** - Índice navegable
   - Lista completa de documentos
   - Enlaces a archivos individuales
   - Distribución temporal

## 🔗 URLs de acceso

Después de publicar en GitHub Pages:

- **Página principal:** `https://leximususal.github.io/ondas-carrel/`
- **Índice:** `https://leximususal.github.io/ondas-carrel/index.xhtml`
- **Datos JSON:** `https://leximususal.github.io/ondas-carrel/index.json`
- **Corpus completo:** `https://leximususal.github.io/ondas-carrel/etc/carrel.txt`
- **Stopwords:** `https://leximususal.github.io/ondas-carrel/etc/stopwords.txt`

## 📝 Uso con Voyant Tools

### Método 1: Cargar corpus completo

1. Ve a https://voyant-tools.org/
2. Carga la URL: `https://leximususal.github.io/ondas-carrel/etc/carrel.txt`
3. Carga stopwords: `https://leximususal.github.io/ondas-carrel/etc/stopwords.txt`

### Método 2: Cargar múltiples documentos

1. Descarga el directorio `txt/` completo
2. Arrastra los 276 archivos .txt a Voyant Tools
3. Aplica las stopwords personalizadas

## 🎯 Palabras clave principales

Top 5 términos más frecuentes (filtrado español):

1. **orquesta** (4,519 ocurrencias)
2. **radio** (4,299 ocurrencias)
3. **música** (4,240 ocurrencias)
4. **estación** (3,559 ocurrencias)
5. **noticias** (2,992 ocurrencias)

## 📚 Comparación con el carrel El Sol

| Característica | El Sol | ONDAS |
|----------------|--------|-------|
| Documentos | 1,273 | 276 |
| Palabras | 1,197,469 | 564,907 |
| Período | 1918-1935 | 1925-1935 |
| Tipo | Diario | Revista semanal |
| Tema | General + música | Radio + música |
| Legibilidad | 57 | 16.27 |

## ⚙️ Regenerar el carrel

Si necesitas regenerar o actualizar el carrel:

```bash
cd /Users/maria
python3 generador_carrel_ondas.py
```

El script:
- Lee de: `/Users/maria/Desktop/ONDAS/ONDAS TXT PRIMERA TRANSCRIPCIÓN`
- Escribe en: `/Users/maria/Desktop/LeximusUSAL/ondas-carrel`
- Procesa: 276 archivos .txt
- Genera: ~17 MB de datos

## 🔍 Validar el carrel

Para verificar la integridad:

```bash
python3 /Users/maria/validar_carrel_ondas.py
```

Debe mostrar: ✅ VALIDACIÓN EXITOSA

## 📖 Referencias

- **Proyecto:** LexiMus - Léxico y ontología de la música en español
- **Código:** PID2022-139589NB-C33
- **Institución:** Universidad de Salamanca
- **Web:** https://leximususal.github.io/

## 📧 Contacto

Para preguntas sobre este carrel:
- Email: maria@leximususal.es
- GitHub: https://github.com/leximususal

---

**Última actualización:** 7 de noviembre de 2025
**Versión del carrel:** 1.0
**Generado con:** Distant Reader methodology
