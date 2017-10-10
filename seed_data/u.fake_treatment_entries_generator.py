from datetime import timedelta, datetime, date
from random import randint


def bee_venom_data_faker(user_treat_id, number):
    """Generates fake user treatment entry data for Bee Venom"""

    start_date = "25-Mar-2017"
    n_date = datetime.strptime(start_date, "%d-%b-%Y")

    for i in range(0, number, 3):
        n_date = n_date + timedelta(days=3)
        value = randint(8, 14)

        print "{}|{}|{}".format(user_treat_id, value, datetime.date(n_date))


def vitaminC_data_faker(user_treatment_id, number):
    """Generates fake user treatment entry data for Vit C."""

    start_date = "25-Mar-2017"
    n_date = datetime.strptime(start_date, "%d-%b-%Y")

    for i in range(number):
        n_date = n_date + timedelta(days=1)
        value = 3000

        print "{}|{}|{}".format(user_treatment_id, value, datetime.date(n_date))


def magnesium_fake_data_generator(user_treatment_id, number):
    """Generates fake user treatment entry data for magnesium supplementation"""

    start_date = "25-Mar-2017"
    n_date = datetime.strptime(start_date, "%d-%b-%Y")

    for i in range(number):
        n_date = n_date + timedelta(days=1)
        value = 500

        print "{}|{}|{}".format(user_treatment_id, value, datetime.date(n_date))

#all users use bee venom
bee_venom_data_faker(1, 180)
bee_venom_data_faker(2, 180)
bee_venom_data_faker(3, 180)
bee_venom_data_faker(4, 180)
bee_venom_data_faker(5, 180)
bee_venom_data_faker(6, 180)
bee_venom_data_faker(7, 180)
bee_venom_data_faker(8, 180)
bee_venom_data_faker(9, 180)
#all users use vit C
vitaminC_data_faker(10, 180)
vitaminC_data_faker(11, 180)
vitaminC_data_faker(12, 180)
vitaminC_data_faker(13, 180)
vitaminC_data_faker(14, 180)
vitaminC_data_faker(15, 180)
vitaminC_data_faker(16, 180)
vitaminC_data_faker(17, 180)
vitaminC_data_faker(18, 180)
#all users use magnesium
magnesium_fake_data_generator(19, 180)
magnesium_fake_data_generator(20, 180)
magnesium_fake_data_generator(21, 180)
magnesium_fake_data_generator(22, 180)
magnesium_fake_data_generator(23, 180)
magnesium_fake_data_generator(24, 180)
magnesium_fake_data_generator(25, 180)
magnesium_fake_data_generator(26, 180)
magnesium_fake_data_generator(27, 180)
