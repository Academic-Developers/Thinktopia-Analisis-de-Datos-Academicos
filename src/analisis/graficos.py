# src/graficos.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
from typing import Optional, List, Dict, Any

# Crear el directorio para guardar los gráficos si no existe
OUTPUT_DIR = os.path.join(os.getcwd(), "outputs", "figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def _save_and_show(fig: plt.Figure, nombre_base: str, resultados: Dict[str, Any]) -> None:
    """ Guarda la figura en OUTPUT_DIR y la muestra en pantalla."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"{nombre_base}_{ts}.png"
    path = os.path.join(OUTPUT_DIR, fname)
    try:
        fig.savefig(path, bbox_inches='tight')
        print(f"Gráfico guardado en: {path}")
        resultados['graficos'].append(path)
    except Exception as e:
        print(f"Error al guardar el gráfico: {e}")
    plt.show()
    plt.close(fig)

def crear_histograma(df: pd.DataFrame, columna: str, resultados: Dict[str, Any]) -> None:
    """Crea un histograma para una columna numérica."""
    if not pd.api.types.is_numeric_dtype(df[columna]):
        print(f"Error: La columna '{columna}' no es numérica y no se puede graficar un histograma.")
        return
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data=df, x=columna, kde=True, ax=ax)
    plt.title(f"Histograma de {columna}", fontsize=16)
    plt.xlabel(columna, fontsize=12)
    plt.ylabel("Frecuencia", fontsize=12)
    _save_and_show(fig, f"hist_{columna}", resultados)

def crear_boxplot(df: pd.DataFrame, columna: str, resultados: Dict[str, Any]) -> None:
    """Crea un boxplot para una columna numérica."""
    if not pd.api.types.is_numeric_dtype(df[columna]):
        print(f"Error: La columna '{columna}' no es numérica y no se puede graficar un boxplot.")
        return

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(data=df, y=columna, ax=ax)
    plt.title(f"Boxplot de {columna}", fontsize=16)
    plt.ylabel(columna, fontsize=12)
    _save_and_show(fig, f"box_{columna}", resultados)

def crear_scatter_plot(df: pd.DataFrame, x_col: str, y_col: str, resultados: Dict[str, Any]) -> None:
    """Crea un diagrama de dispersión para dos columnas numéricas."""
    if not pd.api.types.is_numeric_dtype(df[x_col]) or not pd.api.types.is_numeric_dtype(df[y_col]):
        print("Error: Ambas columnas deben ser numéricas para un diagrama de dispersión.")
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
    plt.title(f"Relación entre {y_col} y {x_col}", fontsize=16)
    plt.xlabel(x_col, fontsize=12)
    plt.ylabel(y_col, fontsize=12)
    _save_and_show(fig, f"scatter_{x_col}_{y_col}", resultados)

def crear_mapa_calor(df: pd.DataFrame, resultados: Dict[str, Any]) -> None:
    """Crea un mapa de calor de la matriz de correlación."""
    numeric_df = df.select_dtypes(include=['number'])
    if numeric_df.empty:
        print("No hay columnas numéricas para el mapa de calor.")
        return
        
    corr_matrix = numeric_df.corr()
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    plt.title("Mapa de Calor de la Matriz de Correlación", fontsize=16)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    _save_and_show(fig, "heatmap_correlacion", resultados)

def menu_graficos(df: pd.DataFrame, resultados: Dict[str, Any]):
    """Muestra el menú de gráficos y gestiona la selección del usuario."""
    while True:
        print("\n--- Menú de Gráficos ---")
        print("1. Histograma (1 variable numérica)")
        print("2. Boxplot (1 variable numérica)")
        print("3. Scatter Plot (2 variables numéricas)")
        print("4. Mapa de Calor (Todas las numéricas)")
        print("5. Volver al menú principal")
        try:
            opt = int(input("Elija el tipo de gráfico: "))
        except ValueError:
            print("Debe ingresar un número.")
            continue
        
        if opt == 5:
            break
        
        from .analisis_datos import seleccionar_columnas
        
        if opt == 1:
            columnas = seleccionar_columnas(df, 'histograma')
            if columnas and len(columnas) == 1:
                crear_histograma(df, columnas[0], resultados)
            else:
                print("Por favor, seleccione solo una columna numérica.")
        
        elif opt == 2:
            columnas = seleccionar_columnas(df, 'boxplot')
            if columnas and len(columnas) == 1:
                crear_boxplot(df, columnas[0], resultados)
            else:
                print("Por favor, seleccione solo una columna numérica.")
        
        elif opt == 3:
            columnas = seleccionar_columnas(df, 'scatter plot')
            if columnas and len(columnas) == 2:
                crear_scatter_plot(df, columnas[0], columnas[1], resultados)
            else:
                print("Por favor, seleccione exactamente dos columnas numéricas.")
        
        elif opt == 4:
            crear_mapa_calor(df, resultados)
        
        else:
            print("Opción inválida.")
        
        input("\nPresione Enter para continuar...")