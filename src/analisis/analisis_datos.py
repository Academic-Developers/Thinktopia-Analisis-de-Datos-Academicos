import os
import pandas as pd
from typing import Optional, Dict, Any,List

def _default_path(filename: str = "student_performance.csv") -> str:
    """Devuelve la ruta absoluta del archivo de datos."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_dir, "data", filename)

def cargar_datos() -> Optional[pd.DataFrame]:
    """Carga el archivo CSV de datos de estudiantes y devuelve un DataFrame de pandas.
    Retorna None si ocurre un error."""
    path = os.path.abspath(_default_path(filename="student_performance.csv"))
    try:
        df = pd.read_csv(path)
        print(f"\nCargado: {len(df)} filas x {len(df.columns)} columnas desde:\n  {path}")
        return df
    except Exception as err:
        print("Error al cargar CSV:", err)
        return None

def limpiar_datos(df: Optional[pd.DataFrame]) -> Optional[pd.DataFrame]:
    """Devuelve un DataFrame limpio: elimina duplicados y muestra cuántos nulos hay."""
    if df is None or df.empty:
        return None
    df_limpio = df.drop_duplicates()
    print(f"Filas eliminadas por duplicados: {len(df) - len(df_limpio)}")
    print("Valores nulos por columna después de limpiar:")
    print(df_limpio.isnull().sum())
    return df_limpio

def obtener_resumen_inicial(df: Optional[pd.DataFrame], n: int = 6) -> Optional[Dict[str, Any]]:
    """Devuelve un resumen inicial del DataFrame."""
    if df is None or df.empty:
        return None
    return {
        "shape": df.shape,
        "head": df.head(n),
        "nulls": df.isnull().sum(),
        "describe": df.describe().transpose(),
        "dtypes": df.dtypes,
        "df": df  # Agregamos el DataFrame completo para usarlo en otras funciones
    }

def obtener_valores_unicos(df: Optional[pd.DataFrame]) -> Optional[Dict[str, Any]]:
    """Devuelve un diccionario con los valores únicos de cada columna categórica."""
    if df is None or df.empty:
        return None
    return {col: df[col].unique() for col in df.select_dtypes(include=['object', 'category']).columns}

def imprimir_resumen(resumen: Optional[Dict[str, Any]]) -> None:
    """Imprime el resumen inicial del DataFrame."""
    if resumen is None:
        print("No hay datos para mostrar el resumen.")
        return
    
    print("\n--- Resumen inicial de las Primeras 6 Filas ---")
    print(f"Cant de Filas: {resumen['shape'][0]}, Cant de Columnas: {resumen['shape'][1]}")
    print("\nPrimeras filas:")
    print(resumen['head'].to_string(index=False))
    print("\nValores nulos por columna:")
    print(resumen['nulls'])
    print("\nDescripción estadistica (numérica):")
    print(resumen['describe'])
    print("\nTipos de datos por columna:")
    print(resumen['dtypes'])

    # Aquí llamamos a obtener_valores_unicos() y lo imprimimos
    df_completo = resumen.get('df')
    valores_unicos = obtener_valores_unicos(df_completo)
    if valores_unicos:
        print("\n--- Valores Únicos por Columna Categórica ---")
        for col, valores in valores_unicos.items():
            print(f"- {col}: {valores}")

def obtener_columnas_info(df: Optional[pd.DataFrame]) -> Optional[pd.DataFrame]:
    """Devuelve un DataFrame con información de columnas: tipo y valores únicos."""
    if df is None or df.empty:
        return None
    return pd.DataFrame({
        'dtype': df.dtypes,
        'valores_unicos': df.nunique()
    })

def imprimir_columnas_info(info: Optional[pd.DataFrame]) -> None:
    """Imprime la información de columnas generada por obtener_columnas_info."""
    if info is None:
        print("No hay datos para mostrar columnas.")
        return
    print("\nColumnas disponibles:")
    for i, (col, row) in enumerate(info.iterrows()):
        print(f"  {i+1}. {col} (dtype={row['dtype']}) - {row['valores_unicos']} valores únicos")

def seleccionar_columnas(df: Optional[pd.DataFrame], purpose: str = 'general') -> Optional[str]:
    """Permite al usuario seleccionar una columna del DataFrame por nombre o índice."""
    info = obtener_columnas_info(df)
    imprimir_columnas_info(info)
    if df is None or df.empty:
        return None
    entrada = input(f"Ingrese los números o nombres de las columnas separadas con coma para {purpose}: ").strip()
    columnas = [col.strip() for col in entrada.split(",")]
    if all(col.isdigit() for col in columnas):
        indices = [int(col) - 1 for col in columnas]
        if all(0 <= idx < len(df.columns) for idx in indices):
            return df.columns[indices].tolist()
        else:
            print("Índice fuera de rango.")
            return None
    else:
        if entrada in df.columns:
            return entrada
        else:
            print("Nombre de columna no encontrado.")
            return None

def seleccionar_columnas(df: Optional[pd.DataFrame], purpose: str = 'general') -> Optional[List[str]]:
    """
    Permite al usuario seleccionar una o varias columnas del DataFrame.
    
    Args:
        df: DataFrame de pandas a procesar.
        purpose: Cadena que describe el propósito de la selección.
    
    Returns:
        Una lista de nombres de columnas seleccionadas o None si la selección es inválida.
    """
    if df is None or df.empty:
        print("No hay datos para seleccionar columnas.")
        return None

    imprimir_columnas_info(obtener_columnas_info(df))
    
    entrada = input(f"Ingrese los números o nombres de las columnas para {purpose} (separados por coma): ").strip()
    
    if not entrada:
        print("Selección cancelada.")
        return None
        
    nombres_seleccionados = []
    
    # Procesa cada entrada separada por coma
    for item in [col.strip() for col in entrada.split(',')]:
        if item.isdigit():
            idx = int(item) - 1
            if 0 <= idx < len(df.columns):
                nombres_seleccionados.append(df.columns[idx])
            else:
                print(f"Advertencia: El índice '{item}' está fuera de rango y será ignorado.")
        elif item in df.columns:
            nombres_seleccionados.append(item)
        else:
            print(f"Advertencia: El nombre de columna '{item}' no se encontró y será ignorado.")

    if not nombres_seleccionados:
        print("No se seleccionó ninguna columna válida.")
        return None
    
    return list(set(nombres_seleccionados)) # Retorna una lista sin duplicados


def sugerencias_mejora(df: Optional[pd.DataFrame]) -> None:
    """Proporciona sugerencias de mejora basadas en el análisis de los datos."""
    print("\n--- Sugerencias de mejora (generales) ---")
    print("- Implementar alertas para estudiantes con asistencia baja.")
    print("- Revisar correlación entre entrega de tareas y puntajes.")
    print("- Tutores focalizados para asignaturas con baja media.")
    print("- Habilitar seguimiento por estudiante para detectar tendencia a la baja.")