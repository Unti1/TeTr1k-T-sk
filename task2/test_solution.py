import os
import csv
import pytest
import asyncio
from task2.solution import get_animals_count

@pytest.mark.asyncio
async def test_beasts_file_creation():
    # Запускаем функцию
    await get_animals_count()
    
    # Проверяем, что файл создан
    assert os.path.exists('beasts.csv')
    
    # Проверяем содержимое файла
    with open('beasts.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
        
        # Проверяем, что файл не пустой
        assert len(rows) > 0
        
        # Проверяем формат данных
        for row in rows:
            assert len(row) == 2
            assert len(row[0]) == 1  # Первая колонка - одна буква
            assert row[1].isdigit()  # Вторая колонка - число
            
        # Проверяем, что буквы отсортированы
        letters = [row[0] for row in rows]
        assert letters == sorted(letters) 