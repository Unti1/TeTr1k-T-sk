# import datetime
from typing import Dict, List

def appearance(intervals: Dict[str, List[int]]) -> int:
    lesson_start, lesson_end = intervals['lesson']
    # print(f"\nУрок: {datetime.datetime.fromtimestamp(lesson_start)} - {datetime.datetime.fromtimestamp(lesson_end)}")
    
    # Создаем список всех точек входа и выхода
    points = []
    
    # Добавляем точки ученика
    # print("\nИнтервалы ученика:")
    for i in range(0, len(intervals['pupil']), 2):
        start, end = intervals['pupil'][i:i+2]
        # print(f"  {datetime.datetime.fromtimestamp(start)} - {datetime.datetime.fromtimestamp(end)}")
        if start < lesson_end and end > lesson_start:
            points.append((max(start, lesson_start), 'pupil', 1))
            points.append((min(end, lesson_end), 'pupil', -1))
    
    # Добавляем точки учителя
    # print("\nИнтервалы учителя:")
    for i in range(0, len(intervals['tutor']), 2):
        start, end = intervals['tutor'][i:i+2]
        # print(f"  {datetime.datetime.fromtimestamp(start)} - {datetime.datetime.fromtimestamp(end)}")
        if start < lesson_end and end > lesson_start:
            points.append((max(start, lesson_start), 'tutor', 1))
            points.append((min(end, lesson_end), 'tutor', -1))
    
    # Сортируем точки по времени
    points.sort()
    
    # Подсчитываем общее время присутствия
    total_time = 0
    pupil_count = 0
    tutor_count = 0
    prev_time = None
    
    # print("\nСобытия:")
    for time, who, delta in points:
        # print(f"  {datetime.datetime.fromtimestamp(time)}: {who} {'вход' if delta == 1 else 'выход'}")
        
        # Если оба присутствуют и есть предыдущее время
        if pupil_count > 0 and tutor_count > 0 and prev_time is not None:
            time_diff = time - prev_time
            total_time += time_diff
            # print(f"    Пересечение: {datetime.datetime.fromtimestamp(prev_time)} - {datetime.datetime.fromtimestamp(time)} = {time_diff} сек")
        
        # Обновляем счетчики
        if who == 'pupil':
            pupil_count += delta
        else:
            tutor_count += delta
        
        prev_time = time
    
    # print(f"\nОбщее время: {total_time} секунд")
    return total_time