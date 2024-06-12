# Sistema de Recomendación con Aprendizaje por Refuerzo Integrando Ratings

## 1. Introducción
Los sistemas de recomendación son fundamentales en plataformas de streaming de contenido, comercio electrónico, redes sociales, etc. Mejorar la personalización y la precisión de las recomendaciones es crucial para aumentar la satisfacción del usuario y la retención en la plataforma.

Este proyecto propone implementar un sistema de recomendación utilizando técnicas de aprendizaje por refuerzo (RL) que integre datos reales de los usuarios y calificaciones del contenido (1 a 5 estrellas). Para ello, se usará parte de la data de Netflix Prize disponible en [kaggle](https://www.kaggle.com/datasets/netflix-inc/netflix-prize-data), filtrando desde 1 hasta el id_customer 100,000. El objetivo del modelo es generar sugerencias del siguiente contenido a ver, dada la puntuación media de usuarios a los contenidos vistos el mismo día que el contenido actual.

## 2. Planteamiento del Problema
El reto es desarrollar un sistema de recomendación que pueda adaptarse dinámicamente a las preferencias cambiantes de los usuarios y, a la vez, reconciliar diferentes tipos de retroalimentación que pueden ser contradictorios. La solución debe aprender de la interacción continua con los usuarios para mejorar la relevancia de las recomendaciones ofrecidas.

## 3. Objetivos
- **Maximizar la relevancia de las recomendaciones**: Ajustar las sugerencias para alinearlas con las preferencias explícitas e implícitas de los usuarios.
- **Incrementar la interacción del usuario**: Aumentar las interacciones de los usuarios con las recomendaciones a través de feedback positivo.
- **Mejorar la precisión de la predicción**: Reducir los casos de recomendaciones no relevantes ajustando continuamente el modelo a través del aprendizaje por refuerzo.

## 4. Métricas de Éxito
Podrían utilizarse métricas tales como tasa de clicks, tasa de Likes vs. Dislikes, y feedback de los usuarios para medir la eficacia del sistema. Sin embargo, esto se considera como una fase que está fuera del alcance de este proyecto, y por lo tanto no será incluido.

## 5. Diseño de la Solución

### Ambiente
El ambiente simula la interacción en una plataforma donde cada usuario interactúa con el sistema de recomendación. Los estados son definidos por el historial de interacción de los usuarios, con el cual se pasa de un contenido a otro con determinada probabilidad, siendo esta la probabilidad de recomendarlo.

### Estados
Cada estado estará determinado por el contenido dentro de la base de datos, con la restricción de no recomendar el mismo contenido que se vio previamente. El agente tiene como objetivo recomendar la mayor cantidad de contenidos recibiendo refuerzos positivos, evitando el estado terminal de recomendar un contenido con puntuación media inferior a 3 estrellas.

### Acciones
El agente puede recomendar cualquier contenido que el usuario no haya visto todavía. La decisión se basa en la política aprendida, que busca maximizar las recompensas futuras según las interacciones previas.

### Recompensas
La función de recompensa integra ratings dados como 1 a 5 estrellas, escalando esta variable de la siguiente manera:
- 1 si el rating medio es 5 estrellas (máximo refuerzo positivo).
- 0 si es 3 estrellas.
- -1 si es 1 estrella (máximo refuerzo negativo).

### Agente de Aprendizaje
Utilizamos Q-learning con una tabla de valores Q para cada acción posible (estar en un contenido x1 y pasar a un contenido x2). El agente aprende de las recompensas recibidas para actualizar sus predicciones sobre qué acciones maximizarán las recompensas futuras dado el estado actual.

## 6. Implementación
La implementación se realiza en Python utilizando bibliotecas como NumPy para las operaciones matemáticas y Pandas para la manipulación de datos. El sistema se prueba inicialmente con una muestra de los datos.

Tras la ejecución de 2000 episodios y la siguiente configuración de parámetros, le toma 9 minutos y 46 segundos ejecutar el entrenamiento en un PC con Windows 10, procesador Ryzen 7 y 16 GB de RAM.

## Instalación
1. Clonar el repositorio:
    ```bash
    git clone https://github.com/usuario/RL--Agente_recomendador_de_contenido.git
    cd RL--Agente_recomendador_de_contenido
    ```

2. Instalar las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

3. Ejecutar los notebooks de Jupyter:
    ```bash
    jupyter notebook
    ```

## Autores
Andrés Forero, Edwin López.
---
