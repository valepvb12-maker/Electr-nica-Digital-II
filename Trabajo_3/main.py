from machine import Pin, ADC, Timer  
# Importamos:
# Pin → para usar los pines del ESP32
# ADC → para leer señales analógicas
# Timer → para controlar la frecuencia de muestreo automáticamente

# CONFIGURACIÓN ECG 
sensor_ecg = ADC(Pin(34))            
# Configuramos el pin 34 como entrada analógica (sensor ECG)

sensor_ecg.atten(ADC.ATTN_11DB)      
# Ajustamos el rango de voltaje hasta ~3.3V

sensor_ecg.width(ADC.WIDTH_12BIT)    
# Resolución de 12 bits → valores de 0 a 4095

lo_p = Pin(18, Pin.IN)               
# Pin que detecta si el electrodo positivo está conectado

lo_m = Pin(19, Pin.IN)               
# Pin que detecta si el electrodo negativo está conectado


# LED INDICADOR
led = Pin(2, Pin.OUT)   
# Configuramos el pin 2 como salida (LED)

led.value(1)            
# Encendemos el LED → indica que el sistema está activo


# CONFIG FILTROS 
filtro_prom = False
filtro_med = False
filtro_expo = False
# Inicialmente todos los filtros están desactivados


# SELECCIÓN DE FILTROS POR USUARIO 
print("\n CONFIGURACIÓN DE FILTROS")
print("1: Promedio")
print("2: Mediana")
print("3: Exponencial")
print("Ejemplo: 1,2  o  2,3  o  1,2,3")
print("0: Ninguno")
# Mostramos menú en consola

opcion = input("Seleccione filtros: ")
# El usuario escribe qué filtros quiere usar

if opcion != "0":
    opciones = opcion.split(",")
    # Separamos lo que escribió (ej: "1,2" → ["1","2"])

    if "1" in opciones:
        filtro_prom = True
    # Activa filtro promedio

    if "2" in opciones:
        filtro_med = True
    # Activa filtro mediana

    if "3" in opciones:
        filtro_expo = True
    # Activa filtro exponencial


# FILTRO PROMEDIO 
b_prom = []      
# Lista donde se guardan las muestras

N = 10           
# Cantidad de muestras para el promedio

def f_promedio(valor):
    b_prom.append(valor)            
    # Agrega nuevo valor

    if len(b_prom) > N:             
        b_prom.pop(0)               
        # Elimina el valor más viejo

    return sum(b_prom) / len(b_prom)  
    # Retorna el promedio de los valores


# FILTRO MEDIANA 
b_med = []      
# Lista para muestras

M = 5           
# Tamaño de la ventana

def f_mediana(valor):
    b_med.append(valor)             
    # Agrega valor

    if len(b_med) > M:              
        b_med.pop(0)
        # Elimina el más viejo

    ordenado = sorted(b_med)        
    # Ordena los datos

    return ordenado[len(ordenado)//2]  
    # Devuelve el valor central (mediana)


# FILTRO EXPONENCIAL 
a = 0.2
# Factor de suavizado

valor_exp = 0
# Guarda el valor filtrado anterior

def f_exponencial(valor):
    global valor_exp
    # Permite modificar la variable global

    valor_exp = a * valor + (1 - a) * valor_exp  
    # Combina valor nuevo y anterior (suavizado)

    return valor_exp
    # Retorna valor filtrado


# DETECCIÓN DE LATIDOS 
umbral = 2800
# Valor que debe superar la señal para considerar un latido

latido_ant = False
# Variable para evitar detectar el mismo latido varias veces


# ARCHIVO 
archivo = open("medicion_ecg.txt", "w")  
# Archivo donde se guardarán los datos


# CONTADOR DE MUESTRAS 
num_m = 1000   
# Número total de muestras a tomar

contador = 0   
# Contador de muestras


# FUNCIÓN QUE EJECUTA EL TIMER 
def leer_ecg(t):
    global latido_ant, contador
    # Variables globales que se modifican dentro de la función

    # Verifica si electrodos están desconectados
    if lo_p.value() == 1 or lo_m.value() == 1:
        print("Electrodos desconectados")

    else:
        raw = sensor_ecg.read()   
        # Lectura cruda del ADC (0–4095)

        v = raw                   
        # Copia del valor

        # Aplicar filtros
        if filtro_med:
            v = f_mediana(v)

        if filtro_prom:
            v = f_promedio(v)

        if filtro_expo:
            v = f_exponencial(v)

        v = int(v)                
        # Convertimos a entero

        print(v)                  
        # Mostramos el valor en consola

        archivo.write(str(v) + "\n")  
        # Guardamos el dato en el archivo

        # Detección de latido
        if v > umbral and not latido_ant:
            print("Latido")
            latido_ant = True
            # Detecta el pico

        # Histeresis (evita múltiples detecciones)
        if v < umbral - 200:
            latido_ant = False
            # Espera a que la señal baje para detectar otro latido

    contador += 1  
    # Aumenta el contador

    # Cuando llega al número deseado, detiene el Timer
    if contador >= num_m:
        timer.deinit() 
        # Detiene el Timer

        archivo.close()
        # Cierra el archivo

        led.value(0) 
        # Apaga el LED

        print("Datos guardados en medicion_ecg.txt")


# CONFIGURACIÓN DEL TIMER 
timer = Timer(0)
# Creamos un Timer

# Ejecuta la función cada 5 ms → 200 Hz
timer.init(period=5, mode=Timer.PERIODIC, callback=leer_ecg)
# Llama a la función leer_ecg cada 5 ms automáticamente
