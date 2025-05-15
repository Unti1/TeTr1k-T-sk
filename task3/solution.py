from typing import Dict, List

def appearance(intervals: Dict[str, List[int]]) -> int:
    # Получаем границы урока
    lesson_start, lesson_end = intervals['lesson']
    
    # Создаем список всех событий (вход/выход)
    events = []
    
    # Добавляем события ученика
    for i in range(0, len(intervals['pupil']), 2):
        start, end = intervals['pupil'][i:i+2]
        if start < lesson_end and end > lesson_start:
            events.append((max(start, lesson_start), 1))  # Вход
            events.append((min(end, lesson_end), -1))     # Выход
    
    # Добавляем события учителя
    for i in range(0, len(intervals['tutor']), 2):
        start, end = intervals['tutor'][i:i+2]
        if start < lesson_end and end > lesson_start:
            events.append((max(start, lesson_start), 1))  # Вход
            events.append((min(end, lesson_end), -1))     # Выход
    
    # Сортируем события по времени
    events.sort()
    
    # Подсчитываем общее время присутствия
    total_time = 0
    current_count = 0
    prev_time = None
    
    for time, delta in events:
        if current_count == 2 and prev_time is not None:  # Оба присутствуют
            total_time += time - prev_time
        current_count += delta
        prev_time = time
    
    return total_time 