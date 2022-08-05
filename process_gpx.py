import folium
import pandas as pd
from pandas.io.json import json_normalize
import argparse
from gpxplotter import (
    read_gpx_file,
    create_folium_map,
    add_segment_to_map,
    add_all_tiles,
)
import branca.colormap
from gpxplotter.common import RELABEL
import json
import requests
import warnings
warnings.filterwarnings("ignore")

parser= argparse.ArgumentParser()
parser.add_argument('-g', '--gpx', help= 'GPX file.')
parser.add_argument('-o', '--output', action= 'store_true', help= 'Produce output csv files.')
parser.add_argument('-v', '--valhalla', action= 'store_true', help= 'Use Valhalla map matching (beta).')
args= parser.parse_args()

#Plotting functions
def add_colored_line(the_map, segment, color_by, cmap='viridis', line_options=None):
	zdata = data[color_by]
	avg = (0.5 * (zdata[1:] + zdata[:-1])).dropna()
	minz, maxz = min(avg), max(avg)
	uniq = len(set(zdata))
	if uniq < 10:
		levels = uniq + 1
	else:
		levels = 10
	linmap = getattr(branca.colormap.linear, cmap)
	colormap = linmap.scale(minz, maxz).to_step(levels)
	colormap.caption = RELABEL.get(color_by, color_by)
	if line_options is None:
		line_options = {'weight': 6}
	line_options['weight'] = line_options.get('weight', 6)
	line = folium.ColorLine(positions=segment, colormap=colormap,
							colors=avg, control=False, **line_options)
	line.add_to(the_map)
	the_map.add_child(colormap)
	return
	
def folium_plot(data):
	f = folium.Figure(width=500, height=500)

	the_map= folium.Map(location=[data.lat.median(), data.lon.median()],
						zoom_start = 15, tiles='openstreetmap').add_to(f)
	'''
	folium.ColorLine(
			positions = list(zip(data.lat, data.lon)), # tuple of coordinates 
			colors = data.distance, # map each segment with the speed 
			colormap= ['b', 'r', 'y'],
			weight= 5,
			nb_steps= 100).add_to(the_map)
	'''
	add_colored_line(the_map, list(zip(data.lat, data.lon)), color_by= 'distance', cmap='viridis', line_options=None)
	folium.Marker(location= [data.iloc[0].lat, data.iloc[0].lon],
				icon=folium.Icon(color='black', icon='home', prefix='fa'), popup= 'Start').add_to(the_map)
	folium.Marker(location= [data.iloc[-1].lat, data.iloc[-1].lon],
				  icon=folium.Icon(color='black', icon='bus', prefix='fa'), popup= 'Finish').add_to(the_map)
	return the_map

for track in read_gpx_file(args.gpx):
    data= track   

time= pd.Series(data['segments'][0]['time'])
lats= pd.Series(data['segments'][0]['lat'])
lons= pd.Series(data['segments'][0]['lon'])
distance= pd.Series(data['segments'][0]['distance'])
elevation= pd.Series(data['segments'][0]['elevation'])
speed = pd.Series(data['segments'][0]['velocity'])

data= pd.DataFrame({'lat':lats, 'lon':lons, 'time':time,
'distance': distance, 'elevation': elevation, 'speed': speed})

the_map= folium_plot(data)
the_map.save(f'{args.gpx[:-4]}_plot.html')

print('\n#####################################################################\n')

print(f'Stats for GPX File: {args.gpx}\n')
print(f'Total distance = {round(data.distance.max()/1000,2)} km')
print(f'Total time = {round((data.iloc[-1].time - data.time[0]).seconds/60,2)} minutes')
print(f'Elevation change = {round(data.elevation.max()-data.elevation.min(),2)} m')
print(f'Average speed = {round(data.speed.mean()*1.61,2)} km/hr')
print(f'Track map saved in script directory as: {args.gpx[:-4]}_plot.html')
if args.output:
	data.to_csv(f'{args.gpx[:-4]}.csv', index= False)
	print(f'Track data saved in gpx directory as: {args.gpx[:-4]}.csv')
print('\n#####################################################################\n')

if args.valhalla:
	print('\n#####################################################################\n')
	print('Running Valhalla Map Matching (Meili)')
	data = data.sort_values(by=['time'], ascending = True)
	#Optimizing data to get it to Valhalla's Meili
	meili = data[['lon', 'lat', 'time']]
	
	#Preparing the request to Valhalla's Meili
	meili_coordinates = meili.to_json(orient='records')
	meili_head = '{"shape":'
	meili_tail = ""","search_radius": 150, "shape_match":"map_snap", "costing":"auto", "format":"osrm"}""" 
	meili_request_body = meili_head + meili_coordinates + meili_tail
	
	#Sending a request to Valhalla's Meili
	#url = "http://localhost:8002/trace_route" ### local host needs to be set up
	url = "https://valhalla1.openstreetmap.de/trace_route"
	headers = {'Content-type': 'application/json'}
	data = str(meili_request_body)
	try:
		r = requests.post(url, data=data, headers=headers)
	except:
		print('Valhalla server at limit. Map Matching failed!')
	
	#Receiving Valhalla's Meili response
	if r.status_code == 200:    
		response_text = json.loads(r.text)
		resp = str(response_text['tracepoints'])
		resp = resp.replace("'waypoint_index': None", "'waypoint_index': '#'")
		resp = resp.replace("None", "{'matchings_index': '#', 'name': '', 'waypoint_index': '#', 'alternatives_count': 0, 'distance': 0, 'location': [0.0, 0.0]}")
		resp = resp.replace("'", '"')
		resp = json.dumps(resp)
		resp = json.loads(resp)
        
		#Create a dataframe for response contents
		df_response = pd.read_json(resp)
		df_response = df_response[['name', 'distance', 'location']]
		df_trip_matched = pd.merge(meili, df_response, left_index=True, right_index=True)
	   
	   #Break down location into longitude and latitude for matched coordinates
		for i, row in df_trip_matched.iterrows():
			df_trip_matched.at[i, 'longitude'] = df_trip_matched.at[i,'location'][0]
			df_trip_matched.at[i, 'latitude'] = df_trip_matched.at[i,'location'][1]
        
			#Formatting: saving Meili output + original cooridinates for unmatched points
			if df_trip_matched.at[i, 'longitude'] == 0.0:
				df_trip_matched.at[i, 'longitude'] = df_trip_matched.at[i,'lon']
				df_trip_matched.at[i, 'latitude'] = df_trip_matched.at[i,'lat']
			
		df_trip_matched = df_trip_matched.drop(['location', 'lon', 'lat'], 1)
		df_trip_matched.rename(columns={'longitude': 'lon', 'latitude':'lat'}, inplace= True)
		df_trip_matched['distance']= df_trip_matched.distance.cumsum() #*0.3048
	
		data= df_trip_matched
		the_map= folium_plot(data)
		the_map.save(f'{args.gpx[:-4]}_valhalla_plot.html')
		print(f'Map Matching Successful! See: {args.gpx[:-4]}_valhalla_plot.html')
		if args.output:
			df_trip_matched.to_csv(f'{args.gpx[:-4]}.csv', index= False)
			print(f'Track data saved in gpx directory as: {args.gpx[:-4]}.csv')
		print('\n#####################################################################\n')