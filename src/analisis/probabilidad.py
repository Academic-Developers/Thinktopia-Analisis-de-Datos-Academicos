# import operator
# from .analisis_datos import seleccionar_columna

# _ops = {
#     ">": operator.gt,
#     "<": operator.lt,
#     ">=": operator.ge,
#     "<=": operator.le,
#     "==": operator.eq,
#     "!=": operator.ne,
# }

# def _leer_condicion(df, label):
#     col = seleccionar_columna(df, label)
#     if not col:
#         return None
#     print("Operadores válidos: >", "<", ">=", "<=","==", "!=")
#     op = input("Operador: ").strip()
#     val = input("Valor (número o texto): ").strip()
#     # intentar convertir a float si posible
#     try:
#         if "." in val or val.isdigit():
#             val_conv = float(val) if "." in val else int(val)
#         else:
#             val_conv = val
#     except:
#         val_conv = val
#     if op not in _ops:
#         print("Operador inválido.")
#         return None
#     return (col, _ops[op], val_conv)

# def _aplica_cond(df, cond):
#     col, op_func, val = cond
#     try:
#         return op_func(df[col], val)
#     except Exception as e:
#         # intentar conversión segura
#         try:
#             return op_func(df[col].astype(float), float(val))
#         except Exception:
#             return op_func(df[col].astype(str), str(val))

# def _prob_condicional(df, cond_A, cond_B):
#     mask_B = _aplica_cond(df, cond_B)
#     n_B = mask_B.sum()
#     if n_B == 0:
#         return None, 0, 0
#     mask_AandB = mask_B & _aplica_cond(df, cond_A)
#     p = mask_AandB.sum() / n_B
#     return p, int(mask_AandB.sum()), int(n_B)

# def menu_probabilidades(df, resultados):
#     while True:
#         print("\n--- Menú de probabilidades ---")
#         print("1) P(buena nota | alta asistencia)")
#         print("2) P(entrega tarea | buena nota)")
#         print("3) Probabilidad personalizada")
#         print("4) Volver")
#         opt = input("Elija opción: ").strip()
#         if opt == "4":
#             break
#         if opt == "1":
#             print("Defina columna de nota y de asistencia.")
#             condA = _leer_condicion(df, "Condición A (ej. nota >= 85)")
#             condB = _leer_condicion(df, "Condición B (ej. asistencia >= 90)")
#             if condA and condB:
#                 p, na, nb = _prob_condicional(df, condA, condB)
#                 if p is None:
#                     print("No hay casos que cumplan la condición B.")
#                 else:
#                     print(f"P(A|B) = {p:.4f} ({na}/{nb})")
#                     resultados['probabilidades']['A|B']= {'p':p, 'AandB':na, 'B':nb}
#         elif opt == "2":
#             print("Defina columna de nota y de entrega (o similar).")
#             condA = _leer_condicion(df, "Condición A (ej. entrega == 'sí')")
#             condB = _leer_condicion(df, "Condición B (ej. nota >= 80)")
#             if condA and condB:
#                 p, na, nb = _prob_condicional(df, condA, condB)
#                 if p is None:
#                     print("No hay casos que cumplan la condición B.")
#                 else:
#                     print(f"P(A|B) = {p:.4f} ({na}/{nb})")
#                     resultados['probabilidades']['A|B_entrega']= {'p':p, 'AandB':na, 'B':nb}
#         elif opt == "3":
#             print("Defina condición A")
#             condA = _leer_condicion(df, "Condición A")
#             print("Defina condición B")
#             condB = _leer_condicion(df, "Condición B")
#             if condA and condB:
#                 p, na, nb = _prob_condicional(df, condA, condB)
#                 if p is None:
#                     print("No hay casos que cumplan la condición B.")
#                 else:
#                     print(f"P(A|B) = {p:.4f} ({na}/{nb})")
#                     resultados['probabilidades']['personalizada']= {'p':p, 'AandB':na, 'B':nb}
#         else:
#             print("Opción inválida.")