# PI-MLOps-Ernesto
PROYECTO INDIVIDUAL Nº1 -Machine Learning Operations (MLOps)

## Contenido

- [Contexto](#contexto)
- [Rol a desarrollar](#rol-a-desarrollar)
- [Trabajo Realizado](#trabajo-realizado)

## Características

Para este proyecto se nos proporcionó un dataset donde deberiamos hacer un trabajo situándose en el rol de un MLOps Engineer, esto como parte del módulo de proyectos prácticos individuales que se tiene planificado dentro del BootCamp Henry

## Rol a desarrollar
Para este proyecto tendremos que trabajar como **`Data Scientist`** para una start-up que provee servicios de agregación de plataformas de streaming. Para el cual tienes que crear tu primer Modelo de Machine Learning que brindará un sistema de recomendación, ya que la empresa aun no brinda esta opcion dentro del negocio.

Nos brindaron un dataset [movies_dataset](https://github.com/CARRILLOJARA96/PI-MLOps-Ernesto/tree/main/datasets) el cual está sin trabajar por lo que requiere muchas transformaciones durante el **`ETL`** y **`EDA`**.

Tambien Realizar algunas funciones de consulta dentro **`Modelo ML`**, **`Desarrollo del API`**


## Trabajo Realizado

#### ETL

Inicialmente se hizo el ETL , en el cual se hicieron las siguientes transformaciones

+ Algunos campos, como **`belongs_to_collection`**, **`production_companies`** y otros (ver diccionario de datos) están anidados, esto es o bien tienen un diccionario o una lista como valores en cada fila, ¡deberán desanidarlos para poder  y unirlos al dataset de nuevo hacer alguna de las consultas de la API! O bien buscar la manera de acceder a esos datos sin desanidarlos.

+ Los valores nulos de los campos **`revenue`**, **`budget`** deben ser rellenados por el número **`0`**.
  
+ Los valores nulos del campo **`release date`** deben eliminarse.

+ De haber fechas, deberán tener el formato **`AAAA-mm-dd`**, además deberán crear la columna **`release_year`** donde extraerán el año de la fecha de estreno.

+ Crear la columna con el retorno de inversión, llamada **`return`** con los campos **`revenue`** y **`budget`**, dividiendo estas dos últimas **`revenue / budget`**, cuando no hay datos disponibles para calcularlo, deberá tomar el valor **`0`**.

+ Eliminar las columnas que no serán utilizadas, **`video`**,**`imdb_id`**,**`adult`**,**`original_title`**,**`vote_count`**,**`poster_path`** y **`homepage`**.

#### DESARROLO API

Despues de Obtener los datos limpios, proposimos disponibilizar los datos de la empresa usando el framework ***FastAPI*** en el cual se crearon 6 funciones para los endpoints que se consumirán en la [API](https://github.com/CARRILLOJARA96/PI-MLOps-Ernesto/blob/main/main.py).
  
+    '''Se ingresa el mes y la funcion retorna la cantidad de peliculas que se estrenaron ese mes (nombre del mes, en str, ejemplo 'enero') historicamente'''

+    '''Se ingresa el dia y la funcion retorna la cantidad de peliculas que se estrenaron ese dia (de la semana, en str, ejemplo 'lunes') historicamente'''

+    '''Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio'''

+    '''Ingresas el pais, retornando la cantidad de peliculas producidas en el mismo'''

+    '''Ingresas la productora, retornando la ganancia total y la cantidad de peliculas que produjeron'''

+   '''Ingresas la pelicula, retornando la inversion, la ganancia, el retorno y el año en el que se lanzo'''

### EDA

Despues de hacer el ETL se realizó un análisis exploratorio de los datos para comprender las relaciones entre las variables, asi descubrir patrones interesantes que puedan ser útiles en análisis posteriores y en el desarrollo del  Modelo para la Recomendación

### Modelo de Recomendación

Se creó un modelo para recomendar películas a los usuarios, basándose en la similitud de puntuación , donde al ingresar el titulo de una película obtendremos una lista de 5 películas similares que nos recomienda el modelo de Machine Learning, este de manera descendente según el número de puntuación.

### Deployment

Se usó FastAPI para crear el API y Render para disponibilizar el Api desde en un servidor Web en el siguiente enlace [https://mlops1.onrender.com/docs](https://mlops1.onrender.com/docs)




