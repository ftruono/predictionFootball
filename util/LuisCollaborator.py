import requests

import config


class LuisCollaborator:

    def analyze_message(self, msg):
        # The URL parameters to use in this REST call.
        params = {
            'query': msg,
            'timezoneOffset': '0',
            'verbose': 'true',
            'show-all-intents': 'true',
            'spellCheck': 'false',
            'staging': 'false',
            'subscription-key': config.DefaultConfig.LUIS_KEY1
        }

        response = requests.get(
            f'{config.DefaultConfig.LUIS_ENDPOINT}luis/prediction/v3.0/apps/{config.DefaultConfig.LUIS_APPID}/slots/production/predict',
            headers={}, params=params)

        json_result = response.json()
        return json_result["prediction"]["topIntent"], self.__analyze_entities__(
            json_result["prediction"]["entities"])

    def __analyze_entities__(self, entities):
        if entities:
            if "Teams" in entities and len(entities["Teams"]) > 1:
                return entities["Teams"][0], entities["Teams"][1]
            elif "number" in entities:
                return entities["number"][0]
        else:
            return {}
