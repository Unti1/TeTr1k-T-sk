import aiohttp
import asyncio
from bs4 import BeautifulSoup
import csv
from collections import defaultdict
from asyncio import Semaphore

async def get_page_content(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as response:
        # print(await response.text())
        return await response.text()

async def process_category_page(session: aiohttp.ClientSession, url: str, semaphore: Semaphore) -> dict:
    async with semaphore:
        html = await get_page_content(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Находим все ссылки на животных в указанной структуре
        animal_links = soup.select('div.mw-category-group ul li a')

        # Подсчитываем количество животных по первой букве
        animals_count = defaultdict(int)
        for link in animal_links:
            animal_name = link.text
            if animal_name:
                first_letter = animal_name[0].upper()
                animals_count[first_letter] += 1
                
        return dict(animals_count)

async def get_animals_count():
    # URL страницы с животными
    url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
    
    # Словарь для подсчета животных по буквам
    animals_count = defaultdict(int)
    
    # Создаем семафор для ограничения количества одновременных запросов
    semaphore = Semaphore(10)
    
    async with aiohttp.ClientSession() as session:
        # Получаем страницу
        html = await get_page_content(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Находим все ссылки на категории в блоке индекса
        category_links = soup.select('div.ts-module-Индекс_категории-container > ul.ts-module-Индекс_категории-multi-items> li > a')
        # Создаем список задач для обработки категорий
        tasks = []
        for category_link in category_links:
            task = asyncio.create_task(process_category_page(session, category_link['href'], semaphore))
            tasks.append(task)
        
        # Ждем завершения всех задач
        results = await asyncio.gather(*tasks)
        
        # Объединяем результаты
        for result in results:
            for letter, count in result.items():
                animals_count[letter] += count
    
    # Записываем результаты в CSV файл
    with open('beasts.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for letter in sorted(animals_count.keys()):
            writer.writerow([letter, animals_count[letter]])

async def main():
    await get_animals_count()

if __name__ == '__main__':
    asyncio.run(main()) 