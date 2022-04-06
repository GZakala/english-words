from actions import adding, repeat, repeat_last
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['english']

# Коллекции в базе данных
nouns = db.nouns
verbs = db.verbs
phrases = db.phrases

# Блок с приветствием и выбором действия
print()
print('Привет! Давай начнем изучение иностранных слов.')
print('Выбери действие, которое хочешь выполнить')
print('\t1 <-- Записать новые слова')
print('\t2 <-- Повторить имеющиеся слова в случайном порядке')
print('\t3 <-- Повторить последние записанные слова')

# Выбор и валидация действия
while True:
    action_type = int(input('Введите выбранное число: '))

    if action_type not in (1, 2, 3):
        print('Введите число от 1 до 3')
        continue

    break

# Блок с выбором типа слов
print()
print('Какие именно слова мы будем использовать?')
print('\t1 <-- Существительные')
print('\t2 <-- Глаголы')
print('\t3 <-- Фразы')

# Выбор и валидация выбранных слов
while True:
    words_type = int(input('Введите выбранное число: '))

    if words_type not in (1, 2, 3):
        print('Введите число от 1 до 3')
        continue

    break


if words_type == 1:
    collection = nouns
elif words_type == 2:
    collection = verbs
else:
    collection = phrases


if action_type == 1:
    action = adding(collection)
elif action_type == 2:
    action = repeat(collection)
else:
    action = repeat_last(collection)


action.call()