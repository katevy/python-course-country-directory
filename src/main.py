"""
Запуск приложения.
"""

import asyncclick as click

from reader import Reader
from renderer import Renderer


@click.command()
@click.option(
    "--location",
    "-l",
    "location",
    type=str,
    help="Страна и/или город",
    prompt="Страна и/или город",
)
async def process_input(location: str) -> None:
    """
    Поиск и вывод информации о стране, погоде и курсах валют.

    :param str location: Страна и/или город
    """

    location_info = await Reader().find(location)
    if location_info:
        location_table, capital_table, weather_table, news_table = await Renderer(
            location_info
        ).render()

        click.secho("Информация о cтране:", fg="green")
        click.secho(location_table)

        click.secho("\nИнформация о столице:", fg="green")
        click.secho(capital_table)

        click.secho("\nИнформация о погоде:", fg="green")
        click.secho(weather_table)

        click.secho("\nНовости:", fg="green")
        click.secho(news_table)

    else:
        click.secho("Информация отсутствует.", fg="yellow")


if __name__ == "__main__":
    # запуск обработки входного файла
    # pylint: disable=E1120
    process_input(_anyio_backend="asyncio")
