import folium
import branca.colormap
from gpxplotter.common import RELABEL


def add_colored_line(data, the_map, segment, color_by, cmap='viridis', line_options=None):
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

    the_map = folium.Map(location=[data.lat.median(), data.lon.median()],
                         zoom_start=15, tiles='openstreetmap').add_to(f)
    '''
    folium.ColorLine(
            positions = list(zip(data.lat, data.lon)), # tuple of coordinates 
            colors = data.distance, # map each segment with the speed 
            colormap= ['b', 'r', 'y'],
            weight= 5,
            nb_steps= 100).add_to(the_map)
    '''
    add_colored_line(data, the_map, list(zip(data.lat, data.lon)), color_by='distance', cmap='viridis', line_options=None)
    folium.Marker(location=[data.iloc[0].lat, data.iloc[0].lon],
                  icon=folium.Icon(color='black', icon='home', prefix='fa'), popup='Start').add_to(the_map)
    folium.Marker(location=[data.iloc[-1].lat, data.iloc[-1].lon],
                  icon=folium.Icon(color='black', icon='bus', prefix='fa'), popup='Finish').add_to(the_map)
    return the_map

