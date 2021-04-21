class Config:
    cities = {}
    subfolder_archive = 'archive'
    subfolder_tmp = 'tmp'
    filename_source = 'data.txt'
    path_data = 'vol_mount/raw_data'
    filename_status = '.status'

class Updater:
    def __init__(self, func_update, func_get_latest_datetime = None):
        self.update = func_update
        self.get_latest_datetime = func_get_latest_datetime

class City:
    def __init__(self, name, funcs, link_data_source):
        self.name = name
        self.funcs = funcs
        self.link_data_source = link_data_source

import os
import shutil
import pycurl
def prepare_target_dir(target_dir):
    try:
        if not os.access(target_dir, os.W_OK):
            os.makedirs(target_dir, exist_ok = True)
    except Exception:
        raise

    dir_archive = os.path.join(target_dir, Config.subfolder_archive)
    try:
        os.makedirs(dir_archive, exist_ok = True)
    except Exception:
        raise

    dir_tmp = os.path.join(target_dir, Config.subfolder_tmp)
    try:
        os.makedirs(dir_tmp, exist_ok = True)
    except Exception:
        raise

def prepare_target_file(target_dir, filename):
    prepare_target_dir(target_dir)
    dir_tmp = os.path.join(target_dir, Config.subfolder_tmp)
    file_tmp = os.path.join(dir_tmp, filename)
    if os.path.isfile(file_tmp):
        os.remove(file_tmp)

def finalize_target_file(target_dir, filename):
    dir_archive = os.path.join(target_dir, Config.subfolder_archive)
    dir_tmp = os.path.join(target_dir, Config.subfolder_tmp)
    file_tmp = os.path.join(dir_tmp, filename)
    if os.path.exists(file_tmp):
        file_target = os.path.join(target_dir, filename)
        if os.path.exists(file_target):
            file_archive = os.path.join(dir_archive, filename)
            shutil.move(file_target, file_archive)
        shutil.move(file_tmp, file_target)

def curl(url, target_dir, filename):
    prepare_target_file(target_dir, filename)

    dir_tmp = os.path.join(target_dir, Config.subfolder_tmp)
    file_tmp = os.path.join(dir_tmp, filename)
    with open(file_tmp, 'wb') as f:
        c = pycurl.Curl()
        c.setopt(c.VERBOSE, True)
        c.setopt(c.URL, url)
        c.setopt(c.WRITEDATA, f)
        c.perform()
        c.close()

    finalize_target_file(target_dir, filename)


import json 
from datetime import datetime

##### Ottawa, ON, CA #####
city_ottawa_on_ca = City('Ottawa, ON, CA', None, 'https://open.ottawa.ca/datasets/6bfe7832017546e5b30c5cc6a201091b/geoservice')
def updater_ottawa_on_ca():
    try:
        query_url = 'https://opendata.arcgis.com/datasets/6bfe7832017546e5b30c5cc6a201091b_0/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json'
        prepare_target_file(os.path.join(Config.path_data, city_ottawa_on_ca.name), Config.filename_source)
        curl(query_url, os.path.join(Config.path_data, city_ottawa_on_ca.name), Config.filename_source)
        finalize_target_file(os.path.join(Config.path_data, city_ottawa_on_ca.name), Config.filename_source)
        return True
    except:
        return False

def get_latest_datetime_ottawa_on_ca():
    try:
        with open(os.path.join(Config.path_data, city_ottawa_on_ca.name, Config.filename_source)) as f:
            json_data = json.load(f)
            features = json_data['features']
            return datetime.fromtimestamp(max([f['attributes']['Date'] for f in features]) // 1000)
    except:
        return None

city_ottawa_on_ca.funcs = Updater(updater_ottawa_on_ca, get_latest_datetime_ottawa_on_ca)
Config.cities[city_ottawa_on_ca.name] = city_ottawa_on_ca


##### Toronto, ON, CA #####
import requests
city_toronto_on_ca = City('Toronto, ON, CA', None, 'https://open.toronto.ca/dataset/covid-19-cases-in-toronto/')
def updater_toronto_on_ca():
    try:
        prepare_target_file(os.path.join(Config.path_data, city_toronto_on_ca.name), Config.filename_source)
        url = "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/package_show"
        params = { "id": "64b54586-6180-4485-83eb-81e8fae3b8fe"}
        package = requests.get(url, params = params).json()
        print(package["result"])

        for idx, resource in enumerate(package["result"]["resources"]):
            if resource["datastore_active"]:
                url = "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search"
                p = { "id": resource["id"], "sort": "_id desc", "limit" : 50000 }
                data = requests.get(url, params = p).json()
                with open( os.path.join(Config.path_data, city_toronto_on_ca.name, Config.filename_source), 'w' ) as outfile:
                    json.dump(data, outfile, indent=4, sort_keys=True, default=str)
                break

        finalize_target_file(os.path.join(Config.path_data, city_toronto_on_ca.name), Config.filename_source)
        return True
    except:
        return False
def get_latest_datetime_toronto_on_ca():
    try:
        with open(os.path.join(Config.path_data, city_toronto_on_ca.name, Config.filename_source)) as f:
            json_data = json.load(f)
            json_data = json_data['result']['records']
            return datetime. strptime(max([r['Reported Date'] for r in json_data]), '%Y-%m-%d')
    except:
        return None

city_toronto_on_ca.funcs = Updater(updater_toronto_on_ca, get_latest_datetime_toronto_on_ca)
Config.cities[city_toronto_on_ca.name] = city_toronto_on_ca

city_other = City('Add your own city here', None, None)
Config.cities[city_other.name] = city_other
