from machine import Pin, mem32  # Importa la clase Pin para configurar pines y mem32 para acceder a registros del ESP32
import time, random  # Importa time para manejar tiempos y random para generar números aleatorios

OUT, EN = 0x3FF44004, 0x3FF44020  # Guarda las direcciones de memoria de los registros OUT (estado del pin) y EN (configuración entrada/salida)

LEDS = [1<<22, 1<<21, 1<<19]  # Crea máscaras binarias desplazando 1 a los bits 22, 21 y 19 (GPIO 22, 21 y 19)

mem32[EN] = LEDS[0] | LEDS[1] | LEDS[2]  # Activa los bits correspondientes en el registro EN para configurar esos pines como salida

inicio = Pin(33, Pin.IN, Pin.PULL_DOWN)  # Configura el pin 33 como entrada con resistencia pull-down

j1 = [Pin(27, Pin.IN, Pin.PULL_DOWN),  # Configura pin 27 como botón del jugador 1
      Pin(26, Pin.IN, Pin.PULL_DOWN),  # Configura pin 26 como botón del jugador 1
      Pin(25, Pin.IN, Pin.PULL_DOWN),  # Configura pin 25 como botón del jugador 1
      Pin(32, Pin.IN, Pin.PULL_DOWN)]  # Configura pin 32 como botón del jugador 1

j2 = [Pin(4, Pin.IN, Pin.PULL_DOWN),   # Configura pin 4 como botón del jugador 2
      Pin(15, Pin.IN, Pin.PULL_DOWN),  # Configura pin 15 como botón del jugador 2
      Pin(18, Pin.IN, Pin.PULL_DOWN),  # Configura pin 18 como botón del jugador 2
      Pin(2, Pin.IN, Pin.PULL_DOWN)]   # Configura pin 2 como botón del jugador 2

simon_sw = Pin(14, Pin.IN, Pin.PULL_UP)  # Configura pin 14 como botón Simon con pull-up
fin_sw = Pin(13, Pin.IN, Pin.PULL_UP)    # Configura pin 13 como botón Fin con pull-up

buzzer = Pin(23, Pin.OUT)  # Configura pin 23 como salida para el buzzer

p1 = p2 = ronda = 0  # Inicializa puntajes y ronda en 0
jug = 1  # Inicializa número de jugadores en 1
simon = fin = False  # Inicializa banderas de control en False

DEBOUNCE_MS = 50  # Define tiempo de debounce en milisegundos

simon_raw = 1  # Guarda lectura inmediata del botón Simon
simon_raw_time = 0  # Guarda instante del último cambio del botón Simon
simon_stable = 1  # Guarda estado confirmado del botón Simon

fin_raw = 1  # Guarda lectura inmediata del botón Fin
fin_raw_time = 0  # Guarda instante del último cambio del botón Fin
fin_stable = 1  # Guarda estado confirmado del botón Fin

def check_buttons():  # Define función para revisar botones con debounce
    global simon, fin  # Indica que se usarán variables globales
    global simon_raw, simon_raw_time, simon_stable  # Indica uso de variables globales de Simon
    global fin_raw, fin_raw_time, fin_stable  # Indica uso de variables globales de Fin

    now = time.ticks_ms()  # Obtiene tiempo actual en milisegundos

    val = simon_sw.value()  # Lee valor actual del botón Simon

    if val != simon_raw:  # Si cambió respecto a última lectura
        simon_raw = val  # Actualiza valor inmediato
        simon_raw_time = now  # Guarda momento del cambio

    if time.ticks_diff(now, simon_raw_time) > DEBOUNCE_MS:  # Si el cambio dura más de 50 ms
        if simon_stable == 1 and simon_raw == 0:  # Si pasó de 1 a 0
            simon = True  # Activa modo Simon
        simon_stable = simon_raw  # Actualiza estado estable

    val = fin_sw.value()  # Lee valor actual del botón Fin

    if val != fin_raw:  # Si cambió respecto a última lectura
        fin_raw = val  # Actualiza valor inmediato
        fin_raw_time = now  # Guarda momento del cambio

    if time.ticks_diff(now, fin_raw_time) > DEBOUNCE_MS:  # Si el cambio dura más de 50 ms
        if fin_stable == 1 and fin_raw == 0:  # Si pasó de 1 a 0
            fin = True  # Activa finalización del juego
        fin_stable = fin_raw  # Actualiza estado estable

def led_on(n):  # Define función para encender LED
    mem32[OUT] |= LEDS[n-1]  # Activa bit correspondiente en registro OUT

def led_off(n):  # Define función para apagar LED
    mem32[OUT] &= ~LEDS[n-1]  # Limpia bit correspondiente en registro OUT

