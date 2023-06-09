import numpy as np
from sklearn.linear_model import LinearRegression

# Nombres de los meses en español
nombres_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

# Ingresar la demanda mes a mes en los periodos 2021 y 2022
demanda_2021 = []
demanda_2022 = []

print("Ingresar la demanda mes a mes para el periodo 2021:")
for mes in range(1, 13):
    demanda = int(input(f"Ingrese la producción del mes de {nombres_meses[mes-1]}: "))
    demanda_2021.append(demanda)

print("Ingresar la demanda mes a mes para el periodo 2022:")
for mes in range(1, 13):
    demanda = int(input(f"Ingrese la producción del mes de {nombres_meses[mes-1]}: "))
    demanda_2022.append(demanda)

# Paso 1: Calcular el índice de estacionalidad promedio para cada mes
indices_estacionalidad = []
for mes in range(1, 13):
    demanda_mensual = [demanda_2021[mes-1], demanda_2022[mes-1]]
    produccion_p1p2 = sum(demanda_mensual)
    promedio_p1p2 = produccion_p1p2 / len(demanda_mensual)
    promedio_total = sum(demanda_2021 + demanda_2022) / len(demanda_2021 + demanda_2022)
    indice_estacionalidad = round(promedio_p1p2 / promedio_total, 2)
    indices_estacionalidad.append(indice_estacionalidad)

# Paso 2: Calcular la producción desestacionalizada del periodo 2021 y 2022
produccion_desestacionalizada_2021 = [round(demanda_2021[i] / indices_estacionalidad[i], 2) for i in range(12)]
produccion_desestacionalizada_2022 = [round(demanda_2022[i] / indices_estacionalidad[i], 2) for i in range(12)]

# Paso 3: Ajustar una línea de regresión lineal a los datos desestacionalizados del periodo 2021 y 2022
X = np.arange(1, 25).reshape((-1, 1))
y = np.array(produccion_desestacionalizada_2021 + produccion_desestacionalizada_2022)
modelo_regresion = LinearRegression().fit(X[:len(y)], y)

# Paso 4: Calcular la producción del periodo 2023 considerando el índice de estacionalidad
produccion_desestacionalizada_2023 = modelo_regresion.predict(X[12:])
produccion_2023 = [round(produccion_desestacionalizada_2023[i] * indices_estacionalidad[i], 2) for i in range(12)]

# Imprimir los resultados del periodo 2023
for mes, factor, produccion in zip(range(1, 13), indices_estacionalidad, produccion_2023):
    print(f"Mes de {nombres_meses[mes-1]} - Factor de Estacionalidad: {factor}, Producción: {produccion} piezas")
