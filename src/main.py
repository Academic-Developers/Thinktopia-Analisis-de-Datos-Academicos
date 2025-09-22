import analisis.analisis_datos as analisis_datos
import analisis.estadisticas as estadisticas
import analisis.graficos as graficos
import analisis.probabilidad as probabilidad
import informes.informe as informe

def main_menu():
    print("╔" + "═" * 65 + "╗")
    print("║{:^65}║".format("Thinktopia: Análisis de Datos Académicoss"))
    print("╠" + "═" * 65 + "╣")
    print("║{:^65}║".format("Menú de Análisis de Rendimiento Estudiantil"))
    print("╠" + "═" * 65 + "╣")
    print("║ {:<2} {:<60}║".format("1.", "📂 Cargar y mostrar resumen de los datos"))
    print("║ {:<2} {:<60}║".format("2.", "🧹 Limpiar datos (eliminar duplicados)"))
    print("║ {:<2} {:<60}║".format("3.", "🔍 Mostrar valores únicos de columnas categóricas"))
    print("║ {:<2} {:<60}║".format("4.", "📊 Análisis estadístico descriptivo"))
    print("║ {:<2} {:<60}║".format("5.", "📈 Generar gráficos de visualización"))
    print("║ {:<2} {:<60}║".format("6.", "🔢 Analizar probabilidad condicional"))
    print("║ {:<2} {:<60}║".format("7.", "💡 Ver propuesta de estrategias de mejora"))
    print("║ {:<2} {:<60}║".format("8.", "📝 Guardar resultados en un informe"))
    print("║ {:<2} {:<60}║".format("9.", "🚪 Salir de la aplicación"))
    print("╚" + "═" * 65 + "╝")

    try:
        opcion = int(input("Seleccione la opción que desea realizar: "))
        return opcion
    except ValueError:
        return -1

def main():
    df = None
    resultados = {
        'estadisticas': {},
        'graficos': [],
        'probabilidades': {}
    }
    while True:
        try:
            opcion = main_menu()
            if opcion == 1:
                df = analisis_datos.cargar_datos()
                df_global = analisis_datos.limpiar_datos(df)
                if df_global is not None:
                    resumen = analisis_datos.obtener_resumen_inicial(df)
                    analisis_datos.imprimir_resumen(resumen)
                    info = analisis_datos.obtener_columnas_info(df)
                    analisis_datos.imprimir_columnas_info(info)
                else:
                    print("No se pudo cargar o limpiar el DataFrame.")

            elif opcion == 2:
                if df is None:
                    mostrar_mensaje_cargar_datos()
                else:
                    df = analisis_datos.limpiar_datos(df)
            elif opcion == 3:
                if df is None:
                    mostrar_mensaje_cargar_datos()
                else:
                    unicos = analisis_datos.obtener_valores_unicos(df)
                    print("\nValores únicos por columna categórica:")
                    for col, vals in unicos.items():
                        print(f"  {col}: {list(vals)}")
            elif opcion == 4:
                if df is None:
                    mostrar_mensaje_cargar_datos()
                else:
                    col = analisis_datos.seleccionar_columna(df, purpose='estadística')
                    if col:
                        res = estadisticas.mostrar_estadisticas_generales(df, col)
                        resultados['estadisticas'][col] = res
            elif opcion == 5:
                if df is None:
                    mostrar_mensaje_cargar_datos()
                else:
                    graficos.menu_graficos(df, resultados)
            elif opcion == 6:
                if df is None:
                    mostrar_mensaje_cargar_datos()
                else:
                    probabilidad.menu_probabilidades(df, resultados)
            elif opcion == 7:
                if df is None:
                    mostrar_mensaje_cargar_datos()
                else:
                    analisis_datos.sugerencias_mejora(df)
            elif opcion == 8:
                if df is None:
                    mostrar_mensaje_cargar_datos()
                else:
                    informe.guardar_informe(resultados, df)
            elif opcion == 9:
                print("Saliendo de la aplicación. ¡Hasta luego!")
                break
            else:
                print("Opción no válida. Intente nuevamente.")
        except Exception as err:
            print(f"Ocurrió un error inesperado: {err}")
            input("Presione Enter para continuar...")

def mostrar_mensaje_cargar_datos():
    print("Primero debes cargar los datos (opción 1).")

if __name__ == "__main__":
    main()