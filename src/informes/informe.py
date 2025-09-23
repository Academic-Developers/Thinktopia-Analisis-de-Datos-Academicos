import os
from datetime import datetime
import json
import pandas as pd
from typing import Optional, Dict, Any

OUTPUT_DIR = os.path.join(os.getcwd(), "outputs", "reports")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def _resultado_a_texto(resultados: Dict[str, Any], df: Optional[pd.DataFrame]) -> str:
    """ Convierte los resultados del análisis y los metadatos del DataFrame a un formato de texto con secciones. """
    lines = []
    lines.append(f"# Informe de Análisis - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append("## Introducción\n")
    lines.append("Este informe presenta un análisis descriptivo de un conjunto de datos académicos, destacando patrones clave en el rendimiento estudiantil, la correlación entre variables y las probabilidades.\n")

    # Resumen del DataFrame
    if df is not None and not df.empty:
        lines.append("## Resumen del Conjunto de Datos\n")
        lines.append(f"- **Filas**: {df.shape[0]}")
        lines.append(f"- **Columnas**: {df.shape[1]}")
        lines.append("- **Valores nulos por columna**:\n")
        for col, count in df.isnull().sum().items():
            lines.append(f"    - `{col}`: {count}")
    
    # Estadísticas guardadas
    lines.append("\n## Análisis Estadístico\n")
    for col, stats in resultados.get('estadisticas', {}).items():
        lines.append(f"### Estadísticas de la columna: `{col}`\n")
        for k, v in stats.items():
            if isinstance(v, float):
                lines.append(f"- **{k}**: {v:.2f}")
            else:
                lines.append(f"- **{k}**: {v}")
    
    # Gráficos generados
    lines.append("\n## Visualizaciones de Datos\n")
    if resultados.get('graficos'):
        lines.append("Los siguientes gráficos han sido generados y guardados para complementar el análisis. Puede encontrarlos en la carpeta de `outputs/figures`.\n")
        for g in resultados['graficos']:
            lines.append(f"- **{os.path.basename(g)}**")
            # En un informe de Markdown, puedes incrustar la imagen directamente
            lines.append(f"![Gráfico de {os.path.basename(g)}]({g})\n")
    else:
        lines.append("No se generaron gráficos en este análisis.")

    # Probabilidades
    lines.append("\n## Análisis de Probabilidad Condicional\n")
    if resultados.get('probabilidades'):
        for k, v in resultados['probabilidades'].items():
            lines.append(f"- **{k}**: {v}")
    else:
        lines.append("No se realizó un análisis de probabilidad en esta sesión.")
    
    lines.append("\n## Conclusiones y Propuestas\n")
    lines.append("Basado en el análisis, aquí se pueden incluir las conclusiones clave y las propuestas de mejora, como la correlación entre las horas de estudio y el rendimiento, la importancia de la asistencia, etc.")
    lines.append("Puedes editar este informe manualmente para incluir tus propias conclusiones.")
    
    return "\n".join(lines)

def guardar_informe(resultados: Dict[str, Any], df: Optional[pd.DataFrame], filename: Optional[str] = None) -> Optional[str]:
    """ Guarda el informe en un archivo Markdown y los resultados crudos en JSON. """
    if filename is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_base = f"report_{ts}"
    else:
        filename_base = os.path.splitext(filename)[0]
    
    md_path = os.path.join(OUTPUT_DIR, f"{filename_base}.md")
    json_path = os.path.join(OUTPUT_DIR, f"{filename_base}.json")

    try:
        contenido = _resultado_a_texto(resultados, df)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(contenido)
        
        # Guardamos un JSON con resultados crudos para referencia
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(resultados, f, indent=2, default=str)
        
        print(f"Informe completo guardado en: {md_path}")
        print(f"Resultados crudos guardados en: {json_path}")
        return md_path
    except Exception as e:
        print(f"Error al guardar el informe: {e}")
        return None