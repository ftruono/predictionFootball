# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json

import requests
from botbuilder.core import ActivityHandler, TurnContext, CardFactory
from botbuilder.schema import ChannelAccount, Attachment, Activity
from pandas import DataFrame

import config
from dialogs.adaptive_card_predict import ADAPTIVE_CARD_CONTENT
from util.ExtractorInfo import ExtractorInfo


class MyBot(ActivityHandler):
    csvData: DataFrame
    extractorInfo: ExtractorInfo

    def __init__(self, csvData: DataFrame) -> None:
        super().__init__()
        self.csvData = csvData
        self.extractorInfo = ExtractorInfo(self.csvData)
        # with open('resource/metadata.json') as f:
        #   self.json_data = json.load(f)

    async def on_message_activity(self, turn_context: TurnContext):
        if turn_context.activity.value:
            if (turn_context.activity.value["home"] and turn_context.activity.value["away"]):

                home, away = format_teams(turn_context.activity.value["home"], turn_context.activity.value["away"])
                self.extractorInfo.set_away(away)
                self.extractorInfo.set_home(home)
                error = self.extractorInfo.check_if_is_a_valids_teams()
                if (len(error["validation"]) > 0):
                    str = ""
                    for err in error["validation"]:
                        str += "Squadra: " + err + " non valida \n\n"
                    await turn_context.send_activity(str)
                else:
                    rate_home, rate_away, shot_home, shot_away, shot_target_home, shot_target_away, ph_home, ph_away = self.extractorInfo.calculate_features()
                    payload = {
                        "data": [self.json_data["home_teams"][home], self.json_data["away_teams"][away], shot_home,
                                 shot_away,
                                 shot_target_home, shot_target_away, rate_home, rate_away, ph_home, ph_away]}
                    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
                    result_http = requests.post(config.DefaultConfig.MODEL_LINK_PREDICTION, json=payload,
                                                headers=headers)
                    result_prod = result_http.json()["predict_proba"]
                    winner = who_win(self, result_prod)
                    await turn_context.send_activity(format_result_string(self, result_prod, winner, home, away))
            else:
                await  turn_context.send_activity("Manca una squadra!")

        if (turn_context.activity.text == '/list'):
            all_teams = load_teams(self)
            str = ""
            for t in all_teams:
                str += t + "\n\n"
            await  turn_context.send_activity(str)
        elif (turn_context.activity.text == '/predict'):
            response = Activity(type='message', attachments=[create_adaptive_card(self)])
            await turn_context.send_activity(response)

        # await turn_context.send_activity(f"You said '{turn_context.activity.text}'")

    async def on_members_added_activity(
            self,
            members_added: ChannelAccount,
            turn_context: TurnContext
    ):

        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "Benvenuto sul bot \n\n Per vedere la lista delle squadre: /list \n\n Per eseguire una predizione /predict")


def format_teams(home, away):
    return home.strip().capitalize(), away.strip().capitalize()


def create_adaptive_card(self) -> Attachment:
    return CardFactory.adaptive_card(ADAPTIVE_CARD_CONTENT)


def load_teams(self):
    return self.csvData.HomeTeam.unique()


def who_win(self, list):
    return list.index(max(list))


def format_result_string(self, list, winner, home, away):
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
