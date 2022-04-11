import re

intervals = {
    "год": 3.154e+7,
    "месяц": 2.628e+6,
    "неделя": 604800,
    "день": 86400,
    "час": 3600,
    "минута": 60,
    "секунда": 1,

    "г": 3.154e+7,
    "мес": 2.628e+6,
    "нед": 604800,
    "дн": 86400,
    "ч": 3600,
    "мин": 60,
    "сек": 1,

    "м": 60,
    "с": 1,
}


def parse_interval(text: str) -> int:
    unix = 0

    tags = re.findall(r'(\d+)([. ]|)(год|месяц|неделя|день|час|минута|секунда|мес|нед|дн|мин|сек|г|ч|м|с|)', text)
    for k, _, v in tags:
        if not k:
            continue
        try:
            unix += int(k) * intervals[v]
        except KeyError:
            continue
    return unix


def parse_cron_text(cron: str) -> dict:
    """Парс CRON выражения для планировщика задач"""
    second, minute, hour, day, month, day_of_week, year = cron.split(' ')
    return {
        key: value
        for key, value in dict(
            second=second, minute=minute,
            hour=hour, day=day,
            month=month, day_of_week=day_of_week,
            year=year
        ).items()
        if value != "?"
    }
