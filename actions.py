import re
import random
from secrets import choice
from pymongo.errors import DuplicateKeyError


def choice_output_def():
    print()
    print('Каким образом выводить слова?')
    print('\t1 <-- "slowly -> медленно"')
    print('\t2 <-- "медленно -> slowly"')
    print('\t3 <-- "slowly -> медленно" или "медленно -> slosly"')
    
    while True:
        choice = int(input('Введите число: '))
        if choice not in (1, 2, 3):
            print('Введите число от 1 до 3')
            continue
        
        break
    
    return choice
    

class adding:
    def __init__(self, collection):
        self.collection = collection
    

    def call(self):
        print()
        print('Для остановки введите слово "break"')
        print('Вводите данные, как показано в следующем примере')
        print(': slowly = медленно')

        while True:
            new_word = {}
            input_word = input(': ')

            if 'break' in input_word:
                break
            
            # Обработка слова
            word = re.search(r'.+ =', input_word)[0][:-3]
            if word != '':
                new_word['word'] = word
            else:
                print('Некорректный ввод слова')
                continue

            # Обработка перевода
            translate = re.search(r'= .+', input_word)[0][3:]
            if translate != '':
                new_word['translate'] = translate
            else:
                print('Некорректный ввод перевода')

            # Индексом будет являться само слово
            _id = word
            new_word['_id'] = _id
            
            # Также добавим номер по счету для каждого слова, что бы
            # можно было обращаться к последним словам
            num_id = len(list(self.collection.find({})))
            new_word['num_id'] = num_id + 1

            # Добавление слова в коллекцию
            try:
                self.collection.insert_one(new_word)
            except DuplicateKeyError:
                print('Слово уже существует в базе данных, хотите его заменить?')
                replacement = input(': ').lower()

                if 'yes' in replacement or 'нуы' in replacement or 'да' in replacement or 'lf' in replacement or '+' in replacement:
                    self.collection.update_one({'_id': _id}, {'$set': {'translate': translate}})
                    print('Заменено')


class repeat:
    def __init__(self, collection):
        self.collection = collection
    

    def call(self):
        len_collection = len(list(self.collection.find({})))
        if len_collection == 0:
            print()
            print('В этой коллекции, пока, нет слов')
            return

        # Спросим, как выводить данные
        choice_output = choice_output_def()

        print()
        print('Для остановки введите слово "break"')

        while True:
            # Получим случайное слово из коллекции
            random_num_id = random.sample(range(1, len_collection), 1)[0]
            sample_word = self.collection.find_one({'num_id': random_num_id})

            if choice_output == 1:
                input_word = input(f'{sample_word["word"]} -> ')
                translate = sample_word['translate']
            elif choice_output == 2:
                input_word = input(f'{sample_word["translate"]} -> ')
                translate = sample_word['word']
            else:
                # Используем рандом, что бы выбрать из (перевести С английского или перевести НА английский)
                random_translate = random.randint(1, 2)

                # Просим ввести перевод этого слова
                if random_translate == 1:
                    input_word = input(f'{sample_word["word"]} -> ')
                else:
                    input_word = input(f'{sample_word["translate"]} -> ')
    
                if random_translate == 1:
                    translate = sample_word['translate']
                else:
                    translate = sample_word['word']

            if 'break' in input_word:
                break

            # Проверяем, является ли перевод верным
            if input_word == translate:
                print('\tВерно!')
            else:
                print(f'\tНет, верный перевод -> {translate}')
            


class repeat_last:
    def __init__(self, collection):
        self.collection = collection


    def call(self):
        # Узнаем длину всей коллекции
        len_collection = len(list(self.collection.find({})))
        if len_collection == 0:
            print()
            print('В этой коллекции, пока, нет слов')
            return

        # Спросим, как выводить данные
        choice_output = choice_output_def()

        print()
        print('Для остановки введите слово "break"')

        # Получим количество нужных слов
        num_words = int(input('Введите количество слов для повторения: '))

        # Найдем минимальным номер num_id в коллекции для наших слов, что бы брать 
        # документа с таким номером или больше
        min_num_id = self.collection.count() - num_words

        # Получим все нужные индексы в случайном порядке
        random_num_id = random.sample(range(min_num_id, len_collection), num_words)

        # Достанем документы с полученными индексами
        words = self.collection.find({'$in': {'num_id': random_num_id}})
        
        for word in words:
            if choice_output == 1:
                input_word = input(f'{word["word"]} -> ')
                translate = word['translate']
            elif choice_output == 2:
                input_word = input(f'{word["translate"]} -> ')
                translate = word['word']
            else:
                # Используем рандом, что бы выбрать из (перевести С английского или перевести НА английский)
                random_translate = random.randint(1, 2)

                # Просим ввести перевод этого слова
                if random_translate == 1:
                    input_word = input(f'{word["word"]} -> ')
                else:
                    input_word = input(f'{word["translate"]} -> ')
    
                if random_translate == 1:
                    translate = word['translate']
                else:
                    translate = word['word']

            if 'break' in input_word:
                break

            # Проверяем, является ли перевод верным
            if input_word == translate:
                print('\tВерно!')
            else:
                print(f'\tНет, верный перевод -> {translate}')