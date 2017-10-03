"""Helper functions for BEEtLyme web app"""

from model import connect_to_db, db, User, Symptom, Treatment, UserSymptom
from model import UserTreatment, SymptomEntry, TreatmentEntry
from datetime import datetime
import gviz_api


def run_entry_queries(graph_options, user_id):
    """runs queries to get user symptom entries for graphing """

    entries_list = SymptomEntry.query.join(UserSymptom, Symptom).filter(UserSymptom.user_id == user_id, Symptom.name.in_(graph_options))

    graph_data_dict = {}

    for entry in entries_list:
        key = datetime.date(entry.created_at)
        if key not in graph_data_dict:
            graph_data_dict[key] = {}

        graph_data_dict[key][entry.user_symp.symptom.name] = entry.value

    for date in graph_data_dict:
        values = graph_data_dict[date]
        for option in graph_options:
            if option not in values:
                graph_data_dict[date][option] = None

    print "The graph_data_dict was generated", graph_data_dict
    return graph_data_dict



def create_data_table(graph_options, graph_data_dict):
    """Takes output from run_entry_queries and formats it for data table."""

    description = {}
    description['date'] =  ('date', 'Date')
    for option in graph_options:
        description[option.lower()] = ('number', option)

    list_of_dicts = []

    for date in graph_data_dict:
        values = graph_data_dict[date]
        mini_dict = {}
        mini_dict["date"] = date
        for option in graph_options:
            mini_dict[option.lower()] = values[option]
            list_of_dicts.append(mini_dict)

    graph_options = [option.lower() for option in graph_options]
    column_order = ('date',) + tuple(graph_options)
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(list_of_dicts)
    print "Content-type: text/plain"
    print
    result = data_table.ToJSon(columns_order=column_order, order_by='date')
    print "the result from the create_data function was generated"

    return result


if __name__ == "__main__":

    from server import app

    connect_to_db(app)