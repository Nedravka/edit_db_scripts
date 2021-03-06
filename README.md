# Скрипт для изменения базы данных электронного дневника школы

Репозиторий содержит набор функций позволяющий улучшить успеваемость отдельного ученика

## Подготовка к работе

- Скачайте и запустите репозиторий [электронного дневника школы](https://github.com/devmanorg/e-diary/tree/master)
- Установите зависимости командой `pip install -r requirements.txt`
- Создайте БД командой `python3 manage.py migrate`
- Замените созданную БД на полноценную 
- Добавьте в директорию скачанного репозитория файл `scripts.py`


## Запуск скрипта

- Запустите Django Shell коммандой `python3 manage.py shell`
- Импортируйте скрипты из файла командой `from scripts import *`
- Выберите нужный скрипт и запустите соответствующей командой

## Описание функций скрипта
### Исправление оценок:

Данный функция позволяет изменить оценки конкретному ученику, вызывается следующей командой:

    fix_marks(schoolkid_name='Фролов Иван', low_point_bound=4, point_to_update=5)

В качестве параметров функция принимает значения:

 - `schoolkid_name='Фролов Иван'` - имя ученика 
 
- `low_point_bound=4` -  оценка ниже которой будут исправлены

- `point_to_update=5` - значение на которое будут исправлены отметки

### Удаление замечаний:

Данная функция позволяет удалить все замечания к конкретному ученику, вызывается следующей командой:

    remove_chastisements(schoolkid_name='Фролов Иван')
    
В качестве параметров функция принимает значения:

 - `schoolkid_name='Фролов Иван'` - имя ученика 
 
### Добавление похвалы:

Данная функция позволяет добавить похвалу конкретному ученику, по контретному уроку, вызывается следующей командой:
 
    create_commendation(schoolkid_name='Фролов Иван', subject='Музыка')
    
В качестве параметров функция принимает значения:

- `schoolkid_name='Фролов Иван'` - имя ученика 

- `subject='Музыка'` - название предмета

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
