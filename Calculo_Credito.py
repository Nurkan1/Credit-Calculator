import math
import locale
import os
import subprocess
import datetime

# Establecer la configuración regional para formatear números
locale.setlocale(locale.LC_ALL, '')

# Marca del programa
marca_programa = "NurSoftware"
derehcos_reservados = "© 2024 NurSoftware. Todos los derechos reservados."

# Función para imprimir un mensaje con formato y color
def imprimir_coloreado(mensaje, codigo_color):
    print(f"\033[{codigo_color}m{mensaje}\033[0m")

# Función para calcular los detalles del préstamo y guardar la tabla de amortización
def calcular_prestamo(principal, tasa_interes_anual, años):
    # Convertir la tasa de interés anual a mensual
    tasa_interes_mensual = tasa_interes_anual / 12
    pagos_totales = años * 12

    # Calcular el pago mensual
    pago_mensual = principal * (tasa_interes_mensual * math.pow(1 + tasa_interes_mensual, pagos_totales)) / (math.pow(1 + tasa_interes_mensual, pagos_totales) - 1)

    # Crear la tabla de amortización
    tabla_amortizacion = []
    saldo_restante = principal
    for numero_pago in range(1, pagos_totales + 1):
        pago_interes = saldo_restante * tasa_interes_mensual
        pago_principal = pago_mensual - pago_interes
        saldo_restante -= pago_principal
        tabla_amortizacion.append([numero_pago, pago_mensual, pago_principal, pago_interes, saldo_restante])

    # Calcular el total de intereses pagados
    total_intereses = sum(fila[3] for fila in tabla_amortizacion)

    # Calcular la totalidad a pagar
    total_pagar = principal + total_intereses

    return tabla_amortizacion, pago_mensual, total_intereses, total_pagar

# Función para guardar la tabla de amortización en un archivo
def guardar_tabla_amortizacion(tabla_amortizacion, nombre_credito, pago_mensual, total_intereses, total_pagar, años):
    # Crear el directorio 'calculos' si no existe
    if not os.path.exists("calculos"):
        os.makedirs("calculos")

    # Calcular la duración del préstamo en años o meses
    duracion = años if años > 1 else años * 12

    # Solicitar al usuario el nombre del archivo
    nombre_archivo = input("Ingrese el nombre del archivo para guardar la tabla de amortización (sin extensión): ")

    # Guardar la tabla de amortización en un archivo
    fecha_hora_actual = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    ruta_archivo = os.path.join("calculos", f"{nombre_archivo},{fecha_hora_actual}.txt")
    with open(ruta_archivo, "w") as archivo:
        archivo.write("© 2024 NurSoftware. Todos los derechos reservados\n\n")
        archivo.write(f"Tabla de Amortización - {nombre_credito}\n")
        archivo.write(f"Credito Solisitado: {locale.currency(principal, grouping=True)}\n")
        archivo.write(f"El pago del préstamo de: {locale.currency(principal, grouping=True)} Tendrá una cuota mensual de: {locale.currency(pago_mensual, grouping=True)}\n")
        archivo.write(f"Tasa de Interés Anual: {tasa_interes_anual * 100:.2f}%\n")
        archivo.write(f"Total de interes a pagar: {locale.currency(total_intereses, grouping=True)}\n")
        archivo.write(f"Totalidad a pagar: {locale.currency(total_pagar, grouping=True)}\n")
        archivo.write(f"Duración del préstamo: {duracion} {'años' if años > 1 else 'meses'}\n")
        archivo.write("\nExplicación:\n")
        archivo.write("Esta tabla muestra cómo se distribuyen tus pagos mensuales durante el préstamo. Cada fila indica:\n")
        archivo.write("1. Número de Pago: El orden en que realizas los pagos.\n")
        archivo.write("2. Pago Mensual Total: La cantidad que pagas cada mes.\n")
        archivo.write("3. Pago Principal: La parte del pago que reduce tu deuda original.\n")
        archivo.write("4. Pago de Intereses: La parte del pago que cubre el costo del préstamo.\n")
        archivo.write("5. Saldo Restante del Préstamo: La cantidad que aún debes después de cada pago mensual.\n\n")
        archivo.write("En resumen, la tabla detalla cómo se dividen tus pagos entre el pago del préstamo y los intereses, y cómo disminuye tu deuda con el tiempo.\n")

        archivo.write("+---------+-----------------+-----------------+-----------------+-----------------+\n")
        archivo.write("| Pago No.| Pago Mensual    | Pago Principal  | Pago Interés    | Saldo Restante  |\n")
        archivo.write("+---------+-----------------+-----------------+-----------------+-----------------+\n")
        for fila in tabla_amortizacion:
            archivo.write(f"|    {fila[0]:<4} | {locale.currency(fila[1], grouping=True):>15} | {locale.currency(fila[2], grouping=True):>15} | {locale.currency(fila[3], grouping=True):>15} | {locale.currency(fila[4], grouping=True):>15} |\n")
        archivo.write("+---------+-----------------+-----------------+-----------------+-----------------+\n")
        archivo.write("© 2024 NurSoftware. Todos los derechos reservados\n\n")
    print("¡Tabla de amortización guardada con éxito!")
    return ruta_archivo

