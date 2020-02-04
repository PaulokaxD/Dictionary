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
    related_message = soup.find(text=f'Entradas que contienen la forma «{word}»:')

    if soup.find(text="Aviso: ") or related_message:
        if soup.find(text=re.compile(r'La(s)* entrada(s)* que se muestra(n)* a continuación podría(n)* estar relacionada(s)*:')) or related_message:
            print(f'\nNo se encontro la palabra {word} pero \nlas siguientes estan relacionadas:')
            if related_message:
                possible_words = soup.select(".otras a")
            else:
                possible_words = soup.select(".item-list a")
            for possible_word in possible_words:
                print('          ',possible_word.text)
            
            if input("\n¿Te referias a alguna de ellas? si/otro\n") == 'si':
                sol = search_word(input('Introduzca la palabra:'))
        else:
            print(f"\nLa palabra {word} no esta en el diccionario")
    else:
        dict_meaning = {}
        for k, entry in enumerate(soup.select("#resultados > article"), start=1):

            val_meaning = {}
            
            for i, meaning in enumerate(entry.find_all("p", class_=re.compile(r"^j[1-9]?$")), start=1):
                meaning_text = meaning.text
                print(meaning_text)
                if(input('\n¿Quiere añadir esta entrada?si/otro ') == 'si'):
                    val_meaning[i] = meaning_text

            for i,meaning in enumerate(entry.find_all('p', class_='l2'), start=len(val_meaning)+1):
                meaning_text = meaning.text
                print(meaning_text)
                if(input('\n¿Quiere añadir esta entrada?si/otro ') == 'si'):
                    val_meaning[i] = meaning_text

            expressions_name = entry.find_all("p", class_=re.compile(r"^k[1-9]?$"))
            expressions_info = entry.find_all("p", class_='m') 
            expressions_info.extend(entry.find_all('p', class_='l2'))

            longitude = len(expressions_info)
            if longitude == len(expressions_name):
                for a in range(longitude):
                    expressions_name_text = expressions_name[a].text
                    expressions_info_text = expressions_info[a].text
                    print(expressions_name_text,expressions_info_text)
                    if(input('\n¿Quiere añadir esta entrada?si/otro ') == 'si'):
                        val_meaning[expressions_name_text] = expressions_info_text
            else:
                a = -1
                for info_entry in expressions_info:
                    info_text = info_entry.text
                    if info_text[0] in {"1", 'V'}:
                        a += 1
                        name_text = expressions_name[a].text
                        print(name_text, info_text)
                        if(input('\n¿Quiere añadir esta entrada?si/otro ') == 'si'):
                            val_meaning[name_text] = [info_text]                        
                    else:
                        name_text = expressions_name[a].text
                        print(name_text, info_text)
                        if(input('\n¿Quiere añadir esta entrada?si/otro ') == 'si'):
                            if(val_meaning.get(name_text) is None):
                                val_meaning[name_text] = [info_text]
                            else:
                                val_meaning[name_text].append(info_text)
                                
            other_entrys = entry.find_all("p", class_=re.compile(r"^l3?$"))
            other_entrys_text = []
            for i in range(len(other_entrys)):
                other_entry_text = other_entrys[i].text
                print(other_entry_text)
                if(input('\n¿Quiere añadir esta entrada?si/otro ') == 'si'):
                    other_entrys_text.append(other_entrys[i].text)
            if other_entrys_text:
                val_meaning['otras entradas'] = other_entrys_text

            if val_meaning:
                dict_meaning[k] = val_meaning
        if dict_meaning:
            sol = (word,dict_meaning)
            print('\nSe ha añadido correctamente')
        else:
            print(f'\nNo se ha guardado información sobre la palabra "{word}"')
    other_words = soup.find(text=re.compile(r'Otra(s)* entrada(s)* que contiene(n)* la(s)* forma(s)*(\W{2}\w*)+\S:'))
    if other_words:
        possible_words = soup.select(".otras a")
        print('\nQuizas te interesen estas palabras relacionadas:')
        for possible_word in possible_words:
                print('          ',possible_word.text)
    return sol


def record_word(word, file):
    if os.stat(f"{file}.json").st_size == 0:
            with open(f"{file}.json", "r+",encoding="utf-8") as empty_file:
                empty_file.write('{}')
    with open(f"{file}.json", "r+",encoding="utf-8") as read_file:
        dictionary = json.load(read_file)
    res = search_word(word)
    if res:
        if res[0] not in dictionary or (res[0] in dictionary and input(f"\n¿Quieres reescribir la entrada {res[0]}? si/otro\n") == "si"):
            dictionary[res[0]] = res[1]
            dictionary = dict(sorted(dictionary.items())) #poner mas bonico
            with open(f"{file}.json", "w", encoding="utf-8") as write_file:
                json.dump(dictionary, write_file, ensure_ascii=False, indent=4)


def copy_dictionary(file_dict,new_file):
    dictionary = {}
    with open(f'{file_dict}.json', 'r', encoding='utf-8') as read_file:
        dictionary = json.load(read_file)
    with open(f'{new_file}.json', 'w', encoding='utf-8') as write_file:
        json.dump(dictionary, write_file, ensure_ascii=False, indent=4)
    print('\nSe ha copiado correctamente')


#hacer tkinter de entrys
#hacer word
#frases hechas 'a pesar de' o tiempos verbales
#ver si, al meter un nuevo dicc, se raya o no

if __name__ == "__main__":
    # word = input("\n¿Que palabra desea buscar? ")
    # record_word(word, "dict_file")
    copy_dictionary('dict_file','dict_copy')
