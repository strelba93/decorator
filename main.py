
import os
from _datetime import datetime

def logger(old_function):
    def new_function(*args, **kwargs):
        call_time = datetime.now().strftime('%d-%m-%Y function call time %H:%M:%S')
        old_func_name = old_function.__name__
        res = old_function(*args, **kwargs)
        with open('main.log', 'a', encoding='utf-8') as file:
            file.write(f'Function call date: {call_time}, '
                       f'Name function: {old_func_name}, '
                       f'Function arguments: {args, kwargs}, '
                       f'Function value: {res}\n')
        return res

    return new_function

list = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

@logger
def flat_generator(list_of_lists):
    start = 0
    end = 0
    while end != len(list_of_lists[start]):
        yield list_of_lists[start][end]
        end += 1
        if end >= len(list_of_lists[start]):
            start += 1
            end = 0
        if start == len(list_of_lists):
            break

def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)
    flat_generator(list)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


def logger2(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            call_time = datetime.now().strftime('%d-%m-%Y function call time %H:%M:%S')
            old_func_name = old_function.__name__
            res = old_function(*args, **kwargs)
            with open(path, 'a', encoding='utf-8') as file:
                file.write(f'Function call date: {call_time}, '
                           f'Name function: {old_func_name}, '
                           f'Function arguments: {args, kwargs}, '
                           f'Function value: {res}\n')
            return res

        return new_function
    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger2(path)
        def hello_world():
            return 'Hello World'

        @logger2(path)
        def summator(a, b=0):
            return a + b

        @logger2(path)
        def div(a, b):
            return a / b

        @logger2(path)
        def flat_generator2(list_of_lists):
            start = 0
            end = 0
            while end != len(list_of_lists[start]):
                yield list_of_lists[start][end]
                end += 1
                if end >= len(list_of_lists[start]):
                    start += 1
                    end = 0
                if start == len(list_of_lists):
                    break
           
        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)
        flat_generator2(list)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'







if __name__ == '__main__':
    test_1()
    test_2()

