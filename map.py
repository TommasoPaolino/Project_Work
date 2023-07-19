import streamlit as st
import pandas as pd
import geopandas
import folium 
from streamlit_folium import st_folium
from shapely import wkt
import plotly.express as px
import webbrowser
from bokeh.models.widgets import Div

st.set_page_config(layout="wide")
st.title("Dashboard Mappa")

if st.sidebar.button("AI"):
    #js = "window.open('http://57.129.6.81:8502/')"  # New tab or window
    js = "window.location.href = 'http://localhost:8503/'"  # Current tab
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)
st.sidebar.title("Controlli")
df=pd.read_csv("chilometri.csv")

def mappa(df3, df4, df5):


	lista_df = [df5,df3,df4]
	label = ["incidenti", "feriti", "morti"]
	esistente = []
	for indice in range(3):
		if(len(lista_df[indice])>0):
			esistente.append((lista_df[indice], label[indice] ))
	layer=  True
	for dataframe in esistente:
		if(dataframe[1] == "incidenti"):
			df5 = dataframe[0].drop(index=dataframe[0].loc[dataframe[0].incidente<st.sidebar.slider('Incidenti', 1, 100, 1)].index)
			if(len(df5)>0):
				
				df5 = df.merge(df5, how="right", on=["chilometri","STRADA"])
				gdf = geopandas.GeoDataFrame(
    			df5, geometry=geopandas.points_from_xy(df5.longitudine, df5.latitudine), crs="EPSG:4326")
				
				check_incidenti = st.sidebar.checkbox("Incidenti")
				

				m = gdf.explore(column = "incidente", name="Incidenti",cmap='summer', marker_type="marker", style_kwds = dict(style_function= lambda x: {
            "html": f"""
	<svg fill="{x["properties"]["__folium_color"]}" height="32px" width="32px" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
	 viewBox="0 200 480.825 480.825" xml:space="preserve">
<g>
	<path d="M290.207,188.296c-2.823-1.735-6.519-0.856-8.254,1.966l-45.567,74.047c-1.737,2.822-0.857,6.518,1.965,8.255
		c0.98,0.603,2.066,0.891,3.139,0.891c2.015,0,3.982-1.015,5.116-2.856l45.567-74.047
		C293.909,193.729,293.029,190.033,290.207,188.296z"/>
	<path d="M222.466,244.96c1.166,1.676,3.033,2.574,4.931,2.574c1.182,0,2.377-0.35,3.421-1.075c2.72-1.893,3.392-5.632,1.499-8.352
		l-34.175-49.127c-1.892-2.719-5.631-3.39-8.352-1.499c-2.72,1.893-3.392,5.632-1.499,8.353L222.466,244.96z"/>
	<path d="M240.793,227.091c0.52,0.139,1.04,0.205,1.554,0.205c2.65,0,5.076-1.77,5.793-4.452l19.224-71.91
		c0.856-3.201-1.045-6.49-4.247-7.347c-3.204-0.854-6.491,1.046-7.346,4.247l-19.224,71.91
		C235.69,222.945,237.592,226.234,240.793,227.091z"/>
	<path d="M274.393,249.834c1.03,2.154,3.178,3.412,5.417,3.412c0.868,0,1.749-0.189,2.584-0.588l16.375-7.831
		c2.99-1.43,4.254-5.012,2.825-8.002c-1.429-2.989-5.012-4.253-8.001-2.824l-16.375,7.831
		C274.228,243.262,272.964,246.844,274.393,249.834z"/>
	<path d="M221.889,201.065c0.716,2.685,3.141,4.456,5.793,4.456c0.512,0,1.032-0.066,1.55-0.204
		c3.202-0.855,5.105-4.142,4.251-7.344l-11.391-42.72c-0.854-3.201-4.141-5.103-7.343-4.252c-3.202,0.854-5.105,4.142-4.251,7.344
		L221.889,201.065z"/>
	<path d="M234.214,287.646h-0.403v-5.336c0-4.824-3.917-7.322-7.247-8.35l-4.479-8.423c-0.61-1.148-1.741-1.928-3.031-2.091
		l-34.26-4.324l-31.767-50.333c-0.733-1.161-2.01-1.865-3.383-1.865H60.69c-1.641,0-3.115,1.002-3.719,2.527l-18.482,46.66H21.128
		c-8.945,0-14.075,5.13-14.075,14.075v17.713C3.012,288.872,0,292.517,0,296.852v6.92c0,5.076,4.13,9.205,9.206,9.205h20.963
		c2.054,13.824,13.998,24.466,28.384,24.466c14.387,0,26.332-10.642,28.386-24.466l69.541,0.001
		c2.054,13.824,13.998,24.465,28.383,24.465c14.387,0,26.332-10.641,28.386-24.465h20.964c5.076,0,9.205-4.13,9.205-9.206v-6.92
		C243.419,291.775,239.29,287.646,234.214,287.646z M58.553,319.442c-5.899,0-10.698-4.8-10.698-10.7c0-5.9,4.799-10.7,10.698-10.7
		c5.9,0,10.7,4.8,10.7,10.7C69.253,314.643,64.453,319.442,58.553,319.442z M184.864,319.442c-5.899,0-10.698-4.8-10.698-10.7
		c0-5.9,4.799-10.7,10.698-10.7c5.9,0,10.701,4.8,10.701,10.7C195.564,314.643,190.764,319.442,184.864,319.442z"/>
	<path d="M473.772,287.899v-17.713c0-8.945-5.13-14.075-14.076-14.075h-17.361l-18.482-46.66c-0.604-1.525-2.078-2.527-3.719-2.527
		h-76.493c-1.373,0-2.65,0.704-3.383,1.865l-31.767,50.333l-34.26,4.324c-1.29,0.163-2.42,0.942-3.031,2.091l-4.479,8.423
		c-3.331,1.027-7.247,3.525-7.247,8.35v5.336h-0.403c-5.076,0-9.206,4.13-9.206,9.206v6.92c0,5.076,4.129,9.206,9.206,9.206h20.964
		c2.054,13.824,13.999,24.465,28.386,24.465c14.385,0,26.33-10.641,28.383-24.465l57.081-0.001
		c2.054,13.824,13.999,24.466,28.386,24.466c14.386,0,26.33-10.642,28.384-24.466h20.963c5.076,0,9.206-4.129,9.206-9.205v-6.92
		C480.825,292.517,477.814,288.872,473.772,287.899z M308.422,319.442c-5.9,0-10.701-4.8-10.701-10.7c0-5.9,4.8-10.7,10.701-10.7
		c5.899,0,10.698,4.8,10.698,10.7C319.121,314.643,314.321,319.442,308.422,319.442z M422.272,319.442c-5.9,0-10.7-4.8-10.7-10.7
		c0-5.9,4.8-10.7,10.7-10.7c5.899,0,10.698,4.8,10.698,10.7C432.97,314.643,428.171,319.442,422.272,319.442z"/>
</g>
</svg>"""
        },
    ) , marker_kwds=dict(icon=folium.DivIcon()), legend = None, show=check_incidenti)
				layer= False
				
				
		
				

		elif(dataframe[1] == "feriti"):

			df3 = dataframe[0].drop(index=dataframe[0].loc[dataframe[0].feriti<st.sidebar.slider('Feriti', 1, 100, 1)].index)
			if(len(df3)>0):
				check_feriti = st.sidebar.checkbox("Feriti")
				df3 = df.merge(df3, how="right", on=["chilometri","STRADA"])
				gdf_feriti = geopandas.GeoDataFrame(
    			df3, geometry=geopandas.points_from_xy(df3.longitudine, df3.latitudine), crs="EPSG:4326")
				if(layer):
					m = None
				m = gdf_feriti.explore(m=m ,column = "feriti", name="Feriti",marker_type="marker",  style_kwds = dict(style_function= lambda x: {
            "html": f"""
	<svg fill="{x["properties"]["__folium_color"]}" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
	 width="24px" height="24px" viewBox="0 0 863.5 863.5" xml:space="preserve"
	>
<g>
	<path d="M76.851,823.15c53.8,53.8,141.1,53.8,194.9,0l551.4-551.4c53.8-53.8,53.8-141.1,0-194.9l-36.5-36.5
		c-53.801-53.8-141.101-53.8-194.9,0L40.351,591.75c-53.8,53.8-53.8,141.1,0,194.9L76.851,823.15z M301.151,721.85
		c-9,9-23.7,9-32.7,0s-9-23.699,0-32.699s23.7-9,32.7,0C310.25,698.15,310.25,712.75,301.151,721.85z M364.151,658.85
		c-9,9-23.7,9-32.7,0s-9-23.699,0-32.699s23.7-9,32.7,0C373.25,635.15,373.25,649.85,364.151,658.85z M752.05,205.451
		c9-9,23.7-9,32.7,0s9,23.7,0,32.7s-23.7,9-32.7,0S743.05,214.55,752.05,205.451z M721.85,301.15c-9,9-23.699,9-32.699,0
		s-9-23.7,0-32.7s23.699-9,32.699,0S730.85,292.15,721.85,301.15z M688.65,142.05c9-9,23.699-9,32.699,0s9,23.7,0,32.7
		s-23.699,9-32.699,0S679.65,151.15,688.65,142.05z M658.85,364.151c-9,9-23.699,9-32.699,0s-9-23.7,0-32.7s23.699-9,32.699,0
		C667.95,340.451,667.95,355.151,658.85,364.151z M658.45,237.851c-9,9-23.7,9-32.7,0s-9-23.7,0-32.7s23.7-9,32.7,0
		S667.45,228.75,658.45,237.851z M625.25,78.65c9-9,23.7-9,32.7,0s9,23.7,0,32.7s-23.7,9-32.7,0S616.25,87.75,625.25,78.65z
		 M562.35,141.65c9-9,23.7-9,32.7,0s9,23.7,0,32.7s-23.7,9-32.7,0C553.25,165.351,553.25,150.75,562.35,141.65z M595.45,300.75
		c-9,9-23.7,9-32.7,0s-9-23.7,0-32.7s23.7-9,32.7,0C604.55,277.05,604.55,291.75,595.45,300.75z M499.35,204.65c9-9,23.7-9,32.7,0
		s9,23.7,0,32.7s-23.7,9-32.7,0C490.25,228.351,490.25,213.65,499.35,204.65z M275.951,428.05l152.2-152.2
		c11.699-11.7,30.699-11.7,42.399,0l117.101,117.1c11.699,11.7,11.699,30.7,0,42.399l-152.2,152.2c-11.7,11.7-30.7,11.7-42.4,0
		l-117.1-117.1C264.151,458.75,264.151,439.75,275.951,428.05z M268.05,562.75c9-9,23.7-9,32.7,0s9,23.7,0,32.7s-23.7,9-32.7,0
		C258.951,586.45,258.951,571.75,268.05,562.75z M238.25,784.85c-9,9-23.7,9-32.7,0s-9-23.699,0-32.699s23.7-9,32.7,0
		S247.25,775.75,238.25,784.85z M237.851,658.45c-9,9-23.7,9-32.7,0s-9-23.7,0-32.7s23.7-9,32.7,0
		C246.85,634.75,246.85,649.35,237.851,658.45z M204.65,499.35c9-9,23.7-9,32.7,0c9,9,9,23.7,0,32.7c-9,9-23.7,9-32.7,0
		C195.55,523.05,195.55,508.35,204.65,499.35z M174.851,721.45c-9,9-23.7,9-32.7,0s-9-23.7,0-32.7s23.7-9,32.7,0
		S183.851,712.35,174.851,721.45z M141.65,562.35c9-9,23.7-9,32.7,0s9,23.7,0,32.7s-23.7,9-32.7,0S132.65,571.35,141.65,562.35z
		 M78.65,625.25c9-9,23.7-9,32.7,0s9,23.7,0,32.7s-23.7,9-32.7,0S69.65,634.35,78.65,625.25z"/>
</g>
</svg>"""
        },    ) , marker_kwds=dict(icon=folium.DivIcon()), legend = None, show=check_feriti)
				layer= False
			
		else:
			df4 = dataframe[0].drop(index=dataframe[0].loc[dataframe[0].morti<st.sidebar.slider('Morti', 1, 100, 1)].index)
			if(len(df4)>0):
				if(layer):
					m = None
				check_morti = st.sidebar.checkbox("Morti")
				df4 = df.merge(df4, how="right", on=["chilometri","STRADA"])
				gdf_morti = geopandas.GeoDataFrame(
    			df4, geometry=geopandas.points_from_xy(df4.longitudine, df4.latitudine), crs="EPSG:4326")
				m = gdf_morti.explore(m=m ,column = "morti", name="Morti",marker_type="marker",   style_kwds = dict(style_function= lambda x: {
            "html": f"""
	<?xml version="1.0" encoding="iso-8859-1"?>
<!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg fill="{x["properties"]["__folium_color"]}" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
	 width="24px" height="24px" viewBox="0 30 535.812 535.812"
	 xml:space="preserve">
<g>
	<g>
		<path d="M154.514,264.364c0,0,24.61,4.187,44.7,17.335c20.085,13.16,27.797,37.087,27.797,37.087h77.757
			c0,0,11.795-34.121,30.524-42.832c18.719-8.741,47.935-14.591,47.935-14.591s-1.261,0.42-0.455-37.448
			c25.958-24.038,39.363-54.001,39.363-89.61C422.136,60.131,353.065,0,267.893,0c-85.167,0-154.213,60.131-154.213,134.304
			c0,35.312,15.653,67.418,41.208,91.391C153.598,251.262,154.514,264.364,154.514,264.364z M330.751,121.81
			c23.623,0,42.762,22.35,42.762,49.896c0,27.564-19.15,49.891-42.762,49.891c-23.623,0-42.762-22.338-42.762-49.891
			C287.989,144.16,307.14,121.81,330.751,121.81z M265.791,228.229l4.735,6.09c11.857,15.256,16.891,35.819,17.112,36.684
			l-12.389,2.978c-0.047-0.158-3.206-12.985-10.066-24.814c-7.976,12.285-8.828,23.605-8.839,23.74l-12.71-0.853
			c0.07-0.823,1.518-20.277,17.089-38.038L265.791,228.229z M208.947,121.81c23.628,0,42.756,22.35,42.756,49.896
			c0,27.564-19.139,49.891-42.756,49.891s-42.761-22.338-42.761-49.891C166.174,144.16,185.318,121.81,208.947,121.81z"/>
		<path d="M430.158,418.204c-17.562-8.676-39.388-2.639-48.846,13.499c-2.358,4.04-3.736,8.36-4.169,12.669l-71.931-35.626
			l71.476-36.853c0.654,3.83,1.985,7.648,4.181,11.232c9.715,15.986,31.703,21.696,49.079,12.729
			c17.363-8.969,23.553-29.193,13.813-45.179c-7.182-11.794-20.995-17.96-34.739-16.804c8.232-10.182,9.738-24.265,2.557-36.047
			c-9.727-15.986-31.691-21.696-49.078-12.728c-17.353,8.968-23.564,29.193-13.814,45.191c3.06,4.997,7.311,8.99,12.227,11.863
			l-93.172,48.062l-94.06-46.58c4.858-2.941,9.056-7.006,12.004-12.051c9.423-16.148,2.849-36.257-14.678-44.956
			c-17.533-8.688-39.404-2.627-48.833,13.522c-6.959,11.887-5.19,25.945,3.24,35.988c-13.755-0.934-27.482,5.465-34.43,17.375
			c-9.435,16.139-2.854,36.27,14.673,44.945c17.545,8.676,39.41,2.64,48.833-13.51c2.143-3.62,3.41-7.45,3.958-11.304l72.165,35.731
			l-71.265,36.736c-0.514-4.285-1.95-8.57-4.391-12.588c-9.733-15.975-31.698-21.695-49.073-12.728
			c-17.387,8.968-23.582,29.192-13.82,45.179c7.158,11.794,20.996,17.971,34.733,16.826c-8.25,10.183-9.733,24.254-2.581,36.036
			c9.745,15.997,31.709,21.696,49.097,12.728c17.363-8.968,23.564-29.192,13.796-45.178c-2.75-4.555-6.562-8.256-10.953-11.047
			l91.928-47.409l92.816,45.949c-4.344,2.86-8.093,6.609-10.767,11.21c-9.435,16.149-2.872,36.27,14.678,44.957
			c17.562,8.688,39.399,2.627,48.846-13.511c6.972-11.899,5.185-25.958-3.246-36.001c13.743,0.936,27.464-5.465,34.424-17.375
			C454.26,447.023,447.674,426.891,430.158,418.204z"/>
	</g>
</g>
</svg>"""
        },    ) , marker_kwds=dict(icon=folium.DivIcon()), legend = None, show=check_morti)
				layer= False

	gdf_flusso =pd.read_csv("Flusso.csv")
	gdf_flusso = gdf_flusso.drop(index=gdf_flusso.loc[gdf_flusso.FLOW>st.sidebar.slider('Flusso', 1000, 13_000_000, 13_000_000)].index)
	df_flusso = gdf_flusso.copy()
	gdf_flusso= geopandas.GeoDataFrame(
    			gdf_flusso, geometry=geopandas.points_from_xy(gdf_flusso.longitudine, gdf_flusso.latitudine), crs="EPSG:4326")

	try:
		if(layer):
				m = None
		check_flusso = st.sidebar.checkbox("Flusso")
		m = gdf_flusso.explore(m=m, column = "FLOW", name="Flusso", cmap = "summer",  marker_type="marker", show=check_flusso, style_kwds = dict(style_function= lambda x: {
            "html": f"""<svg style="width: 24px; height: 24px;vertical-align: middle;fill: {x["properties"]["__folium_color"]};overflow: hidden;" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M512 597.994667q108.010667 0 225.002667 46.997333t116.992 123.008l0 85.994667-684.010667 0 0-85.994667q0-76.010667 116.992-123.008t225.002667-46.997333zM512 512q-69.994667 0-120-50.005333t-50.005333-120 50.005333-121.002667 120-51.008 120 51.008 50.005333 121.002667-50.005333 120-120 50.005333z"  /></svg>"""
        },    ) , marker_kwds=dict(icon=folium.DivIcon()), legend = None)
	except:
		pass

	folium.LayerControl().add_to(m)

	st_folium(m, width=1500)
	try:
		if check_incidenti:
			strada  = st.selectbox("Strada ", pd.unique(df5.STRADA))
			fig = px.bar(df5.loc[df5.STRADA==strada], x="chilometri", y="incidente", width=1500,labels={'chilometri': 'Km', 'incidente':'Numero Incidenti'})
			fig.update_layout(title=f'Numero incidenti {strada}')
			st.plotly_chart(fig,use_container_width=False)
	except:
		pass
	try:
		if check_feriti:
			strada_feriti  = st.selectbox("Strada  ", pd.unique(df3.STRADA))
			fig = px.bar(df3.loc[df3.STRADA==strada_feriti], x="chilometri", y="feriti", width=1500,labels={'chilometri': 'Km', 'feriti':'Numero Feriti'})
			fig.update_layout(title=f'Numero feriti {strada_feriti}')
			st.plotly_chart(fig,use_container_width=False)
	except:
		pass

	try:
		if check_morti:
			strada_morti  = st.selectbox("Strada   ", pd.unique(df4.STRADA))
			fig = px.bar(df4.loc[df4.STRADA==strada_morti], x="chilometri", y="morti", width=1500,labels={'chilometri': 'Km', 'morti':'Numero Morti'})
			fig.update_layout(title=f'Numero morti {strada_morti}')
			st.plotly_chart(fig,use_container_width=False)
	except:
		pass

	try:
		if check_flusso:
			df_flusso = df_flusso.groupby("COMUNE").FLOW.mean().sort_values(ascending=False).reset_index()
			fig = px.bar(df_flusso, x="COMUNE", y="FLOW", width=1500,labels={'COMUNE': 'Comune', 'FLOW':'Flusso'})
			fig.update_layout(title=f'Flusso persone')
			st.plotly_chart(fig,use_container_width=False)
	except:
		pass


	
	
	

	


