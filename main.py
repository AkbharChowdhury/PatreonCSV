import pandas as pd
from itertools import takewhile
from typing import NamedTuple
from enum import StrEnum


class Person(NamedTuple):
    firstname: str
    lastname: str


class Columns(StrEnum):
    FirstName = "FirstName"
    LastName = "LastName"

html_tag = lambda tag: lambda message: f'<{tag}>{message}</{tag}>'
no_rewards: str = 'No Reward'


def get_list_html(names: list[str]) -> str:
    li = html_tag('li')
    patrons: list[str] = [f'\n\t{li(name)}' for name in names]
    return ''.join(patrons)


def create_patron_html(names: list[str]) -> str:
    return f"""
        <p>There are currently {len(names)} public contributors. Thank You!</p>\
        \n<ul>{get_list_html(names)}</ul>
            """.strip()


def show_patrons():
    patrons_data = pd.read_csv('patrons.csv', usecols=['FirstName', 'LastName'], skiprows=[1])
    filtered_patrons = takewhile(lambda row: row.FirstName != no_rewards, patrons_data.itertuples())
    patron_names = [f'{row.FirstName},{row.LastName}' for row in filtered_patrons]
    patrons_details = create_patron_html(patron_names)
    print(patrons_details)


def pythonic_patrons():
    columns = [column.value for column in Columns]
    df = pd.read_csv('patrons.csv', usecols=[*columns], skiprows=[1], index_col=Columns.FirstName)
    filtered_patrons: pd.DataFrame = df.loc[:no_rewards][:-1]
    filtered_patrons.reset_index(drop=False, inplace=True)
    patron_names: list[str] = filtered_patrons.loc[:, ["FirstName", "LastName"]].values.tolist()
    people: list[Person] = [Person(*person) for person in patron_names]
    names: list[str] = [f"{person.firstname} {person.lastname}" for person in people]
    patrons_summary: str = create_patron_html(names=names)
    print(patrons_summary)


def main():
    pythonic_patrons()
    show_patrons()


if __name__ == '__main__':
    main()
