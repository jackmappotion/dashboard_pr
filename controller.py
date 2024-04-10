import pandas as pd

time_columns=['5시30분', '6시00분', '6시30분','7시00분', '7시30분', '8시00분', '8시30분', '9시00분', '9시30분',
 '10시00분', '10시30분', '11시00분', '11시30분', '12시00분', '12시30분', '13시00분', '13시30분',
 '14시00분', '14시30분', '15시00분', '15시30분', '16시00분', '16시30분', '17시00분','17시30분',
 '18시00분', '18시30분', '19시00분', '19시30분', '20시00분', '20시30분','21시00분', '21시30분',
 '22시00분', '22시30분', '23시00분', '23시30분', '00시00분','00시30분', '01시00분']


class Controller:
    def __init__(self, df) -> None:
        self.df = df

    def find_station_number(
        self, weekday_type, line_number, station_name, way
    ):
        df = self.df.copy()
        station_number = df[
            (df["요일구분"] == weekday_type)
            & (df["호선"] == line_number)
            & (df["출발역"] == station_name)
            & (df["상하구분"] == way)
        ]["역번호"].iloc[0]
        return station_number

    @staticmethod
    def get_station_numbers(station_number, way):
        if way == "상선":
            station_numbers = [station_number + i for i in range(-1, 5)]
        elif way == "하선":
            station_numbers = [station_number - i for i in range(-1, 5)]
        return station_numbers

    def filter_using_df(self, station_numbers, way, weekday_type):
        df = self.df.copy()
        using_df = df[
            (df["역번호"].isin(station_numbers))
            & (df["상하구분"] == way)
            & (df["요일구분"] == weekday_type)
        ].copy()
        if way == "상선":
            using_df.sort_values("역번호", inplace=True)

        elif way == "하선":
            using_df.sort_values("역번호", ascending=False, inplace=True)
        return using_df

    @staticmethod
    def format_final_df(using_df):
        final_df = using_df.set_index("출발역").loc[:, time_columns].T
        return final_df

    def __call__(self, line_number, station_name, way, weekday_type):
        station_number = self.find_station_number(
            weekday_type, line_number, station_name, way
        )
        station_numbers = self.get_station_numbers(station_number, way)
        using_df = self.filter_using_df(station_numbers, way, weekday_type)
        final_df = self.format_final_df(using_df)
        return final_df
