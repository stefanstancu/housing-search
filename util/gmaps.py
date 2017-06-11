import json
import googlemaps

travel_params = {
    'mode': 'transit',
    'units': 'metric',
    'transit_mode': [
        'subway',
        'bus'
    ],
    'traffic_model': 'best_guess'
}


class Gmap:
    def __init__(self):
        # Load API Key
        api_dict = json.load(open('api_keys.json'))
        self.gmaps_api_key = api_dict['gmaps']
        self.gmap = googlemaps.Client(key=self.gmaps_api_key)

    def directions(self, start_address, end_address):
        """
            Computes the directions using gmaps api
        Args:
            start_address: (string) raw address of starting location
            end_address: (string) raw address of destination

        Returns:
            Not sure yet
        """
        return self.gmap.directions(
            origin=start_address,
            destination=end_address,
            mode=travel_params['mode'],
            units=travel_params['units'],
            transit_mode=travel_params['transit_mode'],
            traffic_model=travel_params['transit_mode']
        )

        # def geocode(self, address):
        #     """
        #         Wrapper to geocode binding, for readability
        #     Args:
        #         address: (string) the raw address from source
        #     Returns:
        #         Not sure yet
        #
        #     """
        #     return self.gmap.geocode(address)
