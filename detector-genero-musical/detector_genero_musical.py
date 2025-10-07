#!/usr/bin/env python3
"""
Detector Automático de Género en Personas Musicales
Linguistic Gender Detection for Musical Press Analysis

Este script analiza textos musicales (revistas, prensa, corpus) y detecta automáticamente
menciones de hombres y mujeres relacionados con la música mediante:
- Listas de nombres españoles históricos y actuales
- Patrones contextuales de tratamiento formal (Don/Doña, Sr./Sra.)
- Términos profesionales masculinos/femeninos
- Análisis estadístico con ratios de sesgo de género

Proyecto: LexiMus - Universidad de Salamanca
Autor: María [Generado con Claude Code]
Licencia: MIT
"""

import os
import re
import json
from collections import Counter, defaultdict
from datetime import datetime

class DetectorGeneroMusical:
    def __init__(self, base_directory):
        """
        Inicializa el detector de género

        Args:
            base_directory (str): Ruta al directorio con archivos TXT
        """
        self.base_directory = base_directory
        self.resultados = {}
        self.total_archivos = 0
        self.total_palabras = 0

        # =================================================================
        # LISTAS DE NOMBRES INTERNACIONALES (Español, Alemán, Inglés, Francés)
        # =================================================================

        # Nombres masculinos históricos y actuales
        self.nombres_masculinos = {
            # === ESPAÑOLES ===
            # Clásicos históricos (s. XIX-XX)
            'manuel', 'antonio', 'josé', 'francisco', 'juan', 'pedro', 'luis',
            'carlos', 'miguel', 'rafael', 'fernando', 'jesús', 'ángel', 'diego',
            'pablo', 'andrés', 'ramón', 'tomás', 'enrique', 'alberto', 'joaquín',
            'ricardo', 'felipe', 'ignacio', 'jaime', 'sergio', 'alejandro',
            # Compositores/músicos históricos españoles
            'isaac', 'ruperto', 'federico', 'emilio', 'adolfo', 'conrado',
            # Nombres modernos
            'david', 'daniel', 'jorge', 'adrián', 'iván', 'rubén', 'mario',
            'oscar', 'héctor', 'raúl', 'víctor', 'hugo', 'marcos', 'álvaro',

            # === ALEMANES ===
            # Compositores y músicos clásicos
            'wolfgang', 'ludwig', 'johann', 'johannes', 'richard', 'franz',
            'robert', 'felix', 'gustav', 'anton', 'max', 'carl', 'karl',
            'friedrich', 'wilhelm', 'heinrich', 'otto', 'hermann', 'ernst',
            'paul', 'hans', 'klaus', 'günter', 'werner', 'helmut',

            # === INGLESES ===
            # Nombres históricos y modernos
            'william', 'george', 'thomas', 'james', 'john', 'charles',
            'henry', 'edward', 'benjamin', 'samuel', 'andrew', 'michael',
            'peter', 'christopher', 'stephen', 'matthew', 'mark', 'luke',
            'paul', 'simon', 'philip', 'oliver', 'alexander', 'nicholas',

            # === FRANCESES ===
            # Compositores y músicos
            'claude', 'maurice', 'gabriel', 'georges', 'hector', 'camille',
            'jean', 'pierre', 'jacques', 'louis', 'françois', 'rené',
            'andré', 'philippe', 'michel', 'henri', 'marcel', 'antoine',
            'laurent', 'nicolas', 'olivier', 'julien', 'sébastien', 'damien'
        }

        # Nombres femeninos históricos y actuales
        self.nombres_femeninos = {
            # === ESPAÑOLAS ===
            # Clásicos históricos
            'maría', 'carmen', 'josefa', 'dolores', 'pilar', 'teresa',
            'ana', 'francisca', 'isabel', 'rosa', 'antonia', 'mercedes',
            'concepción', 'concha', 'victoria', 'angeles', 'trinidad',
            'encarnación', 'amparo', 'remedios', 'esperanza', 'asunción',
            # Músicas/cantantes históricas
            'consuelo', 'rosario', 'emilia', 'carlota', 'matilde', 'eugenia',
            'margarita', 'carolina', 'elvira', 'adela', 'julia', 'luisa',
            # Nombres modernos
            'laura', 'sara', 'patricia', 'marta', 'elena', 'raquel',
            'cristina', 'paula', 'andrea', 'silvia', 'natalia', 'beatriz',
            'lucía', 'sofía', 'alba', 'claudia', 'sandra', 'mónica',

            # === ALEMANAS ===
            # Compositoras y cantantes
            'clara', 'fanny', 'alma', 'hildegard', 'sophie', 'louise',
            'martha', 'greta', 'helene', 'margarete', 'elisabeth', 'anna',
            'katarina', 'katharina', 'ingrid', 'ursula', 'brigitte', 'petra',
            'angelika', 'monika', 'sabine', 'susanne', 'heike', 'andrea',

            # === INGLESAS ===
            # Nombres históricos y modernos
            'elizabeth', 'mary', 'margaret', 'catherine', 'jane', 'anne',
            'victoria', 'charlotte', 'emily', 'sarah', 'rebecca', 'jessica',
            'jennifer', 'lisa', 'susan', 'patricia', 'barbara', 'linda',
            'emma', 'olivia', 'sophia', 'grace', 'lily', 'lucy', 'amy',

            # === FRANCESAS ===
            # Compositoras y cantantes
            'germaine', 'lili', 'nadia', 'cécile', 'louise', 'pauline',
            'marie', 'jeanne', 'françoise', 'catherine', 'brigitte', 'sylvie',
            'isabelle', 'sophie', 'claire', 'amélie', 'charlotte', 'julie',
            'aurélie', 'mélanie', 'céline', 'valérie', 'sandrine', 'florence'
        }

        # =================================================================
        # TRATAMIENTOS FORMALES
        # =================================================================

        self.tratamientos_masculinos = [
            r'\bdon\s+\w+',           # Don Manuel
            r'\bd\.\s+\w+',           # D. Manuel
            r'\bsr\.\s+\w+',          # Sr. García
            r'\bseñor\s+\w+',         # Señor García
            r'\bmaestro\s+\w+',       # Maestro Albéniz
            r'\bmtro\.\s+\w+',        # Mtro. Albéniz
            r'\bprof\.\s+\w+',        # Prof. García (masculino)
        ]

        self.tratamientos_femeninos = [
            r'\bdoña\s+\w+',          # Doña Carmen
            r'\bdª\.\s+\w+',          # Dª. Carmen
            r'\bdña\.\s+\w+',         # Dña. Carmen
            r'\bsra\.\s+\w+',         # Sra. García
            r'\bseñora\s+\w+',        # Señora García
            r'\bmaestra\s+\w+',       # Maestra Malibran
            r'\bmtra\.\s+\w+',        # Mtra. Malibran
        ]

        # =================================================================
        # TÉRMINOS PROFESIONALES MUSICALES
        # =================================================================

        self.profesiones_masculinas = [
            'compositor', 'pianista', 'violinista', 'director', 'guitarrista',
            'tenor', 'barítono', 'bajo', 'organista', 'concertista',
            'virtuoso', 'solista', 'maestro', 'crítico', 'musicólogo',
            'cantante', 'intérprete', 'ejecutante', 'autor', 'profesor',
            'violonchelista', 'flautista', 'oboísta', 'clarinetista',
            'trompetista', 'violista', 'contrabajista', 'saxofonista'
        ]

        self.profesiones_femeninas = [
            'compositora', 'pianista', 'violinista', 'directora', 'guitarrista',
            'soprano', 'mezzosoprano', 'mezzo-soprano', 'contralto',
            'organista', 'concertista', 'virtuosa', 'solista', 'maestra',
            'crítica', 'musicóloga', 'cantante', 'intérprete', 'ejecutante',
            'autora', 'profesora', 'violonchelista', 'flautista', 'oboísta',
            'clarinetista', 'trompetista', 'violista', 'contrabajista',
            'cantaora', 'bailaora', 'arpista', 'saxofonista'
        ]

        # =================================================================
        # CONTEXTO DIVERSIDAD Y SESGOS
        # =================================================================

        self.terminos_diversidad = [
            'gitano', 'gitana', 'flamenco', 'flamenca', 'afroamericano',
            'afroamericana', 'negro', 'negra', 'judío', 'judía', 'árabe',
            'oriental', 'indígena', 'latinoamericano', 'latinoamericana',
            'hispano', 'hispana', 'mestizo', 'mestiza'
        ]

    # =====================================================================
    # MÉTODOS DE DETECCIÓN
    # =====================================================================

    def detectar_nombres_personas(self, contenido):
        """
        Detecta nombres propios completos (nombre + apellido) usando múltiples patrones contextuales

        Returns:
            dict: {
                'masculinos': Counter,  # Nombres detectados
                'femeninos': Counter,   # Nombres detectados
                'masculinos_completos': list,  # Nombres completos encontrados
                'femeninos_completos': list    # Nombres completos encontrados
            }
        """
        nombres_detectados = {
            'masculinos': Counter(),
            'femeninos': Counter(),
            'masculinos_completos': [],
            'femeninos_completos': []
        }

        # Buscar nombres masculinos con contexto mejorado
        for nombre in self.nombres_masculinos:
            # Patrón 1: Nombre solo (menos peso)
            patron_simple = r'\b' + nombre.capitalize() + r'\b'
            matches_simple = re.finditer(patron_simple, contenido, re.IGNORECASE)

            # Patrón 2: Nombre + Apellido(s) - Más específico
            # Captura: "Manuel de Falla", "José García López", "Isaac Albéniz"
            # Busca nombre + partícula (opcional) + apellido + segundo apellido (opcional)
            patron_completo = r'\b' + nombre.capitalize() + r'\s+(?:de\s+|del\s+|de\s+la\s+|de\s+las\s+|de\s+los\s+|von\s+|van\s+)?[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)?\b'
            matches_completos = list(re.finditer(patron_completo, contenido, re.IGNORECASE))

            # Contar coincidencias de nombres completos (prioritario)
            if matches_completos:
                for match in matches_completos:
                    nombre_completo = match.group(0)
                    # Limpiar: remover palabras en minúscula al final (verbos, artículos)
                    nombre_completo = re.sub(r'\s+[a-záéíóúñ]+$', '', nombre_completo)
                    nombres_detectados['masculinos_completos'].append(nombre_completo)
                    nombres_detectados['masculinos'][nombre] += 1
            else:
                # Si no hay nombre completo, contar menciones simples (con menor certeza)
                count = len(list(matches_simple))
                if count > 0:
                    nombres_detectados['masculinos'][nombre] = count

        # Buscar nombres femeninos con contexto mejorado
        for nombre in self.nombres_femeninos:
            # Patrón 1: Nombre solo
            patron_simple = r'\b' + nombre.capitalize() + r'\b'
            matches_simple = re.finditer(patron_simple, contenido, re.IGNORECASE)

            # Patrón 2: Nombre + Apellido(s)
            # Captura: "María Callas", "Carmen de Burgos", "Rosa García Ascot"
            # Busca nombre + partícula (opcional) + apellido + segundo apellido (opcional)
            patron_completo = r'\b' + nombre.capitalize() + r'\s+(?:de\s+|del\s+|de\s+la\s+|de\s+las\s+|de\s+los\s+|von\s+|van\s+)?[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)?\b'
            matches_completos = list(re.finditer(patron_completo, contenido, re.IGNORECASE))

            if matches_completos:
                for match in matches_completos:
                    nombre_completo = match.group(0)
                    # Limpiar: remover palabras en minúscula al final (verbos, artículos)
                    nombre_completo = re.sub(r'\s+[a-záéíóúñ]+$', '', nombre_completo)
                    nombres_detectados['femeninos_completos'].append(nombre_completo)
                    nombres_detectados['femeninos'][nombre] += 1
            else:
                count = len(list(matches_simple))
                if count > 0:
                    nombres_detectados['femeninos'][nombre] = count

        return nombres_detectados

    def detectar_tratamientos_formales(self, contenido):
        """
        Detecta tratamientos formales (Don, Doña, Sr., Sra., etc.)

        Returns:
            dict: {'masculinos': int, 'femeninos': int}
        """
        tratamientos = {
            'masculinos': 0,
            'femeninos': 0
        }

        # Contar tratamientos masculinos
        for patron in self.tratamientos_masculinos:
            matches = re.findall(patron, contenido, re.IGNORECASE)
            tratamientos['masculinos'] += len(matches)

        # Contar tratamientos femeninos
        for patron in self.tratamientos_femeninos:
            matches = re.findall(patron, contenido, re.IGNORECASE)
            tratamientos['femeninos'] += len(matches)

        return tratamientos

    def detectar_profesiones_musicales(self, contenido):
        """
        Detecta menciones de profesiones musicales por género

        Returns:
            dict: {'masculinas': Counter, 'femeninas': Counter}
        """
        profesiones = {
            'masculinas': Counter(),
            'femeninas': Counter()
        }

        contenido_lower = contenido.lower()

        # Profesiones masculinas
        for profesion in self.profesiones_masculinas:
            count = len(re.findall(r'\b' + re.escape(profesion) + r'\b',
                                  contenido_lower))
            if count > 0:
                profesiones['masculinas'][profesion] = count

        # Profesiones femeninas
        for profesion in self.profesiones_femeninas:
            count = len(re.findall(r'\b' + re.escape(profesion) + r'\b',
                                  contenido_lower))
            if count > 0:
                profesiones['femeninas'][profesion] = count

        return profesiones

    def detectar_diversidad_cultural(self, contenido):
        """
        Detecta menciones de diversidad étnica/cultural

        Returns:
            Counter: Conteo de términos de diversidad
        """
        diversidad = Counter()
        contenido_lower = contenido.lower()

        for termino in self.terminos_diversidad:
            count = len(re.findall(r'\b' + re.escape(termino) + r'\b',
                                  contenido_lower))
            if count > 0:
                diversidad[termino] = count

        return diversidad

    # =====================================================================
    # ANÁLISIS ESTADÍSTICO
    # =====================================================================

    def calcular_ratio_genero(self, masculino, femenino):
        """
        Calcula el ratio de sesgo de género

        Returns:
            float: Ratio masculino/femenino (ej: 17.8 significa 17.8:1)
        """
        if femenino == 0:
            return float('inf') if masculino > 0 else 0.0
        return round(masculino / femenino, 2)

    def analizar_archivo(self, filepath):
        """
        Analiza un archivo de texto completo

        Returns:
            dict: Resultados completos del análisis
        """
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                contenido = f.read()

            # Conteo de palabras
            palabras = len(contenido.split())

            # Detecciones
            nombres = self.detectar_nombres_personas(contenido)
            tratamientos = self.detectar_tratamientos_formales(contenido)
            profesiones = self.detectar_profesiones_musicales(contenido)
            diversidad = self.detectar_diversidad_cultural(contenido)

            # Totales
            total_masculino = (
                sum(nombres['masculinos'].values()) +
                tratamientos['masculinos'] +
                sum(profesiones['masculinas'].values())
            )

            total_femenino = (
                sum(nombres['femeninos'].values()) +
                tratamientos['femeninos'] +
                sum(profesiones['femeninas'].values())
            )

            # Resultados
            resultado = {
                'archivo': os.path.basename(filepath),
                'ruta': filepath,
                'palabras': palabras,
                'detecciones': {
                    'nombres': {
                        'masculinos': dict(nombres['masculinos']),
                        'femeninos': dict(nombres['femeninos']),
                        'masculinos_completos': nombres['masculinos_completos'],
                        'femeninos_completos': nombres['femeninos_completos'],
                        'total_masculinos': sum(nombres['masculinos'].values()),
                        'total_femeninos': sum(nombres['femeninos'].values())
                    },
                    'tratamientos': tratamientos,
                    'profesiones': {
                        'masculinas': dict(profesiones['masculinas']),
                        'femeninas': dict(profesiones['femeninas']),
                        'total_masculinas': sum(profesiones['masculinas'].values()),
                        'total_femeninas': sum(profesiones['femeninas'].values())
                    },
                    'diversidad': dict(diversidad),
                    'total_diversidad': sum(diversidad.values())
                },
                'totales': {
                    'menciones_masculinas': total_masculino,
                    'menciones_femeninas': total_femenino,
                    'ratio_sesgo': self.calcular_ratio_genero(
                        total_masculino, total_femenino
                    )
                }
            }

            return resultado

        except Exception as e:
            print(f"❌ Error analizando {filepath}: {e}")
            return None

    def analizar_directorio(self, directorio=None):
        """
        Analiza todos los archivos TXT en un directorio

        Args:
            directorio (str): Ruta al directorio (usa base_directory si None)
        """
        if directorio is None:
            directorio = self.base_directory

        print(f"📂 Analizando directorio: {directorio}")

        archivos_txt = []
        for root, dirs, files in os.walk(directorio):
            for file in files:
                if file.endswith('.txt'):
                    archivos_txt.append(os.path.join(root, file))

        print(f"📄 Encontrados {len(archivos_txt)} archivos TXT")

        # Verificar si hay archivos para analizar
        if len(archivos_txt) == 0:
            print("\n⚠️  ADVERTENCIA: No se encontraron archivos .txt en el directorio especificado.")
            print("   Verifica que:")
            print("   1. La ruta del directorio sea correcta")
            print("   2. Los archivos tengan extensión .txt (no .pdf, .docx, etc.)")
            print("   3. Los archivos estén directamente en la carpeta o subcarpetas\n")

        # Analizar cada archivo
        resultados_archivos = []
        total_masc = 0
        total_fem = 0
        total_palabras = 0

        for i, filepath in enumerate(archivos_txt, 1):
            print(f"⚙️  Procesando {i}/{len(archivos_txt)}: {os.path.basename(filepath)}")

            resultado = self.analizar_archivo(filepath)
            if resultado:
                resultados_archivos.append(resultado)
                total_masc += resultado['totales']['menciones_masculinas']
                total_fem += resultado['totales']['menciones_femeninas']
                total_palabras += resultado['palabras']

        # Consolidar resultados
        self.resultados = {
            'metadata': {
                'directorio': directorio,
                'total_archivos': len(resultados_archivos),
                'total_palabras': total_palabras,
                'fecha_analisis': datetime.now().isoformat()
            },
            'resumen_general': {
                'menciones_masculinas_total': total_masc,
                'menciones_femeninas_total': total_fem,
                'ratio_sesgo_general': self.calcular_ratio_genero(total_masc, total_fem),
                'porcentaje_masculino': round(
                    (total_masc / (total_masc + total_fem) * 100)
                    if (total_masc + total_fem) > 0 else 0, 2
                ),
                'porcentaje_femenino': round(
                    (total_fem / (total_masc + total_fem) * 100)
                    if (total_masc + total_fem) > 0 else 0, 2
                )
            },
            'archivos': resultados_archivos
        }

        return self.resultados

    def guardar_resultados(self, output_file='resultados_deteccion_genero.json'):
        """
        Guarda los resultados en JSON

        Args:
            output_file (str): Nombre del archivo de salida
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.resultados, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Resultados guardados en: {output_file}")
        return output_file

    def generar_reporte_texto(self, output_file='reporte_genero.txt'):
        """
        Genera un reporte legible en texto plano

        Args:
            output_file (str): Nombre del archivo de salida
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("ANÁLISIS DE GÉNERO EN PERSONAS MUSICALES\n")
            f.write("Proyecto LexiMus - Universidad de Salamanca\n")
            f.write("="*80 + "\n\n")

            # Metadata
            meta = self.resultados['metadata']
            f.write(f"📂 Directorio: {meta['directorio']}\n")
            f.write(f"📄 Archivos analizados: {meta['total_archivos']}\n")
            f.write(f"📝 Total palabras: {meta['total_palabras']:,}\n")
            f.write(f"📅 Fecha: {meta['fecha_analisis']}\n\n")

            # Resumen general
            f.write("-"*80 + "\n")
            f.write("RESUMEN GENERAL\n")
            f.write("-"*80 + "\n")
            resumen = self.resultados['resumen_general']
            f.write(f"👨 Menciones masculinas: {resumen['menciones_masculinas_total']:,} "
                   f"({resumen['porcentaje_masculino']}%)\n")
            f.write(f"👩 Menciones femeninas: {resumen['menciones_femeninas_total']:,} "
                   f"({resumen['porcentaje_femenino']}%)\n")

            ratio = resumen['ratio_sesgo_general']
            if ratio == float('inf'):
                f.write(f"⚠️  Ratio de sesgo: ∞:1 (solo menciones masculinas)\n")
            else:
                f.write(f"📊 Ratio de sesgo de género: {ratio}:1 (masculino:femenino)\n")

            f.write("\n")
            f.write("INTERPRETACIÓN:\n")
            if ratio > 10:
                f.write(f"❌ Sesgo extremo detectado ({ratio}:1). Dominancia masculina severa.\n")
            elif ratio > 5:
                f.write(f"⚠️  Sesgo alto detectado ({ratio}:1). Desbalance significativo.\n")
            elif ratio > 2:
                f.write(f"⚠️  Sesgo moderado detectado ({ratio}:1).\n")
            else:
                f.write(f"✅ Representación relativamente equilibrada ({ratio}:1).\n")

            f.write("\n")

            # Top 10 archivos con mayor sesgo
            f.write("-"*80 + "\n")
            f.write("TOP 10 ARCHIVOS CON MAYOR SESGO DE GÉNERO\n")
            f.write("-"*80 + "\n")

            archivos_ordenados = sorted(
                [a for a in self.resultados['archivos']
                 if a['totales']['ratio_sesgo'] != float('inf')],
                key=lambda x: x['totales']['ratio_sesgo'],
                reverse=True
            )[:10]

            for i, archivo in enumerate(archivos_ordenados, 1):
                f.write(f"{i}. {archivo['archivo']}\n")
                f.write(f"   Ratio: {archivo['totales']['ratio_sesgo']}:1 | "
                       f"Masc: {archivo['totales']['menciones_masculinas']} | "
                       f"Fem: {archivo['totales']['menciones_femeninas']}\n\n")

        print(f"✅ Reporte guardado en: {output_file}")
        return output_file

    def generar_web_interactiva(self, output_file='analisis_genero.html'):
        """
        Genera una página web interactiva con visualizaciones

        Args:
            output_file (str): Nombre del archivo HTML de salida
        """
        if not self.resultados:
            print("❌ Error: No hay resultados para generar web. Ejecuta analizar_directorio() primero.")
            return None

        meta = self.resultados['metadata']
        resumen = self.resultados['resumen_general']
        ratio = resumen['ratio_sesgo_general']

        # Preparar datos para gráficos
        archivos_data = []
        for archivo in self.resultados['archivos'][:20]:  # Top 20 archivos
            if archivo['totales']['ratio_sesgo'] != float('inf'):
                archivos_data.append({
                    'nombre': archivo['archivo'][:30],  # Truncar nombre
                    'masculinas': archivo['totales']['menciones_masculinas'],
                    'femeninas': archivo['totales']['menciones_femeninas'],
                    'ratio': archivo['totales']['ratio_sesgo']
                })

        # Top nombres completos detectados
        todos_nombres_completos_masc = Counter()
        todos_nombres_completos_fem = Counter()
        for archivo in self.resultados['archivos']:
            # Contar nombres completos (prioritario)
            for nombre_completo in archivo['detecciones']['nombres']['masculinos_completos']:
                todos_nombres_completos_masc[nombre_completo] += 1
            for nombre_completo in archivo['detecciones']['nombres']['femeninos_completos']:
                todos_nombres_completos_fem[nombre_completo] += 1

        top_nombres_masc = todos_nombres_completos_masc.most_common(10)
        top_nombres_fem = todos_nombres_completos_fem.most_common(10)

        # Generar HTML
        html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análisis de Género en Personas Musicales</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}

        header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
        }}

        .stat-card {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}

        .stat-card .icon {{
            font-size: 3em;
            margin-bottom: 15px;
        }}

        .stat-card .value {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }}

        .stat-card.masculino .value {{
            color: #3498db;
        }}

        .stat-card.femenino .value {{
            color: #e91e63;
        }}

        .stat-card.ratio .value {{
            color: #f39c12;
        }}

        .stat-card.archivos .value {{
            color: #9b59b6;
        }}

        .stat-card .label {{
            font-size: 1.1em;
            color: #666;
        }}

        .interpretation {{
            padding: 30px 40px;
            background: #fff3cd;
            border-left: 5px solid #f39c12;
            margin: 0 40px;
            border-radius: 10px;
        }}

        .interpretation.extreme {{
            background: #f8d7da;
            border-left-color: #dc3545;
        }}

        .interpretation.high {{
            background: #fff3cd;
            border-left-color: #ffc107;
        }}

        .interpretation.moderate {{
            background: #d1ecf1;
            border-left-color: #17a2b8;
        }}

        .interpretation.balanced {{
            background: #d4edda;
            border-left-color: #28a745;
        }}

        .interpretation h3 {{
            margin-bottom: 10px;
            font-size: 1.4em;
        }}

        .charts-section {{
            padding: 40px;
        }}

        .chart-container {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}

        .chart-container h2 {{
            margin-bottom: 20px;
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}

        canvas {{
            max-height: 400px;
        }}

        .metadata {{
            padding: 40px;
            background: #f8f9fa;
            border-top: 1px solid #dee2e6;
        }}

        .metadata-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}

        .metadata-item {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .metadata-item .icon {{
            font-size: 1.5em;
        }}

        .metadata-item .info {{
            flex: 1;
        }}

        .metadata-item .label {{
            font-size: 0.9em;
            color: #666;
        }}

        .metadata-item .value {{
            font-weight: bold;
            color: #333;
        }}

        footer {{
            text-align: center;
            padding: 30px;
            background: #2c3e50;
            color: white;
        }}

        footer a {{
            color: #3498db;
            text-decoration: none;
        }}

        footer a:hover {{
            text-decoration: underline;
        }}

        .top-names {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }}

        .names-list {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
        }}

        .names-list h3 {{
            margin-bottom: 15px;
            color: #667eea;
        }}

        .names-list.masculino h3 {{
            color: #3498db;
        }}

        .names-list.femenino h3 {{
            color: #e91e63;
        }}

        .name-item {{
            display: flex;
            justify-content: space-between;
            padding: 10px;
            background: white;
            margin-bottom: 8px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}

        .name-item .name {{
            font-weight: bold;
        }}

        .name-item .count {{
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎵 Análisis de Género en Personas Musicales</h1>
            <p>Proyecto LexiMus - Universidad de Salamanca</p>
        </header>

        <div class="stats-grid">
            <div class="stat-card masculino">
                <div class="icon">👨</div>
                <div class="value">{resumen['menciones_masculinas_total']:,}</div>
                <div class="label">Menciones Masculinas<br>({resumen['porcentaje_masculino']}%)</div>
            </div>

            <div class="stat-card femenino">
                <div class="icon">👩</div>
                <div class="value">{resumen['menciones_femeninas_total']:,}</div>
                <div class="label">Menciones Femeninas<br>({resumen['porcentaje_femenino']}%)</div>
            </div>

            <div class="stat-card ratio">
                <div class="icon">📊</div>
                <div class="value">{"∞" if ratio == float('inf') else f"{ratio}"} : 1</div>
                <div class="label">Ratio de Sesgo<br>(Masculino:Femenino)</div>
            </div>

            <div class="stat-card archivos">
                <div class="icon">📄</div>
                <div class="value">{meta['total_archivos']}</div>
                <div class="label">Archivos Analizados</div>
            </div>
        </div>

        <div class="interpretation {'extreme' if ratio > 10 else 'high' if ratio > 5 else 'moderate' if ratio > 2 else 'balanced'}">
            <h3>📈 Interpretación del Sesgo de Género</h3>
            <p>
                {'❌ <strong>Sesgo extremo detectado.</strong> La dominancia masculina es severa (' + str(ratio) + ':1), indicando una representación casi exclusiva de hombres en el corpus analizado.' if ratio > 10 else
                 '⚠️ <strong>Sesgo alto detectado.</strong> Existe un desbalance significativo (' + str(ratio) + ':1) hacia menciones masculinas.' if ratio > 5 else
                 '⚠️ <strong>Sesgo moderado.</strong> Las menciones masculinas superan notablemente a las femeninas (' + str(ratio) + ':1).' if ratio > 2 else
                 '✅ <strong>Representación relativamente equilibrada.</strong> El ratio (' + str(ratio) + ':1) sugiere una distribución más equitativa.'}
            </p>
            <p style="margin-top: 10px; font-size: 0.95em; color: #666;">
                <strong>Contexto:</strong> En el proyecto LexiMus, el análisis de 25.8 millones de palabras en prensa musical española (1842-2024) reveló un ratio de 17.8:1, evidenciando dominancia masculina histórica en el periodismo musical.
            </p>
        </div>

        <div class="charts-section">
            <div class="chart-container">
                <h2>📊 Distribución General por Género</h2>
                <canvas id="pieChart"></canvas>
            </div>

            <div class="chart-container">
                <h2>📈 Comparativa por Archivo (Top 20)</h2>
                <canvas id="barChart"></canvas>
            </div>

            <div class="chart-container">
                <h2>👥 Personas Más Mencionadas (Nombres Completos)</h2>
                <div class="top-names">
                    <div class="names-list masculino">
                        <h3>👨 Top 10 Masculinos</h3>
                        {''.join([f'<div class="name-item"><span class="name">{nombre}</span><span class="count">{count} menciones</span></div>' for nombre, count in top_nombres_masc])}
                    </div>
                    <div class="names-list femenino">
                        <h3>👩 Top 10 Femeninos</h3>
                        {''.join([f'<div class="name-item"><span class="name">{nombre}</span><span class="count">{count} menciones</span></div>' for nombre, count in top_nombres_fem])}
                    </div>
                </div>
            </div>
        </div>

        <div class="metadata">
            <h2 style="margin-bottom: 20px; color: #667eea;">ℹ️ Información del Análisis</h2>
            <div class="metadata-grid">
                <div class="metadata-item">
                    <span class="icon">📂</span>
                    <div class="info">
                        <div class="label">Directorio analizado</div>
                        <div class="value">{meta['directorio']}</div>
                    </div>
                </div>
                <div class="metadata-item">
                    <span class="icon">📝</span>
                    <div class="info">
                        <div class="label">Total de palabras</div>
                        <div class="value">{meta['total_palabras']:,}</div>
                    </div>
                </div>
                <div class="metadata-item">
                    <span class="icon">📅</span>
                    <div class="info">
                        <div class="label">Fecha de análisis</div>
                        <div class="value">{meta['fecha_analisis']}</div>
                    </div>
                </div>
                <div class="metadata-item">
                    <span class="icon">🔬</span>
                    <div class="info">
                        <div class="label">Metodología</div>
                        <div class="value">Detección lingüística automática</div>
                    </div>
                </div>
            </div>
        </div>

        <footer>
            <p><strong>Proyecto LexiMus</strong> - Universidad de Salamanca, Instituto Complutense de Ciencias Musicales, Universidad de La Rioja</p>
            <p>Financiación: PID2022-139589NB-C33</p>
            <p style="margin-top: 10px;">
                <a href="https://github.com/LeximusUSAL/detector-genero-musical" target="_blank">🔗 GitHub Repository</a> |
                <a href="resultados_deteccion_genero.json" target="_blank">📊 Datos JSON</a>
            </p>
            <p style="margin-top: 15px; font-size: 0.9em; opacity: 0.8;">
                🤖 Generado con Detector Automático de Género Musical v1.0
            </p>
        </footer>
    </div>

    <script>
        // Gráfico de pastel
        const ctxPie = document.getElementById('pieChart').getContext('2d');
        new Chart(ctxPie, {{
            type: 'doughnut',
            data: {{
                labels: ['Masculino', 'Femenino'],
                datasets: [{{
                    data: [{resumen['menciones_masculinas_total']}, {resumen['menciones_femeninas_total']}],
                    backgroundColor: ['#3498db', '#e91e63'],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            font: {{
                                size: 14
                            }},
                            padding: 20
                        }}
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                const total = {resumen['menciones_masculinas_total'] + resumen['menciones_femeninas_total']};
                                const percentage = ((value / total) * 100).toFixed(1);
                                return label + ': ' + value.toLocaleString() + ' (' + percentage + '%)';
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Gráfico de barras
        const ctxBar = document.getElementById('barChart').getContext('2d');
        new Chart(ctxBar, {{
            type: 'bar',
            data: {{
                labels: {json.dumps([a['nombre'] for a in archivos_data])},
                datasets: [
                    {{
                        label: 'Masculinas',
                        data: {json.dumps([a['masculinas'] for a in archivos_data])},
                        backgroundColor: '#3498db',
                        borderRadius: 5
                    }},
                    {{
                        label: 'Femeninas',
                        data: {json.dumps([a['femeninas'] for a in archivos_data])},
                        backgroundColor: '#e91e63',
                        borderRadius: 5
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                scales: {{
                    x: {{
                        stacked: false,
                        ticks: {{
                            font: {{
                                size: 10
                            }},
                            maxRotation: 90,
                            minRotation: 45
                        }}
                    }},
                    y: {{
                        stacked: false,
                        beginAtZero: true
                    }}
                }},
                plugins: {{
                    legend: {{
                        position: 'top',
                        labels: {{
                            font: {{
                                size: 14
                            }}
                        }}
                    }},
                    tooltip: {{
                        callbacks: {{
                            afterLabel: function(context) {{
                                const index = context.dataIndex;
                                const ratios = {json.dumps([a['ratio'] for a in archivos_data])};
                                return 'Ratio: ' + ratios[index] + ':1';
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""

        # Guardar HTML
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ Web interactiva generada: {output_file}")
        return output_file


# ==========================================================================
# FUNCIÓN PRINCIPAL
# ==========================================================================

def main():
    """
    Ejecuta el análisis completo

    Uso:
        python3 detector_genero_musical.py /ruta/a/tus/archivos

    Si no se especifica ruta, pedirá ingresarla manualmente.
    """
    import sys

    # Verificar si se pasó directorio como argumento
    if len(sys.argv) > 1:
        directorio_base = sys.argv[1]
    else:
        print("🎵 DETECTOR AUTOMÁTICO DE GÉNERO EN PERSONAS MUSICALES")
        print("="*80)
        print("\n⚠️  No se especificó directorio.\n")
        print("Opciones:")
        print("  1. Ejecutar con argumento: python3 detector_genero_musical.py /ruta/a/archivos")
        print("  2. Ingresar ruta manualmente ahora\n")

        directorio_base = input("📂 Ingresa la ruta completa a tu directorio de archivos TXT: ").strip()

        # Eliminar comillas si el usuario las pegó
        directorio_base = directorio_base.strip('"').strip("'")

    # Validar que el directorio existe
    if not os.path.exists(directorio_base):
        print(f"\n❌ ERROR: El directorio '{directorio_base}' no existe.")
        print("   Verifica la ruta e intenta nuevamente.\n")
        return

    if not os.path.isdir(directorio_base):
        print(f"\n❌ ERROR: '{directorio_base}' no es un directorio.\n")
        return

    print("\n🎵 DETECTOR AUTOMÁTICO DE GÉNERO EN PERSONAS MUSICALES")
    print("="*80)
    print(f"📂 Directorio: {directorio_base}\n")

    # Inicializar detector
    detector = DetectorGeneroMusical(directorio_base)

    # Ejecutar análisis
    resultados = detector.analizar_directorio()

    # Guardar resultados
    detector.guardar_resultados('resultados_deteccion_genero.json')
    detector.generar_reporte_texto('reporte_genero.txt')
    detector.generar_web_interactiva('analisis_genero.html')

    # Imprimir resumen
    print("\n" + "="*80)
    print("✅ ANÁLISIS COMPLETADO")
    print("="*80)
    resumen = resultados['resumen_general']
    print(f"👨 Menciones masculinas: {resumen['menciones_masculinas_total']:,}")
    print(f"👩 Menciones femeninas: {resumen['menciones_femeninas_total']:,}")
    print(f"📊 Ratio de sesgo: {resumen['ratio_sesgo_general']}:1")
    print(f"\n📁 Archivos generados:")
    print(f"   - resultados_deteccion_genero.json (datos completos)")
    print(f"   - reporte_genero.txt (resumen legible)")
    print(f"   - analisis_genero.html (web interactiva)")
    print(f"\n🌐 Abre 'analisis_genero.html' en tu navegador para ver los resultados interactivos")


if __name__ == "__main__":
    main()
