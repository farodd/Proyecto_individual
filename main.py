"""
FUNCIONES API'S
"""

#importamos librerias a usar
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


#instanciamos la aplicación
app = FastAPI()


# definimos funciones de carga de dataframes
def cargar_df_f1():
    df_f1 =pd.read_parquet('Datasets/df_f1.parquet')
    return df_f1

def cargar_df_f2():
    df_f2 =pd.read_parquet('Datasets/df_f2.parquet')
    return df_f2

def cargar_df_f3():
    df_f3 =pd.read_parquet('Datasets/df_f3.parquet')
    return df_f3

def cargar_df_f4():
    df_f4 =pd.read_parquet('Datasets/df_f4.parquet')
    return df_f4

def cargar_df_f5():
    df_f5 = pd.read_parquet('Datasets/df_f5.parquet')
    return df_f5

def cargar_df_f6():
    df_f6 = pd.read_parquet('Datasets/df_f6.parquet')
    return df_f6

def cargar_df_modelo():
    df_modelo_final = pd.read_parquet('Datasets/df_modelo_final.parquet')
    return df_modelo_final

# HTML de la página de presentación
pagina_presentacion = """
<!DOCTYPE html>
<html>
<head>
    <title>Mi Página Web en FastAPI</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 5px;
        }
        h1 {
            color: #333;
        }
        p {
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Bienvenido a mi entorno FastAPI</h1>
        <p>Podrán ver la API al agregar "/docs" al final de la URL.</p>
        <div>
    </div>
</body>
</html>
"""

# MOSTRAMOS LA PRESENTACIÓN
@app.get("/", response_class=HTMLResponse)
async def mostrar_pagina_presentacion():
    return pagina_presentacion

