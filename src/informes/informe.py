import os
from datetime import datetime
import json

OUTPUT_DIR = os.path.join(os.getcwd(), "outputs", "reports")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def _resultado_a_texto(resultados):
    """ Convierte los resultados del análisis a un formato de texto. """
    lines = []
    lines.append("# Informe de análisis\n")
    lines.append("## Estadísticas guardadas\n")
    for col, stats in resultados.get('estadisticas', {}).items():
        lines.append(f"### Columna: {col}")
        for k, v in stats.items():
            lines.append(f"- {k}: {v}")
    lines.append("\n## Gráficos generados")
    for g in resultados.get('graficos', []):
        lines.append(f"- {g}")
    lines.append("\n## Probabilidades")
    for k, v in resultados.get('probabilidades', {}).items():
        lines.append(f"- {k}: {v}")
    return "\n".join(lines)

def guardar_informe(resultados, df, filename=None):
    """ Guarda el informe en un archivo Markdown y los resultados crudos en JSON. """
    if filename is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(OUTPUT_DIR, f"report_{ts}.md")
    contenido = _resultado_a_texto(resultados)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(contenido)
    # además guardamos un JSON con resultados crudos si hace falta
    json_path = filename.replace(".md", ".json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2)
    print(f"Informe guardado en: {filename}")
    print(f"Resultados crudos guardados en: {json_path}")
    return filename