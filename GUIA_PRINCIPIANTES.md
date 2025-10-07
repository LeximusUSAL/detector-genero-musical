# 🎵 Guía para Principiantes (Sin Conocimientos de Informática)

## ¿Qué hace este programa?

Este programa **lee archivos de texto** (revistas musicales, artículos) y **cuenta automáticamente** cuántas veces aparecen hombres y mujeres músicos. Luego te da un **informe con gráficos**.

---

## ⚠️ Antes de empezar

**Necesitas tener instalado:**
- **Python 3** (un programa para ejecutar scripts)

**¿No sabes si lo tienes?** Sigue estos pasos:

### En Mac:
1. Abre la aplicación **Terminal** (búscala en Spotlight con Cmd+Espacio)
2. Escribe esto y pulsa Enter:
   ```bash
   python3 --version
   ```
3. Si ves algo como `Python 3.11.5` → ✅ **Lo tienes instalado**
4. Si ves un error → ❌ **Necesitas instalarlo** (busca "instalar Python 3 en Mac" en Google)

### En Windows:
1. Abre **Símbolo del sistema** (búscalo en el menú Inicio)
2. Escribe esto y pulsa Enter:
   ```bash
   python --version
   ```
3. Si ves algo como `Python 3.11.5` → ✅ **Lo tienes instalado**
4. Si ves un error → ❌ **Descárgalo de** https://www.python.org/downloads/

---

## 📥 Paso 1: Descargar el programa

### Opción A: Descargar como ZIP (MÁS FÁCIL) ⭐ RECOMENDADO

1. **Ve a:** https://github.com/LeximusUSAL/detector-genero-musical
2. **Haz clic** en el botón verde que dice **"< > Code"** (arriba a la derecha)
3. **Selecciona** "Download ZIP" (opción al final del menú)
4. **Guarda** el archivo en tu escritorio
5. **Descomprime** el archivo ZIP (doble clic en él)
6. Ahora tendrás una carpeta llamada `detector-genero-musical-main` en tu escritorio

**Renombra** la carpeta a `detector-genero-musical` (quita el "-main") para que sea más fácil de escribir.

### Opción B: Usar Terminal/Consola (si sabes usar comandos)

```bash
git clone https://github.com/LeximusUSAL/detector-genero-musical.git
cd detector-genero-musical
```

---

## 📂 Paso 2: Preparar tus archivos de texto

**IMPORTANTE:** Tus archivos deben estar en formato `.txt` (texto plano).

**Ejemplo de organización:**

```
Mi_Carpeta_de_Textos/
├── revista_1920_01.txt
├── revista_1920_02.txt
├── revista_1921_01.txt
└── revista_1921_02.txt
```

**¿Tienes archivos PDF?** Necesitas convertirlos a `.txt` primero:
- En Mac: Abre el PDF, ve a Archivo > Exportar como texto
- En Windows: Usa Adobe Reader > Archivo > Guardar como texto
- O usa una web como https://pdftotext.com/

---

## ▶️ Paso 3: Ejecutar el programa

### En Mac:

1. **Abre Terminal** (Cmd+Espacio, escribe "Terminal")

2. **Ve a la carpeta del programa** (escribe esto y pulsa Enter):
   ```bash
   cd ~/Desktop/detector-genero-musical
   ```
   *(Asume que descomprimiste y renombraste la carpeta en el escritorio)*

3. **Ejecuta el programa** (copia y pega TODA esta línea):
   ```bash
   python3 detector_genero_musical.py ~/Desktop/Mi_Carpeta_de_Textos
   ```

   **¡OJO!** Cambia `~/Desktop/Mi_Carpeta_de_Textos` por la **ruta real** donde tienes tus archivos `.txt`

### En Windows:

1. **Abre Símbolo del sistema** (Win+R, escribe `cmd`, Enter)

2. **Ve a la carpeta del programa**:
   ```bash
   cd %USERPROFILE%\Desktop\detector-genero-musical
   ```

3. **Ejecuta el programa**:
   ```bash
   python detector_genero_musical.py C:\Users\TuNombre\Desktop\Mi_Carpeta_de_Textos
   ```

   **¡OJO!** Cambia la ruta por donde tienes tus archivos