#FUNCION 1
def cantidad_filmaciones_mes(mes):
    df_f1 = cargar_df_f1()
    #Mapeo de nombre de meses en español a números de mes
    meses= {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    #Obtener el número del mes a partir del nombre del mes en español
    mes_numero = meses.get(mes.lower())
    if mes_numero is None:
        return "Mes inválido"

    #Filtrar las peliculas por el mes solicitado
    peliculas_mes = df_f1[df_f1['release_date'].dt.month == mes_numero]

    #Contar la cantidad de películas
    cantidad_películas = peliculas_mes.shape[0]

    return f"{cantidad_películas} cantidad de peliculas fueronfueron estrenadas el mes de {mes.capitalize()}"

#FUNCION 2
def cantidad_filmaciones_dia(Dia):
    df_f2 = cargar_df_f2()
    # Días de la semana en español y su correspondencia con strftime('%A')
    dias_semana = {
        'lunes': 'Monday',
        'martes': 'Tuesday',
        'miercoles': 'Wednesday',
        'jueves': 'Thursday',
        'viernes': 'Friday',
        'sabado': 'Saturday',
        'domingo': 'Sunday'
    }
    
    # Convertir el día en español a su nombre correspondiente en inglés
    dia_ingles = dias_semana.get(Dia.lower(), None)
    
    if dia_ingles:
        # Filtrar las películas que se estrenaron en el día especificado
        peliculas_dia = df_f2[df_f2['release_date'].apply(lambda x: pd.to_datetime(x).strftime('%A')) == dia_ingles]
        
        # Contar la cantidad de películas
        cantidad = len(peliculas_dia)
        
        # Mensaje de retorno
        return f"{cantidad} cantidad de películas fueron estrenadas en los días {Dia.capitalize()}"
    else:
        return f"No se encontró el día '{Dia}' en el dataset."

#FUNCION 3

def score_titulo(titulo_de_la_filmacion):
    df_f3 = cargar_df_f3()
    # Convertir el título ingresado a minúsculas
    titulo_de_la_filmacion = titulo_de_la_filmacion.strip().lower()
    
    # Convertir los títulos en el DataFrame a minúsculas
    df_f3.loc[:, 'title'] = df_f3['title'].str.strip().str.lower()
    
    # Buscar la película por título (en minúsculas)
    pelicula = df_f3[df_f3['title'] == titulo_de_la_filmacion]
    
    # Verificar si se encontró la película
    if len(pelicula) == 0:
        return f"No se encontró la película '{titulo_de_la_filmacion}' en la base de datos."
    
    # Obtener información de la película
    titulo = pelicula['title'].values[0]
    año_estreno = pelicula['release_year'].values[0]
    score = pelicula['vote_average'].values[0]
    
    # Construir el mensaje de retorno
    mensaje = f"La película '{titulo}' fue estrenada en el año {año_estreno} con un score/popularidad de {score}."
    
    return mensaje

# FUNCION 4

def votos_titulo(titulo_de_la_filmacion):
    df_f4 = cargar_df_f4()
    # Normalizar el título de la filmación: quitar espacios y convertir a minúsculas
    titulo_normalizado = titulo_de_la_filmacion.strip().lower()

    # Filtrar el DataFrame para encontrar el título, ignorando mayúsculas, minúsculas y espacios
    filmacion = df_f4[df_f4['title'].str.strip().str.lower() == titulo_normalizado]

    if not filmacion.empty:
        # Obtener los valores de 'vote_count' y 'vote_average'
        vote_count = filmacion['vote_count'].values[0]
        vote_average = filmacion['vote_average'].values[0]
        title = filmacion['title'].values[0]
        release_year = filmacion['release_year'].values[0]
        
        # Verificar si tiene al menos 2000 valoraciones
        if vote_count >= 2000:
            return f"La película {title} fue estrenada en el año {release_year}. La misma cuenta con un total de {vote_count} valoraciones, con un promedio de {vote_average}."
        else:
            return "La filmación no cumple con el requisito de tener al menos 2000 valoraciones, no se devuelve ningún valor."
    else:
        return "No se encontró ninguna filmación con el título proporcionado."


# FUNCION 5
def get_actor(nombre_actor):
    df_f5 = cargar_df_f5()
    #Normalizar el nombre del actor (convertir a minúsculas y eliminar espacios
    nombre_actor = nombre_actor.replace(" ", "").lower()
    cantidad_peliculas = 0
    retorno_total = 0.0
    
    # Recorrer el DataFrame para buscar al actor y calcular retorno total y cantidad de películas
    for index, row in df_f5.iterrows():
        #Normalizar el nombre del actor en caada fila del DataFrame
        actor_en_registro = row['actor_name'].replace(" ", "").lower()

        #comparar nombre normalizados
        if actor_en_registro== nombre_actor:
            retorno_total += row['return']
            cantidad_peliculas += 1
    
    # Calcular el promedio de retorno
    if cantidad_peliculas > 0:
        promedio_retorno = round(retorno_total / cantidad_peliculas, 2)
    else:
        promedio_retorno = 0.0
    
    # Generar el mensaje de retorno
    mensaje = f"El actor {nombre_actor} ha participado en {cantidad_peliculas} filmaciones, ha conseguido un retorno de {round(retorno_total, 2)} con un promedio de {promedio_retorno} por filmación."
    
    return mensaje


#FUNCION 6

def get_director(nombre_director):
    df_f6 = cargar_df_f6()
    nombre_director = ''.join(nombre_director.lower().split())
    # Filtrar por el nombre del director y el trabajo específico (suponemos 'Director')
    director_data = df_f6[(df_f6['member_name'].str.lower().str.replace( ' ', '') == nombre_director) & (df_f6['job'] == 'Director')]

    if director_data.empty:
        return f"No se encontraron datos para el director {nombre_director}"

    # Preparar los datos para devolver
    director_info = []
    for index, row in director_data.iterrows():
        info_pelicula = {
            'Película': row['title'],
            'Fecha de lanzamiento': (pd.to_datetime(row['release_date']).date()).strftime('%Y-%m-%d'),
            'Retorno': round(row['return'],4),
            'Costo': row['budget'],
            'Ganancia': row['revenue']
        }
        director_info.append(info_pelicula)

    return director_info

#FUNCION 7

def recomendacion(titulo):
    df_modelo_final = cargar_df_modelo()
    titulo = titulo.replace(" ", "").lower()
    
    titulo = titulo.replace(" ", "").lower()
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df_modelo_final['title'].values.astype('U'))
    similitudes = cosine_similarity(tfidf_matrix)
    # Filter the input movie by its title
    selected_movie = df_modelo_final[df_modelo_final['title'].str.replace(" ", "").str.lower() == titulo]
    
    if selected_movie.empty:
        return ["Movie with the specified title does not exist in the database."]

        # Get similarity scores of the input movie with all movies
    similarity_scores = similitudes[selected_movie.index[0]]
    
    # Get indices of top 5 most similar movies (excluding the input movie)
    similar_movie_indices = similarity_scores.argsort()[::-1][1:6]
    
    # Get titles of recommended movies
    recommended_movies = df_modelo_final.iloc[similar_movie_indices]['title'].unique().tolist()
    
    recommended_movies = [movie for movie in recommended_movies if movie.replace(" ", "").lower() != titulo]

        # Ensure we have exactly 5 recommendations
    if len(recommended_movies) < 5:
        additional_movies = df_modelo_final[~df_modelo_final['title'].str.replace(" ", "").str.lower().isin([titulo] + recommended_movies)]
        recommended_movies += additional_movies['title'].unique().tolist()[:5 - len(recommended_movies)]
    return recommended_movies
    

