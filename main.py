import pandas as pd
from itertools import takewhile


def html_tag(tag: str):
    def wrap_text(message: str):
        return f'<{tag}>{message}</{tag}>'

    return wrap_text


def get_list_html(names: list[str]):
    patrons: str = ''
    li = html_tag('li')
    for name in names:
        patrons += f'\n\t{li(name)}'
    return patrons


def create_patron_html(names: list[str]) -> str:
    html_output = ''
    html_output += f'<p>There are currently {len(names)} public contributors. Thank You!</p>'
    html_output += '\n<ul>'
    html_output+= get_list_html(names)
    html_output += '\n</ul>'
    return html_output


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
