# Cuna Multifuncional Inteligente con ESP32

## Descripción

En este proyecto se desarrolló una Cuna Multifuncional Inteligente utilizando un ESP32, sensores y actuadores para monitorear las condiciones ambientales y el estado del bebé en tiempo real.

El sistema permite supervisar temperatura, humedad, iluminación, presencia del bebé y movimiento de la cuna. Además, cuenta con sistemas automáticos de alerta, enfriamiento y balanceo para mejorar la seguridad y el confort del bebé.

---

## Componentes del Sistema

### Entradas

* Sensor DHT11 (temperatura y humedad)
* Sensor de luz
* Sensor MPU6050 (aceleración y movimiento)
* Botón de presencia del bebé

### Procesamiento

* ESP32
* Lectura de sensores
* Detección de movimiento
* Verificación de temperatura y humedad
* Monitoreo de iluminación
* Gestión de alarmas
* Control automático de actuadores

### Salidas

* Ventilador
* Módulo Peltier
* Servo motor
* LED verde
* LED rojo
* Buzzer

---

## Funcionamiento del Sistema

### Presencia del Bebé

El sistema verifica continuamente si hay un bebé en la cuna mediante un botón de presencia.

Cuando no se detecta presencia:

* Se apagan todos los actuadores.
* El sistema entra en modo de espera.

Cuando se detecta presencia:

* Se inicia el monitoreo completo de todos los sensores.

---

### Temperatura y Humedad

El sensor DHT11 realiza mediciones constantes de temperatura y humedad.

Si la temperatura supera el límite establecido:

* Se activa el ventilador.
* Se activa el módulo Peltier.
* Se genera una condición de alarma.

Si la humedad se encuentra fuera del rango permitido:

* Se genera una alerta para informar una condición ambiental inadecuada.

---

### Iluminación

El sensor de luz monitorea las condiciones de iluminación del entorno.

El sistema puede identificar:

* Ambiente iluminado.
* Ambiente oscuro.

Esta información puede utilizarse para supervisar las condiciones de descanso del bebé.

---

### Movimiento

El sensor MPU6050 mide continuamente la aceleración de la cuna.

El sistema puede identificar:

* Reposo normal.
* Movimiento moderado.
* Movimiento brusco.

Cuando se detecta movimiento superior al umbral establecido:

* Se genera una alarma.
* El servo motor realiza un movimiento de balanceo.

---

## Sistema de Alarmas

Las alarmas pueden generarse por:

* Temperatura alta.
* Humedad fuera de rango.
* Movimiento detectado.
* Combinación de múltiples condiciones.

Cuando ocurre una alarma:

* Se enciende el LED rojo.
* Se activa el buzzer.
* Se registra la causa de la alarma.

---

## Indicadores Visuales

### LED Verde

Indica que todas las condiciones del sistema son normales.

### LED Rojo

Indica que existe una condición de alarma o advertencia.

---

## Actuadores

### Ventilador

Permite mejorar la ventilación cuando la temperatura aumenta.

### Módulo Peltier

Ayuda a disminuir la temperatura dentro de la cuna.

### Servo Motor

Realiza movimientos de balanceo cuando se detecta movimiento mediante el MPU6050.

### Buzzer

Genera alertas sonoras cuando se presentan condiciones anormales.

---

## Código

El código principal del proyecto se encuentra en:

```text
main.py
```

Incluye:

* Lectura de sensores.
* Detección de presencia.
* Monitoreo ambiental.
* Detección de movimiento.
* Control de ventilador.
* Control de módulo Peltier.
* Control de servo motor.
* Sistema de alarmas.
* Gestión de LEDs indicadores.

---

## Evidencias

Las imágenes, videos y pruebas de funcionamiento se encuentran en la carpeta correspondiente del repositorio.

---

## Documentación

La documentación técnica completa del proyecto incluye:

* Diagrama de bloques.
* Lista de materiales.
* Código comentado.
* Manual de usuario.
* Evidencias de funcionamiento.

---

## Resultados

Se logró desarrollar una Cuna Multifuncional Inteligente funcional basada en ESP32.

El sistema permite monitorear variables ambientales y de movimiento en tiempo real, generar alertas automáticas y activar actuadores que contribuyen a mantener condiciones adecuadas para la seguridad y el bienestar del bebé.

Además, el proyecto demuestra la integración de sensores, actuadores y sistemas embebidos para aplicaciones de monitoreo y asistencia en entornos infantiles.
