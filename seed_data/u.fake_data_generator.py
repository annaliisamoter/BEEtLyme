from datetime import timedelta, datetime, date
from random import randint

def random_data_by_1(user_symp_id, number):
    """Generates 'number' of random input values taking user_symp_id and number as args.
        Mimics real world data by only moving one or two points up or down from
        entry to entry.
    """

    starting_int = randint(1, 9)
    start_date = "25-Mar-2017"
    n_date = datetime.strptime(start_date, "%d-%b-%Y")

    for i in range(number):
        n_date = n_date + timedelta(days=1)
        
        if starting_int <= 1:
            value = 2
            starting_int = value
        elif starting_int <= 9:
            value = randint((starting_int - 1), (starting_int + 1))
            starting_int = value
        elif starting_int >= 10:
            value = 9
            starting_int = value
        

        print "{}|{}|{}".format(user_symp_id, value, datetime.date(n_date))


def random_data_by_2(user_symp_id, number):
    """Generates 'number' of random input values taking user_symp_id and number as args.
        Moves up and down in a bigger range.
    """

    starting_int = randint(1, 9)
    start_date = "25-Mar-2017"
    n_date = datetime.strptime(start_date, "%d-%b-%Y")

    for i in range(number):
        n_date = n_date + timedelta(days=1)

        if starting_int <= 1:
            value = 2
            starting_int = value
        elif starting_int <= 9:
            value = randint((starting_int - 2), (starting_int + 2))
            starting_int = value
        elif starting_int >= 10:
            value = 8
            starting_int = value
        

        print "{}|{}|{}".format(user_symp_id, value, datetime.date(n_date))


def completely_random_data(user_symp_id, number):
    """Generates 'number' of completely random input values (0-10) taking user_symp_id and number as args."""

    start_date = "25-Mar-2017"
    n_date = datetime.strptime(start_date, "%d-%b-%Y")

    for i in range(number):
        n_date = n_date + timedelta(days=1)
        value = randint(0, 10)

        print "{}|{}|{}".format(user_symp_id, value, datetime.date(n_date))


random_data_by_1(1, 180)
random_data_by_1(2, 180)
random_data_by_1(3, 180)
random_data_by_1(4, 180)
random_data_by_1(5, 180)
random_data_by_1(6, 180)

random_data_by_2(7, 180)
random_data_by_2(8, 180)
random_data_by_2(9, 180)
random_data_by_2(10, 180)
random_data_by_2(11, 180)

completely_random_data(12, 180)
completely_random_data(13, 180)
completely_random_data(14, 180)
completely_random_data(15, 180)
completely_random_data(16, 180)






