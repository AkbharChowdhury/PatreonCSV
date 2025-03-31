import pandas as pd
from itertools import takewhile


html_tag = lambda tag: lambda message: f'<{tag}>{message}</{tag}>'

def get_list_html(names: list[str]):
    li = html_tag('li')
    patrons_list = [f'\n\t{li(name)}' for name in names]
    return ''.join(patrons_list)


def create_patron_html(names: list[str]) -> str:
    return f"""
        <p>There are currently {len(names)} public contributors. Thank You!</p>\
        \n<ul>{get_list_html(names)}</ul>
            """.strip()


def show_patrons():
    patrons_data = pd.read_csv('patrons.csv', usecols=['FirstName', 'LastName'], skiprows=[1])
    filtered_patrons = takewhile(lambda row: row.FirstName != 'No Reward', patrons_data.itertuples())
    patron_names = [f'{row.FirstName},{row.LastName}' for row in filtered_patrons]
    patrons_details = create_patron_html(patron_names)
    print(patrons_details)


def main():
    show_patrons()


if __name__ == '__main__':
    main()
