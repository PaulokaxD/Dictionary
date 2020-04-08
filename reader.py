import requests
from bs4 import BeautifulSoup
import re
import json
import os

url = "https://dle.rae.es/{word}"


def search_word(word):

    page = requests.get(url.format(word=word))
    soup = BeautifulSoup(page.content, "html.parser")
    sol = ()
    related_message = soup.find(
        text=re.compile(r"Entrada(s)* que contiene(n)* la(s)* forma(s)*(\W{2}\w*)+\S:")
    )

    if soup.find(text="Aviso: ") or related_message:  # ver como poner condiconal boniko
        if (
            soup.find(
                text=re.compile(
                    r"La(s)* entrada(s)* que se muestra(n)* a continuacion podria(n)* estar relacionada(s)*:"
                )
            )
            or related_message
        ):
            print(
                f"\nNo se encontro la palabra {word} pero \nlas siguientes estan relacionadas: "
            )
            if related_message:
                possible_words = soup.select(".otras a")
            else:
                possible_words = soup.select(".item-list a")
            for possible_word in possible_words:
                print(f"{possible_word.text: ^35}")

            if input("\n¿Te referias a alguna de ellas? si/otro\n") == "si":
                sol = search_word(input("Introduzca la palabra:"))
        else:
            print(f"\nLa palabra {word} no esta en el diccionario")
    else:
        dict_meaning = {}
        for k, entry in enumerate(soup.select("#resultados > article"), start=1):

            val_meaning = {}

            entrys_mas_l2 = entry.find_all(
                "p", class_=re.compile(r"^j[1-9]?$")
            ) + entry.find_all(
                "p", class_="l2"
            )  # cuidado con l2. Se guardaria tambien las de las frases hechas si hubiere de ambos tipos a la vez
            for i, meaning in enumerate(entrys_mas_l2, start=1):
                meaning_text = meaning.text
                print(meaning_text)
                if ask_user():
                    val_meaning[i] = meaning_text

            expressions_name = entry.find_all("p", class_=re.compile(r"^k[1-9]?$"))
            expressions_info = entry.find_all("p", class_="m") + soup.select(
                ".k6 ~ .l2"
            )
            longitude = len(expressions_info)

            if longitude == len(expressions_name):
                for expression_name, expression_info in zip(
                    expressions_name, expressions_info
                ):
                    expressions_name_text = expression_name.text
                    meaning_text = expression_info.text
                    print(expressions_name_text, meaning_text)
                    if ask_user():
                        val_meaning[expressions_name_text] = meaning_text
            else:
                a = -1
                for info_entry in expressions_info:
                    meaning_text = info_entry.text
                    if meaning_text[0] in {"1", "V"}:
                        a += 1
                        name_text = expressions_name[a].text
                        print(name_text, meaning_text)
                        if ask_user():
                            val_meaning[name_text] = [meaning_text]
                    else:
                        name_text = expressions_name[a].text
                        print(name_text, meaning_text)
                        if ask_user():
                            if name_text in val_meaning:
                                val_meaning[name_text] = [meaning_text]
                            else:
                                val_meaning[name_text].append(meaning_text)

            other_entrys_text = []
            for other_entry in entry.find_all("p", class_=re.compile(r"^l3?$")):
                other_entry_text = other_entry.text
                print(other_entry_text)
                if ask_user():
                    other_entrys_text.append(other_entry_text)
            if other_entrys_text:
                val_meaning["otras entradas"] = other_entrys_text

            if val_meaning:
                dict_meaning[k] = val_meaning

        if dict_meaning:
            sol = (word, dict_meaning)
            print("\nSe ha añadido correctamente")
        else:
            print(f'\nNo se ha guardado información sobre la palabra "{word}"')

    if soup.find(
        text=re.compile(
            r"Otra(s)* entrada(s)* que contiene(n)* la(s)* forma(s)*(\W{2}\w*)+\S:"
        )
    ):
        possible_words = soup.select(".otras a")
        print("\nQuizas te interesen estas palabras relacionadas:")
        for possible_word in possible_words:
            print(f"{possible_word.text: ^45}")
    return sol


def ask_user():
    return input("\n¿Quiere añadir esta entrada?si/otro ") in {"si", "yes"}


def record_word(word, file):
    if not os.path.isfile(f"{file}.json") or os.stat(f"{file}.json").st_size == 0:
        dictionary = {}
    else:
        with open(f"{file}.json", encoding="utf-8") as read_file:
            dictionary = json.load(read_file)
    res = search_word(word)
    if res:
        if res[0] not in dictionary or (
            res[0] in dictionary
            and input(f"\n¿Quieres reescribir la entrada {res[0]}? si/otro\n") == "si"
        ):
            dictionary[res[0]] = res[1]
            dictionary = dict(sorted(dictionary.items()))  # poner mas bonico
            with open(f"{file}.json", "w", encoding="utf-8") as write_file:
                json.dump(dictionary, write_file, ensure_ascii=False, indent=4)


def copy_dictionary(file_dict, new_file):
    dictionary = {}
    with open(f"{file_dict}.json", "r", encoding="utf-8") as read_file:
        dictionary = json.load(read_file)
    with open(f"{new_file}.json", "w", encoding="utf-8") as write_file:
        json.dump(dictionary, write_file, ensure_ascii=False, indent=4)
    print("\nSe ha copiado correctamente")


# corregir 'una' dando no o si a 1 acepcion
# hacer word
# frases hechas 'a pesar de' o tiempos verbales, plurales...
# ordenar bien palabras, pues tildes las pone al final

if __name__ == "__main__":
    word = input("\n¿Que palabra desea buscar? ")
    record_word(word, "dict_file")
    # copy_dictionary('dict_file','dict_copy')
