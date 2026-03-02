from machine import Pin, mem32  # Importa Pin para manejar GPIO y mem32 para acceder directamente a registros de memoria del ESP32
import time, random  # Importa el módulo time para manejar tiempos y random para generar números aleatorios

# Registros para LEDs  # Indica que a continuación se configuran los registros para controlar LEDs
OUT, EN = 0x3FF44004, 0x3FF44020  # Define las direcciones de memoria del registro de salida (OUT) y habilitación (EN)
LEDS = [1<<22, 1<<21, 1<<19]  # Crea máscaras binarias para los pines GPIO22, GPIO21 y GPIO19
mem32[EN] = LEDS[0]|LEDS[1]|LEDS[2]  # Habilita esos tres pines como salidas escribiendo en el registro EN

# Pines  # Indica que se configuran los pines de entrada y salida
inicio = Pin(33, Pin.IN, Pin.PULL_DOWN)  # Configura el botón de inicio en GPIO33 como entrada con resistencia pull-down

# Jugador 1  # Sección de botones del jugador 1
j1 = [Pin(27, Pin.IN, Pin.PULL_DOWN), Pin(26, Pin.IN, Pin.PULL_DOWN),  # Configura GPIO27 y GPIO26 como botones de entrada con pull-down
      Pin(25, Pin.IN, Pin.PULL_DOWN), Pin(32, Pin.IN, Pin.PULL_DOWN)]  # Configura GPIO25 y GPIO32 como botones de entrada con pull-down

# Jugador 2  # Sección de botones del jugador 2
j2 = [Pin(4, Pin.IN, Pin.PULL_DOWN), Pin(15, Pin.IN, Pin.PULL_DOWN),  # Configura GPIO4 y GPIO15 como botones de entrada con pull-down
      Pin(18, Pin.IN, Pin.PULL_DOWN), Pin(2, Pin.IN, Pin.PULL_DOWN)]  # Configura GPIO18 y GPIO2 como botones de entrada con pull-down

simon_sw = Pin(14, Pin.IN, Pin.PULL_UP)  # Configura el interruptor del modo Simon en GPIO14 con pull-up
fin_sw   = Pin(13, Pin.IN, Pin.PULL_UP)  # Configura el interruptor de fin de juego en GPIO13 con pull-up
buzzer = Pin(23, Pin.OUT)  # Configura el GPIO23 como salida para controlar el buzzer

# Variables del juego  # Sección de variables principales del sistema
p1 = p2 = ronda = 0  # Inicializa puntaje jugador 1, jugador 2 y número de ronda en cero
jug = 1  # Variable que indica cantidad de jugadores, por defecto 1
simon = fin = False  # Banderas booleanas para indicar si se activa modo Simon o si el juego termina

# Variables para debounce de botones  # Sección para evitar rebotes mecánicos en botones
DEBOUNCE_MS = 50  # Tiempo mínimo en milisegundos para validar una pulsación estable
simon_raw = 1  # Último valor leído del botón Simon
simon_raw_time = 0  # Momento en que cambió el valor del botón Simon
simon_stable = 1  # Valor estable confirmado del botón Simon
fin_raw = 1  # Último valor leído del botón Fin
fin_raw_time = 0  # Momento en que cambió el valor del botón Fin
fin_stable = 1  # Valor estable confirmado del botón Fin
 
def check_buttons():  # Define función para leer botones con antirrebote
    """Lee los botones con debounce y actualiza las banderas simon y fin."""  # Describe lo que hace la función
    global simon, fin  # Permite modificar variables globales simon y fin
    global simon_raw, simon_raw_time, simon_stable  # Permite modificar variables globales de debounce Simon
    global fin_raw, fin_raw_time, fin_stable  # Permite modificar variables globales de debounce Fin
    now = time.ticks_ms()  # Obtiene tiempo actual en milisegundos
    # Botón SIMON  # Sección para evaluar botón Simon
    val = simon_sw.value()  # Lee estado actual del botón Simon
    if val != simon_raw:  # Si cambió respecto a la última lectura
        simon_raw = val  # Actualiza valor leído
        simon_raw_time = now  # Guarda momento del cambio
    if time.ticks_diff(now, simon_raw_time) > DEBOUNCE_MS:  # Si pasó tiempo suficiente para validar estabilidad
        if simon_stable == 1 and simon_raw == 0:  # Si detecta transición de alto a bajo
            simon = True  # Activa bandera de modo Simon
        simon_stable = simon_raw  # Actualiza estado estable
    # Botón FIN  # Sección para evaluar botón Fin
    val = fin_sw.value()  # Lee estado actual del botón Fin
    if val != fin_raw:  # Si cambió respecto a la última lectura
        fin_raw = val  # Actualiza valor leído
        fin_raw_time = now  # Guarda momento del cambio
    if time.ticks_diff(now, fin_raw_time) > DEBOUNCE_MS:  # Si pasó tiempo suficiente
        if fin_stable == 1 and fin_raw == 0:  # Si detecta transición válida
            fin = True  # Activa bandera de fin de juego
        fin_stable = fin_raw  # Actualiza estado estable
 
