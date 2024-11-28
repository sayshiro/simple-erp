document.addEventListener('DOMContentLoaded', function() {
    // Получаем все необходимые элементы формы
    const form = document.querySelector('form');
    const typeSelect = document.getElementById('type_id');
    const gradeSelect = document.getElementById('grade_id');
    const thicknessInput = document.getElementById('thickness');
    const widthInput = document.getElementById('width');
    const lengthInput = document.getElementById('length');
    const diameterInput = document.getElementById('diameter');
    const stockInput = document.getElementById('stock');
    const weightPerUnitInput = document.getElementById('weight_per_unit');

    // Объект для хранения плотностей марок стали
    let gradeDensities = {};

    // Загружаем плотности марок стали при загрузке страницы
    fetch('/metal/grades')
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка при получении данных о плотностях');
            }
            return response.json();
        })
        .then(data => {
            console.log('Полученные плотности:', data);
            gradeDensities = data;
            // Выполняем начальный расчет после загрузки плотностей
            updateFieldVisibility();
            updateWeight();
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Не удалось загрузить данные о плотностях материалов. Будет использовано стандартное значение.');
        });

    // Функция для расчета массы
    function calculateWeight() {
        const type = typeSelect.options[typeSelect.selectedIndex]?.text || '';
        const gradeId = gradeSelect.value;
        const density = gradeDensities[gradeId] || 7.85; // г/см³, используем стандартную плотность если не задана
        
        console.log('Тип:', type);
        console.log('ID марки:', gradeId);
        console.log('Плотность:', density);
        
        let volume = 0; // см³
        
        try {
            if (type === 'Лист') {
                // Для листа: объем = длина * ширина * толщина
                const t = parseFloat(thicknessInput.value) || 0;
                const w = parseFloat(widthInput.value) || 0;
                const l = parseFloat(lengthInput.value) || 0;
                
                console.log('Размеры листа:', { толщина: t, ширина: w, длина: l });
                
                if (t <= 0 || w <= 0 || l <= 0) {
                    return 0;
                }
                
                volume = (t * w * l) / 1000; // переводим мм в см
            } else if (type === 'Труба круглая') {
                // Для трубы: объем = π * ((D/2)² - ((D-2t)/2)²) * L
                const d = parseFloat(diameterInput.value) || 0;
                const t = parseFloat(thicknessInput.value) || 0;
                const l = parseFloat(lengthInput.value) || 0;
                
                console.log('Размеры трубы:', { диаметр: d, толщина: t, длина: l });
                
                if (d <= 0 || t <= 0 || l <= 0) {
                    return 0;
                }
                
                if (t >= d/2) {
                    alert('Толщина стенки не может быть больше или равна половине диаметра трубы');
                    return 0;
                }
                
                const r = d / 2;
                const ri = (d - 2 * t) / 2;
                volume = Math.PI * (Math.pow(r, 2) - Math.pow(ri, 2)) * l / 1000; // переводим мм в см
            }
            
            console.log('Объем (см³):', volume);
            
            // Масса = объем * плотность
            const weight = volume * density / 1000; // переводим в кг
            console.log('Рассчитанная масса (кг):', weight);
            
            // Округляем до 3 знаков после запятой
            return Math.round(weight * 1000) / 1000;
        } catch (error) {
            console.error('Ошибка при расчете веса:', error);
            return 0;
        }
    }

    // Функция обновления веса единицы
    function updateWeight() {
        const weight = calculateWeight();
        console.log('Обновление веса:', weight);
        if (weight > 0) {
            weightPerUnitInput.value = weight;
        } else {
            weightPerUnitInput.value = '';
        }
    }

    // Добавляем слушатели событий для всех полей, влияющих на вес
    [typeSelect, gradeSelect, thicknessInput, widthInput, lengthInput, diameterInput].forEach(input => {
        if (input) {
            ['change', 'input'].forEach(event => {
                input.addEventListener(event, () => {
                    console.log('Изменение поля:', input.id);
                    updateWeight();
                });
            });
        }
    });

    // Показываем/скрываем поля в зависимости от типа металлопроката
    function updateFieldVisibility() {
        const type = typeSelect.options[typeSelect.selectedIndex]?.text || '';
        console.log('Обновление видимости полей для типа:', type);
        
        const listFields = document.querySelectorAll('.list-fields');
        const pipeFields = document.querySelectorAll('.pipe-fields');
        
        if (type === 'Лист') {
            listFields.forEach(field => field.style.display = 'block');
            pipeFields.forEach(field => {
                if (!field.classList.contains('list-fields')) {
                    field.style.display = 'none';
                }
            });
            // Очищаем поля трубы
            if (diameterInput) diameterInput.value = '';
        } else if (type === 'Труба круглая') {
            listFields.forEach(field => {
                if (!field.classList.contains('pipe-fields')) {
                    field.style.display = 'none';
                }
            });
            pipeFields.forEach(field => field.style.display = 'block');
            // Очищаем поля листа
            if (widthInput) widthInput.value = '';
        }
        
        updateWeight();
    }

    // Добавляем слушатель изменения типа
    typeSelect.addEventListener('change', updateFieldVisibility);
    
    // Добавляем валидацию формы перед отправкой
    form.addEventListener('submit', function(event) {
        const weight = calculateWeight();
        console.log('Отправка формы, вес:', weight);
        
        if (weight <= 0) {
            event.preventDefault();
            alert('Не удалось рассчитать вес. Пожалуйста, проверьте введенные размеры.');
            return;
        }
        
        // Убеждаемся, что вес установлен перед отправкой
        weightPerUnitInput.value = weight;
    });
});
