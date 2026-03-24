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

# Generamos el filtro de despliegue de la data en la tabla
# Por defecto el checkbox , queremos que muestre todas la marcas sin filtro. Una vez que se activa el filtro se genera el proceso de filtrado
if st.checkbox('Include manufactures with less than 100 ads'):
    # Contamos cuantos automóviles tenemos por marca
    brand_counts= df['brand'].value_counts()
    # Generamos el de las marcas a mantener discriminando las que tienen menos de 100 en su cuenta y guardamos su index
    brands_to_keep = brand_counts[brand_counts < 100].index
    # se realiza la discrimination de la data por las marcas que se encuentran en la variable almacenada para la discriminación 
    df = df[df['brand'].isin(brands_to_keep)]
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
    
    fig.add_trace(go.Bar(
        x=subset['brand'],
        y=subset['count'],
        name=vehicle_type, # Le damos el nombre a la leyenda y activa el color

    ))

# 3. Configuración estética
fig.update_layout(
    barmode='stack', # Apila las barras para  crear un histograma con barras apiladas
    xaxis_title="manufacturer",
    yaxis_title="count",
    legend_title="Tipo de Vehículo",
    template="plotly_white", # Fondo blanco para que los colores resalten
    xaxis={'categoryorder':'total descending'}, # Ordena de mayor a menor
)
fig.update_xaxes(tickangle=45)
# Lógica a ejecutar cuando se hace clic en el botón
if hist_button:
    st.plotly_chart(fig)


st.header('Histogram of condition vs model_year')
st.space('large')

# Creamos la figura donde será desplegado el histograma
hist_cond_vs_model = go.Figure()

# Agrupamos la data con respecto al año y condición 
condition_count = car_data.groupby(['model_year', 'condition']).size().reset_index(name='count')


# asignación de colores profesionales para dar mejor presentation al gráfico
colors = px.colors.qualitative.Vivid

# Iteramos por cada año para crear las capas de color de los marcadores de condición
for i, condition_label in enumerate(condition_count['condition'].unique()):
    subset = condition_count[condition_count['condition'] == condition_label]

    hist_cond_vs_model.add_trace(go.Scatter(
        x = subset['model_year'],
        y = subset['count'],
        mode = 'lines',
        stackgroup = 'one',
        line = dict(width=0.5, color=colors[i % len(colors)]),
        name=condition_label,
        opacity=0.5,
        fill = 'tonexty',
        fillcolor = colors[i % len(colors)]
    ))

hist_cond_vs_model.update_layout(
    barmode='overlay',
    xaxis_title='model_year',
    yaxis_title='count',
    legend_title='Condition',
    hovermode= 'x unified'
)

st.plotly_chart(hist_cond_vs_model)

# ----------------------------------------------------------------------------------------------------
# Damos un espacio entre actividades
st.space('large')
#Ubicamos la descripción de la actividad a delegar
st.header('Compare price distribution between manufactures')
#Indicamos cuales son las marcas a elegir en el primer select
brand_to_select= car_data['brand']
def clear_selection(option: int):
    if option == 1:
        st.session_state.first_manufacturer = None
    else:
        st.session_state.second_manufacturer = None
manufacture_second_selection = None
# Filtramos para que no aparezca lo que ya seleccionamos en el segundo (si existe)
options_1 = [b for b in brand_to_select if b != st.session_state.get('second_manufacturer')]
# Generamos el primer select para el manufacturer a comparar
manufacture_first_selection = st.selectbox(
    "Select manufacturer 1", # Este será el label asociado al select
    options=  options_1 , # asignamos los valores de las opciones a mostrar
    index=None, # no incluye los indices del las opciones
    placeholder="Select a manufacturer to compare...", # mantiene el place holder
    accept_new_options=True, 
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
    accept_new_options=True, 
    key='second_manufacturer' #asignamos un id para poder rastrear la selección y posteriormente limpiarla si asi lo deseamos
)

# Si el manufacturer uno fue seleccionado podemos mostrar la selección realizada
if manufacture_second_selection is not None:
    st.write("First manufacturer selected: ", manufacture_second_selection) # Con esta linea desplegamos en el DOM la opción seleccionada
    st.button('Clear second selection', on_click=clear_selection, args=(2,)) # La coma es necesaria para indicar que es una tupla y asi poder eliminar el contenido. Aunado a ello, esta linea asegura la aparición del botón cuando el primer manufacturer fue seleccionado

st.space('small')
# Creamos el histograma de comparación por marcas seleccionadas

selected_brands = [b for b in [manufacture_first_selection, manufacture_second_selection] if b is not None]
if selected_brands: 
    st.header(f"Price distribution for: {', '.join(selected_brands).title()}")
    filter_data = car_data[car_data['brand'].isin(selected_brands)]
    is_normalized = st.checkbox('Normalize histogram')
    comparison_df = filter_data.groupby(['brand', 'price']).size().reset_index(name='count')
    compare_manufacturer_hist = go.Figure()
    colors = px.colors.qualitative.Bold


    for i, brand in enumerate(selected_brands):
        subset = comparison_df[comparison_df['brand'] == brand]

        y_values = subset['count']
        if is_normalized:
            y_values = (subset['count'] / subset['count'].sum() * 100)

        compare_manufacturer_hist.add_trace(go.Histogram(
            x=subset['price'],
            y=y_values,
            name=brand, # Le damos el nombre a la leyenda y activa el color
            marker=dict(
                color=colors[i % len(colors)],
                line=dict(color='black', width=0.1)
            ),
            opacity=0.8,
            nbinsx=50,
            histnorm='percent' if is_normalized else None
        ))


    compare_manufacturer_hist.update_layout(
        barmode='group', # 'group' es mejor para comparar 2 marcas que 'stack'
        xaxis_title='Price ($)',
        yaxis_title='Percentage (%)' if is_normalized else 'Count',
        legend_title='Manufacturers',
        template='plotly_white'
    )

    compare_manufacturer_hist.update_xaxes(tickangle=45)
    st.plotly_chart(compare_manufacturer_hist)

else:
    st.info("Please select at least one manufacturer above to see the comparison.")