---

## 🤔 No sé cuál es la ruta de mi carpeta

### Método fácil (Mac):

1. **Arrastra la carpeta** donde tienes los `.txt` al Terminal
2. Se pegará automáticamente la ruta completa
3. Cópiala y úsala en el comando

### Método fácil (Windows):

1. **Abre la carpeta** donde están tus archivos
2. **Haz clic** en la barra de direcciones (arriba)
3. **Copia** la ruta (Ctrl+C)
4. **Pégala** en el comando

---

## ✅ Paso 4: Ver los resultados

El programa creará **3 archivos** en la misma carpeta donde está el script:

1. **`analisis_genero.html`** ← 🌐 **ABRE ESTE** (doble clic)
   - Gráficos interactivos bonitos
   - Fácil de entender

2. **`reporte_genero.txt`** ← 📄 Resumen en texto simple
   - Ábrelo con Bloc de notas / TextEdit

3. **`resultados_deteccion_genero.json`** ← 🔧 Datos técnicos
   - No lo necesitas abrir (es para programadores)

---

## 🚨 Problemas comunes

### Error: "python3: command not found"

**En Mac:**
- Prueba con `python` en vez de `python3`
- O instala Python 3 desde https://www.python.org/downloads/

**En Windows:**
- Prueba con `python` en vez de `python3`

### Error: "No such file or directory"

**Solución:**
- Verifica que la ruta de tu carpeta sea correcta
- Asegúrate de que los archivos sean `.txt` (no `.pdf` o `.docx`)

### Error: "No se encuentran archivos TXT"

**Solución:**
- Revisa que tus archivos tengan la extensión `.txt`
- Mira dentro de la carpeta que especificaste (puede que estén en una subcarpeta)

### El programa se ejecuta pero dice "0 archivos encontrados"

**Solución:**
- Tus archivos NO están en formato `.txt`
- Convierte tus PDFs o Word a texto plano primero

---

## 📞 ¿Necesitas ayuda?

**Si tienes problemas:**

1. **Revisa** que Python 3 esté instalado (`python3 --version`)
2. **Verifica** que tus archivos sean `.txt`
3. **Comprueba** que la ruta de la carpeta sea correcta
4. **Lee** la sección "Solución de Problemas" del tutorial completo: https://github.com/LeximusUSAL/detector-genero-musical/blob/main/TUTORIAL_DETECTOR_GENERO.md

**Si nada funciona:**
- Abre un "Issue" en GitHub: https://github.com/LeximusUSAL/detector-genero-musical/issues
- Describe exactamente qué error ves (copia el mensaje de error)

---

## 🎓 Ejemplo completo paso a paso

**Imagina que tienes:**
- 10 archivos `.txt` de revistas musicales
- Están en tu escritorio en una carpeta llamada "MisRevistas"

**Pasos:**

1. **Descargar el programa** (Opción A del Paso 1)
2. **Abrir Terminal** (Mac) o Símbolo del sistema (Windows)
3. **Escribir**:

   **Mac:**
   ```bash
   cd ~/Desktop/detector-genero-musical
   python3 detector_genero_musical.py ~/Desktop/MisRevistas
   ```

   **Windows:**
   ```bash
   cd %USERPROFILE%\Desktop\detector-genero-musical
   python detector_genero_musical.py %USERPROFILE%\Desktop\MisRevistas
   ```

4. **Esperar** (puede tardar unos segundos/minutos)
5. **Abrir** `analisis_genero.html` (doble clic)
6. **Ver los gráficos** 🎉

---

## ✨ Consejo final

**La primera vez puede parecer complicado**, pero una vez que lo hagas UNA vez, las siguientes serán **muy fáciles**.

Si tienes dudas, **pide ayuda a alguien que sepa usar la Terminal/Consola** para que te guíe la primera vez. ¡Es más fácil de lo que parece!

---

**Creado por:** Proyecto LexiMus - Universidad de Salamanca
**Licencia:** MIT (uso libre)
