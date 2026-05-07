from machine import Pin, I2C, PWM  # Importamos módulos: Pin (pines), I2C (comunicación), PWM (señal buzzer)
import ssd1306  # Librería para controlar la pantalla OLED
import time  # Para trabajar con tiempos
import random  # Para valores aleatorios

# ========== HARDWARE ==========
i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # Configuramos I2C con pin 22 (reloj) y 21 (datos)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)  # Inicializamos pantalla de 128x64 píxeles

btn_up = Pin(16, Pin.IN, Pin.PULL_UP)  # Botón subir (1 sin presionar, 0 presionado)
btn_down = Pin(17, Pin.IN, Pin.PULL_UP)  # Botón bajar
btn_start = Pin(14, Pin.IN, Pin.PULL_UP)  # Botón iniciar/pausa

buzzer = PWM(Pin(27))  # Buzzer en pin 27 con PWM
buzzer.duty(0)  # Apagamos buzzer

led = Pin(2, Pin.OUT)  # LED como salida
led.off()  # Apagamos LED

# ========== DEBOUNCE OPTIMIZADO ==========
last_edge_time = {}  # Guarda el tiempo de la última pulsación válida
last_hold_time = {}  # Guarda el tiempo de repetición al mantener presionado
last_state = {}  # Guarda el estado anterior del botón

DEBOUNCE_MS = 150  # Tiempo de antirrebote
HOLD_INTERVAL = 60  # Tiempo entre repeticiones al mantener presionado

def is_pressed(btn, hold=False):  # Función para detectar pulsaciones
    now = time.ticks_ms()  # Tiempo actual en milisegundos

    if btn not in last_edge_time:  # Si es la primera vez que se usa ese botón
        last_edge_time[btn] = 0  # Inicializamos tiempo de pulsación
        last_hold_time[btn] = 0  # Inicializamos tiempo de hold
        last_state[btn] = 1  # Estado inicial (no presionado)

    current = btn.value()  # Estado actual del botón

    if last_state[btn] == 1 and current == 0:  # Detecta cambio de no presionado a presionado
        if time.ticks_diff(now, last_edge_time[btn]) > DEBOUNCE_MS:  # Si pasó el tiempo antirrebote
            last_edge_time[btn] = now  # Guardamos tiempo de pulsación válida
            last_state[btn] = current  # Actualizamos estado
            return True  # Confirmamos pulsación válida

    if hold and current == 0:  # Si se permite hold y el botón sigue presionado
        if time.ticks_diff(now, last_hold_time[btn]) > HOLD_INTERVAL:  # Si pasó el intervalo de repetición
            last_hold_time[btn] = now  # Guardamos tiempo
            return True  # Se considera como repetición de pulsación

    last_state[btn] = current  # Actualizamos estado para la siguiente lectura
    return False  # Si nada se cumplió, no hubo pulsación

# ========== SPRITE ==========
player_sprite = [  # Definimos jugador como matriz 8x8 de bits (1=encendido, 0=apagado)
    0b00111000,
    0b01111100,
    0b10101010,
    0b11111110,
    0b01111100,
    0b01000100,
    0b10000010,
    0b00000000
]

# ========== ESTADOS ==========
STATE_MENU = 0  # Estado menú
STATE_GAME = 1  # Estado juego
STATE_PAUSE = 2  # Estado pausa
STATE_GAME_OVER = 3  # Estado final
state = STATE_MENU  # Estado inicial

victory = False  # Variable para saber si ganó

# ========== VARIABLES ==========
modes = ["CLASICO", "TIEMPO", "HARDCORE"]  # Modos de juego
mode_index = 0  # Índice del modo actual

player_y = 20  # Posición vertical inicial del jugador
player_size = 8  # Tamaño del jugador
obstacles = []  # Lista de obstáculos
bullets = []  # Lista de disparos
score = 0  # Puntaje inicial
start_time = 0  # Tiempo de inicio
speed = 2  # Velocidad de obstáculos
spawn_rate = 1500  # Tiempo entre aparición de obstáculos
last_spawn = 0  # Último tiempo de spawn
last_shot = 0  # Último disparo

