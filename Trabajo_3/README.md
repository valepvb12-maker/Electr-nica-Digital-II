Trabajo 3 - Sistema avanzado de medición de reflejos con ESP32

Descripción
El proyecto consiste en el diseño e implementación de un sistema de adquisición de señal biomédica en tiempo real utilizando un microcontrolador ESP32.

El sistema captura una señal analógica proveniente de un sensor ECG, la digitaliza mediante el ADC interno y aplica técnicas de filtrado digital para mejorar la calidad de la señal. Además, permite visualizar la señal en tiempo real y almacenarla para su posterior análisis.

Componentes del Sistema

Entradas
Sensor biomédico ECG (AD8232)
Electrodos

Procesamiento
Microcontrolador ESP32
Conversión ADC a 12 bits
Frecuencia de muestreo de 200 Hz
Implementación de filtros digitales:

* Promedio móvil
* Mediana
* Exponencial (IIR)
  Activación y desactivación de filtros
  Procesamiento de señal en tiempo real

Salidas
Señal visualizada en Serial Plotter
Archivo .txt con los datos adquiridos
Detección de latidos mediante umbral (threshold)

Funcionamiento del Sistema

Adquisición de señal
El sistema lee la señal analógica del sensor ECG a través del ADC del ESP32, convirtiéndola en valores digitales entre 0 y 4095.

Filtrado de señal
La señal adquirida se procesa mediante filtros digitales (promedio, mediana y exponencial), los cuales pueden activarse individualmente o en cascada para mejorar la calidad de la señal y reducir el ruido.

Visualización
Los datos se envían al Serial Plotter, permitiendo observar la señal en tiempo real.

Almacenamiento
Los valores de la señal filtrada se almacenan en un archivo de texto (.txt) en la memoria del ESP32.

Detección de latidos
Se implementa un sistema de detección basado en un umbral (threshold), el cual permite identificar los picos de la señal asociados a los latidos del corazón, evitando múltiples detecciones mediante control de estado.

Código
El código del proyecto se encuentra en: main.py

Incluye lectura ADC, aplicación de filtros digitales, control de muestreo y detección de latidos.

Evidencia
Las imágenes del montaje se encuentran en la carpeta: imagenes

Documentación
El documento completo del proyecto está disponible en: DOCUMENTACION.pdf

Resultados
Se logró adquirir y procesar una señal ECG en tiempo real, mejorando su calidad mediante filtrado digital y permitiendo la detección de latidos, así como el almacenamiento de los datos para análisis posterior.