df_progetto = pd.read_csv("Progetto.csv")
df_progetto["incidente"] = df_progetto.chilometri

colonne = list(df_progetto.columns)
option = st.sidebar.selectbox(
    "Filtro 1",
    (colonne))
lista = list(pd.unique(df_progetto[option]))
lista.insert(0, "")
value = st.sidebar.selectbox("Valore opzione 1",lista )

option1 = st.sidebar.selectbox(
    "Filtro 2",
    (colonne))
lista1 = list(pd.unique(df_progetto[option1]))
lista1.insert(0, "")
value1 = st.sidebar.selectbox("Valore opzione 2",lista1 )

option2 = st.sidebar.selectbox(
    "Filtro 3",
    (colonne))
lista2 = list(pd.unique(df_progetto[option2]))
lista2.insert(0, "")
value2 = st.sidebar.selectbox("Valore opzione 3",lista2)


filtri = [option, option1, option2]
valori = [value, value1, value2]
selezionati = []
for indice in range(3):
	if(valori[indice] != ""):
		selezionati.append((filtri[indice], valori[indice]))

for filtro in selezionati:
	try:
		df_progetto = df_progetto.loc[df_progetto[filtro[0]]==filtro[1]]
	except:
		pass



	
df3 = df_progetto.groupby(by= ["chilometri", "STRADA"]).sum(["feriti", "morti"]).loc[:,["feriti"]].reset_index()
df4 = df_progetto.groupby(by= ["chilometri", "STRADA"]).sum(["feriti", "morti"]).loc[:,["morti"]].reset_index()
df5 = df_progetto.groupby(by= ["chilometri", "STRADA"]).incidente.count().reset_index()
mappa(df3,df4,df5)


