import pandas as pd
import matplotlib.pyplot as plt
import json
from typing import List, Dict, Union


def make_data_frame(file_name: str) -> pd.DataFrame:
    top_100_songs_data_frame: pd.DataFrame = pd.read_csv(file_name)
    return top_100_songs_data_frame


def day_month_year_format(date: str) -> str:
    """Данная функция принимает строку-дату из столбца Date 
    и возвращает дату в единном виде:
    "day (day's number) month (month's name) year (four-digit number)".
    Дата вида "1 January 2001" остаётся без измений.
    Дата вида "1.January.01" приводится к виду "1 January 2001".
    Если последние 2 цифры (цифры года) больше 23, это означает,
    что песня выпущена в 20 веке:
    дата вида "1.January.22" приведётся к виду "1 January 2022",
    а дата вида "1.January.70" - к виду "1 January 1970"."""
    final_date: str = date
    if '.' in date:
        second_dot_index: int = date.rfind('.')
        if int(date[date.rfind('.') + 1:]) > 23:
            date_with_fourdigit_year: str = date.replace(
                date[second_dot_index + 1:], '19' + date[second_dot_index + 1:])
        else:
            date_with_fourdigit_year: str = date.replace(
                date[second_dot_index + 1:], '20' + date[second_dot_index + 1:])
        final_date: str = date_with_fourdigit_year.replace('.', ' ')
    return final_date


def get_ed_sheeran_songs(data_frame: pd.DataFrame) -> List[str]:
    """Данная функция возвращает список песен из data_frame,
    которые исполняет Ed Sheeran (в том числе с кем-то)."""
    ed_sheeran_songs_list: List[str] = list(
        data_frame[data_frame.Artist.str.startswith('Ed Sheeran')]['Song'])
    return ed_sheeran_songs_list


def get_the_oldest_songs(data_frame: pd.DataFrame) -> List[str]:
    """Данная функция возвращает список из 3 самых старых песен в data_frame."""
    songs_dates: pd.DataFrame = data_frame['Release Date']
    years_indexes: List[int] = []
    the_oldest_songs_list: List[str] = []
    songs_years: List[str] = [day_month_year_format(songs_date)[-4:] 
                              for songs_date in list(songs_dates)]
    for year in sorted(songs_years):
        if len(years_indexes) < 3:
            years_indexes.append(songs_years.index(year))
    for index in years_indexes:
        the_oldest_songs_list.append(data_frame['Song'][index])
    return the_oldest_songs_list


def get_total_streams_for_artist(data_frame: pd.DataFrame) -> Dict[str, float]:
    """Данная функция возвращает словарь, где ключом является исполнитель,
    а значением - суммарное количество прослушиваний у этого исполнителя
    в миллиардах из data_frame."""
    artist_total_streams_dict: Dict[str, float] = {}
    for artist in data_frame.Artist.unique():
        streams_list: List[str] = list(data_frame['Streams (Billions)']
                                       [(data_frame.Artist == artist)])
        new_streams_list: List[float] = [float(stream.replace(',', '.')) 
                                         for stream in streams_list]
        sum_of_streams: float = round(sum(new_streams_list), 3)
        artist_total_streams_dict[artist] = sum_of_streams
    return artist_total_streams_dict


def write_result_in_json(data_frame: pd.DataFrame):
    """Данная функция записывает результаты функций
    get_ed_sheeran_songs(),
    get_the_oldest_songs(),
    get_total_streams_for_artist()
    в файл формата .json."""
    result: Dict[str, Union[List[str], Dict[str, float]]] = {
     'All songs performed by Ed Sheeran (including with someone)':
     get_ed_sheeran_songs(data_frame),
     'The three oldest songs':
     get_the_oldest_songs(data_frame),
     'Total number of streams for each artist (Billions)':
     get_total_streams_for_artist(data_frame)
    }

    with open("result.json", "w") as json_file:
        json.dump(result, json_file, indent=2)


def make_number_of_songs_by_year_histogram(data_frame: pd.DataFrame):
    """Данная функция рисует гистограмму количества популярых песен
    в зависимости от года выпуска и сохраняет её как .png файл."""
    songs_release_dates: List[str] = list(data_frame['Release Date'])
    formatted_songs_release_dates: List[str] = [day_month_year_format(date) 
                                                for date in songs_release_dates]
    songs_release_years: List[str] = [date[-4:] 
                                      for date in formatted_songs_release_dates]
    plt.figure(figsize=(10, 5))
    plt.hist(sorted(songs_release_years), bins=60)
    plt.title('Number of songs by year')
    plt.xlabel('Year')
    plt.ylabel('Number of songs')
    plt.savefig('Number of songs by year.png')


def main():
    new_data_frame: pd.DataFrame = make_data_frame('spotify_songs_top_100.csv')
    get_ed_sheeran_songs(new_data_frame)
    get_the_oldest_songs(new_data_frame)
    get_total_streams_for_artist(new_data_frame)
    write_result_in_json(new_data_frame)
    make_number_of_songs_by_year_histogram(new_data_frame)


main()
