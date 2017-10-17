"""Helper functions for BEEtLyme web app"""

from model import connect_to_db, db, User, Symptom, Treatment, UserSymptom
from model import UserTreatment, SymptomEntry, TreatmentEntry, FullMoon, NewMoon
from datetime import datetime


def plotly_helper_symp(symptom_option, user_id):
    """Query db for plotly graph
        Takes a graph_option and user_id passed in from graph options url.
        Return a dict ready for trace implementation.
          example:
          {
          'type': "scatter",
          'mode': "lines",
          'name': 'Symptom 1',
          'x': [datetime objects],
          'y': [corresponding symptom values],
        }
    """
    entry_objects = SymptomEntry.query.join(UserSymptom, Symptom).filter(UserSymptom.user_id == user_id, Symptom.name == symptom_option).order_by(SymptomEntry.created_at).all()
    return {
        'type': 'scatter',
        'mode': 'lines',
        'name': symptom_option,
        'line': {'shape': 'spline'},
        'showlegend': 'true',
        'x':  [entry_obj.created_at.strftime("%Y-%m-%d") for entry_obj in entry_objects],
        'y': [entry_obj.value for entry_obj in entry_objects]
    }


def plotly_helper_treat(treatment_option, user_id):
    """Query db for plotly graph
        Takes a graph_option and user_id passed in from graph options url.
        Return a dict ready for trace implementation.
          example:
          {
          'type': "scatter",
          'mode': "lines",
          'name': 'Treatment',
          'x': [date string],
          'y': [corresponding treatment values],
        }
    """
    entry_objects = TreatmentEntry.query.join(UserTreatment, Treatment).filter(UserTreatment.user_id == user_id, Treatment.name == treatment_option).order_by(TreatmentEntry.created_at).all()

    if treatment_option == 'Bee Venom':
        return {
            'type': 'scatter',
            'mode': 'lines',
            'name': treatment_option,
            'line': {'shape': 'spline'},
            'showlegend': 'true',
            'x':  [entry_obj.created_at.strftime("%Y-%m-%d") for entry_obj in entry_objects],
            'y': [entry_obj.value for entry_obj in entry_objects],
        }
    else:
        return {
            'type': 'scatter',
            'mode': 'lines',
            'name': treatment_option,
            'line': {'shape': 'spline'},
            'showlegend': 'true',
            'x':  [entry_obj.created_at.strftime("%Y-%m-%d") for entry_obj in entry_objects],
            'y': [entry_obj.value for entry_obj in entry_objects],
            'yaxis': 'y2',
        }


def get_date_range(total_data):
    """Calculates the range of dates to get moon phases for."""

    first_date = total_data['data'][0]['x'][0]
    last_date = total_data['data'][0]['x'][-1]
    first_date = datetime.strptime(first_date, '%Y-%m-%d')
    last_date = datetime.strptime(last_date, '%Y-%m-%d')
    date_range = (first_date, last_date)
    return date_range


def full_moon_phase_overlay(date_range):
    """creates trace data for full moon phase graph overlay."""

    dates = db.session.query(FullMoon.full_moon_date).filter(FullMoon.full_moon_date.between(date_range[0], date_range[1])).all()
    print "dates from within the db query for full_moon phase helper function", dates
    return {
        'mode': 'markers',
        'type': 'scatter',
        'name': 'Full Moons',
        'showlegend': 'true',
        'marker': {
                'color': '#d3d3d3',
                'size': 20},
        'x': [date[0].strftime("%Y-%m-%d") for date in dates],
        'y': [16 for date in dates]
        }


def new_moon_phase_overlay(date_range):
    """creates trace data for new moon phase graph overlay."""

    dates = db.session.query(NewMoon.new_moon_date).filter(NewMoon.new_moon_date.between(date_range[0], date_range[1])).all()
    print "dates from within the db query for new_moon phase helper function", dates
    return {
        'mode': 'markers',
        'type': 'scatter',
        'name': 'New Moons',
        'showlegend': 'true',
        'marker': {
                'color': 'black',
                'size': 20
                },
        'x': [date[0].strftime("%Y-%m-%d") for date in dates],
        'y': [16 for date in dates]
        }



if __name__ == "__main__":  #pragma: no cover

    from server import app

    connect_to_db(app)