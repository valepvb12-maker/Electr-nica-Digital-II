Trabajo 4 - Juego Dodger con ESP32
Descripción

Este proyecto consiste en un juego hecho con ESP32, una pantalla OLED, botones, buzzer y un led.

El objetivo del juego es esquivar obstáculos que aparecen en la pantalla mientras el jugador se mueve hacia arriba y abajo. Además, el juego tiene diferentes modos y la dificultad aumenta mientras pasa el tiempo.

Componentes del Sistema
Entradas
Botón subir
Botón bajar
Botón start
Procesamiento
ESP32
Manejo de estados
Generación de obstáculos
Sistema de disparos
Detección de colisiones
Control de dificultad
Salidas
Pantalla OLED SSD1306
Buzzer
LED
Funcionamiento del Sistema
Menú

Al iniciar, aparece un menú para seleccionar el modo de juego.

Movimiento

El jugador puede moverse verticalmente usando los botones.

Obstáculos

Los obstáculos aparecen aleatoriamente y se mueven hacia la izquierda.

Modos de juego

El juego cuenta con:

Clásico
Tiempo
Hardcore
Disparos

En modo hardcore el jugador puede disparar obstáculos.

Colisiones

Si el jugador choca con un obstáculo, la partida termina.

Sonido

El buzzer genera sonidos en diferentes acciones del juego.

Código

El código principal se encuentra en:

main.py

Incluye:

control de botones
lógica del juego
obstáculos
disparos
colisiones
dibujo en pantalla
sonidos
Evidencia

Las imágenes y videos del funcionamiento se encuentran en la carpeta del proyecto.

Documentación

La documentación completa del proyecto se encuentra en:

DOCUMENTACION.pdf

Resultados

Se logró desarrollar un juego funcional en ESP32 con diferentes modos, sonidos, obstáculos y aumento progresivo de dificultad.
