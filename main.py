import io

import pandas as pd
from itertools import takewhile
from typing import NamedTuple
from enum import StrEnum
import textwrap

sample_text = """
What is Lorem Ipsum?
Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

Why do we use it?
It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).


Where does it come from?
Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem

"""

wrapper = textwrap.TextWrapper(width=50)

original = wrapper.fill(text=textwrap.dedent(text=sample_text))

# print('Original:\n')
# print(original)

shortened_wrapped = wrapper.fill(text=textwrap.shorten(text=original, width=200))
#
# print('\nShortened:\n')
# print(shortened_wrapped)

from itertools import groupby
from operator import itemgetter
# employees = [
#     ("Alice", "Engineering"),
#     ("Markus", "Engineering"),
#     ("Alan", "Engineering"),
#     ("Bob", "Marketing"),
#     ("Charlie", "Engineering"),
#     ("Diana", "HR"),
#     ("John", "HR"),
#     ("Amy", "HR"),
#     ("Evan", "Marketing"),
#     ("Alukar", "Marketing"),
# ]
#
# department_group = dict(key=itemgetter(1))
# employees.sort(**department_group)
# for department, group in groupby(employees, **department_group):
#     print(f"\n{department} Department:")
#     emp_grouped = [n for n in list(group)]
#     names = sorted([n[0] for n in emp_grouped])
#     [print(f"  - {name}") for name in names]
#


class Person(NamedTuple):
    firstname: str
    lastname: str


class Columns(StrEnum):
    FirstName = "FirstName"
    LastName = "LastName"


html_tag = lambda tag: lambda message: f'<{tag}>{message}</{tag}>'
no_rewards: str = 'No Reward'


def patron_list(names: list[str]) -> str:
    li = html_tag('li')
    patrons = (f'\n\t{li(name)}' for name in names)
    return ''.join(patrons)


def create_patron_html(names: list[str]) -> str:
    return textwrap.dedent(f"""
        <p>There are currently {len(names)} public contributors. Thank You!</p>
        <ul>{patron_list(names)}</ul>
            """.strip())


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
    # show_patrons()


if __name__ == '__main__':
    main()
