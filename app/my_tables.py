from flask_table import Table, Col
from flask import Markup

class Results(Table):
    id = Col('Id', show=False)
    city = Col('City')
    link = Col('Link')
    time_last_data_obtained = Col('Time last data obtained')
    time_of_latest_pull = Col('Time of latest pull')
    link_data_source = Col('Link to data source')

class Item(object):
    def __init__(self, city, link, time_last_data_obtained, time_of_latest_pull, link_data_source):
        self.city = city
        self.link = ( Markup(f'<a href="{link}" target="_blank" title="This will take you to Jupyter Notebooks hosted by docker on your own workstation.">Probe data of {city}</a>') ) if link else None
        self.time_last_data_obtained = time_last_data_obtained
        self.time_of_latest_pull = time_of_latest_pull
        self.link_data_source = Markup(f'<a href="{link_data_source}" target="_blank">{link_data_source}</a>') if link_data_source else None
