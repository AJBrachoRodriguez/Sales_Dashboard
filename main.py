import streamlit as st
import pandas as pd
import psycopg2 as post
import mapgraphs as mapgraph
import linegraphs as linesgraph
import bargraphs as bargraph
import pizzagraph as pizzagraph
import linegraphsSellers as linesSellers
import bargraphsTopCities as barTopCities

## settings of the layoout
st.set_page_config(
    page_title="Dashboard Sales 2019 - 2021",
    layout='wide',
    initial_sidebar_state='expanded'
)
st.title("SalesPro  🛒 \n 2019 - 2021")
st.sidebar.image('fashionShop.jpeg')

## dataframes
df_final = pd.read_csv('df_final.csv')
df_map = pd.read_csv('df_map.csv')
df_bar = pd.read_csv('df_bar.csv')
df_lines = pd.read_csv('df_lines.csv')
df_pizza = pd.read_csv('df_pizza.csv')
df_lines_Sellers = pd.read_csv('df_lines_Sellers.csv')
df_bar_Top_Cities = pd.read_csv('df_graph_TopCities.csv')

## filters

st.sidebar.title('Filters')

# states: multiselect
states = ['Bahia', 'Rio de Janeiro','Paraíba','Distrito Federal','Minas Gerais','Paraná','Mato Grosso del Sur',
          'San Pablo','Goiás','Amazonas','Ceará','Río Grande del Sur','Acre','Rondonia','Mato Grosso',
          'Roraima','Pernambuco','Maranhao','Pará','Santa Catarina','Sergipe','Tocantins','Amapá','Piauí',
          'Espírito Santo','Alagoas','Río Grande del Norte']

states_multiselect = st.sidebar.multiselect('States',states)

# products: selectbox
products = sorted(list(df_final['product_type'].dropna().unique()))
products.insert(0,'All')
product = st.sidebar.selectbox('Products',products)

if product!='All':
    df_bar = df_bar[df_bar['product_type']==product]

# ages: checkbox
ages = st.sidebar.checkbox('All the period',value=True)


# we use df_lines because instead of df_final because it has the column 'year'.
if not ages:
    age = st.sidebar.slider('Age',df_lines['year'].min(),df_lines['year'].max())
if not ages:
    df_lines = df_lines[df_lines['year']==age]


# filtering the data
if states_multiselect:
    df_final = df_final[df_final['state_name'].isin(states_multiselect)]
else:
    df_final = df_final

# processing of the 'df_final'
df_map = df_final.groupby(['initials_state','state_name'])['valor_total'].sum().reset_index().sort_values(by='valor_total',ascending=False)

## graphics
graph_map = mapgraph.create_graph(df_map)
graph_bar = bargraph.create_graph(df_bar)
graph_lines = linesgraph.create_graph(df_lines)
graph_pizza = pizzagraph.create_graph(df_pizza)
graph_lines_Sellers = linesSellers.create_graph(df_lines_Sellers)
graph_bar_Top_Cities = barTopCities.create_graph(df_bar_Top_Cities)

## setting of the columns
col1,col2 = st.columns(2)
with col1:
     if states_multiselect:
        st.metric(f'**Total revenue {states_multiselect}**',value=f"{df_final['valor_total'].sum()/1e6:.1f} M$")
        st.plotly_chart(graph_map,use_container_width=True)
        st.plotly_chart(graph_bar,use_container_width=True)
        st.plotly_chart(graph_lines_Sellers,use_container_width=True)

     else:
        st.metric(f'**Total revenue**',value=f"{df_final['valor_total'].sum()/1e6:.1f} M$")
        st.plotly_chart(graph_map,use_container_width=True)
        st.plotly_chart(graph_bar,use_container_width=True)
        st.plotly_chart(graph_lines_Sellers,use_container_width=True)

         
with col2:
    if states_multiselect:
        st.metric(f'**Total items sold {states_multiselect}**',value=f"{df_final['cantidad'].sum()/1e3:.1f} k")
        st.plotly_chart(graph_lines,use_container_width=True)
        st.plotly_chart(graph_pizza,use_container_width=True)
        st.plotly_chart(graph_bar_Top_Cities,use_container_width=True)

    else:
        st.metric(f'**Total items sold**',value=f"{df_final['cantidad'].sum()/1e3:.1f} k")
        st.plotly_chart(graph_lines,use_container_width=True)
        st.plotly_chart(graph_pizza,use_container_width=True)
        st.plotly_chart(graph_bar_Top_Cities,use_container_width=True)


## dataframe

df_final = df_final.drop('Unnamed: 0',axis=1)
st.write('Data')
st.dataframe(df_final)
