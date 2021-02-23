# Text_Based_browser

### Данный проект был написан как проект трека Python Developer платформы JetBrains Academy

Задание(переведено):
>Возможность прочитать онлайн-документацию или найти что-то в Интернете из командной строки или терминала может действительно пригодиться. Давайте воспользуемся Python для создания текстового браузера. В этом проекте вы создадите упрощенный браузер, который будет игнорировать JS и CSS, не будет иметь файлов cookie и будет отображать только ограниченный набор тегов. Но в некоторых ситуациях его все равно будет достаточно, и строить его будет весело!
Результаты обучения
В этом проекте вы узнаете, как работает HTTP и как с ним работать в Python. Вы познакомитесь с вводом и выводом Python. Вам также потребуется проанализировать HTML, так что вы тоже получите некоторый опыт в этом.

Это приложение является упрощенной версией браузера: оно умеет делать делать запросы и отображать содержимое сайтов(частично: отображает только содержимое a, p, ul, ol и li тегов). Содержимое выводится в созданные файлы в директории dir_for_files и в консоль. Причем содержимое a тегов выводится в консоль синим цветом.

Работа приложения:
![пример работы](img/screenshot.png)

Код приложения:  

``` python
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
```
