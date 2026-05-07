# Trabajo 4 - Juego Dodger con ESP32

## Descripción
En este trabajo hicimos un juego usando una ESP32, una pantalla OLED, botones, buzzer y un led.

La idea del juego es esquivar obstáculos moviendo el personaje hacia arriba y abajo. También agregamos diferentes modos de juego, sonidos y un sistema donde la dificultad aumenta mientras pasa el tiempo.

---

# Componentes del sistema

## Entradas
- Botón subir
- Botón bajar
- Botón start

## Procesamiento
- ESP32
- Manejo de estados
- Movimiento del jugador
- Generación de obstáculos
- Sistema de disparos
- Detección de colisiones
- Control de dificultad

## Salidas
- Pantalla OLED SSD1306
- Buzzer
- Led indicador

---

# Funcionamiento del juego

## Menú
Cuando el juego inicia aparece un menú donde se puede escoger el modo de juego usando los botones.

## Movimiento
El jugador puede moverse verticalmente para esquivar los obstáculos.

## Obstáculos
Los obstáculos aparecen aleatoriamente y se mueven hacia la izquierda de la pantalla.

## Modos de juego
El juego tiene tres modos:
- Clásico
- Tiempo
- Hardcore

Cada modo cambia la dificultad y velocidad del juego.

## Disparos
En el modo hardcore se pueden lanzar disparos para destruir obstáculos.

## Colisiones
Si el jugador toca un obstáculo, el juego termina.

## Sonido
El buzzer se usa para dar sonidos cuando pasan acciones dentro del juego.

---

# Código
El código principal del proyecto se encuentra en:

`main.py`

Incluye:
- control de botones
- lógica del juego
- obstáculos
- disparos
- colisiones
- dibujo en pantalla
- sonidos

---

# Evidencia
Las imágenes y videos del funcionamiento del proyecto se encuentran en la carpeta correspondiente.

---

# Documentación
La documentación completa del proyecto se encuentra en:

`DOCUMENTACION.pdf`

---

# Resultados
Se logró hacer un juego funcional usando la ESP32 y la pantalla OLED.

El juego responde en tiempo real, tiene diferentes modos, sonidos, obstáculos y aumento progresivo de dificultad.
