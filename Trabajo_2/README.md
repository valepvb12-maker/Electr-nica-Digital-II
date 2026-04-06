# Trabajo 2 - Grúa Robótica con ESP32

## Descripción
El proyecto consiste en el diseño e implementación de una grúa robótica de sobremesa con 2 grados de libertad (GDL), controlada mediante un microcontrolador ESP32.

El sistema permite el control manual mediante potenciómetros y cuenta con modos automáticos activados por interrupciones.

## Componentes del Sistema

### Entradas
- 2 Potenciómetros:
  - Control de rotación de la base
  - Control de elevación del brazo
- 2 Pulsadores:
  - Retorno a posición inicial
  - Secuencia automática

### Procesamiento
- Microcontrolador ESP32
- Conversión ADC:
  - Potenciómetro 1: 12 bits
  - Potenciómetro 2: 10 bits
- Generación de señal PWM para servomotores
- Manejo de interrupciones
- Uso de variables de estado (modo manual / automático)

### Salidas
- 2 Servomotores:
  - Servo 1: rotación de la base
  - Servo 2: movimiento del brazo
- LED verde: indica modo manual
- LED rojo: indica modo automático
- Buzzer: alerta durante el modo automático

## Funcionamiento del Sistema

### Modo Manual
Los potenciómetros controlan directamente el movimiento de los servos. El sistema convierte la señal analógica a valores PWM, permitiendo control en tiempo real. El LED verde permanece encendido.

### Modo Automático - Retorno
Se activa mediante un pulsador con interrupción. La grúa regresa automáticamente a su posición inicial. Durante este proceso se enciende el LED rojo y se activa el buzzer. Al finalizar, el sistema vuelve al modo manual.

### Modo Automático - Secuencia
Se ejecuta una rutina predefinida de movimientos. El sistema opera de forma automática y, al finalizar, retorna al modo manual.

## Código
El código del proyecto se encuentra en:
`/codigo/main.py`

Incluye lectura ADC, control PWM, manejo de interrupciones y lógica de estados.

## Evidencia
Las imágenes del montaje se encuentran en:
`/imagenes/`

## Documentación
El documento completo del proyecto está disponible en:
`documentacion.pdf`

## Resultados
Se implementó una grúa robótica funcional con control manual y automático, integrando sensores analógicos, actuadores y manejo de interrupciones en el ESP32.