#LAS SIGUIENTES FUNCIONES SON CON EL FIN DE PODER SABER QUE ERRORES SON LOS QUE SE ESTÁN GENERÁNDO
#RUTA FUNCION 1

@app.get("/peliculas_por_mes/{mes}", response_model=dict)
async def contar_movies_por_mes(mes:str):
    try:
        result = cantidad_filmaciones_mes(mes)

        return JSONResponse(content=jsonable_encoder(result), media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer al archivo Parquet: {str(e)}")
    
#RUTA FUNCION 2

@app.get("/Peliculas_por_día/{dia}", response_model=dict)
async def contar_peliculas_por_dia(dia:str):
    try:
        result = cantidad_filmaciones_dia(dia)

        return JSONResponse(content=jsonable_encoder(result), media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer al archivo Parquet: {str(e)}")
    
#RUTA FUNCION 3

@app.get("/Score_de_titulo/{titulo_de_la_filmacion}", response_model=dict)
async def score_por_titulo(titulo_de_la_filmacion:str):
    try:
        result = score_titulo(titulo_de_la_filmacion)

        return JSONResponse(content=jsonable_encoder(result), media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer al archivo Parquet: {str(e)}")
    
#RUTA FUNCION 4

@app.get("/votos_title/{titulo_de_la_filmacion}", response_model=dict)
async def votes_title(titulo_de_la_filmacion:str):
    try:
        result = votos_titulo(titulo_de_la_filmacion)

        return JSONResponse(content=jsonable_encoder(result), media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer al archivo Parquet: {str(e)}")

#RUTA FUNCION 5    

@app.get("/Info_actor/{nombre_actor}", response_model=dict)
async def Obtener_actor(nombre_actor:str):
    try:
        result = get_actor(nombre_actor)

        return JSONResponse(content=jsonable_encoder(result), media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer al archivo Parquet: {str(e)}")
    
#RUTA FUNCION 6

@app.get("/info_director/{nombre_director}", response_model=dict)
async def Obtener_director(nombre_director:str):
    try:
        result = get_director(nombre_director)

        return JSONResponse(content=jsonable_encoder(result), media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer al archivo Parquet: {str(e)}")
    
#RUTA FUNCION 7

@app.get("/Recomendación_película/{titulo}", response_model=dict)
async def Obtener_recomendacion(titulo:str):
    try:
        result = recomendacion(titulo)

        return JSONResponse(content=jsonable_encoder(result), media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta ;)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer al archivo Parquet: {str(e)}")