# Función para comparar dos préstamos
def comparar_prestamos(tabla_amortizacion1, tabla_amortizacion2, nombre_credito1, nombre_credito2, principal1, principal2, tasa_interes_anual1, tasa_interes_anual2, años1, años2):
    # Calcular la suma de los intereses pagados para cada préstamo
    intereses_pagados1 = sum(fila[3] for fila in tabla_amortizacion1)
    intereses_pagados2 = sum(fila[3] for fila in tabla_amortizacion2)

    # Calcular el total de cada préstamo
    total1 = principal1 + intereses_pagados1
    total2 = principal2 + intereses_pagados2

    # Calcular la duración de cada préstamo
    duracion1 = años1 if años1 > 1 else años1 * 12
    duracion2 = años2 if años2 > 1 else años2 * 12

    # Crear la tabla de comparación
    tabla_comparacion = [
        ["Nombre", nombre_credito1, nombre_credito2],
        ["Total", locale.currency(total1, grouping=True), locale.currency(total2, grouping=True)],
        ["Duración", f"{duracion1} {'años' if años1 > 1 else 'meses'}", f"{duracion2} {'años' if años2 > 1 else 'meses'}"],
        ["Intereses pagados", locale.currency(intereses_pagados1, grouping=True), locale.currency(intereses_pagados2, grouping=True)]
    ]

    # Calcular la diferencia en intereses pagados entre los dos préstamos
    diferencia_intereses = intereses_pagados2 - intereses_pagados1

    # Calcular la diferencia en el saldo restante al final del préstamo
    diferencia_saldo_restante = tabla_amortizacion2[-1][4] - tabla_amortizacion1[-1][4]

    return diferencia_intereses, diferencia_saldo_restante, tabla_comparacion

# Función para guardar los resultados de la comparación en un archivo
def guardar_resultados_comparacion(diferencia_intereses, diferencia_saldo_restante, tabla_comparacion, nombre_credito1, nombre_credito2, principal1, principal2):
    try:
        # Solicitar al usuario el nombre del archivo
        nombre_archivo = input("Ingrese el nombre del archivo para guardar los resultados de la comparación (sin extensión): ")

        # Guardar los resultados de la comparación en un archivo
        fecha_hora_actual = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        ruta_archivo = os.path.join("calculos", f"{nombre_archivo}_{fecha_hora_actual}.txt")
        with open(ruta_archivo, "w") as archivo:
            archivo.write(f"Comparación de Préstamos - {nombre_credito1} vs {nombre_credito2}\n")
            archivo.write("+-------------------------+-----------------+-----------------+\n")
            archivo.write(f"| {'Indicador':<25} | {nombre_credito1:^17} | {nombre_credito2:^17} |\n")
            archivo.write("+-------------------------+-----------------+-----------------+\n")
            for fila in tabla_comparacion:
                archivo.write(f"| {fila[0]:<25} | {fila[1]:^17} | {fila[2]:^17} |\n")
            archivo.write("+-------------------------+-----------------+-----------------+\n")
            archivo.write(f"{nombre_credito1}: {locale.currency(principal1, grouping=True)}\n")
            archivo.write(f"{nombre_credito2}: {locale.currency(principal2, grouping=True)}\n")
            archivo.write(f"Diferencia en Intereses Pagados: {locale.currency(diferencia_intereses, grouping=True)}\n")
            archivo.write(f"Diferencia en Saldo Restante: {locale.currency(diferencia_saldo_restante, grouping=True)}\n")
            archivo.write("+-------------------------+-----------------+-----------------+\n")
            archivo.write("© 2024 NurSoftware. Todos los derechos reservados\n")
        print("¡Resultados de la comparación guardados con éxito!")
        return ruta_archivo
    except IOError:
        print("Error: No se pudo guardar el archivo.")
        return None

