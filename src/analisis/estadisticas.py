import pandas as pd

def calcular_media(series: pd.Series):
    return series.mean()

def calcular_mediana(series: pd.Series):
    return series.median()

def calcular_moda(series: pd.Series):
    mod = series.mode()
    return mod.tolist()

def calcular_medidas_basicas(df, columna):
    s = df[columna].dropna()
    return {
        'count': int(s.count()),
        'mean': float(s.mean()) if not s.empty else None,
        'median': float(s.median()) if not s.empty else None,
        'mode': calcular_moda(s),
        'std': float(s.std()) if not s.empty else None,
        'min': float(s.min()) if not s.empty else None,
        '25%': float(s.quantile(0.25)) if not s.empty else None,
        '75%': float(s.quantile(0.75)) if not s.empty else None,
        'max': float(s.max()) if not s.empty else None,
    }

def mostrar_estadisticas_generales(df, columna):
    medidas = calcular_medidas_basicas(df, columna)
    print(f"\n--- Estadísticas para '{columna}' ---")
    for k, v in medidas.items():
        print(f"{k:6}: {v}")
    return medidas