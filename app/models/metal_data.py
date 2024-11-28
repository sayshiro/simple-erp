"""Начальные данные для металлопроката"""

METAL_TYPES = [
    {
        'name': 'Лист',
        'description': 'Листовой прокат',
        'measurement_unit': 'кг'
    },
    {
        'name': 'Труба круглая',
        'description': 'Круглые трубы',
        'measurement_unit': 'м'
    },
    {
        'name': 'Труба профильная',
        'description': 'Профильные трубы прямоугольного и квадратного сечения',
        'measurement_unit': 'м'
    },
    {
        'name': 'Уголок',
        'description': 'Уголок равнополочный и неравнополочный',
        'measurement_unit': 'м'
    },
    {
        'name': 'Швеллер',
        'description': 'Швеллер',
        'measurement_unit': 'м'
    },
    {
        'name': 'Арматура',
        'description': 'Арматура для железобетонных конструкций',
        'measurement_unit': 'м'
    }
]

METAL_GOSTS = [
    {
        'number': '19903-2015',
        'name': 'Прокат листовой горячекатаный',
        'description': 'Сортамент',
        'metal_type': 'Лист'
    },
    {
        'number': '8732-78',
        'name': 'Трубы стальные бесшовные горячедеформированные',
        'description': 'Сортамент',
        'metal_type': 'Труба круглая'
    },
    {
        'number': '8639-82',
        'name': 'Трубы стальные квадратные',
        'description': 'Сортамент',
        'metal_type': 'Труба профильная'
    },
    {
        'number': '8509-93',
        'name': 'Уголки стальные горячекатаные равнополочные',
        'description': 'Сортамент',
        'metal_type': 'Уголок'
    }
]

METAL_GRADES = [
    {
        'name': 'Ст3',
        'description': 'Сталь конструкционная углеродистая обыкновенного качества',
        'properties': {
            'temporary_resistance': '380-490',
            'yield_strength': '255',
            'relative_extension': '26'
        },
        'usage': 'Для несущих элементов сварных и несварных конструкций и деталей'
    },
    {
        'name': '09Г2С',
        'description': 'Сталь конструкционная низколегированная',
        'properties': {
            'temporary_resistance': '490-630',
            'yield_strength': '345',
            'relative_extension': '21'
        },
        'usage': 'Для сварных конструкций и деталей, работающих при температуре от -70 до +425°С'
    }
]