# Función para abrir un archivo en el visor predeterminado
def abrir_archivo(ruta_archivo):
    if os.name == 'nt':
        os.startfile(ruta_archivo)  # En sistemas Windows
    else:
        subprocess.call(['xdg-open', ruta_archivo])  # En sistemas Unix-like

# Línea separadora para una mejor legibilidad
separador = "-" * 50

# Bucle principal del programa
while True:
    # Menú principal
    print(separador)
    print("© 2024 NurSoftware. Todos los derechos reservados")
    print(separador)
    imprimir_coloreado(f"Menú del {marca_programa}:", "1;34")  # Texto azul en negrita
    print("1. Calcular préstamo")
    print("2. Mostrar último cálculo")
    print("3. Comparar Préstamos")
    print("4. Salir")
    print(separador)
    opcion = input("Ingrese su elección: ")

    # Realizar acción basada en la opción del usuario
    if opcion == "1":
        principal = float(input("Principal: ").replace(",", ""))
        tasa_interes_anual = float(input("Tasa de Interés Anual (en porcentaje): ").replace(",", "")) / 100
        años = int(input("Duración en años: "))
        nombre_credito = input("Nombre del crédito: ")
        tabla_amortizacion, pago_mensual, total_intereses, total_pagar = calcular_prestamo(principal, tasa_interes_anual, años)
        ruta_archivo = guardar_tabla_amortizacion(tabla_amortizacion, nombre_credito, pago_mensual, total_intereses, total_pagar, años)
        abrir_archivo(ruta_archivo)  # Mostrar el archivo después de guardarlo
    elif opcion == "2":
        if 'ruta_archivo' not in locals():
            print("Primero debe calcular un préstamo.")
        else:
            abrir_archivo(ruta_archivo)
    elif opcion == "3":
        # Entrada de los detalles del primer préstamo
        imprimir_coloreado("Ingrese los detalles del primer préstamo:", "1;34")  # Texto azul en negrita
        print(separador)
        nombre_credito1 = input("Nombre del crédito: ")
        principal1 = float(input("Principal: ").replace(",", ""))
        tasa_interes_anual1 = float(input("Tasa de Interés Anual (en porcentaje): ").replace(",", "")) / 100
        años1 = int(input("Duración en años: "))
        tabla_amortizacion1, pago_mensual1, _, _ = calcular_prestamo(principal1, tasa_interes_anual1, años1)

        # Entrada de los detalles del segundo préstamo
        imprimir_coloreado("Ingrese los detalles del segundo préstamo:", "1;34")  # Texto azul en negrita
        print(separador)
        nombre_credito2 = input("Nombre del crédito: ")
        principal2 = float(input("Principal: ").replace(",", ""))
        tasa_interes_anual2 = float(input("Tasa de Interés Anual (en porcentaje): ").replace(",", "")) / 100
        años2 = int(input("Duración en años: "))
        tabla_amortizacion2, pago_mensual2, _, _ = calcular_prestamo(principal2, tasa_interes_anual2, años2)

        # Realizar la comparación de préstamos
        diferencia_intereses, diferencia_saldo_restante, tabla_comparacion = comparar_prestamos(tabla_amortizacion1, tabla_amortizacion2, nombre_credito1, nombre_credito2, principal1, principal2, tasa_interes_anual1, tasa_interes_anual2, años1, años2)

        # Guardar los resultados de la comparación
        ruta_archivo = guardar_resultados_comparacion(diferencia_intereses, diferencia_saldo_restante, tabla_comparacion, nombre_credito1, nombre_credito2, principal1, principal2)
        abrir_archivo(ruta_archivo)  # Mostrar el archivo después de guardarlo
    elif opcion == "4":
        print(f"¡Gracias por usar {marca_programa}. Hasta luego!")
        break
    else:
        print("Opción inválida. Por favor, ingrese una opción válida.")
