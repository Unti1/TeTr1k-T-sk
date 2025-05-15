from typing import Callable, Any
import inspect

def strict(func: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Получаем аннотации типов из функции
        annotations = func.__annotations__
        
        # Проверяем типы позиционных аргументов
        for i, (arg_name, arg_value) in enumerate(inspect.signature(func).parameters.items()):
            if i < len(args):
                expected_type = annotations.get(arg_name)
                if expected_type and not isinstance(args[i], expected_type):
                    raise TypeError(f"Argument '{arg_name}' must be of type {expected_type.__name__}, got {type(args[i]).__name__}")
        
        # Проверяем типы именованных аргументов
        for arg_name, arg_value in kwargs.items():
            expected_type = annotations.get(arg_name)
            if expected_type and not isinstance(arg_value, expected_type):
                raise TypeError(f"Argument '{arg_name}' must be of type {expected_type.__name__}, got {type(arg_value).__name__}")
        
        return func(*args, **kwargs)
    
    return wrapper 