from datacenter.models import *
from random import choice


def check_input_data(schoolkid_name, subject=None):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        Subject.objects.get(title=subject, year_of_study=schoolkid.year_of_study)
    except Schoolkid.DoesNotExist:
        return print('Такого ученика не существует, проверьте написание имени/фамилии')
    except Schoolkid.MultipleObjectsReturned:
        return print('Найдено несколько учеников с таким именем/фамилией, уточните данные')
    except Subject.DoesNotExist:
        return print('Предмета с таким названием не существует, проверьте написание')


def fix_marks(schoolkid_name='Фролов Иван', low_point_bound=4, point_to_update=5):
    if not check_input_data(schoolkid_name):
        return
    schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    mark = Mark.objects.filter(schoolkid=schoolkid, points__lt=low_point_bound)
    mark.update(points=point_to_update)


def remove_chastisements(schoolkid_name='Фролов Иван'):
    if not check_input_data(schoolkid_name):
        return
    schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    delete_chastisements = Chastisement.objects.filter(schoolkid=schoolkid_name).delete()


def create_commendation(schoolkid_name='Фролов Иван', subject='Музыка'):
    if not check_input_data(schoolkid_name, subject):
        return

    variants_of_commendations = [
        'Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!', 'Великолепно!', 'Прекрасно!',
        'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!',
        'Очень хороший ответ!', 'Талантливо!', 'Ты сегодня прыгнул выше головы!',
        'Я поражен!', 'Уже существенно лучше!', 'Потрясающе!', 'Замечательно!',
        'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!', 'Здорово!',
        'Это как раз то, что нужно!', 'Я тобой горжусь!',
        'С каждым разом у тебя получается всё лучше!',
        'Мы с тобой не зря поработали!', 'Я вижу, как ты стараешься!',
        'Ты растешь над собой!', 'Ты многое сделал, я это вижу!',
        'Теперь у тебя точно все получится!'
    ]
    schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    serialize_lessons = Lesson.objects.filter(subject__title=subject,
                                              year_of_study=schoolkid.year_of_study,
                                              group_letter=schoolkid.group_letter).order_by('date')

    commendation_to_schoolkid = Commendation.objects.create(text=choice(variants_of_commendations),
                                                            created=serialize_lessons.last().date,
                                                            schoolkid=schoolkid,
                                                            subject=serialize_lessons.last().subject,
                                                            teacher=serialize_lessons.last().teacher)
