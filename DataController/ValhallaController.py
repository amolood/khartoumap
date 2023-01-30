import requests
import json
import pandas as pd

class Valhalla:
    """

    """
    def __init__(self, data):
        self.data = data
        self.meili = self.data[['lon', 'lat', 'time']]
        self.meili_coordinates = self.meili.to_json(orient='records')
        self.meili_head = '{"shape":'
        self.meili_tail = ""","search_radius": 150, "shape_match":"map_snap", "costing":"auto", "format":"osrm"}"""
        self.meili_request_body = self.meili_head + self.meili_coordinates + self.meili_tail
        self.url = "https://valhalla1.openstreetmap.de/trace_route"
        self.headers = {'Content-type': 'application/json'}
        self.data = str(self.meili_request_body)

    def valhalla_request(self):

        """
        :return:
        """

        try:
            r = requests.post(self.url, data=self.data, headers=self.headers)
        except:
            print('Valhalla server at limit. Map Matching failed!')
            exit()
        return r

    def valhalla_response(self):

        """
        :return:
        """

        if self.valhalla_request().status_code == 200:
            response_text = json.loads(self.valhalla_request().text)
            response = str(response_text['tracepoints'])
            response = response.replace("'waypoint_index': None", "'waypoint_index': '#'")
            response = response.replace("None",
                                        "{'matchings_index': '#', 'name': '', 'waypoint_index': '#', 'alternatives_count': 0, 'distance': 0, 'location': [0.0, 0.0]}")
            response = response.replace("'", '"')
            response = json.dumps(response)
            response = json.loads(response)
            return response


    def valhalla_df(self):

        """
        :return:
        """

        response_df = pd.read_json(self.valhalla_response())
        response_df = response_df[['name', 'distance', 'location']]
        map_matched_df = pd.merge(self.meili, response_df, left_index=True, right_index=True)
        for i, row in map_matched_df.iterrows():
            map_matched_df.at[i, 'longitude'] = map_matched_df.at[i, 'location'][0]
            map_matched_df.at[i, 'latitude'] = map_matched_df.at[i, 'location'][1]
            if map_matched_df.at[i, 'longitude'] == 0.0:
                map_matched_df.at[i, 'longitude'] = map_matched_df.at[i, 'lon']
                map_matched_df.at[i, 'latitude'] = map_matched_df.at[i, 'lat']

        map_matched_df = map_matched_df.drop(['location', 'lon', 'lat'], 1)
        map_matched_df.rename(columns={'longitude': 'lon', 'latitude': 'lat'}, inplace=True)
        map_matched_df['distance'] = map_matched_df.distance.cumsum()  # *0.3048

        return map_matched_df