def led_all_off():  # Define función para apagar todos los LEDs
    mem32[OUT] &= ~(LEDS[0] | LEDS[1] | LEDS[2])  # Limpia bits de todos los LEDs

def buz(v):  # Define función para controlar buzzer
    buzzer.value(v)  # Asigna valor 1 o 0 al buzzer

def puntos():  # Define función para mostrar puntajes
    print(f"\n--- PUNTOS: J1={p1}" + (f" J2={p2}" if jug==2 else "") + " ---")  # Imprime puntaje según cantidad de jugadores

def simon_juego():  # Define función principal del juego Simon
    global p1, simon, fin  # Indica uso de variables globales

    print("\n🎲 SIMON DICE (usa J1)")  # Muestra mensaje de inicio

    bt = j1[:4]  # Asigna lista de botones del jugador 1
    est = [1,2,3,4]  # Define lista de estímulos posibles
    seq = []  # Inicializa lista vacía para secuencia
    r = 1  # Inicializa ronda en 1
    perdio = False  # Inicializa bandera de pérdida

    time.sleep(1)  # Espera 1 segundo

    while not perdio and not fin and simon:  # Ejecuta mientras no pierda ni termine
        print(f"Ronda {r}")  # Muestra número de ronda
        time.sleep(1)  # Espera 1 segundo

        seq.append(random.randint(0,3))  # Agrega número aleatorio entre 0 y 3 a la secuencia

        for i in seq:  # Recorre cada elemento de la secuencia
            check_buttons()  # Verifica botones especiales
            e = est[i]  # Obtiene estímulo real según índice

            if e <= 3:  # Si corresponde a LED
                led_on(e)  # Enciende LED
                time.sleep(0.8)  # Mantiene encendido 0.8 segundos
                led_off(e)  # Apaga LED
            else:  # Si corresponde a buzzer
                buz(1)  # Enciende buzzer
                time.sleep(0.8)  # Mantiene sonido 0.8 segundos
                buz(0)  # Apaga buzzer

            time.sleep(0.3)  # Espera 0.3 segundos entre estímulos

        for esp in seq:  # Recorre secuencia para turno del jugador
            print("Tu turno...")  # Muestra mensaje
            press = None  # Inicializa variable de botón presionado

            while press is None and not fin and simon:  # Espera hasta que presione botón válido
                check_buttons()  # Verifica botones especiales

                for i, b in enumerate(bt):  # Recorre botones del jugador
                    if b.value():  # Si detecta pulsación
                        time.sleep(0.05)  # Espera 50 ms
                        if b.value():  # Verifica que siga presionado
                            press = i  # Guarda índice del botón presionado

                            if i <= 2:  # Si corresponde a LED
                                led_on(i+1)  # Enciende LED
                                time.sleep(0.2)  # Mantiene encendido
                                led_off(i+1)  # Apaga LED
                            else:  # Si corresponde a buzzer
                                buz(1)  # Enciende buzzer
                                time.sleep(0.2)  # Mantiene sonido
                                buz(0)  # Apaga buzzer

                            while b.value():  # Espera a que se suelte botón
                                check_buttons()  # Verifica botón fin
                                time.sleep(0.05)  # Pequeña espera

                            break  # Sale del for cuando detecta botón

                time.sleep(0.01)  # Pequeña pausa para estabilidad

            if fin or not simon:  # Si se presionó fin o salió del modo
                break  # Sale del turno

            if press == esp:  # Compara botón presionado con esperado
                print("✓ Correcto")  # Indica acierto

                if press <= 2:  # Si LED
                    led_on(press + 1)  # Enciende LED
                    time.sleep(0.3)  # Mantiene encendido
                    led_off(press + 1)  # Apaga LED
                else:  # Si buzzer
                    buz(1)  # Enciende buzzer
                    time.sleep(0.3)  # Mantiene sonido
                    buz(0)  # Apaga buzzer

                time.sleep(0.2)  # Espera antes de continuar
            else:  # Si no coincide
                print("✗ Perdiste")  # Indica pérdida
                perdio = True  # Marca que perdió
                p1 += r * 50  # Suma puntos según ronda
                print(f"Bonus +{r*50}")  # Muestra puntos obtenidos

                for _ in range(3):  # Repite 3 veces sonido de error
                    buz(1)  # Enciende buzzer
                    time.sleep(0.2)  # Espera
                    buz(0)  # Apaga buzzer
                    time.sleep(0.2)  # Espera

                break  # Sale del turno

        r += 1  # Incrementa número de ronda
        time.sleep(1)  # Espera antes de siguiente ronda

    led_all_off()  # Apaga todos los LEDs
    buz(0)  # Apaga buzzer
    print("Volviendo...\n")  # Muestra mensaje final
    simon = False  # Desactiva modo Simon
