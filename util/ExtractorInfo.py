import pandas as pd
from azureml.core import Dataset
from pandas import DataFrame


class ExtractorInfo:
    __csvData__: DataFrame
    __home__ = ""
    __away__ = ""

    def __init__(self, csvData: DataFrame) -> None:
        super().__init__()
        self.csvData = csvData

    def set_home(self, home):
        self.home = home

    def set_away(self, away):
        self.away = away

    def calculate_features(self):
        rate_home = self.__winningRate__(self.home)
        rate_away = self.__winningRate__(self.away)
        shot_home = self.__avg_shots__(self.home)
        show_away = self.__avg_shots__(self.away)
        shot_target_home = self.__avg_shots_on_target__(self.home)
        shot_target_away = self.__avg_shots_on_target__(self.away)
        ph_home = self.__performance_last_five__(self.home)
        ph_away = self.__performance_last_five__(self.away)
        return rate_home, rate_away, shot_home, show_away, shot_target_home, shot_target_away, ph_home, ph_away

    def __winningRate__(self, team):
        n_match = self.csvData.loc[(self.csvData["HomeTeam"] == team) | (self.csvData["AwayTeam"] == team)][
            "FTR"].count()
        win_home = self.csvData.loc[(self.csvData["HomeTeam"] == team) & (self.csvData["FTR"] == 'H')]["FTR"].count()
        win_away = self.csvData.loc[(self.csvData["AwayTeam"] == team) & (self.csvData["FTR"] == 'A')]["FTR"].count()
        return round((win_home + win_away) * 100 / n_match, 1)

    def __avg_shots__(self, team):
        n_match = self.csvData.loc[(self.csvData["HomeTeam"] == team) | (self.csvData["AwayTeam"] == team)][
            "FTR"].count()
        shot_home = self.csvData.loc[(self.csvData["HomeTeam"] == team)]["HS"].sum()
        shot_away = self.csvData.loc[(self.csvData["AwayTeam"] == team)]["AS"].sum()
        return int((shot_away + shot_home) / n_match)

    def __avg_shots_on_target__(self, team):
        n_match = self.csvData.loc[(self.csvData["HomeTeam"] == team) | (self.csvData["AwayTeam"] == team)][
            "FTR"].count()
        shot_home = self.csvData.loc[(self.csvData["HomeTeam"] == team)]["HST"].sum()
        shot_away = self.csvData.loc[(self.csvData["AwayTeam"] == team)]["AST"].sum()
        return int( (shot_away + shot_home) / n_match)

    def __performance_last_five__(self, team):
        last_five = self.csvData.loc[(self.csvData["HomeTeam"] == team) | (self.csvData["AwayTeam"] == team)].tail(5)
        home_win = last_five.loc[(last_five["HomeTeam"] == team) & (last_five["FTR"] == 'H')]["FTR"].count().tolist()
        away_win = last_five.loc[(last_five["AwayTeam"] == team) & (last_five["FTR"] == 'A')]["FTR"].count().tolist()

        home_lost = last_five.loc[(last_five["HomeTeam"] == team) & (last_five["FTR"] == 'A')]["FTR"].count().tolist()
        away_lost = last_five.loc[(last_five["AwayTeam"] == team) & (last_five["FTR"] == 'H')]["FTR"].count().tolist()
        return ((home_win + away_win) - ((home_lost + away_lost)))

    def check_if_is_a_valids_teams(self):
        valid = {"validation": []}
        if (self.csvData.loc[self.csvData["HomeTeam"] == self.home].size == 0):
            valid["validation"].append(self.home)
        if (self.csvData.loc[self.csvData["AwayTeam"] == self.away].size == 0):
            valid["validation"].append(self.away)
        return valid
