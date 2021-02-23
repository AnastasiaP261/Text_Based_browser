import os
import argparse
import re
import requests
import colorama as col

from bs4 import BeautifulSoup


def reform(r):
    col.init()
    soup = BeautifulSoup(r.content, 'html.parser')
    res = ''

    for child in soup.recursiveChildGenerator():
        if child.name in ['p', 'ul', 'ol', 'li']:
            res += col.Style.RESET_ALL + child.text + '\n'
        elif child.name == 'a':
            res += col.Fore.BLUE + child.text + '\n'
    return re.sub(r'\n\n', '', res)


def choice_site():
    address = input()
    if re.search(r'^(https?://)([-a-zA-Z0-9_]*\.[-a-zA-Z0-9_]*){1,}$', address):
        r = requests.get(address)
        file_name = re.search(r'([-a-zA-Z0-9_]*\.[-a-zA-Z0-9_]*){1,}$', address)
        return reform(r), file_name
    elif re.search(r'^([-a-zA-Z0-9_]*\.[-a-zA-Z0-9_]*){1,}$', address):
        file_name = address
        address = 'https://' + address
        r = requests.get(address)
        return reform(r), file_name
    elif 'exit' == address:
        return '', '0'
    else:
        return '', '-1'


def main():
    parser = argparse.ArgumentParser(description="taking directory")
    parser.add_argument("directory", help="Give directory for caching pages")
    args = parser.parse_args()

    if not os.path.exists(args.directory):
        os.mkdir(args.directory)

    while True:
        content, name = choice_site()

        if name == '0':
            break
        print(content)
        if name == '-1':
            print('Error: Incorrect URL.')
            continue

        with open(f'{args.directory}/{name}', 'w', encoding='utf-8') as f:
            f.write(content)


main()
