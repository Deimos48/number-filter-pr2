"""Исходная версия фильтра чисел с преднамеренной ошибкой."""


def _validate_int(value, name="value"):
    if type(value) is not int:
        raise TypeError(f"{name} must be an integer")


def _validate_numbers(numbers):
    if not isinstance(numbers, (list, tuple)):
        raise TypeError("numbers must be a list or tuple")
    for number in numbers:
        _validate_int(number, "number")


def is_prime(number: int) -> bool:
    """Вернуть True, если number является простым числом."""
    _validate_int(number, "number")
    # ПРЕДНАМЕРЕННАЯ ОШИБКА: должно быть number < 2.
    if number < 1:
        return False
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True


def filter_primes(numbers: list[int] | tuple[int, ...]) -> list[int]:
    _validate_numbers(numbers)
    return [number for number in numbers if is_prime(number)]


def split_even_odd(numbers: list[int] | tuple[int, ...]) -> tuple[list[int], list[int]]:
    _validate_numbers(numbers)
    even = [number for number in numbers if number % 2 == 0]
    odd = [number for number in numbers if number % 2 != 0]
    return even, odd


def fibonacci_up_to(limit: int) -> list[int]:
    _validate_int(limit, "limit")
    if limit < 0:
        raise ValueError("limit must be non-negative")
    result = []
    first, second = 0, 1
    while first <= limit:
        result.append(first)
        first, second = second, first + second
    return result


def filter_divisible(numbers: list[int] | tuple[int, ...], divisor: int) -> list[int]:
    _validate_numbers(numbers)
    _validate_int(divisor, "divisor")
    if divisor == 0:
        raise ValueError("divisor must not be zero")
    return [number for number in numbers if number % divisor == 0]
