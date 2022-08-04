from datacenter.models import (
    Chastisement,
    Commendation,
    Lesson,
    Mark,
    Schoolkid,
    Subject,
)
from random import choice
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist


def get_schoolkid(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        return schoolkid

    except Schoolkid.DoesNotExist:
        raise ObjectDoesNotExist(
            'Такого ученика не существует,'
            'проверьте написание имени/фамилии')

    except Schoolkid.MultipleObjectsReturned:
        raise MultipleObjectsReturned(
            'Найдено несколько учеников с таким именем/фамилией, '
            'уточните данные')


def get_subject(subject, schoolkid):
    try:

        return Subject.objects.get(
            title=subject,
            year_of_study=schoolkid.year_of_study
        )

    except Subject.DoesNotExist:
        raise ObjectDoesNotExist(
            'Предмета с таким названием не существует,'
            ' проверьте написание')


def fix_marks(
        low_bound_point=3,
        schoolkid_name='Фролов Иван',
        needed_points=5
):

    schoolkid = get_schoolkid(schoolkid_name)

    update_bad_marks = Mark.objects.filter(
        schoolkid=schoolkid,
        points__lt=low_bound_point
    ).update(
        points=needed_points
    )


def remove_chastisements(schoolkid_name='Фролов Иван'):

    schoolkid = get_schoolkid(schoolkid_name)

    delete_chastisements_of_schoolkid = Chastisement.objects.filter(
        schoolkid=schoolkid
    ).delete()


def create_commendation(
        schoolkid_name='Фролов Иван',
        subject_name='Музыка'
):

    schoolkid = get_schoolkid(schoolkid_name)

    subject = get_subject(subject_name, schoolkid)

    variants_of_commendations = [
        'Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!', 'Великолепно!', 'Прекрасно!',
        'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!',
        'Очень хороший ответ!', 'Талантливо!',
        'Ты сегодня прыгнул выше головы!', 'Я поражен!',
        'Уже существенно лучше!', 'Потрясающе!', 'Замечательно!',
        'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!', 'Здорово!',
        'Это как раз то, что нужно!', 'Я тобой горжусь!',
        'С каждым разом у тебя получается всё лучше!',
        'Мы с тобой не зря поработали!', 'Я вижу, как ты стараешься!',
        'Ты растешь над собой!', 'Ты многое сделал, я это вижу!',
        'Теперь у тебя точно все получится!'
    ]

    serialize_lessons = Lesson.objects.select_related(
        'subject',
        'teacher'
    ).filter(
        subject__year_of_study=schoolkid.year_of_study,
        subject=subject
    ).order_by('date').last()

    create_commendation_to_schoolkid = Commendation.objects.create(
        text=choice(variants_of_commendations),
        created=serialize_lessons.date,
        schoolkid=schoolkid,
        subject=serialize_lessons.subject,
        teacher=serialize_lessons.teacher,
        )