# Selección de modo al inicio  # Comentario que indica que aquí comienza la selección del modo de juego
print("\n----SISTEMA DE REFLEJOS------")  # Muestra en pantalla el título del sistema
print(" La victoria no lo es todo: es lo único! ")  # Muestra una frase motivacional
print("Presiona el botón Azul...")  # Indica al usuario que debe presionar el botón azul para comenzar
while not inicio.value():  # Bucle que espera hasta que el botón de inicio sea presionado
    check_buttons()  # Revisa el estado de todos los botones
    time.sleep(0.1)  # Pequeña pausa para evitar lecturas demasiado rápidas
time.sleep(0.3)  # Pequeña pausa adicional para evitar rebotes del botón
 
print("(Individual: presiona 1 vez / Multiplayer: presiona 2 veces)")  # Explica cómo seleccionar el modo de juego
c, t0 = 0, time.ticks_ms()  # Inicializa el contador de pulsaciones y guarda el tiempo inicial
while time.ticks_diff(time.ticks_ms(), t0) < 5000:  # Permite contar pulsaciones durante 5 segundos
    check_buttons()  # Revisa el estado de los botones
    if inicio.value():  # Si el botón de inicio es presionado
        c += 1  # Incrementa el contador de pulsaciones
        print(f"Pulsación {c}")  # Muestra cuántas veces se ha presionado
        while inicio.value():  # Espera hasta que el botón sea soltado
            check_buttons()  # Sigue revisando botones
            time.sleep(0.05)  # Pequeña pausa anti-rebote
        time.sleep(0.2)  # Pausa adicional para estabilidad
jug = 2 if c >= 2 else 1  # Define 2 jugadores si se presionó 2 o más veces, si no 1 jugador
print(f"\n{'2 jugadores' if jug==2 else '1 jugador'}")  # Muestra cuántos jugadores participarán
print("Controles: SW14=Simon, SW13=Fin")  # Indica los botones especiales del sistema
puntos()  # Muestra los puntos actuales
 
