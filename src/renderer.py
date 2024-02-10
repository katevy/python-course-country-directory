"""
Функции для формирования выходной информации.
"""

from decimal import ROUND_HALF_UP, Decimal

from tabulate import tabulate

from collectors.models import LocationInfoDTO


class Renderer:
    """
    Генерация результата преобразования прочитанных данных.
    """

    def __init__(self, location_info: LocationInfoDTO) -> None:
        """
        Конструктор.

        :param location_info: Данные о географическом месте.
        """

        self.location_info = location_info

    async def render(self) -> str:
        """
        Форматирование прочитанных данных.

        :return: Результат форматирования
        """

        location = [
            ["Страна", self.location_info.location.name],
            ["Регион", self.location_info.location.subregion],
            ["Языки", await self._format_languages()],
            ["Население страны", f"{await self._format_population()} чел."],
            ["Площадь", f"{self.location_info.location.area} кв. км."],
            ["Курсы валют", await self._format_currency_rates()],
        ]

        capital = [
            ["Столица", self.location_info.location.capital],
            ["Широта", self.location_info.location.latitude],
            ["Долгота", self.location_info.location.longitude],
        ]

        weather = [
            ["Время получения данных", f"{self.location_info.weather.date_time}"],
            ["Температура", f"{self.location_info.weather.temp} °C"],
            ["Давление", f"{self.location_info.weather.pressure}"],
            ["Видимость", f"{self.location_info.weather.visibility}"],
            ["Скорость ветра", f"{self.location_info.weather.wind_speed}"],
            ["Влажность", f"{self.location_info.weather.humidity}"],
        ]

        news = []
        for n in self.location_info.news:
            news.append(
                [n.source, n.author or "", n.published_at, n.title, n.description]
            )

        headers = ["Источник", "Автор", "Дата публикации", "Название", "Описание"]

        news_table = tabulate(news, headers=headers, tablefmt="grid")

        location_table = tabulate(location, tablefmt="grid")
        capital_table = tabulate(capital, tablefmt="grid")
        weather_table = tabulate(weather, tablefmt="grid")

        return location_table, capital_table, weather_table, news_table

    async def _format_languages(self) -> str:
        """
        Форматирование информации о языках.

        :return:
        """

        return ", ".join(
            f"{item.name} ({item.native_name})"
            for item in self.location_info.location.languages
        )

    async def _format_population(self) -> str:
        """
        Форматирование информации о населении.

        :return:
        """

        # pylint: disable=C0209
        return "{:,}".format(self.location_info.location.population).replace(",", ".")

    async def _format_currency_rates(self) -> str:
        """
        Форматирование информации о курсах валют.

        :return:
        """

        return ", ".join(
            f"{currency} = {Decimal(rates).quantize(exp=Decimal('.01'), rounding=ROUND_HALF_UP)} руб."
            for currency, rates in self.location_info.currency_rates.items()
        )
