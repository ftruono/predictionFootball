# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json

from botbuilder.core import ActivityHandler, TurnContext, CardFactory
from botbuilder.schema import ChannelAccount, Attachment, Activity
from pandas import DataFrame

from dialogs.adaptive_card_predict import ADAPTIVE_CARD_CONTENT
from util.BingCollaborator import BingCollaborator
from util.ExtractorInfo import ExtractorInfo
from util.LuisCollaborator import LuisCollaborator
from util.PredictionCollaborator import PredictionCollaborator


class MyBot(ActivityHandler):
    csvData: DataFrame
    extractor_info: ExtractorInfo
    luis: LuisCollaborator
    prediction: PredictionCollaborator
    bing: BingCollaborator

    def __init__(self, csvData: DataFrame):
        super().__init__()
        self.csvData = csvData
        self.extractor_info = ExtractorInfo(self.csvData)
        with open('resource/metadata.json') as f:
            self.json_data = json.load(f)

        self.prediction = PredictionCollaborator(self.json_data, self.extractor_info)
        self.luis = LuisCollaborator()
        self.bing = BingCollaborator()

    async def on_message_activity(self, turn_context: TurnContext):
        if turn_context.activity.value:
            if (turn_context.activity.value["home"] and turn_context.activity.value["away"]):
                result = self.prediction.predict_match(turn_context.activity.value["home"],
                                                       turn_context.activity.value["away"])
                await turn_context.send_activity(result)
            else:
                await  turn_context.send_activity("Manca una squadra!")

        if (turn_context.activity.text == '/list'):
            await  turn_context.send_activity(self.load_teams())
        elif (turn_context.activity.text == '/predict'):
            response = Activity(type='message', attachments=[self.create_adaptive_card()])
            await turn_context.send_activity(response)
        else:
            intent, entities = self.luis.analyze_message(turn_context.activity.text)
            await turn_context.send_activity(self.handle_luis_intent(intent, entities))

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
        all_teams = self.csvData.HomeTeam.unique()
        str = ""
        for t in all_teams:
            str += t + "\n\n"
        return str

    def handle_luis_intent(self, intent, entities):
        if (intent == 'list'):
            return self.load_teams()
        elif (intent == 'predict'):
            if (entities is None):
                return "Manca una squadra"
            return self.prediction.predict_match(entities[0],
                                                 entities[1])
        elif (intent == 'stats'):
            if (not entities and entities>3000):
                return "Formato anno non corretto"
            return self.extractor_info.get_stats(str(entities))
        elif (intent == 'matchs'):
            return self.bing.get_link_matchs()
        else:
            return "LUIS non ha riconosciuto nessun pattern nella tua frase!"
