# Proyecto individual N°1 - Machine Learning Operations (MLOps)
## Introducción
En este proyecto se busca desarrollar un Producto Mínimo Viable (MVP) junto a una API que sea desplegada en algún servicio en la nube y a su vez implementar un modelo de Machine Learning.
Para esto, son proporcionados dos data sets fundamentales para el proyecto, los cuales incluyen breve información financiera de las películas, especificaciones de las mismas, información de los actores y de los miembros del creadores de la película

La primera consideración para el MVP es el desarrollo y aplicación de las 6 funciones que retornen información relevante sobre los datos pasados como parámetros y así tener respuestas a las preguntas proporcionadas.

Las funciones en este caso buscan obtener la cantidad de filmaciones al mes, la cantidad de filmaciones al día, el puntaje de la película, los votos de la película, obtener las participaciones de algun actor y sus ganancias por película, obtener el éxito medido por el retorno obtenido por una película de segun su director. por ultimo, lo más importante es desarrollar un modelo de aprendizaje automática el cual proporcionará recomendaciones para los usuarios permitiendo a los usuarios tomar decisiones basadas en las que ésta entregue.

En resumen, este proyecto conlleva a una buena manera de que los usuarios puedan tener recomendaciones a partir de sus películas favoritas y poder adentrarse en películas similares.

## Contexto
Esta start-up se dedica a la agregación de plataformas de streaming, ofreciendo a los usuarios una experiencia unificada para acceder a un amplio catálogo de películas y series. Con el crecimiento constante del catálogo, se vuelve esencial personalizar las recomendaciones para mejorar la satisfacción del usuario. Este proyecto se enfoca en desarrollar un sistema de recomendación de películas desde cero, abordando el desafío de datos en bruto y sin procesar para crear un MVP (Producto Mínimo Viable) efectivo y rápido.

## Datasets
El proyecto esta basado en dos datasets:
1. movies_dataset: información relacionada a los juegos que se encuentran dentro de la plataforma. por ejemplo: generos, titulo, fecha de lanzamiento, etc.
2. credits: información detallada de todos los miembros de reparto de las peliculas. por ejemplo: nombre de los artistas, nombre de los miembros del reparto, trabajo de cada miembro, etc.
Los detalles de los datasets se encuentra en el siguiente enlace: [Datasets](Diccionario de Datos - PIMLOps.xlsx)
## Desarrollo
El detalle del proyecto se puede obtener del siguiente enlace: [Repositorio](Desarrollo.ipynb)
En este apartado se tendrá de forma breve una explicación paso a paso del proyecto

### 1. Ingesta de datos:
Se inicia el proyecto cargando los datasets para poder trabajarlos

### 2. Tratamiento de datos - ETL
Al tener cargado los datos, es necesario que los limpiemos y transformemos para que sean útiles. el proceso implica transformar los datos buscando la coherencia de los mismos y poder lograr cumplir con el objetivo sin presentar inconsistencias.

### 3. Desarrollo de funciones y disponibilización de datos
Una de las partes más importantes del proyecto es crear las funciones, las cuales se encuentran detalladas a continuación:
- cantidad_filmaciones_mes( Mes ): Se ingresa un mes en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas en el mes consultado en la totalidad del dataset.
  
- cantidad_filmaciones_dia( Dia ): Se ingresa un día en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas en día consultado en la totalidad del dataset.
  
- score_titulo( titulo_de_la_filmación ): Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score.
  
- votos_titulo( titulo_de_la_filmación ): Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones. La misma variable deberá de contar con al menos 2000 valoraciones, caso contrario, debemos contar con un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningun valor.
  
- get_actor( nombre_actor ): Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, la cantidad de películas que en las que ha participado y el promedio de retorno. La definición no deberá considerar directores.
  
- get_director( nombre_director ): Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.

Estas funciones mencionadas deben poder ser consumidas de forma local y desde un servidor web. por lo cual se utilizó framework FastAPI y el servidor web Render.
El desarrollo de las funciones y la utilización del framework se puede ver en el siguiente archivo: [FastAPI](main.py)

### 4. Análisis exploratorio de datos - EDA
En este paso se busca realizar el análisis exploratorio de los datos presentes en el archivo como la base para la creación del modelo de recomendación para proseguir con la finalización del proyecto

### 5. Modelamiento (Machine Learning Model Development)
Aquí, se desarrolla el modelo de ML en la cual se utilizan los datos preparados anteriormente. dado a que se solicitaba la recomendación de películas se utiliza el data set movies_dataset. esto incluye la creación de la función, el modelo y la adaptación de los datos para que la función pudiese retornar el valor esperado.

La función a crear corresponde a la siguiente:
- recomendacion( titulo ): Se ingresa el nombre de una película y te recomienda las similares en una lista de 5 valores.

Este punto, al igual que los anteriores se encuentran en la fastAPI y deployados en Render.

### Deployment


