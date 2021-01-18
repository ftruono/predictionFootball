import datetime

import pandas as pd
from pandas import DataFrame


class ExtractorInfo:
    __csvData__: DataFrame
    home = ""
    away = ""

    def __init__(self, csvData: DataFrame) -> None:
        super().__init__()
        self.__csvData__ = csvData

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
        n_match = self.__csvData__.loc[(self.__csvData__["HomeTeam"] == team) | (self.__csvData__["AwayTeam"] == team)][
            "FTR"].count()
        win_home = self.__csvData__.loc[(self.__csvData__["HomeTeam"] == team) & (self.__csvData__["FTR"] == 'H')][
            "FTR"].count()
        win_away = self.__csvData__.loc[(self.__csvData__["AwayTeam"] == team) & (self.__csvData__["FTR"] == 'A')][
            "FTR"].count()
        return round((win_home + win_away) * 100 / n_match, 1)

    def __avg_shots__(self, team):
        n_match = self.__csvData__.loc[(self.__csvData__["HomeTeam"] == team) | (self.__csvData__["AwayTeam"] == team)][
            "FTR"].count()
        shot_home = self.__csvData__.loc[(self.__csvData__["HomeTeam"] == team)]["HS"].sum()
        shot_away = self.__csvData__.loc[(self.__csvData__["AwayTeam"] == team)]["AS"].sum()
        return int((shot_away + shot_home) / n_match)

    def __avg_shots_on_target__(self, team):
        n_match = self.__csvData__.loc[(self.__csvData__["HomeTeam"] == team) | (self.__csvData__["AwayTeam"] == team)][
            "FTR"].count()
        shot_home = self.__csvData__.loc[(self.__csvData__["HomeTeam"] == team)]["HST"].sum()
        shot_away = self.__csvData__.loc[(self.__csvData__["AwayTeam"] == team)]["AST"].sum()
        return int((shot_away + shot_home) / n_match)

    def __performance_last_five__(self, team):
        last_five = self.__csvData__.loc[
            (self.__csvData__["HomeTeam"] == team) | (self.__csvData__["AwayTeam"] == team)].tail(5)
        home_win = last_five.loc[(last_five["HomeTeam"] == team) & (last_five["FTR"] == 'H')]["FTR"].count().tolist()
        away_win = last_five.loc[(last_five["AwayTeam"] == team) & (last_five["FTR"] == 'A')]["FTR"].count().tolist()

        home_lost = last_five.loc[(last_five["HomeTeam"] == team) & (last_five["FTR"] == 'A')]["FTR"].count().tolist()
        away_lost = last_five.loc[(last_five["AwayTeam"] == team) & (last_five["FTR"] == 'H')]["FTR"].count().tolist()
        return ((home_win + away_win) - ((home_lost + away_lost)))

    def check_if_is_a_valids_teams(self):
        valid = {"validation": []}
        if (self.__csvData__.loc[self.__csvData__["HomeTeam"] == self.home].size == 0):
            valid["validation"].append(self.home)
        if (self.__csvData__.loc[self.__csvData__["AwayTeam"] == self.away].size == 0):
            valid["validation"].append(self.away)
        return valid

    def get_stats(self, year):
        if (len(year) < 4):
            year = '20' + year[-2:]
        year = int(year)
        down_year = datetime.datetime(year=year, month=1, day=1)
        up_year = datetime.datetime(year=year + 1, month=7, day=31)

        self.__csvData__["Date"] = pd.to_datetime(self.__csvData__['Date'])
        restricted_year = self.__csvData__.loc[6
            (self.__csvData__["Date"] > down_year) & (self.__csvData__["Date"] < up_year)]

        restricted_year['Home_Points'] = restricted_year.apply(
            lambda row: 3 if row['FTR'] == 'H' else 0 if row['FTR'] == 'A' else 1,
            axis=1)
        restricted_year['Away_Points'] = restricted_year.apply(
            lambda row: 3 if row['FTR'] == 'A' else 0 if row['FTR'] == 'H' else 1,
            axis=1)

        goal_home_s = restricted_year.groupby("HomeTeam").agg({"FTAG": "sum"})
        goal_away_s = restricted_year.groupby("AwayTeam").agg({"FTHG": "sum"})
        goal_home_d = restricted_year.groupby("HomeTeam").agg({"FTHG": "sum"})
        goal_away_d = restricted_year.groupby("AwayTeam").agg({"FTAG": "sum"})
        goal_home_s.rename(columns={'FTAG': 'GS'}, inplace=True)
        goal_away_s.rename(columns={'FTHG': 'GS'}, inplace=True)
        goal_home_d.rename(columns={'FTHG': 'GS'}, inplace=True)
        goal_away_d.rename(columns={'FTAG': 'GS'}, inplace=True)

        total_home = restricted_year.groupby(["HomeTeam"])["HomeTeam"].count()
        total_away = restricted_year.groupby(["AwayTeam"])["AwayTeam"].count()

        home = pd.DataFrame(restricted_year[['HomeTeam', 'Home_Points']])
        away = pd.DataFrame(restricted_year[['AwayTeam', 'Away_Points']])
        home = home.groupby('HomeTeam').agg(sum)
        away = away.groupby('AwayTeam').agg(sum)
        home.rename(columns={'HomeTeam': 'Team', 'Home_Points': 'Point'}, inplace=True)
        away.rename(columns={'AwayTeam': 'Team', 'Away_Points': 'Point'}, inplace=True)

        overall = home + away
        overall["Home_Points"] = home["Point"]
        overall["Away_Points"] = away["Point"]
        overall["goal_d_total"] = goal_home_d + goal_away_d
        overall["goal_s_total"] = goal_home_s + goal_away_s

        overall["Matchs"] = total_home + total_away

        overall = overall.sort_values(by=['Point'], ascending=False)
        return overall
