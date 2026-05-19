# Trabajo 5 - Sistema de Monitoreo Biomédico con ESP32

## Descripción

En este trabajo realizamos un sistema de monitoreo biomédico utilizando un ESP32, sensores y Telegram.

El sistema permite medir temperatura, humedad y movimiento en tiempo real. Además, cuenta con alertas sonoras, botón de pánico, servidor web y notificaciones automáticas mediante Telegram.

---

## Componentes del sistema

### Entradas

- Sensor DHT22
- Sensor MPU6050
- Botón de pánico

### Procesamiento

- ESP32
- Lectura de sensores
- Detección de movimiento
- Verificación de alertas
- Comunicación WiFi
- Comunicación con Telegram
- Generación de página web

### Salidas

- Página web
- Alertas en Telegram
- Buzzer
- Estados de alarma

---

## Funcionamiento del sistema

### Temperatura y humedad

El sensor DHT22 mide temperatura y humedad constantemente.

Si los valores salen de los límites establecidos, se genera una alerta.

### Movimiento

El MPU6050 detecta aceleración y movimiento.

El sistema puede identificar:

- Reposo
- Movimiento detectado
- Movimiento brusco

### Botón de pánico

Cuando el botón es presionado:

- Se activa una alarma
- Suena el buzzer
- Se envía un mensaje a Telegram

### Alertas

Las alertas pueden ser:

- Temperatura
- Humedad
- Combinada
- Movimiento
- Movimiento brusco
- Botón de pánico

### Telegram

El sistema puede:

- Enviar alertas automáticas
- Responder comandos como:

/temp  
/hum  
/mov  
/umbrales

### Página web

El ESP32 crea un servidor web donde se muestran:

- Temperatura
- Humedad
- Estado del movimiento
- Estado de alarma
- Umbrales configurados

---

## Código

El código principal del proyecto se encuentra en:

main.py

Incluye:

- conexión WiFi
- comunicación Telegram
- lectura de sensores
- manejo de alertas
- servidor web
- control del buzzer
- botón de pánico

---

## Evidencia

Las imágenes y videos del funcionamiento del sistema se encuentran en la carpeta correspondiente.

---

## Documentación

La documentación completa del proyecto se encuentra en:

DOCUMENTACION.pdf

---

## Resultados

Se logró desarrollar un sistema de monitoreo biomédico funcional utilizando ESP32.

El sistema permite supervisar variables en tiempo real, generar alertas automáticas, visualizar datos desde una página web y comunicarse mediante Telegram.
