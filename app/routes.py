from app import app
from flask import render_template
from flask import request
from flask import Markup
from flask import send_from_directory

from datetime import datetime
import json
import os
import markdown

from app.my_tables import Results
from app.my_tables import Item

@app.route('/')
@app.route('/index')
def index():
    table = getTable()
    return render_template('index.html', title='Home page', table=table)

@app.route('/about')
def about():
    with open('README.md', 'r') as f:
        my_content = markdown.markdown(f.read())
    return render_template('about.html', title='About page', my_content=Markup(my_content))

@app.route('/update', methods=['POST'])
def update():
    city_name = request.form.get('city') 
    if city_name:
        print(f'Updating data of {city_name}..')
        if Config.cities[city_name].funcs.update():
            write_status(city_name, "update", { 'success' : datetime.now() })
        else:
            write_status(city_name, "update", { 'fail' : datetime.now() })
    else:
        raise Exception('Internal Error: "city" value is not found in POST request')

    table = getTable()
    return render_template('index.html', table=table)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
from app.config import Config, prepare_target_dir

def getTable() -> Results:
    #return("Hello, World!")
    incoming_url_root = request.url_root
    notebook_url_root = incoming_url_root.replace(":2020/", ":2021/") + 'tree/sample_programs'

    results = []
    for city_name in Config.cities:
        if ( city_name != 'Add your own city here' ) :
            update_button = Markup(f'<form method="post" action="/update">'
                '<button type="submit" class="sbtn btn btn-secondary btn-c" title="Click to load update" onclick="spinner()">Update Data</button>'
                '<div class="loader"> <div class="loading"> </div> </div>'
                f'<input type="hidden" name="city" value="{city_name}" />'
    	        f'</form>'
                """
                <script type="text/javascript">
                function spinner() {
                document.getElementsByClassName("loader")[0].style.display = "block";
                }
                </script> 
                """ \
                )

            results.append(Item(city_name, 
                notebook_url_root, 
                (Config.cities[city_name].funcs.get_latest_datetime)() \
                    if Config.cities[city_name].funcs.get_latest_datetime else None, 
                ( read_time_of_latest_pull(city_name) + update_button ) if update_button else None,
                Config.cities[city_name].link_data_source))
        else:
            results.append(Item(city_name, 
                None,
                None,
                None,
                None))

    table = Results(results)
    table.border = True
  
    return table 

def write_status(city_name, key, value):
    prepare_target_dir(os.path.join(Config.path_data, city_name))
    path_file = os.path.join(Config.path_data, city_name, Config.filename_status)
    with open(path_file, 'w') as f:
        json.dump( { key : value }, f, indent=4, sort_keys=True, default=str )

def read_status(city_name):
    path_file = os.path.join(Config.path_data, city_name, Config.filename_status)
    try:
        with open(path_file) as f:
            json_data = json.load(f)
        return json_data
    except:
        return None

def read_time_of_latest_pull(city_name):
    json_data = read_status(city_name)
    if json_data:
        status_update = json_data['update']
        t = list(status_update.values())[0].split('.')[0]
        td = t.split(' ')[0]
        th = t.split(' ')[1]
        s = list(status_update.keys())[0]
        return f'{td}T{th}Z ({s})'
    else:
        return ""
