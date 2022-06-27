from datacenter.models import (
    Chastisement,
    Commendation,
    Lesson,
    Mark,
    Schoolkid,
    Subject,
)
from random import choice


SERIALIZE_SCHOOLKIDS = list(Schoolkid.objects.all())


def processing_errors_input_data(foo):
    def wprapped_foo(*args, **kwargs):
        try:
            foo(*args, **kwargs)
        except Subject.DoesNotExist:
            print('Проверьте написание названия предмета')
        except Schoolkid.DoesNotExist:
            print(
                'Такого ученика не существует, '
                'проверьте правльность написания входных данных'
            )
        except Schoolkid.MultipleObjectsReturned:
            print(
                'Найдено несколько учеников с '
                'таким именем/фамилией, уточните данные'
            )
    return wprapped_foo


def check_exists_schoolkid(kid):
    if len(kid) > 1:
        raise Schoolkid.MultipleObjectsReturned
    if len(kid) == 0:
        raise Schoolkid.DoesNotExist


@processing_errors_input_data
def fix_marks(
        low_bound_point=4,
        schoolkid_name='Фролов Иван',
        needed_points=5
):
    kid = [schoolkid for schoolkid in SERIALIZE_SCHOOLKIDS if
           schoolkid_name in schoolkid.full_name]

    check_exists_schoolkid(kid)

    update_bad_marks = Mark.objects.filter(
        schoolkid=kid[0],
        points__lt=low_bound_point
    ).update(
        points=needed_points
    )


@processing_errors_input_data
def remove_chastisements(schoolkid_name='Фролов Иван'):

    kid = [schoolkid for schoolkid in SERIALIZE_SCHOOLKIDS if
           schoolkid_name in schoolkid.full_name]

    check_exists_schoolkid(kid)

    delete_kid_chastisment = Chastisement.objects.select_related(
        'schoolkid'
    ).filter(
        schoolkid=kid[0]
    ).delete()


@processing_errors_input_data
def create_commendation(schoolkid_name='Фролов Иван', subject='Музыка'):

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

    kid = [schoolkid for schoolkid in SERIALIZE_SCHOOLKIDS if
           schoolkid_name in schoolkid.full_name]

    check_exists_schoolkid(kid)

    serialize_lessons = Lesson.objects.select_related(
        'subject',
        'teacher'
    ).order_by('date')

    needed_lesson = [lesson for lesson in serialize_lessons if
                     (subject == lesson.subject.title and
                      kid[0].year_of_study == lesson.subject.year_of_study and
                      kid[0].group_letter == lesson.group_letter)]

    if not needed_lesson:
        raise Subject.DoesNotExist

    last_lesson = needed_lesson[-1]

    Commendation.objects.create(
        text=choice(variants_of_commendations),
        created=last_lesson.date,
        schoolkid=kid[0],
        subject=last_lesson.subject,
        teacher=last_lesson.teacher
        )
