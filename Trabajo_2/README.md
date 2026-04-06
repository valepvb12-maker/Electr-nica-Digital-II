from machine import Pin, ADC, PWM  # Importo clases para manejar pines, leer analógico y generar PWM
import time  # Importo librería para manejar tiempos (pausas, milisegundos)

# ------------------ CONFIG ------------------

pot1 = ADC(Pin(34))  # Configuro el potenciómetro 1 en el pin 34 como entrada analógica
pot1.width(ADC.WIDTH_12BIT)  # Defino resolución de 12 bits (0 a 4095)

pot2 = ADC(Pin(35))  # Configuro el potenciómetro 2 en el pin 35
pot2.width(ADC.WIDTH_10BIT)  # Resolución de 10 bits (0 a 1023)

servo1 = PWM(Pin(18), freq=50)  # Servo 1 en pin 18 con PWM a 50 Hz
servo2 = PWM(Pin(19), freq=50)  # Servo 2 en pin 19 con PWM a 50 Hz

led_verde = Pin(2, Pin.OUT)  # LED verde como salida en pin 2
led_rojo = Pin(4, Pin.OUT)   # LED rojo como salida en pin 4

buzzer = Pin(5, Pin.OUT)  # Buzzer como salida en pin 5

btn_reset = Pin(12, Pin.IN, Pin.PULL_UP)  # Botón para volver a inicio (entrada con pull-up)
btn_auto = Pin(14, Pin.IN, Pin.PULL_UP)   # Botón para secuencia automática

modo = "manual"  # Variable que define el estado actual del sistema

# Antirrebote
last_interrupt_time = 0  # Guarda el último tiempo de pulsación
debounce_ms = 200  # Tiempo mínimo entre pulsaciones válidas (200 ms)

# ------------------ FUNCIONES ------------------

def map_value(x, in_min, in_max, out_min, out_max):
    # Función para convertir un valor de un rango a otro (escalamiento)
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def mover_servo(servo, angulo):
    # Recibe un servo y el ángulo al que se quiere mover
    duty = map_value(angulo, 0, 180, 26, 128)  # Convierte el ángulo a PWM (duty)
    servo.duty(duty)  # Envía el duty al servo para que se mueva

def posicion_inicial():
    # Función que mueve ambos servos a la posición inicial (0°)
    for i in range(90, -1, -2):  # Va desde 90 hasta 0 bajando de 2 en 2
        mover_servo(servo1, i)  # Mueve servo 1
        mover_servo(servo2, i)  # Mueve servo 2
        time.sleep(0.02)  # Pausa pequeña para movimiento suave

def secuencia():
    # Función que ejecuta una secuencia automática
    for i in range(0, 90, 2):  # Servo 1 se mueve de 0 a 90
        mover_servo(servo1, i)
        time.sleep(0.02)
    for i in range(90, 0, -2):  # Luego servo 2 se mueve de 90 a 0
        mover_servo(servo2, i)
        time.sleep(0.02)

# ------------------ INTERRUPCIONES ------------------

def manejar_interrupcion(tipo):
    # Función general que maneja lo que pasa al presionar un botón
    global modo, last_interrupt_time  # Permite modificar variables globales
    now = time.ticks_ms()  # Obtiene el tiempo actual en milisegundos
    # Verifica si ya pasó el tiempo de antirrebote
    if time.ticks_diff(now, last_interrupt_time) > debounce_ms:
        last_interrupt_time = now  # Guarda el tiempo de esta pulsación
        modo = tipo  # Cambia el modo del sistema (reset o auto)

def ir_a_inicio(pin):
    # Función que se ejecuta cuando se presiona el botón de reset
    manejar_interrupcion("reset")  # Cambia el modo a "reset"

def rutina_auto(pin):
    # Función que se ejecuta cuando se presiona el botón de secuencia
    manejar_interrupcion("auto")  # Cambia el modo a "auto"

# Configuración de interrupciones
btn_reset.irq(trigger=Pin.IRQ_FALLING, handler=ir_a_inicio)  # Detecta cuando se presiona el botón reset
btn_auto.irq(trigger=Pin.IRQ_FALLING, handler=rutina_auto)   # Detecta cuando se presiona el botón auto

# ------------------ LOOP ------------------

while True:  # Bucle infinito (el programa corre todo el tiempo)
    if modo == "manual":  # Si está en control manual
        led_verde.value(1)  # Enciende LED verde
        led_rojo.value(0)   # Apaga LED rojo
        buzzer.value(0)     # Apaga buzzer
        val1 = pot1.read()  # Lee valor del potenciómetro 1
        val2 = pot2.read()  # Lee valor del potenciómetro 2
        ang1 = map_value(val1, 0, 4095, 0, 180)  # Convierte valor a ángulo
        ang2 = map_value(val2, 0, 1023, 0, 180)
        mover_servo(servo1, ang1)  # Mueve servo 1 según potenciómetro
        mover_servo(servo2, ang2)  # Mueve servo 2 según potenciómetro
        time.sleep(0.05)  # Pequeña pausa
    elif modo == "reset":  # Si se activó el modo de posición inicial
        led_verde.value(0)  # Apaga LED verde
        led_rojo.value(1)   # Enciende LED rojo
        buzzer.value(1)     # Activa buzzer
        posicion_inicial()  # Ejecuta función de regreso a inicio
        buzzer.value(0)  # Apaga buzzer
        modo = "manual"  # Vuelve a modo manual
    elif modo == "auto":  # Si se activó la secuencia automática
        led_verde.value(0)
        led_rojo.value(1)
        buzzer.value(1)
        secuencia()  # Ejecuta la rutina automática
        buzzer.value(0)
        modo = "manual"  # Regresa a modo manual
