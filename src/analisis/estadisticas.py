# src/estadisticas.py
import pandas as pd
from typing import Optional, Dict, Any, List

def calcular_medidas_basicas(series: pd.Series) -> Dict[str, Any]:
    """Calcula las principales medidas de una serie de pandas."""
    if series.empty:
        return {}
    
    return {
        'Conteo': int(series.count()),
        'Media': float(series.mean()),
        'Mediana': float(series.median()),
        'Moda': series.mode().tolist(),
        'Desviacion_Estandar': float(series.std()),
        'Varianza': float(series.var()),
        'Minimo': float(series.min()),
        '25_Percentil': float(series.quantile(0.25)),
        '75_Percentil': float(series.quantile(0.75)),
        'Maximo': float(series.max()),
        'Rango': float(series.max() - series.min())
    }

def mostrar_estadisticas_generales(df: pd.DataFrame, columnas: List[str]) -> Dict[str, Dict[str, Any]]:
    """Muestra y devuelve un diccionario con las estadísticas para las columnas seleccionadas."""
    resultados = {}
    for col in columnas:
        if pd.api.types.is_numeric_dtype(df[col]):
            medidas = calcular_medidas_basicas(df[col].dropna())
            resultados[col] = medidas
            
            print(f"\n--- Estadísticas para la columna: '{col}' ---")
            for k, v in medidas.items():
                if isinstance(v, float):
                    print(f"{k:<20}: {v:.2f}")
                else:
                    print(f"{k:<20}: {v}")
        else:
            print(f"\nAdvertencia: La columna '{col}' no es numérica y se ha omitido.")
            
    return resultados

def calcular_correlaciones(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Calcula y muestra la matriz de correlación entre las variables numéricas del DataFrame.

    Parámetros:
        df (pd.DataFrame): El DataFrame con los datos.

    Retorna:
        Optional[pd.DataFrame]: La matriz de correlación (DataFrame) si hay columnas numéricas, 
        o None si no hay columnas numéricas.
    """
    numeric_df = df.select_dtypes(include=['number'])
    if numeric_df.empty:
        print("No hay columnas numéricas para calcular correlaciones.")
        return None
        
    print("\n--- Matriz de Correlación ---")
    corr_matrix = numeric_df.corr()
    print(corr_matrix)
    return corr_matrix

def agrupar_y_resumir(df: pd.DataFrame, columna_grupo: str, columna_analisis: str) -> Optional[pd.DataFrame]:
    """Agrupa los datos por una columna categórica y resume las estadísticas de otra."""
    if columna_grupo not in df.columns or columna_analisis not in df.columns:
        print("Error: Una o ambas columnas no existen en el DataFrame.")
        return None
    
     # Validación de tipos
    if not pd.api.types.is_categorical_dtype(df[columna_grupo]) and not pd.api.types.is_object_dtype(df[columna_grupo]):
        print(f"Error: La columna '{columna_grupo}' no es categórica.")
        return None
    
    if not pd.api.types.is_numeric_dtype(df[columna_analisis]):
        print(f"Error: La columna '{columna_analisis}' no es numérica.")
        return None

    print(f"\n--- Resumen estadístico agrupado por '{columna_grupo}' ---")
    # Agrupa por la columna categórica y describe la columna numérica
    resumen_grupal = df.groupby(columna_grupo)[columna_analisis].describe()
    print(resumen_grupal)
    return resumen_grupal

