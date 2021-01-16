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
from util.LuisCollaborator import LuisCollaborator
from util.PredictionCollaborator import PredictionCollaborator


class MyBot(ActivityHandler):
    csvData: DataFrame
    extractor_info: ExtractorInfo
    luis: LuisCollaborator
    prediction: PredictionCollaborator

    def __init__(self, csvData: DataFrame):
        super().__init__()
        self.csvData = csvData
        self.extractor_info = ExtractorInfo(self.csvData)
        with open('resource/metadata.json') as f:
            self.json_data = json.load(f)

        self.prediction = PredictionCollaborator(self.json_data, self.extractor_info)

    async def on_message_activity(self, turn_context: TurnContext):
        if turn_context.activity.value:
            if (turn_context.activity.value["home"] and turn_context.activity.value["away"]):
                result = self.prediction.predict_match(turn_context.activity.value["home"],
                                                       turn_context.activity.value["away"])
                await turn_context.send_activity(result)
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
        else:

    # TODO call on luis-collaborator

    async def on_members_added_activity(
            self,
            members_added: ChannelAccount,
            turn_context: TurnContext
    ):

        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "Benvenuto sul bot \n\n Per vedere la lista delle squadre: /list \n\n Per eseguire una predizione /predict")


def create_adaptive_card(self) -> Attachment:
    return CardFactory.adaptive_card(ADAPTIVE_CARD_CONTENT)


def load_teams(self):
    return self.csvData.HomeTeam.unique()
