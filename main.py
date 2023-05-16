#Importación de las librerías necesarias.
from fastapi import FastAPI
import pandas as pd
import uvicorn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Carga de datasets

movies_clean = pd.read_csv("datasets/movies_clean.csv")
data = pd.read_csv("datasets/movies_dataset.csv")

# API structure

app = FastAPI()

# Funcion 1
@app.get('/peliculas_mes/{mes}')
def peliculas_mes(mes:str):
    '''Ingrese un mes en texto y minúscula para poder ver el numero de películas que se estrenaron en ese mes'''
    mes = mes.lower()
    meses = {'enero': 1,'febrero': 2,'marzo': 3,'abril': 4,'mayo': 5,'junio': 6,'julio': 7,'agosto': 8,'septiembre': 9,'octubre': 10,'noviembre': 11,'diciembre': 12}
    mes_numero = meses[mes]

    # Convertir la columna "fecha" a un objeto de tipo fecha
    movies_clean['release_date'] = pd.to_datetime(movies_clean['release_date'])

    try:
        month_filtered = movies_clean[movies_clean['release_date'].dt.month == mes_numero]
    except (ValueError, KeyError, TypeError):
        return None

    month_unique = month_filtered.drop_duplicates(subset='id')
    respuesta = month_unique.shape[0]

    return {'mes':mes, 'cantidad':respuesta}

#funcion 2
@app.get('/peliculas_dia/{dia}')
def peliculas_dia(dia:str):
    '''Ingrese un día de la semana en texto para ver la cantidad de peliculas que se estrenaron ese dia historicamente'''
    days = {'lunes': 'Monday', 'martes': 'Tuesday','miercoles': 'Wednesday','jueves': 'Thursday','viernes': 'Friday','sabado': 'Saturday','domingo': 'Sunday'}
    day = days[dia.lower()]
    lista_peliculas_day = movies_clean[movies_clean['release_date'].dt.day_name() == day].drop_duplicates(subset='id')
    cantidad = lista_peliculas_day.shape[0]

    return {'dia': dia, 'cantidad': cantidad}

#funcion 3
@app.get('/franquicia/{franquicia}')
def franquicia(franquicia:str):
    '''Ingrese la franquicia, para ver la cantidad de peliculas, ganancia total y promedio'''
    movies_clean['belongs_to_collection']=movies_clean['belongs_to_collection'].fillna("")
    franquicia_df=movies_clean[movies_clean['belongs_to_collection'].apply (lambda x: franquicia in str(x))]
    #para calcular la cantidad de peliculas, ganancia totaly promedio
    cantidad_pelis = len(franquicia_df)
    revenue_franq = franquicia_df['revenue'].sum()
    promedio_franq = franquicia_df['revenue'].mean()
    return {'franquicia':franquicia, 'cantidad':cantidad_pelis, 'ganancia_total':revenue_franq, 'ganancia_promedio':promedio_franq}

#funcion 4
@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais:str):
    '''Ingrese el pais, para ver la cantidad de peliculas producidas en ese pais'''
    peliculas_pais = movies_clean[movies_clean['production_countries'].apply(lambda x: pais in str(x) if pd.notnull(x) else False)]
    
    # Elimina las filas duplicadas de la película para evitar contar varias veces una misma película.
    peliculas_pais = peliculas_pais.drop_duplicates(subset='id')
    
    # Cuenta la cantidad de películas restantes después de eliminar los duplicados.
    cantidad_peliculas = len(peliculas_pais)
    
    # Devuelve los resultados en un diccionario con claves legibles.
    return {'pais': pais, 'cantidad': cantidad_peliculas}

#funcion 5
@app.get('/productoras/{productora}')
def productoras(productora:str):
    '''Ingrese la productora, para visualizar la ganancia total y la cantidad de peliculas que produjeron'''
    movies_clean['production_companies']=movies_clean['production_companies'].fillna("")
    productora_df=movies_clean[movies_clean['production_companies'].apply(lambda x: productora in str(x))]

    ganancia_total= productora_df['revenue'].sum()
    cantidad_pelis_prod= len(productora_df)

    return {'productora':productora, 'ganancia_total':ganancia_total, 'cantidad':cantidad_pelis_prod}

#funcion 6
@app.get('/retorno/{pelicula}')
def retorno(pelicula:str):
    '''Ingrese la pelicula para poder ver la inversion, la ganancia, el retorno y el año en el que se lanzo'''
    info_pelicula = movies_clean[(movies_clean['title'] == pelicula)].drop_duplicates(subset='title')
    pelicula_nombre = info_pelicula['title'].iloc[0]
    inversion_pelicula = str(info_pelicula['budget'].iloc[0])
    ganancia_pelicula = str(info_pelicula['revenue'].iloc[0])
    retorno_pelicula = str(info_pelicula['return'].iloc[0])
    year_pelicula = str(info_pelicula['release_year'].iloc[0])

    return {'pelicula':pelicula_nombre, 'inversion':inversion_pelicula, 'ganacia':ganancia_pelicula,'retorno':retorno_pelicula, 'anio':year_pelicula}

#funcion 7

data = data.drop_duplicates(subset = 'title')
C = data['vote_average'].mean()
m = data['vote_count'].quantile(0.90)
data = data.loc[data['vote_count'] >= m]
def weighted_rating(x, m=m, C=C):
    v = x['vote_count']
    R = x['vote_average']
    # Calculation based on the IMDB formula
    return (v/(v+m) * R) + (m/(m+v) * C)
data['score'] = data.apply(weighted_rating, axis=1)
data = data.sort_values('score', ascending = False)
tfidf = TfidfVectorizer(stop_words='english')
data['overview'] = data['overview'].fillna('')
tfidf_matrix = tfidf.fit_transform(data['overview'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
data.reset_index(drop = True, inplace = True)
index = pd.Series(data.index, index = data['title']).drop_duplicates()

#para la recomendacion
@app.get('/recomendacion/{titulo}')
def recomendacion(titulo:str):
    '''Ingrese un nombre de pelicula y te recomiendaremos una lista de 5 películas similares'''
    local_cosine_sim = cosine_sim
    if titulo not in index:
        return "La película no se encuentra entre el 10% de las mejores películas. Intenta con una mejor!"

    idx = index[titulo]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    result = data['title'].iloc[movie_indices]
    return {"Lista que Recomendamos" : list(result)}