# Import libraries
import pandas as pd
import streamlit as st
import plotly.graph_objects as go  # Importación de plotly.graph_objects como go
import plotly.express as px
# streamlit configuration container width
st.html("""
<style>
section[data-testid="stMain"] > div[data-testid="stMainBlockContainer"] {
    max-width: 80rem;
}
</style>
""")

# Leer los datos del archivo CSV
car_data = pd.read_csv('./vehicles_us.csv')
# Insertar el primer titulo
st.header('Data viewer')

# Extraer la marca y la mostramos en la columna llamada 'brand'
car_data['brand'] = car_data['model'].str.split().str[0]
# Reflejamos la data a una variable exclusiva para la tabla
df = car_data
# Contamos cuantos automóviles tenemos por marca
brand_counts= df['brand'].value_counts()
# Generamos el de las marcas a mantener discriminando las que tienen menos de 100 en su cuenta y guardamos su index
brands_to_keep = brand_counts[brand_counts >= 100].index
# se realiza la discrimination de la data por las marcas que se encuentran en la variable almacenada para la discriminación 
df = df[df['brand'].isin(brands_to_keep)]

# Generamos el filtro de despliegue de la data en la tabla
# Por defecto el checkbox , queremos que muestre todas la marcas sin filtro. Una vez que se activa el filtro se genera el proceso de filtrado
if st.checkbox('Include manufactures with less than 100 ads'):
    df= car_data
# Se genera el la tabla en el DOM mediante el método dataframe de streamlit
st.dataframe(df)

# Imprimimos un espacio de linea para  separa la tabla de el histograma

st.space("large")
st.header('Vehicles types by manufacturer')

# Crear un botón en la aplicación Streamlit
hist_button = st.button('Build histogram')

# 1. Agrupamos por fabricante y por modelo ademas de contar las filas
brand_count = car_data.groupby(['brand', 'type']).size().reset_index(name='count')

# Lista de todos los tipos de vehículos que servirá las leyendas
vehicle_types = brand_count['type'].unique()


fig = go.Figure()

# 2. Iteramos por cada tipo de vehículo para crear las capas de color
for vehicle_type in brand_count['type'].unique():
    subset = brand_count[brand_count['type'] == vehicle_type]
    
    fig.add_trace(go.Bar( # Se indica el tipo de gráfico a generar mediante el método add_trace
        x=subset['brand'], # Los valores de la gráfica en el eje x será la columna brand del subset
        y=subset['count'], # Los valores del gráfica en el eje y , será la columna count generada en el filtro brand_count
        name=vehicle_type, # Le damos el nombre a la leyenda y activa el color

    ))

# 3. Configuración estética
fig.update_layout(
    barmode='stack', # Apila las barras para  crear un histograma con barras apiladas
    xaxis_title="manufacturer", # Titulo del eje x en el gráfico
    yaxis_title="count", # Titulo del eje y en el gráfico
    legend_title="Tipo de Vehículo", # Titulo del gráfico
    template="plotly_white", # Fondo blanco para que los colores resalten
    xaxis={'categoryorder':'total descending'}, # Ordena de mayor a menor,
    xaxis=dict(tickangle=45) # Se lle da una inclination a las labels del eje x
)
# Lógica a ejecutar cuando se hace clic en el botón
if hist_button:
    st.plotly_chart(fig) # Se genera el gráfico en el DOM

#-----------------------------------------------------------------------------------------------------------------------
# Generación del segundo gráfico
st.space('large') # Se agrega un espacio separador de area 
st.header('Histogram of condition vs model_year') # Se agrega el titulo 
st.space('large') # Se agrega un espacio separador de area 

# Creamos la figura donde será desplegado el histograma
hist_cond_vs_model = go.Figure()

# Agrupamos la data con respecto al año y condición 
condition_count = car_data.groupby(['model_year', 'condition']).size().reset_index(name='count')


# asignación de colores profesionales para dar mejor presentation al gráfico
colors = px.colors.qualitative.Vivid

