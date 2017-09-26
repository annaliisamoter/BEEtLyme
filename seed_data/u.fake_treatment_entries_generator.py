from datetime import timedelta, datetime, date

def bee_venom_data_faker(user_treat_id, number):
    """Generates fake user treatment entry data"""

    start_date = "25-Mar-2017"
    n_date = datetime.strptime(start_date, "%d-%b-%Y")

    for i in range(0, number, 3):
        n_date = n_date + timedelta(days=3)
        value = 10

        print "{}|{}|{}".format(user_treat_id, value, datetime.date(n_date))


bee_venom_data_faker(1, 180)
bee_venom_data_faker(2, 180)
bee_venom_data_faker(3, 180)
bee_venom_data_faker(4, 180)
bee_venom_data_faker(5, 180)
bee_venom_data_faker(6, 180)
bee_venom_data_faker(7, 180)
bee_venom_data_faker(8, 180)
bee_venom_data_faker(9, 180)