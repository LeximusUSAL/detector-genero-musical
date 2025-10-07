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
        # LISTAS DE NOMBRES ESPAÑOLES (Expandibles)
        # =================================================================

        # Nombres masculinos históricos y actuales comunes en España
        self.nombres_masculinos = {
            # Clásicos históricos (s. XIX-XX)
            'manuel', 'antonio', 'josé', 'francisco', 'juan', 'pedro', 'luis',
            'carlos', 'miguel', 'rafael', 'fernando', 'jesús', 'ángel', 'diego',
            'pablo', 'andrés', 'ramón', 'tomás', 'enrique', 'alberto', 'joaquín',
            'ricardo', 'felipe', 'ignacio', 'jaime', 'sergio', 'alejandro',

            # Compositores/músicos históricos españoles
            'isaac', 'tomás', 'joaquín', 'manuel', 'ruperto', 'federico',
            'emilio', 'pablo', 'andrés', 'adolfo', 'jesús', 'conrado',

            # Nombres modernos
            'david', 'daniel', 'jorge', 'adrián', 'iván', 'rubén', 'mario',
            'oscar', 'héctor', 'raúl', 'víctor', 'hugo', 'marcos', 'álvaro'
        }

        # Nombres femeninos históricos y actuales
        self.nombres_femeninos = {
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
            'lucía', 'sofía', 'alba', 'claudia', 'sandra', 'mónica'
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
        Detecta nombres propios en el texto usando contexto

        Returns:
            dict: {'masculinos': Counter, 'femeninos': Counter}
        """
        nombres_detectados = {
            'masculinos': Counter(),
            'femeninos': Counter()
        }

        # Normalizar contenido
        contenido_lower = contenido.lower()

        # Buscar nombres masculinos con contexto
        for nombre in self.nombres_masculinos:
            # Patrón: nombre con mayúscula seguido de apellido o contexto
            patron = r'\b' + nombre.capitalize() + r'\b(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)?'
            matches = re.finditer(patron, contenido, re.IGNORECASE)
            count = len(list(matches))
            if count > 0:
                nombres_detectados['masculinos'][nombre] = count

        # Buscar nombres femeninos con contexto
        for nombre in self.nombres_femeninos:
            patron = r'\b' + nombre.capitalize() + r'\b(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)?'
            matches = re.finditer(patron, contenido, re.IGNORECASE)
            count = len(list(matches))
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


# ==========================================================================
# FUNCIÓN PRINCIPAL
# ==========================================================================

def main():
    """
    Ejecuta el análisis completo

    MODIFICAR ESTA RUTA según tu estructura de directorios:
    """
    # RUTA DE EJEMPLO - MODIFICAR SEGÚN TU CASO
    directorio_base = "/Users/maria/Desktop/REVISTAS TXT PARA WEBS ESTADÍSTICAS"

    # También puedes analizar un subdirectorio específico:
    # directorio_base = "/Users/maria/Desktop/REVISTAS TXT PARA WEBS ESTADÍSTICAS/TXT-ElSol"

    print("🎵 DETECTOR AUTOMÁTICO DE GÉNERO EN PERSONAS MUSICALES")
    print("="*80)
    print(f"📂 Directorio: {directorio_base}\n")

    # Inicializar detector
    detector = DetectorGeneroMusical(directorio_base)

    # Ejecutar análisis
    resultados = detector.analizar_directorio()

    # Guardar resultados
    detector.guardar_resultados('resultados_deteccion_genero.json')
    detector.generar_reporte_texto('reporte_genero.txt')

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


if __name__ == "__main__":
    main()
