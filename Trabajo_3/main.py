from machine import Pin, ADC, Timer
import time
# Importamos:
# Pin → manejar pines del ESP32
# ADC → leer señal analógica
# Timer → controlar el muestreo automático
# time → para pausas

# -------- LED --------
led = Pin(2, Pin.OUT)
# Configuramos el pin 2 como salida (LED indicador)


# -------- CONFIG ECG --------
ecg = ADC(Pin(34))
# Pin 34 como entrada analógica (sensor ECG)

ecg.atten(ADC.ATTN_11DB)
# Ajusta el rango de medición hasta ~3.3V

ecg.width(ADC.WIDTH_12BIT)
# Resolución de 12 bits → valores de 0 a 4095

lo_plus = Pin(32, Pin.IN)
# Pin que detecta si el electrodo positivo está conectado

lo_minus = Pin(33, Pin.IN)
# Pin que detecta si el electrodo negativo está conectado


# -------- SELECCIÓN DE FILTRO --------
print("Seleccione el filtro:")
print("0 = Sin filtro")
print("1 = Promedio")
print("2 = Mediana")
print("3 = Exponencial")
print("4 = Todos")
# Menú que se muestra al usuario

opcion = int(input("Ingrese opción: "))
# El usuario selecciona qué filtro usar

usar_promedio = False
usar_mediana = False
usar_exponencial = False
# Inicialmente todos los filtros están apagados

# Activamos los filtros según la opción elegida
if opcion == 1:
    usar_promedio = True
elif opcion == 2:
    usar_mediana = True
elif opcion == 3:
    usar_exponencial = True
elif opcion == 4:
    usar_promedio = True
    usar_mediana = True
    usar_exponencial = True


# -------- FILTRO PROMEDIO --------
buffer_prom = []
# Lista donde se guardan las muestras

N = 10
# Número de muestras para el promedio

def filtro_promedio(valor):
    buffer_prom.append(valor)
    # Agrega el nuevo valor

    if len(buffer_prom) > N:
        buffer_prom.pop(0)
        # Elimina el valor más antiguo

    return sum(buffer_prom) / len(buffer_prom)
    # Retorna el promedio (suaviza la señal)


# -------- FILTRO MEDIANA --------
buffer_med = []
M = 5

def filtro_mediana(valor):
    buffer_med.append(valor)

    if len(buffer_med) > M:
        buffer_med.pop(0)

    ordenado = sorted(buffer_med)
    # Ordena los valores

    return ordenado[len(ordenado)//2]
    # Retorna el valor central (elimina ruido)


# -------- FILTRO EXPONENCIAL --------
alpha = 0.2
# Peso del valor nuevo

valor_exp = 0
# Guarda el valor filtrado anterior

def filtro_exponencial(valor):
    global valor_exp

    valor_exp = alpha * valor + (1 - alpha) * valor_exp
    # Combina valor actual y anterior (suavizado)

    return valor_exp


# -------- DETECCION LATIDOS --------
threshold = 2800
# Umbral para detectar un latido

latido_anterior = False
# Evita detectar el mismo latido varias veces


# -------- ARCHIVO --------
archivo = open("ecg.txt", "w")
# Archivo donde se guardan los datos


# -------- CONTROL --------
num_muestras = 1000
# Número total de muestras

contador = 0
# Contador de muestras

terminado = False
# Indica cuando el proceso termina


# -------- FUNCIÓN DEL TIMER --------
def muestreo(timer):
    global contador, latido_anterior, terminado

    # Si ya se alcanzaron las muestras deseadas
    if contador >= num_muestras:
        timer.deinit()
        # Detiene el Timer

        terminado = True
        # Indica que terminó

        led.off()
        # Apaga LED

        return

    # Verifica si electrodos están mal conectados
    if lo_plus.value() == 1 or lo_minus.value() == 1:
        print("Electrodos desconectados")

    else:
        raw = ecg.read()
        # Lectura cruda (0–4095)

        valor = raw

        # -------- FILTROS --------
        if usar_mediana:
            valor = filtro_mediana(valor)

        if usar_promedio:
            valor = filtro_promedio(valor)

        if usar_exponencial:
            valor = filtro_exponencial(valor)

        valor = int(valor)
        # Convertimos a entero

        print(valor)
        # Mostramos la señal

        archivo.write(str(valor) + "\n")
        # Guardamos en archivo

        # -------- DETECCION LATIDO --------
        if valor > threshold and not latido_anterior:
            print("Latido")
            led.on()   # 🔴 LED encendido cuando hay latido
            latido_anterior = True

        # Histeresis (espera a que la señal baje)
        if valor < threshold - 200:
            led.off()  # 🔴 LED apagado
            latido_anterior = False

    contador += 1
    # Aumenta el número de muestras


# -------- INICIAR --------
timer = Timer(0)

timer.init(period=5, mode=Timer.PERIODIC, callback=muestreo)
# Ejecuta la función cada 5 ms → 200 Hz


# -------- ESPERA --------
while not terminado:
    time.sleep(0.1)
# Espera hasta que termine el muestreo


# -------- FINAL --------
archivo.close()
# Cierra el archivo

print("Datos guardados en ecg.txt")