TIME_LIMIT = 60  # Tiempo límite en modo tiempo

buzzer_end_time = 0  # Tiempo en el que el buzzer debe apagarse
buzzer_active = False  # Estado del buzzer

# ========== SONIDO ==========
def buzzer_start(freq=1000, duration_ms=100):  # Función para activar sonido
    global buzzer_end_time, buzzer_active  # Variables globales
    buzzer.freq(freq)  # Frecuencia del sonido
    buzzer.duty(512)  # Encendemos buzzer (50%)
    buzzer_active = True  # Marcamos como activo
    buzzer_end_time = time.ticks_add(time.ticks_ms(), duration_ms)  # Calculamos cuándo debe apagarse

def buzzer_update():  # Función para apagar buzzer cuando se cumpla el tiempo
    global buzzer_active
    if buzzer_active and time.ticks_diff(time.ticks_ms(), buzzer_end_time) >= 0:  # Si ya pasó el tiempo
        buzzer.duty(0)  # Apagamos
        buzzer_active = False  # Marcamos como inactivo

# ========== RESET ==========
def reset_game():  # Reinicia el juego
    global player_y, obstacles, bullets, score, start_time, speed, spawn_rate, last_spawn, last_shot, victory
    player_y = 20  # Posición inicial
    obstacles = []  # Reiniciar obstáculos
    bullets = []  # Reiniciar disparos
    score = 0  # Puntaje en 0
    start_time = time.ticks_ms()  # Tiempo de inicio
    last_spawn = time.ticks_ms()  # Último spawn
    last_shot = time.ticks_ms()  # Último disparo
    victory = False  # No hay victoria

    if modes[mode_index] == "HARDCORE":  # Si es hardcore
        speed = 4  # Mayor velocidad
        spawn_rate = 700  # Obstáculos más rápidos
    else:
        speed = 2  # Velocidad normal
        spawn_rate = 1500  # Aparición normal

