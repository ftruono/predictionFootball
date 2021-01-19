import requests

import config
from util.ExtractorInfo import ExtractorInfo


class PredictionCollaborator:
    extractor_info: ExtractorInfo
    json_data = ""

    def __init__(self, json, extractor_info: ExtractorInfo) -> None:
        super().__init__()
        self.json_data = json
        self.extractor_info = extractor_info

    def predict_match(self, home, away):
        if (isinstance(home, str) and isinstance(away, str)):
            home, away = self.__format_teams__(home, away)
        else:
            home, away = self.__format_teams__(home[0], away[0])
        self.extractor_info.set_away(away)
        self.extractor_info.set_home(home)
        error = self.extractor_info.check_if_is_a_valids_teams()
        if (len(error["validation"]) > 0):
            validation_message = ""
            for err in error["validation"]:
                validation_message += "Squadra: " + err + " non valida \n\n"
            return validation_message
        else:
            rate_home, rate_away, shot_home, shot_away, shot_target_home, shot_target_away, ph_home, ph_away = self.extractor_info.calculate_features()
            payload = {
                "data": [self.json_data["home_teams"][home], self.json_data["away_teams"][away], shot_home,
                         shot_away,
                         shot_target_home, shot_target_away, rate_home, rate_away, ph_home, ph_away]}
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            result_http = requests.post(config.DefaultConfig.MODEL_LINK_PREDICTION, json=payload,
                                        headers=headers)
            result_prod = result_http.json()["predict_proba"]
            winner = self.__who_win__(result_prod)
            return self.__format_result_string__(result_prod, winner, home, away)

    def __format_teams__(self, home, away):
        return home.strip().capitalize(), away.strip().capitalize()

    def __format_result_string__(self, list, winner, home, away):
        final = ""
        if (winner == 0):
            final = "Vittoria per " + away + "\n\n"
        elif (winner == 1):
            final = "Pareggio \n\n"
        else:
            final = "Vittoria per " + home + "\n\n"

        final += "Percentuali: \n\n"
        final += home + " " + str(round(list[-1] * 100, 2)) + "%\n\n"
        final += away + " " + str(round(list[0] * 100, 2)) + "%\n\n"
        final += "Pareggio " + str(round(list[1] * 100, 2)) + "%\n\n"
        return final

    @staticmethod
    def __who_win__(list):
        return list.index(max(list))