# Bucle principal  # Indica que comienza el ciclo principal del juego
while not fin:  # El juego continúa mientras no se active la variable de fin
    check_buttons()  # Revisa constantemente los botones
    if simon:  # Si se activa el modo Simon
        simon_juego()  # Ejecuta la función del juego Simon
        continue  # Regresa al inicio del bucle principal
 
    ronda += 1  # Incrementa el número de ronda
    print(f"\nRONDA {ronda}")  # Muestra el número de la ronda actual
 
    # Espera aleatoria (1-10s) con chequeo de botones  # Comentario descriptivo
    esp = random.randint(1, 10)  # Genera un tiempo de espera aleatorio entre 1 y 10 segundos
    print(f"Espera {esp}s")  # Muestra cuánto tiempo esperará antes del estímulo
    t = time.ticks_ms()  # Guarda el tiempo actual
    while time.ticks_diff(time.ticks_ms(), t) < esp * 1000:  # Espera la cantidad de segundos indicada
        check_buttons()  # Revisa botones durante la espera
        if simon or fin:  # Si se activa Simon o fin
            break  # Sale de la espera
        time.sleep(0.1)  # Pausa corta para estabilidad
    if simon or fin:  # Si se activó alguna condición especial
        continue  # Regresa al inicio del bucle principal
 
    # Estímulo aleatorio (1..4)  # Comentario descriptivo
    est = random.randint(1, 4)  # Genera un número aleatorio entre 1 y 4
    if est <= 3:  # Si el número es 1, 2 o 3
        led_on(est)  # Enciende el LED correspondiente
        print(f"LED{est} ON")  # Indica qué LED se encendió
    else:  # Si el número es 4
        buz(1)  # Activa el buzzer
        print("BUZZER ON")  # Indica que el buzzer está encendido
 
    t0 = time.ticks_ms()  # Guarda el tiempo en que apareció el estímulo
    t1 = t2 = None  # Inicializa los tiempos de respuesta en None
    ok1 = ok2 = err1 = err2 = False  # Inicializa estados de acierto y error en falso
 
    # Ventana de 3 segundos para responder  # Comentario descriptivo
    while time.ticks_diff(time.ticks_ms(), t0) < 3000:  # Permite responder durante 3 segundos
        check_buttons()  # Revisa botones
        if simon or fin:  # Si se activa Simon o fin
            break  # Sale del tiempo de respuesta
        now = time.ticks_ms()  # Guarda el tiempo actual
 
        # Jugador 1  # Comentario descriptivo
        if t1 is None:  # Si el jugador 1 aún no ha respondido
            for i, b in enumerate(j1):  # Recorre los botones del jugador 1
                if b.value():  # Si algún botón está presionado
                    while b.value():  # Espera a que lo suelte
                        check_buttons()  # Revisa botones
                        time.sleep(0.05)  # Pausa anti-rebote
                    if i + 1 == est:  # Si el botón presionado coincide con el estímulo
                        t1 = time.ticks_diff(now, t0)  # Calcula el tiempo de reacción
                        ok1 = True  # Marca respuesta correcta
                        print(f"J1 correcto {t1}ms")  # Muestra tiempo de reacción
                    else:  # Si se equivocó
                        t1 = 3000  # Asigna tiempo máximo
                        err1 = True  # Marca error
                        print("J1 error -50")  # Indica penalización
                        for _ in range(2):  # Repite sonido de error dos veces
                            buz(1)  # Enciende buzzer
                            time.sleep(0.1)  # Espera corta
                            buz(0)  # Apaga buzzer
                            time.sleep(0.05)  # Pausa corta
                    break  # Sale del bucle de botones
 
        # Jugador 2 (si aplica)  # Comentario descriptivo
        if jug == 2 and t2 is None:  # Si hay 2 jugadores y J2 no ha respondido
            for i, b in enumerate(j2):  # Recorre botones de J2
                if b.value():  # Si presiona un botón
                    while b.value():  # Espera a que lo suelte
                        check_buttons()  # Revisa botones
                        time.sleep(0.05)  # Pausa anti-rebote
                    if i + 1 == est:  # Si coincide con el estímulo
                        t2 = time.ticks_diff(now, t0)  # Calcula tiempo de reacción
                        ok2 = True  # Marca respuesta correcta
                        print(f"J2 correcto {t2}ms")  # Muestra tiempo
                    else:  # Si se equivoca
                        t2 = 3000  # Asigna tiempo máximo
                        err2 = True  # Marca error
                        print("J2 error -50")  # Indica penalización
                        for _ in range(2):  # Repite sonido de error
                            buz(1)  # Enciende buzzer
                            time.sleep(0.1)  # Espera
                            buz(0)  # Apaga buzzer
                            time.sleep(0.05)  # Pausa
                    break  # Sale del bucle
 
        if jug == 1 and t1 is not None:  # Si es modo individual y J1 ya respondió
            break  # Sale de la ventana de respuesta
        if jug == 2 and t1 is not None and t2 is not None:  # Si ambos ya respondieron
            break  # Sale de la ventana
        time.sleep(0.01)  # Pequeña pausa para estabilidad
 
    # Apagar estímulo  # Comentario descriptivo
    if est <= 3:  # Si fue un LED
        led_off(est)  # Apaga el LED correspondiente
    else:  # Si fue el buzzer
        buz(0)  # Apaga el buzzer
 
    if simon or fin:  # Si se activó Simon o fin
        continue  # Regresa al inicio del bucle principal
 
    # Asignar tiempos por defecto si no respondieron  # Comentario descriptivo
    if t1 is None:  # Si J1 no respondió
        t1 = 3000  # Asigna tiempo máximo
        print("J1 sin respuesta")  # Indica que no respondió
    if jug == 2 and t2 is None:  # Si J2 no respondió en modo multiplayer
        t2 = 3000  # Asigna tiempo máximo
        print("J2 sin respuesta")  # Indica que no respondió
 
    pts1 = max(0, int((3000 - t1) * 0.1)) if ok1 else (-50 if err1 else 0)  # Calcula puntos de J1
    pts2 = max(0, int((3000 - t2) * 0.1)) if ok2 else (-50 if err2 else 0) if jug == 2 else 0  # Calcula puntos de J2
    p1 += pts1  # Suma puntos a J1
    p2 += pts2  # Suma puntos a J2
 
    print(f"Ronda {ronda}: J1 {pts1} ({t1}ms)" + (f" J2 {pts2} ({t2}ms)" if jug == 2 else ""))  # Muestra resumen de la ronda
    puntos()  # Muestra puntajes actualizados
    time.sleep(2)  # Pausa antes de la siguiente ronda
 
# Fin del juego  # Indica que terminó el bucle principal
print("\nJUEGO TERMINADO")  # Muestra mensaje de finalización
puntos()  # Muestra puntajes finales
if jug == 1:  # Si fue modo individual
    print(f"Puntaje final: {p1}")  # Muestra puntaje final
else:  # Si fue modo multiplayer
    if p1 > p2:  # Si J1 tiene más puntos
        print("GANA J1")  # Declara ganador a J1
    elif p2 > p1:  # Si J2 tiene más puntos
        print("GANA J2")  # Declara ganador a J2
    else:  # Si empatan
        print("EMPATE")  # Indica empate
for _ in range(3):  # Repite tres veces
    buz(1)  # Enciende buzzer
    time.sleep(0.2)  # Espera
    buz(0)  # Apaga buzzer
    time.sleep(0.2)  # Espera
print("Gracias por jugar")  # Mensaje final de despedida
