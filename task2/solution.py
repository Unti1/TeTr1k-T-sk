import requests
from bs4 import BeautifulSoup
import csv
from collections import defaultdict

def get_animals_count():
    # URL страницы с животными
    url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
    
    # Словарь для подсчета животных по буквам
    animals_count = defaultdict(int)
    
    while url:
        # Получаем страницу
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Находим блок с категориями
        content = soup.find('div', {'class': 'mw-category'})
        if not content:
            break
            
        # Получаем все ссылки на животных
        links = content.find_all('a')
        
        # Подсчитываем количество животных по первой букве
        for link in links:
            animal_name = link.text
            if animal_name:
                first_letter = animal_name[0].upper()
                animals_count[first_letter] += 1
        
        # Ищем ссылку на следующую страницу
        next_page = soup.find('a', string='Следующая страница')
        url = f"https://ru.wikipedia.org{next_page['href']}" if next_page else None
    
    # Записываем результаты в CSV файл
    with open('beasts.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for letter in sorted(animals_count.keys()):
            writer.writerow([letter, animals_count[letter]])

if __name__ == '__main__':
    get_animals_count() 