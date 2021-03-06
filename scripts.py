from datacenter.models import (
    Chastisement,
    Commendation,
    Lesson,
    Mark,
    Schoolkid,
    Subject,
)
from random import choice


def catch_errors_processing_input_data(foo):
    def wprapped_foo(*args, **kwargs):
        try:
            foo(*args, **kwargs)
        except Subject.DoesNotExist:
            print('Проверьте написание названия предмета')
        except Schoolkid.DoesNotExist:
            print(
                'Такого ученика не существует, '
                'проверьте правльность написания ФИО'
            )
        except Schoolkid.MultipleObjectsReturned:
            print(
                'Найдено несколько учеников с '
                'таким ФИО, уточните данные'
            )
    return wprapped_foo


@catch_errors_processing_input_data
def fix_marks(
        low_bound_point=3,
        schoolkid_name='Фролов Иван',
        needed_points=55
):

    schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)

    update_bad_marks = Mark.objects.filter(
        schoolkid=schoolkid,
        points__lt=low_bound_point
    ).update(
        points=needed_points
    )


@catch_errors_processing_input_data
def remove_chastisements(schoolkid_name='Фролов Иван'):

    schoolkid = Schoolkid.objects.values(
        'id'
    ).get(
        full_name__contains=schoolkid_name
    )

    delete_chastisements_of_schoolkid = Chastisement.objects.filter(
        schoolkid__id=schoolkid.get('id')
    ).delete()


@catch_errors_processing_input_data
def create_commendation(
        schoolkid_name='Фролов Иван',
        subject='Музыка'
):

    schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)

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
        'subject__id',
        'teacher_id'
    ).values(
        'subject',
        'teacher',
        'date',
        'subject__year_of_study'
    ).filter(
        subject__year_of_study=schoolkid.year_of_study,
        subject__title=subject
    ).order_by('date').last()

    if not serialize_lessons:
        raise Subject.DoesNotExist

    create_commendation_to_schoolkid = Commendation.objects.create(
        text=choice(variants_of_commendations),
        created=serialize_lessons.get('date'),
        schoolkid=schoolkid,
        teacher_id=serialize_lessons.get('teacher'),
        subject_id=serialize_lessons.get('subject')
        )
