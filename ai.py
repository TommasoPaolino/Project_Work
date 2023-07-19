import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from bokeh.models.widgets import Div
import time
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
import pydeck as pdk
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split


st.set_page_config(layout="wide")
st.title("Dashboard Rete Neurale")


if st.sidebar.button("Mappa"):
    #js = "window.location.href = 'http://57.129.6.81:8502/'"  # Current tab
    js = "window.location.href = 'http://localhost:8502/'"
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)
st.sidebar.title("Parametri")
previsione = (st.sidebar.radio("Cosa vuoi prevedere:",("Numero incidenti","Numero feriti","Numero morti"))).replace("Numero", "").replace(" ", "")
Training= st.sidebar.slider("Training set (%)",10,80,60 )
Test= st.sidebar.slider("Test set (%)", 10,100-Training,10)
Normalizzato = st.sidebar.checkbox("Normalizzazione")
Epoche= st.sidebar.slider("Numero epoche", 1,100,1)
Batch = st.sidebar.slider("Batch size", 1,100,1)

livelli = st.sidebar.slider("Livelli", 3,10,3)
nodi = []
activation = []
for i in range(livelli):
       if(i==0):
              nodi.append(st.sidebar.slider(f"Input",1,5,1))
       elif(i==livelli-1):
              nodi.append(1)
              activation.append(st.sidebar.selectbox(f"Funzione Output", ("relu", "softmax", "sigmoid", "tanh")))
       else:
              nodi.append(st.sidebar.slider(f"Nodi livello {i+1}",1,10,1))
              activation.append(st.sidebar.selectbox(f"Funzione livello {i+1}", ("relu", "softmax", "sigmoid", "tanh")))



