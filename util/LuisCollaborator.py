import requests


class LuisCollaborator:
    app_id = ""
    prediction_key = ""

    def __init__(self, app_id, prediction_key) -> None:
        self.app_id = app_id
        self.prediction_key = prediction_key

    def analyze_message(self, msg):
        try:

            ##########
            # Values to modify.

            # YOUR-APP-ID: The App ID GUID found on the www.luis.ai Application Settings page.
            appId = 'YOUR-APP-ID'

            # YOUR-PREDICTION-KEY: Your LUIS authoring key, 32 character value.
            prediction_key = 'YOUR-PREDICTION-KEY'

            # YOUR-PREDICTION-ENDPOINT: Replace with your authoring key endpoint.
            # For example, "https://westus.api.cognitive.microsoft.com/"
            prediction_endpoint = 'https://YOUR-PREDICTION-ENDPOINT/'
            # The headers to use in this REST call.
            headers = {
            }

            # The URL parameters to use in this REST call.
            params = {
                'query': msg,
                'timezoneOffset': '0',
                'verbose': 'true',
                'show-all-intents': 'true',
                'spellCheck': 'false',
                'staging': 'false',
                'subscription-key': self.prediction_key
            }

            response = requests.get(
                f'{prediction_endpoint}luis/prediction/v3.0/apps/{self.app_id}/slots/production/predict',
                headers=headers, params=params)

            print(response.json())
            return response.json()


        except Exception as e:
            # Display the error string.
            print(f'{e}')