# ========== DIFICULTAD ==========
def update_difficulty(now):  # Aumenta dificultad con el tiempo
    global speed, spawn_rate
    elapsed = time.ticks_diff(now, start_time) // 1000  # Tiempo jugado en segundos

    if modes[mode_index] == "CLASICO":
        speed = min(2 + (elapsed // 10), 7)  # Aumenta velocidad gradualmente
        spawn_rate = max(400, 1500 - elapsed * 25)  # Reduce tiempo entre obstáculos

    elif modes[mode_index] == "TIEMPO":
        speed = min(2 + (elapsed // 8), 8)
        spawn_rate = max(350, 1500 - elapsed * 30)

    elif modes[mode_index] == "HARDCORE":
        speed = min(4 + (elapsed // 5), 10)
        spawn_rate = max(200, 700 - elapsed * 20)

# ========== OBSTÁCULOS ==========
def spawn_obstacle():  # Crear obstáculo
    y = random.randint(0, 56)  # Posición vertical
    size = random.randint(6, 10) if modes[mode_index] == "HARDCORE" else 6  # Tamaño variable en hardcore
    obstacles.append({"x": 128, "y": y, "w": size, "h": size})  # Se agrega a la lista

def update_obstacles():  # Movimiento de obstáculos
    global obstacles, score
    for obs in obstacles:
        obs["x"] -= speed  # Se mueven a la izquierda

    nuevos = []  # Nueva lista
    for obs in obstacles:
        if obs["x"] + obs["w"] > 0:  # Si sigue en pantalla
            nuevos.append(obs)
        else:
            score += 1  # Suma punto
            buzzer_start(800, 30)  # Sonido
    obstacles = nuevos  # Actualizamos lista

# ========== DISPAROS ==========
def shoot(now):  # Crear disparos
    global last_shot, bullets
    if modes[mode_index] != "HARDCORE":  # Solo en hardcore
        return
    if time.ticks_diff(now, last_shot) > 200:  # Control de tiempo entre disparos
        bullets.append({"x": 8, "y": player_y + 3})  # Crear bala
        last_shot = now  # Actualizar tiempo

def update_bullets():  # Movimiento de balas
    global bullets
    for b in bullets:
        b["x"] += 6  # Se mueven a la derecha
    bullets = [b for b in bullets if b["x"] < 128]  # Eliminar fuera de pantalla

def check_bullet_collisions():  # Colisiones bala-obstáculo
    global bullets, obstacles, score
    for b in bullets[:]:
        for o in obstacles[:]:
            if (o["x"] < b["x"] < o["x"] + o["w"] and
                o["y"] < b["y"] < o["y"] + o["h"]):
                obstacles.remove(o)  # Eliminar obstáculo
                bullets.remove(b)  # Eliminar bala
                score += 3  # Sumar puntos
                buzzer_start(1200, 50)  # Sonido
                break

# ========== COLISION ==========
def check_player_collision():  # Colisión jugador
    global state
    for o in obstacles:
        if (o["x"] < player_size and
            player_y < o["y"] + o["h"] and
            player_y + player_size > o["y"]):
            led.value(1)  # Encender LED
            buzzer_start(200, 300)  # Sonido
            state = STATE_GAME_OVER  # Fin del juego
            return True
    return False  # No colisión
# ========== DIBUJO ==========
def draw_player():  # Función para dibujar al jugador
    for y in range(8):  # Recorremos las 8 filas del sprite
        row = player_sprite[y]  # Tomamos una fila del sprite
        for x in range(8):  # Recorremos las 8 columnas
            if row & (1 << (7 - x)):  # Verificamos si el bit es 1 (pixel encendido)
                oled.pixel(x, player_y + y, 1)  # Dibujamos el pixel en pantalla

def draw_obstacles():  # Función para dibujar obstáculos
    for o in obstacles:  # Recorremos todos los obstáculos
        for x in range(o["w"]):  # Recorremos su ancho
            for y in range(o["h"]):  # Recorremos su altura
                oled.pixel(o["x"] + x, o["y"] + y, 1)  # Dibujamos cada pixel

def draw_bullets():  # Función para dibujar balas
    for b in bullets:  # Recorremos todas las balas
        oled.pixel(b["x"], b["y"], 1)  # Dibujamos cada bala como un pixel

def draw_hud(now):  # Función para mostrar información del juego
    oled.text("SCORE:{}".format(score), 0, 0)  # Mostramos el puntaje
    elapsed = time.ticks_diff(now, start_time) // 1000  # Tiempo transcurrido en segundos

    if modes[mode_index] == "TIEMPO":  # Si el modo es por tiempo
        remaining = max(0, TIME_LIMIT - elapsed)  # Calculamos tiempo restante (sin negativos)
        oled.text("TIME:{}s".format(remaining), 0, 10)  # Mostramos tiempo restante
    else:
        oled.text("TIME:{}s".format(elapsed), 0, 10)  # Mostramos tiempo transcurrido

# ========== MENU ==========
def menu():  # Función del menú principal
    global mode_index, state  # Variables globales
    oled.fill(0)  # Limpiamos pantalla
    oled.text("DODGER", 40, 5)  # Mostramos título

    for i, m in enumerate(modes):  # Recorremos los modos con índice
        oled.text((">" if i == mode_index else " ") + m, 20, 20 + i*10)  
        # Mostramos los modos, con ">" en el seleccionado

    oled.show()  # Actualizamos pantalla

    if is_pressed(btn_up):  # Si presiona botón arriba
        mode_index = (mode_index - 1) % len(modes)  # Cambia modo hacia arriba
        buzzer_start(1500, 50)  # Sonido

    if is_pressed(btn_down):  # Si presiona botón abajo
        mode_index = (mode_index + 1) % len(modes)  # Cambia modo hacia abajo
        buzzer_start(1500, 50)  # Sonido

    if is_pressed(btn_start):  # Si presiona iniciar
        buzzer_start(2000, 100)  # Sonido
        reset_game()  # Reinicia variables
        state = STATE_GAME  # Cambia a estado de juego

# ========== GAME ==========
def game():  # Función principal del juego
    global player_y, last_spawn, state, victory  # Variables globales

    oled.fill(0)  # Limpiamos pantalla

    if is_pressed(btn_up, hold=True):  # Si mantiene presionado subir
        player_y -= 3  # Subimos jugador

    if is_pressed(btn_down, hold=True):  # Si mantiene presionado bajar
        player_y += 3  # Bajamos jugador

    player_y = max(0, min(56, player_y))  # Limitamos movimiento dentro de pantalla
    now = time.ticks_ms()  # Tiempo actual

    update_difficulty(now)  # Ajustamos dificultad según tiempo

    if modes[mode_index] == "TIEMPO":  # Si modo tiempo
        if time.ticks_diff(now, start_time) // 1000 >= TIME_LIMIT:  # Si se acabó el tiempo
            victory = True  # Ganó
            led.value(1)  # Enciende LED
            state = STATE_GAME_OVER  # Fin del juego
            return  # Salimos de la función

    if time.ticks_diff(now, last_spawn) > spawn_rate:  # Si es momento de crear obstáculo
        spawn_obstacle()  # Creamos obstáculo
        last_spawn = now  # Guardamos tiempo

    if modes[mode_index] == "HARDCORE":  # Si modo hardcore
        shoot(now)  # Disparamos
        update_bullets()  # Movemos balas
        check_bullet_collisions()  # Verificamos colisiones

    update_obstacles()  # Movemos obstáculos

    if check_player_collision():  # Si colisiona jugador
        return  # Salimos

    draw_player()  # Dibujamos jugador
    draw_obstacles()  # Dibujamos obstáculos
    draw_bullets()  # Dibujamos balas
    draw_hud(now)  # Dibujamos información
    oled.show()  # Actualizamos pantalla

    if is_pressed(btn_start):  # Si presiona start
        state = STATE_PAUSE  # Pausa el juego

# ========== PAUSA ==========
def pause():  # Función de pausa
    global state  # Variable global
    oled.fill(0)  # Limpiamos pantalla
    oled.text("PAUSA", 40, 25)  # Mostramos texto
    oled.show()  # Actualizamos pantalla

    if is_pressed(btn_start):  # Si presiona start
        state = STATE_GAME  # Regresa al juego

# ========== GAME OVER ==========
def game_over():  # Función de fin del juego
    global state  # Variable global
    oled.fill(0)  # Limpiamos pantalla

    if victory:  # Si ganó
        oled.text("VICTORIA", 35, 20)  # Mostrar victoria
    else:
        oled.text("GAME OVER", 30, 20)  # Mostrar derrota

    oled.text("SCORE: {}".format(score), 35, 35)  # Mostrar puntaje
    oled.text("PRESS START", 30, 50)  # Indicar reinicio
    oled.show()  # Actualizar pantalla

    if not victory:  # Si perdió
        led.off()  # Apagar LED

    if is_pressed(btn_start):  # Si presiona start
        state = STATE_MENU  # Regresa al menú

# ========== LOOP ==========
while True:  # Bucle infinito
    buzzer_update()  # Actualizamos buzzer (para apagarlo si toca)

    if state == STATE_MENU:  # Si estamos en menú
        menu()  # Ejecutamos menú
    elif state == STATE_GAME:  # Si estamos jugando
        game()  # Ejecutamos juego
    elif state == STATE_PAUSE:  # Si está en pausa
        pause()  # Ejecutamos pausa
    elif state == STATE_GAME_OVER:  # Si terminó el juego
        game_over()  # Ejecutamos pantalla final
