import math
from datetime import date, datetime, time
from dateutil import relativedelta
from .models import CalendarEvent, Schedule, Medicine, MedicalEvent

# converts 1 into 1st, 2 into 2nd, etc.
ordinal = lambda n: "%d%s" % (
    n, "tsnrhtdd"[(math.floor(n / 10) % 10 != 1) * (n % 10 < 4) * n % 10::4])

FOAL_LIMIT = 1


def age(horse):
    return int(horse.age / 12)


def already_exists(events, date, msg):
    if events.count() == 0:
        return False
    e = events.filter(msg=msg)
    e = e.filter(date=date.date())
    if e.count() > 0:
        return True
    return False


def update_history(horse):
    events = CalendarEvent.objects.filter(horse__pk=horse.id)
    already_existing_events = horse.history.events.all()
    for event in events:
        if event.medicine is not None:
            if event.start.date() < date.today():
                msg = "{} received a dose of {} today".format(
                    horse.name,
                    event.medicine.name,
                )
                if not already_exists(already_existing_events, event.start, msg):
                    MedicalEvent.objects.create(
                        date=event.start,
                        msg=msg,
                        history=horse.history)


def update_event(horse=None, medicine=None):
    if medicine is not None:
        delete_event(medicine=medicine)
        horses = medicine.horses.all()
        for horse in horses:
            create_event(horse, medicine)
    elif horse is not None:
        delete_event(horse=horse)
        medicines = horse.medicine_set.all()
        for medicine in medicines:
            create_event(horse, medicine)


def delete_event(horse=None, medicine=None):
    events = None
    print(horse)
    print(medicine)
    if horse is not None and medicine is not None:
        events = CalendarEvent.objects.filter(
            horse__pk=horse.id, medicine__pk=medicine.id)
    elif horse is None and medicine is not None:
        events = CalendarEvent.objects.filter(medicine__pk=medicine.id)
    elif horse is not None and medicine is None:
        events = CalendarEvent.objects.filter(horse__pk=horse.id)
    print(events)
    events.delete()


def delete_temp_event(horse=None, medicine=None):
    events = None
    print(horse)
    print(medicine)
    if horse is not None and medicine is not None:
        events = CalendarEvent.objects.filter(
            horse__pk=horse.id, medicine__pk=medicine.id,
        )
        events = events.filter(start__gt=datetime.today(),)
        events.delete()


def create_birth_event(horse, date):
    CalendarEvent.objects.create(
        title="{} was born today.".format(horse.name),
        start=datetime.combine(date, time.min),
        end=datetime.combine(date, time.max),
        all_day=True,
        medicine=None,
        horse=horse
    )


def create_temp_event(horse, medicine):
    """
    Similar to create_event, but uses the
    built in application data of the medicine
    """
    gender_picker = ["his", "her"]
    frequency = medicine.frequency
    interval = medicine.interval
    classification = medicine.classification
    doses = medicine.doses
    pregnant_matches = classification == Schedule.PREGNANT and \
        horse.pregnant == horse.PREGNANT
    foal_matches = classification == Schedule.FOALS and \
        age(horse) <= FOAL_LIMIT
    age_matches = classification == Schedule.ADULTS and \
        age(horse) > FOAL_LIMIT
    age_matches = age_matches or classification == Schedule.ALL
    if pregnant_matches or foal_matches or age_matches:
        print("passed")
        date = None
        offset = None
        if medicine.date_to_start is not None:
            print("dts is not None")
            date = medicine.date_to_start
        else:
            if horse.pregnant == horse.PREGNANT and \
                    classification == Schedule.PREGNANT:
                print("pregnant")
                print(horse.date_of_impregnation)
                date = horse.date_of_impregnation
            else:
                date = horse.dob
        offset = None
        for doses_count in range(0, doses):
            offset_multiplier = doses_count + 1
            offset_multiplier = offset_multiplier * frequency
            if interval == Schedule.WEEKS:
                offset = relativedelta.relativedelta(
                    weeks=offset_multiplier
                )
                print(offset)
            elif interval == Schedule.MONTHS:
                offset = relativedelta.relativedelta(
                    months=offset_multiplier
                )
            else:
                offset = relativedelta.relativedelta(
                    years=offset_multiplier
                )
            application_date_start = datetime.combine(
                date + offset,
                time.min
            )
            application_date_end = datetime.combine(
                date + offset,
                time.max
            )
            msg = "{} needs {} {} dose of {}".format(
                horse.name, gender_picker[horse.gender],
                ordinal(doses_count + 1), medicine.name)
            print(application_date_start)
            CalendarEvent.objects.create(
                title=msg,
                start=application_date_start,
                end=application_date_end,
                all_day=True,
                medicine=medicine,
                horse=horse
            )