def led_on(n):  # Función para encender un LED específico
    mem32[OUT] |= LEDS[n-1]  # Activa el bit correspondiente al LED seleccionado
 
def led_off(n):  # Función para apagar un LED específico
    mem32[OUT] &= ~LEDS[n-1]  # Desactiva el bit correspondiente al LED seleccionado
 
def led_all_off():  # Función para apagar todos los LEDs
    mem32[OUT] &= ~(LEDS[0]|LEDS[1]|LEDS[2])  # Limpia los bits de los tres LEDs
 
def buz(v):  # Función para controlar buzzer
    buzzer.value(v)  # Envía valor lógico al buzzer
 
def puntos():  # Función para mostrar puntajes actuales
    print(f"\n--- PUNTOS: J1={p1}" + (f" J2={p2}" if jug==2 else "") + " ---")  # Imprime puntaje según cantidad de jugadores
 
# Selección de modo al inicio  # Sección inicial del sistema
print("\n----SISTEMA DE REFLEJOS------")  # Muestra título del sistema
print("Presiona el botón Azul...")  # Indica que debe presionar botón de inicio
while not inicio.value():  # Espera hasta que el botón inicio sea presionado
    check_buttons()  # Revisa botones secundarios
    time.sleep(0.1)  # Pequeña pausa para no saturar CPU
time.sleep(0.3)  # Pequeño retardo después de presionar
 
print("(Individual: presiona 1 vez / Multiplayer: presiona 2 veces)")  # Instrucciones de selección
c, t0 = 0, time.ticks_ms()  # Inicializa contador de pulsaciones y tiempo base
while time.ticks_diff(time.ticks_ms(), t0) < 5000:  # Durante 5 segundos
    check_buttons()  # Revisa botones
    if inicio.value():  # Si detecta pulsación
        c += 1  # Incrementa contador
        while inicio.value():  # Espera que suelte botón
            check_buttons()  # Sigue revisando botones
            time.sleep(0.05)  # Pequeña pausa
        time.sleep(0.2)  # Retardo entre pulsaciones
jug = 2 if c >= 2 else 1  # Define modo de juego según cantidad de pulsaciones
print(f"\n{'2 jugadores' if jug==2 else '1 jugador'}")  # Muestra cantidad de jugadores
print("Controles: SW14=Simon, SW13=Fin")  # Muestra controles disponibles
puntos()  # Muestra puntaje inicial
 
# Bucle principal  # Inicio del ciclo principal del juego
while not fin:  # Mientras no se presione botón Fin
    check_buttons()  # Revisa botones especiales
    if simon:  # Si se activó modo Simon
        pass  # Aquí iría llamada a función Simon si estuviera incluida
        continue  # Vuelve al inicio del ciclo
    ronda += 1  # Incrementa número de ronda
    print(f"\nRONDA {ronda}")  # Muestra número de ronda
    esp = random.randint(1, 10)  # Genera tiempo de espera aleatorio
    t = time.ticks_ms()  # Guarda tiempo inicial de espera
    while time.ticks_diff(time.ticks_ms(), t) < esp * 1000:  # Espera ese tiempo en milisegundos
        check_buttons()  # Revisa botones
        if simon or fin:  # Si se activa Simon o Fin
            break  # Sale de la espera
        time.sleep(0.1)  # Pausa pequeña
    if simon or fin:  # Si se activó alguna bandera
        continue  # Regresa al inicio del ciclo
    est = random.randint(1, 4)  # Genera estímulo aleatorio
    if est <= 3:  # Si es LED
        led_on(est)  # Enciende LED correspondiente
    else:  # Si es buzzer
        buz(1)  # Activa buzzer
    t0 = time.ticks_ms()  # Guarda tiempo inicial de reacción
    t1 = t2 = None  # Inicializa tiempos de respuesta
    ok1 = ok2 = err1 = err2 = False  # Inicializa banderas
    while time.ticks_diff(time.ticks_ms(), t0) < 3000:  # Ventana de 3 segundos
        check_buttons()  # Revisa botones
        if simon or fin:  # Si se activa alguna bandera
            break  # Sale
        now = time.ticks_ms()  # Guarda tiempo actual
        time.sleep(0.01)  # Pausa mínima
    if est <= 3:  # Si era LED
        led_off(est)  # Apaga LED
    else:  # Si era buzzer
        buz(0)  # Apaga buzzer
    puntos()  # Muestra puntajes
    time.sleep(2)  # Espera antes de siguiente ronda
 
print("\nJUEGO TERMINADO")  # Mensaje final
puntos()  # Muestra puntajes finales
for _ in range(3):  # Repite 3 veces
    buz(1)  # Enciende buzzer
    time.sleep(0.2)  # Espera
    buz(0)  # Apaga buzzer
    time.sleep(0.2)  # Espera
print("Gracias por jugar")  # Mensaje de despedida
