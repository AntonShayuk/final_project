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


assert day_month_year_format('10.May.01') == '10 May 2001'
assert day_month_year_format('5 April 2001') == '5 April 2001'
assert day_month_year_format('09.October.99') == '09 October 1999'
assert day_month_year_format('01 September 1999') == '01 September 1999'
assert day_month_year_format('1.March.91') == '1 March 1991'
assert day_month_year_format('31.August.78') == '31 August 1978'
assert day_month_year_format('19.January.23') == '19 January 2023'
assert day_month_year_format('20.February.70') == '20 February 1970'
assert day_month_year_format('29.June.24') == '29 June 1924'
assert day_month_year_format('9 July 2000') == '9 July 2000'
assert day_month_year_format('30.November.09') == '30 November 2009'
assert day_month_year_format('3 December 2025') == '3 December 2025'
