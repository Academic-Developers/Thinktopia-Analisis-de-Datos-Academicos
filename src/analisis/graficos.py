# import os
# import matplotlib.pyplot as plt
# from datetime import datetime
# from .analisis_datos import seleccionar_columna, mostrar_columnas

# OUTPUT_DIR = os.path.join(os.getcwd(), "outputs", "figures")
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# def _save_and_show(fig, nombre_base):
#     ts = datetime.now().strftime("%Y%m%d_%H%M%S")
#     fname = f"{nombre_base}_{ts}.png"
#     path = os.path.join(OUTPUT_DIR, fname)
#     fig.savefig(path, bbox_inches='tight')
#     print(f"Gráfico guardado en: {path}")
#     plt.show()
#     plt.close(fig)
#     return path

# def menu_graficos(df, resultados):
#     while True:
#         print("\n--- Menú de gráficos ---")
#         print("1) Barras  2) Histograma  3) Torta  4) Boxplot  5) Scatter  6) Volver")
#         try:
#             opt = int(input("Elija tipo de gráfico: "))
#         except ValueError:
#             print("Debe ingresar un número.")
#             continue
#         if opt == 6:
#             break
#         if opt in (1,2,3,4):
#             col = seleccionar_columna(df, 'graficar')
#             if not col:
#                 continue
#             fig = plt.figure()
#             if opt == 1:
#                 df[col].value_counts().plot(kind='bar')
#                 plt.title(f"Barras - {col}")
#             elif opt == 2:
#                 df[col].plot(kind='hist')
#                 plt.title(f"Histograma - {col}")
#             elif opt == 3:
#                 vc = df[col].value_counts()
#                 vc.plot(kind='pie', autopct='%1.1f%%')
#                 plt.ylabel('')
#                 plt.title(f"Torta - {col}")
#             elif opt == 4:
#                 df.boxplot(column=col)
#                 plt.title(f"Boxplot - {col}")
#             path = _save_and_show(plt.gcf(), f"{col}_grafico_tipo{opt}")
#             resultados['graficos'].append(path)
#         elif opt == 5:
#             print("Scatter requiere 2 columnas:")
#             x = seleccionar_columna(df, 'eje X')
#             y = seleccionar_columna(df, 'eje Y')
#             if not x or not y:
#                 continue
#             fig = plt.figure()
#             df.plot.scatter(x=x, y=y)
#             plt.title(f"Scatter - {y} vs {x}")
#             path = _save_and_show(plt.gcf(), f"scatter_{x}_vs_{y}")
#             resultados['graficos'].append(path)
#         else:
#             print("Opción inválida.")