def create_event(horse, medicine):
    """
    If the pregnancy status or the age group matches, generate every single
    application event for the medicine and save it.
    """
    schedules = medicine.schedules.all()
    gender_picker = ["his", "her"]
    for schedule in schedules:
        frequency = schedule.frequency
        interval = schedule.interval
        classification = schedule.classification
        doses = schedule.doses
        pregnant_matches = classification == Schedule.PREGNANT and \
            horse.pregnant == horse.PREGNANT
        foal_matches = classification == Schedule.FOALS and \
            age(horse) <= FOAL_LIMIT
        age_matches = classification == Schedule.ADULTS and \
            age(horse) > FOAL_LIMIT
        age_matches = age_matches or classification == Schedule.ALL
        if pregnant_matches or foal_matches or age_matches:
            print("passed")
            date = None
            offset = None
            if medicine.date_to_start is not None:
                print("dts is not None")
                date = medicine.date_to_start
            else:
                if horse.pregnant == horse.PREGNANT and \
                        classification == Schedule.PREGNANT:
                    print("pregnant")
                    print(horse.date_of_impregnation)
                    date = horse.date_of_impregnation
                else:
                    date = horse.dob
            offset = None
            for doses_count in range(0, doses):
                offset_multiplier = doses_count + 1
                offset_multiplier = offset_multiplier * frequency
                if interval == Schedule.WEEKS:
                    offset = relativedelta.relativedelta(
                        weeks=offset_multiplier
                    )
                    print(offset)
                elif interval == Schedule.MONTHS:
                    offset = relativedelta.relativedelta(
                        months=offset_multiplier
                    )
                else:
                    offset = relativedelta.relativedelta(
                        years=offset_multiplier
                    )
                application_date_start = datetime.combine(
                    date + offset,
                    time.min
                )
                application_date_end = datetime.combine(
                    date + offset,
                    time.max
                )
                msg = "{} needs {} {} dose of {}".format(
                    horse.name, gender_picker[horse.gender],
                    ordinal(doses_count + 1), medicine.name)
                print(application_date_start)
                CalendarEvent.objects.create(
                    title=msg,
                    start=application_date_start,
                    end=application_date_end,
                    all_day=True,
                    medicine=medicine,
                    horse=horse
                )


def expired(start_date, today, medicine):
    offset_multiplier = medicine.frequency * medicine.doses
    offset = None
    if medicine.interval == Schedule.WEEKS:
        offset = relativedelta.relativedelta(
            weeks=offset_multiplier
        )
    elif medicine.interval == Schedule.MONTHS:
        offset = relativedelta.relativedelta(
            months=offset_multiplier
        )
    else:
        offset = relativedelta.relativedelta(
            years=offset_multiplier
        )
    final_date = datetime.combine(start_date + offset, time.max)
    return final_date < today


def remove_temporary_medicines(horse):
    temporary_medicines = Medicine.objects.filter(
        date_to_start__isnull=False, horse__pk=horse.id)
    today = datetime.combine(date.today(), time.max)
    condemned_medicines = {}
    for medicine in temporary_medicines:
        medicine_start_date = medicine.date_to_start
        if expired(medicine_start_date, today, medicine):
            condemned_medicines[medicine.id] = medicine
    for medicine in condemned_medicines:
        Medicine.objects.get(pk=medicine).delete()
