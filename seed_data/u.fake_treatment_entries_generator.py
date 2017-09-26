from datetime import timedelta, datetime, date

def bee_venom_data_faker(user_treat_id, number):
    """Generates fake user treatment entry data"""

    start_date = "25-Mar-2017"
    n_date = datetime.strptime(start_date, "%d-%b-%Y")

    for i in range(number, 3):
        n_date = n_date + timedelta(days=1)
        value = 10