nodes = []
edges = []
fisica= st.sidebar.checkbox("Fisica")
if(st.sidebar.button("Applica")):
       
       for livello in range(len(nodi)):
              for nodo in range(nodi[livello]):
                     if(livello==0):
                            nodes.append(Node(id=f"{livello}-{nodo}", label = f"{livello+1}-{nodo+1}", size=25, shape= "circularImage", image="https://upload.wikimedia.org/wikipedia/commons/6/6d/Solid_yellow.png"))
                     elif(livello==len(nodi)-1):
                            nodes.append(Node(id=f"{livello}-{nodo}", label = f"{livello+1}-{nodo+1}", size=30, shape= "circularImage", image="https://upload.wikimedia.org/wikipedia/commons/a/a8/Solid_orange.png"))
                     else:
                            nodes.append(Node(id=f"{livello}-{nodo}", label = f"{livello+1}-{nodo+1}", size=15, shape= "circularImage", image="https://upload.wikimedia.org/wikipedia/commons/e/e5/Solid_blue.png"))
                     try:
                            for nodi_successivi in range(nodi[livello+1]):
                            
                                   edges.append(Edge(source=f"{livello}-{nodo}", 
                                   label="", 
                                   target=f"{livello+1}-{nodi_successivi}", 
                                   ) )
                     except:
                            pass
       progress_text = "Creazione rete neurale... "
       my_bar = st.progress(0, text=progress_text)
       percent_complete = 0
       for j in range(20):
              time.sleep(0.01)
              percent_complete+=1
              my_bar.progress(percent_complete, text=progress_text + f"{percent_complete}%")
       time.sleep(0.4) 
       

       def rete_neurale(colonne):
              global percent_complete
              progress_text = "Visualizzazione rete neurale... "
              for j in range(30):
                     time.sleep(0.03)
                     percent_complete+=1
                     my_bar.progress(percent_complete, text=progress_text + f"{percent_complete}%")
              time.sleep(0.4)

              st.subheader("Rete Neurale")
              st.write(":large_yellow_square: = Input" +5*" " + ":large_blue_square: = Nodo" +5*" " + ":large_orange_square: = Output")
              if(colonne):
                     height = 400
                     width = 1600
              else:
                     height = 400
                     width = 800
              
              

              config = Config(height=height,
                     width=width,
                     nodeHighlightBehavior=True,
                     highlightColor="#F7A7A6",
                     directed=True,
                     collapsible=True,
                     staticGraphWithDragAndDrop=True,
                     physics= fisica,
                     link={'labelProperty': 'label', 'renderLabel': True}
                     )

              return_value = agraph(nodes=nodes, 
                            edges=edges, 
                            config=config)
       
       def normalizzazione(df):
              if(Normalizzato):
                     return (df-df.min())/(df.max()-df.min())
              return df
              
              
       def perfomance_previsioni():
              global percent_complete
              df = pd.read_csv(f"AI_{previsione}.csv")
              y= df[previsione]
              df = df.drop(columns=[previsione])
              nomi = (np.array(OneHotEncoder().fit(np.array(df["STRADA"]).reshape(-1,1)).categories_)).reshape(-1)
              df[nomi] = OneHotEncoder().fit_transform(np.array(df["STRADA"]).reshape(-1,1)).toarray()
              df = df.drop(columns=["STRADA"])
              X_train, X_test, y_train, y_test = train_test_split(df.iloc[:, 0:nodi[0]], y, test_size=Test/100,train_size=Training/100, random_state=42)
              # Costruzione del modello
              model = Sequential()
              model.add(Dense(nodi[1], input_shape=(nodi[0],), activation=activation[0]))
              funzione = 1
              for liv in nodi[2:len(nodi)-1]:
                     model.add(Dense(liv, activation=activation[funzione]))
                     funzione+=1
              model.add(Dense(1, activation="relu"))

                     
              
              # Compilazione del modello
              model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mae', 'mse'])
              # Addestramento del modello con suddivisione dei dati di validazione
              model.fit(normalizzazione(X_train), y_train, epochs=Epoche, batch_size=Batch)
              progress_text = "Allenamento modello... "
              for j in range(30):
                     time.sleep(0.01)
                     percent_complete+=1
                     my_bar.progress(percent_complete, text=progress_text + f"{percent_complete}%")
              time.sleep(0.4)
              
              st.subheader(f"Previsioni sul numero di {previsione}")
              X_test["altezza"] = model.predict(X_test)
              X_test.altezza = X_test.altezza.apply(lambda x: int(x))
              X_test["previsione"] = previsione
              progress_text = "Visualizzazione previsioni... "
              for j in range(18):
                     time.sleep(0.01)
                     percent_complete+=1
                     my_bar.progress(percent_complete, text=progress_text + f"{percent_complete}%")
              time.sleep(0.4)
              st.pydeck_chart(pdk.Deck(
              initial_view_state=pdk.ViewState(
                     latitude=45.11591302676044,
                     longitude=10.92969911884387,
                     zoom=11,
                     pitch=50,
              ),
              layers=[
                     pdk.Layer(
                     'ColumnLayer',
                     data=X_test,
                     get_position='[longitudine, latitudine]',
                     get_elevation = "altezza",
                     radius=200,
                     get_fill_color=["255", "colore", "0"],
                     elevation_scale=100,
                     pickable=True,
                     extruded=True,
                     auto_highlight=True,
                     )],
                     

              map_provider="mapbox",
              map_style=pdk.map_styles.SATELLITE,
              tooltip = { "html": "{previsione} previsti: <b>{altezza}</b><br>Chilometro: <b>{chilometri}</b>", "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"}},
              ),use_container_width=True)
              

       
       if(len(nodi)>=5):
              rete_neurale(True)
              perfomance_previsioni()
              my_bar.progress(percent_complete+1, text="Finito")
              my_bar.empty()
       else:
              left, right = st.columns(2)
              with left:
                     rete_neurale(False)
              with right:
                     perfomance_previsioni()
              my_bar.progress(percent_complete+1, text="Finito")
              time.sleep(0.3)
              my_bar.empty()
