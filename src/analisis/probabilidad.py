# src/probabilidad.py
import pandas as pd
import operator
from typing import Dict, Any, Optional
from .analisis_datos import seleccionar_columnas

# Diccionario de operadores lógicos
_ops = {
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
    "==": operator.eq,
    "!=": operator.ne,
}

def _leer_condicion(df: pd.DataFrame, label: str) -> Optional[tuple]:
    """ Lee una condición del usuario (columna, operador, valor). """
    columnas = seleccionar_columnas(df, f"Condición para {label}")
    if not columnas or len(columnas) > 1:
        print("Debe seleccionar una sola columna.")
        return None
        
    col = columnas[0]
    
    print("Operadores válidos: > < >= <= == !=")
    op = input("Ingrese el operador: ").strip()
    val = input("Ingrese el valor (número o texto): ").strip()
    
    if op not in _ops:
        print("Operador inválido.")
        return None
        
    try:
        # Intenta convertir el valor al tipo de la columna
        dtype = df[col].dtype
        if pd.api.types.is_numeric_dtype(dtype):
            val_conv = float(val) if '.' in val else int(val)
        else:
            val_conv = val
    except ValueError:
        print(f"Error: El valor '{val}' no es compatible con el tipo de la columna '{col}' ({dtype}).")
        return None
        
    return (col, _ops[op], val_conv)

def _aplica_cond(df: pd.DataFrame, cond: tuple) -> pd.Series:
    """ Aplica una condición a un DataFrame y retorna una máscara booleana. """
    col, op_func, val = cond
    return op_func(df[col], val)

def calcular_probabilidad_simple(df: pd.DataFrame, cond: tuple) -> tuple:
    """ Calcula la probabilidad simple P(A). """
    mask_A = _aplica_cond(df, cond)
    n_A = mask_A.sum()
    n_total = len(df)
    p_A = n_A / n_total if n_total > 0 else 0
    return p_A, int(n_A), int(n_total)

def calcular_probabilidad_condicional(df: pd.DataFrame, cond_A: tuple, cond_B: tuple) -> Optional[dict]:
    """
    Calcula la probabilidad condicional P(A|B) = P(A and B) / P(B).
    
    Args:
        df: DataFrame de pandas con los datos.
        cond_A: Tupla (columna, operador, valor) para la condición A.
        cond_B: Tupla (columna, operador, valor) para la condición B.

    Returns:
        Un diccionario con la probabilidad, o None si no se puede calcular.
    """
    try:
        mask_B = _aplica_cond(df, cond_B)
        n_B = mask_B.sum()
        if n_B == 0:
            return None
        
        mask_AandB = mask_B & _aplica_cond(df, cond_A)
        n_AandB = mask_AandB.sum()
        
        p = n_AandB / n_B
        
        return {
            'probabilidad': float(p),
            'casos_cumplen_B': int(n_B),
            'casos_cumplen_AyB': int(n_AandB),
            'condicion_A': cond_A,
            'condicion_B': cond_B
        }
    except Exception as e:
        print(f"Error al calcular probabilidad condicional: {e}")
        return None

def crear_tabla_contingencia(df: pd.DataFrame, col1: str, col2: str) -> Optional[pd.DataFrame]:
    """Crea una tabla de contingencia para dos columnas categóricas."""
    if not (pd.api.types.is_categorical_dtype(df[col1]) or pd.api.types.is_object_dtype(df[col1])) or \
       not (pd.api.types.is_categorical_dtype(df[col2]) or pd.api.types.is_object_dtype(df[col2])):
        print("Error: Las columnas deben ser categóricas para crear una tabla de contingencia.")
        return None

    print(f"\n--- Tabla de contingencia para '{col1}' y '{col2}' ---")
    tabla = pd.crosstab(df[col1], df[col2])
    print(tabla)
    return tabla

def menu_probabilidades(df: pd.DataFrame, resultados: Dict[str, Any]):
    """ Muestra el menú de probabilidades y gestiona la selección del usuario. """
    while True:
        print("\n--- Menú de Probabilidades ---")
        print("1) Calcular probabilidad simple P(A)")
        print("2) Calcular probabilidad condicional P(A|B)")
        print("3) Crear tabla de contingencia")
        print("4) Volver al menú principal")
        
        opt = input("Elija una opción: ").strip()
        
        if opt == "4":
            break
        
        if opt == "1":
            print("\nDefina la condición para el evento A.")
            condA = _leer_condicion(df, "Evento A")
            if condA:
                p, n_A, n_total = calcular_probabilidad_simple(df, condA)
                print(f"P(A) = {p:.4f} ({n_A}/{n_total})")
                resultados['probabilidades']['simple'] = {'p': p, 'n_A': n_A, 'n_total': n_total}

        elif opt == "2":
            print("\nDefina la condición para el evento A (el que deseas predecir).")
            condA = _leer_condicion(df, "Evento A")
            print("\nDefina la condición para el evento B (la condición que ya conoces).")
            condB = _leer_condicion(df, "Evento B")
            if condA and condB:
                res = calcular_probabilidad_condicional(df, condA, condB)
                if res:
                    p = res['probabilidad']
                    n_AandB = res['casos_cumplen_AyB']
                    n_B = res['casos_cumplen_B']
                    print(f"P(A|B) = {p:.4f} ({n_AandB}/{n_B})")
                    resultados['probabilidades']['condicional'] = res
                else:
                    print("No hay casos que cumplan la condición B. La probabilidad no puede ser calculada.")
        
        elif opt == "3":
            columnas = seleccionar_columnas(df, "tabla de contingencia (dos columnas categóricas)")
            if columnas and len(columnas) == 2:
                crear_tabla_contingencia(df, columnas[0], columnas[1])
            else:
                print("Por favor, seleccione exactamente dos columnas categóricas.")

        else:
            print("Opción inválida.")
        
        input("\nPresione Enter para continuar...")