# Iteramos por cada año para crear las capas de color de los marcadores de condición
for i, condition_label in enumerate(condition_count['condition'].unique()): # Se itera sobre el enumerable de la tabla condition_count apoyados en su indice "i" y su valor "condition_label"
    subset = condition_count[condition_count['condition'] == condition_label] # Se crea el subset con la condición para los datos por cada condición especifica

    hist_cond_vs_model.add_trace(go.Scatter( # Se indica el tipo de gráfico a mostrar
        x = subset['model_year'],  # Se asigna la data que estará representando el eje x
        y = subset['count'], # Se asigna la data que estará representando el eje y
        mode = 'lines', # Se asigna el modo de replantación del gráfico de tipo scatter. Esto indica que se conecte los punto son lineas 
        stackgroup = 'one', # Se apilan las linas d eun mismo grupo en lugar de mostrar una por una
        line = dict(width=0.5, color=colors[i % len(colors)]), # Se indica el tipo de ancho de linea y el color por cada trazo utilizando el indice i
        name=condition_label,  # Titulo de las leyendas ubicadas en lado derecho del gráfico
        opacity=0.5, # se indica la opacidad de los trazos del gráfico
        fill = 'tonexty', # Rellena los trazos de color hasta la parte inferior creando aspectos de color solido
        fillcolor = colors[i % len(colors)] # Agrega el color de relleno que en este caso es el mismo color de los trazos
    ))

hist_cond_vs_model.update_layout( # Se actualiza el gráfico para 
    barmode='overlay', # se indica que las barras deben encimarse
    xaxis_title='model_year', # titulo del eje x
    yaxis_title='count', # titulo del eje y
    legend_title='Condition', # titulo del gráfico
    hovermode= 'x unified' # Se agrega la característica de hover para mostrar todos los valores del gráfico por año al mismo tiempo y no de maneta unitaria
)

st.plotly_chart(hist_cond_vs_model) # Se genera el gráfico sobre el DOM

# ----------------------------------------------------------------------------------------------------
# Area del gráfico de comparación de marcas y sus lectores de marcas a comparar

# Damos un espacio entre actividades
st.space('large')
#Ubicamos la descripción de la actividad a delegar
st.header('Compare price distribution between manufactures')
#Indicamos cuales son las marcas a elegir en el primer select
brand_to_select= car_data['brand'].unique() # Se genera el filtro de marcas de la data para encontrar las marcas de autos

#-------------------------------------------------------------------------------------------------------------
#Selectores de marcas a comparar en el gráfico
def clear_selection(option: int): # Function auxiliar de control para limpiar los elementos select. Esto remueve del DOM los select que han sido grabados con valores por ell usuario previamente. Monta le select limpio nuevamente con un valor None 
    if option == 1: # Si la opción es 1 afecta al primer select identificado con el id "first_manufacturer" en el session_state
        st.session_state.first_manufacturer = None
    else: # Si la opción es 1 afecta al primer select identificado con el id "second_manufacturer" en el session_state
        st.session_state.second_manufacturer = None
# Generamos la variable de almacenamiento del select 2 para poder referir al control relacionado con el select 1. Para cuando un valor se asignado primero al select 2 descarte la opción tomada del select 1
manufacture_second_selection = None
# Filtramos para que no aparezca lo que ya seleccionamos en el segundo (si existe)
options_1 = [b for b in brand_to_select if b != st.session_state.get('second_manufacturer')]
# Generamos el primer select para el manufacturer a comparar
manufacture_first_selection = st.selectbox(
    "Select manufacturer 1", # Este será el label asociado al select
    options=  options_1 , # asignamos los valores de las opciones a mostrar
    index=None, # no incluye los indices del las opciones
    placeholder="Select a manufacturer to compare...", # mantiene el place holder
    accept_new_options=False, # Limitamos las opciones del select a las que tenemos en la tabla sin un campo de texto de entrada por el usuario activado.
    key='first_manufacturer' #asignamos un id para poder rastrear la selección y posteriormente limpiarla si asi lo deseamos
)

# Si el manufacturer uno fue seleccionado podemos mostrar la selección realizada
if manufacture_first_selection is not None:
    st.write("First manufacturer selected: ", manufacture_first_selection) # Con esta linea desplegamos en el DOM la opción seleccionada
    st.button('Clear first selection', on_click=clear_selection, args=(1,)) # La coma es necesaria para indicar que es una tupla y asi poder eliminar el contenido. Aunado a ello, esta linea asegura la aparición del botón cuando el primer manufacturer fue seleccionado

# Filtramos para que no aparezca lo que ya seleccionamos en el primero
options_2 = [b for b in brand_to_select if b != st.session_state.get('first_manufacturer')]
# Generamos el segundo select para el manufacturer a comparar
manufacture_second_selection = st.selectbox(
    "Select manufacturer 2", # Este será el label asociado al select
    options= options_2, # asignamos los valores de las opciones a mostrar
    index=None, # no incluye los indices del las opciones
    placeholder="Select a manufacturer to compare...", # mantiene el place holder
    accept_new_options=False, # Limitamos las opciones del select a las que tenemos en la tabla sin un campo de texto de entrada por el usuario activado.
    key='second_manufacturer' #asignamos un id para poder rastrear la selección y posteriormente limpiarla si asi lo deseamos
)

