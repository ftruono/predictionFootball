import requests

import config


class BingCollaborator:

    def get_link_matchs(self):
        # The headers to use in this REST call.
        headers = {
            "Ocp-Apim-Subscription-Key": config.DefaultConfig.BING_KEY
        }
        end_point = config.DefaultConfig.BING_ENDPOINT

        # The URL parameters to use in this REST call.
        params = {
            'q': "prossime partite seria A"
        }

        response = requests.get(
            end_point,
            headers=headers, params=params)

        search_results = response.json()
        str = ""
        limited = search_results["webPages"]["value"][:3]
        for value in limited:
            str += value["name"] + " - " + value["url"] + "\n\n"

        return str