# Si el manufacturer uno fue seleccionado podemos mostrar la selección realizada
if manufacture_second_selection is not None:
    st.write("First manufacturer selected: ", manufacture_second_selection) # Con esta linea desplegamos en el DOM la opción seleccionada
    st.button('Clear second selection', on_click=clear_selection, args=(2,)) # La coma es necesaria para indicar que es una tupla y asi poder eliminar el contenido. Aunado a ello, esta linea asegura la aparición del botón cuando el primer manufacturer fue seleccionado

# ------------------------------------------------------------------------------------------------------------------------------
# Grafico de comparación de marcas seleccionadas
st.space('small')
# Creamos el histograma de comparación por marcas seleccionadas
# Seleccionamos generamos la lista de las marcas seleccionadas descartando los valores None de las opciones no seleccionadas
selected_brands = [b for b in [manufacture_first_selection, manufacture_second_selection] if b is not None]
if selected_brands: # Si hay valores en selected_brands procedamos a la creación del gráfico evitando errores al generar el gráfico con valores None
    st.header(f"Price distribution for: {', '.join(selected_brands).title()}") # se asigna el titulo del gráfico indicando las opciones seleccionadas por el usuario
    filter_data = car_data[car_data['brand'].isin(selected_brands)] # Filtramos la data origina en base a las marcas seleccionadas
    is_normalized = st.checkbox('Normalize histogram') # Se genera la variable contenedora del checkbox de normalización de datos
    comparison_df = filter_data.groupby(['brand', 'price']).size().reset_index(name='count') # Se genera la tabla de conteo de los grupos de datos en base a marca y precio asignando el nombre de  " count " al conteo
    compare_manufacturer_hist = go.Figure() # Se genera la variable referencia del gráfico a mostrar con go
    colors = px.colors.qualitative.Bold # se asigna la paleta de colores a utiliza a la variable colors


    for i, brand in enumerate(selected_brands): # Por medio del enumerable se itera sobre los valores de las marcas seleccionadas por el usuario apoyándonos en el valor del indices "i" para fines de estilos
        subset = comparison_df[comparison_df['brand'] == brand] # Se genera el subset de la data agrupada por conteo de marca precio discriminandola por la marca seleccionada

        y_values = subset['count']#  Se asigna el valor del eje y del gráfico a los valores de subset en su columna count
        if is_normalized: # si el checkbox de normalize esta activo:
            y_values = (subset['count'] / subset['count'].sum() * 100) # normalizamos la data sacando el porcentaje de los valores en su columna count → ( vector de frecuencias count) / (valor total de la  del vector de frecuencias count) * 100 . retornando asi un nuevo vector con valores porcentuales

        compare_manufacturer_hist.add_trace(go.Histogram( # Se genera las especificaciones del gráfico a utilizar en este caso histograma
            x=subset['price'], # Se asignan los valores del eje x. En esta caso los valores del precio en el subset
            y=y_values, # Se asignan los valores del eje y: es ete caso dependiendo de la selección normalice serán los valores de count del subset sin normalizar o normalizados
            name=brand, # Le damos el nombre a la leyenda y activa el color
            marker=dict( # Se asignan los estilos de los trazos en el gráfico
                color=colors[i % len(colors)], # se asigna el color con el apoyo del indice de iteración
                line=dict(color='black', width=0.1) # Se asigna el timo de linea a utilizar
            ),
            opacity=0.8, # Se indica la opacidad del gráfico
            nbinsx=50, # IMPORTANTE: con bins hacemos realidad un gráfico digerible en barras robustas para que no se vea como muchas lineas delgadas. agrupamos por sectores, mostrando asi un gráfico con barras comparativas
            histnorm='percent' if is_normalized else None  # Se indica la normalización del histograma en caso de estar en el modo normalizado. cambia automáticamente el parámetro de medición del eje y de porcentaje a frecuencia
        ))


    compare_manufacturer_hist.update_layout(
        barmode='group', # 'group' es mejor para comparar 2 marcas que 'stack'
        xaxis_title='Price ($)', # titulo del eje x
        yaxis_title='Percentage (%)' if is_normalized else 'Count', # titulo del eje y
        legend_title='Manufacturers', # Titulo de las labels del lado derecho
        template='plotly_white' # titulo del gráfico,
        xaxis=dict(tickangle=45) # Se asigna una rotación de 45° en las labels del eje x
    )

    st.plotly_chart(compare_manufacturer_hist) #Se genera el gráfico en el DOM

else: # Si no ya datos en las brand seleccionadas
    st.info("Please select at least one manufacturer above to see the comparison.") # se muestra un mensaje al usuario de selección de marcas

