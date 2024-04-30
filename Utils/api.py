import requests
import json
import logging
from urllib.parse import urlparse
import datetime
import Utils


def get_admin_uuid_from_url(url):
    try:
        parsed_url = urlparse(url)
        admin_uuid = parsed_url.path.split('/')[2]
        return admin_uuid
    except Exception as e:
        logging.error("Error extracting admin_uuid from URL: %s" % e)
        return None


def select(url, endpoint="/user/"):
    try:
        admin_uuid = get_admin_uuid_from_url(url)
        if not admin_uuid:
            return None
        headers = {'Hiddify-API-Key': admin_uuid}
        response = requests.get(url + endpoint, headers=headers)
        res = Utils.utils.dict_process(
            url, Utils.utils.users_to_dict(response.json()))
        return res
    except Exception as e:
        logging.error("API error: %s" % e)
        return None


def find(url, uuid, endpoint="/user/"):
    try:
        admin_uuid = get_admin_uuid_from_url(url)
        if not admin_uuid:
            return None
        headers = {'Hiddify-API-Key': admin_uuid}
        response = requests.get(
            url + endpoint, params={"uuid": uuid}, headers=headers)
        jr = response.json()
        if len(jr) != 1:
            for user in jr:
                if user['uuid'] == uuid:
                    return user
            return None
        return jr[0]
    except Exception as e:
        logging.error("API error: %s" % e)
        return None


def insert(url, name, usage_limit_GB, package_days, last_reset_time=None, added_by_uuid=None, mode="no_reset",
           last_online="1-01-01 00:00:00", telegram_id=None,
           comment=None, current_usage_GB=0, start_date=None, endpoint="/user/"):
    try:
        admin_uuid = get_admin_uuid_from_url(url)
        if not admin_uuid:
            return None
        import uuid
        uuid = str(uuid.uuid4())
        added_by_uuid = urlparse(url).path.split('/')[2]
        last_reset_time = datetime.datetime.now().strftime("%Y-%m-%d")

        data = {
            "uuid": uuid,
            "name": name,
            "usage_limit_GB": usage_limit_GB,
            "package_days": package_days,
            "added_by_uuid": added_by_uuid,
            "last_reset_time": last_reset_time,
            "mode": mode,
            "last_online": last_online,
            "telegram_id": telegram_id,
            "comment": comment,
            "current_usage_GB": current_usage_GB,
            "start_date": start_date
        }
        jdata = json.dumps(data)
        headers = {'Content-Type': 'application/json',
                   'Hiddify-API-Key': admin_uuid}
        response = requests.post(url + endpoint, data=jdata, headers=headers)
        return uuid
    except Exception as e:
        logging.error("API error: %s" % e)
        return None


def update(url, uuid, endpoint="/user/", **kwargs):
    try:
        admin_uuid = get_admin_uuid_from_url(url)
        if not admin_uuid:
            return None
        user = find(url, uuid)
        if not user:
            return None
        for key in kwargs:
            user[key] = kwargs[key]
        headers = {'Content-Type': 'application/json',
                   'Hiddify-API-Key': admin_uuid}
        response = requests.post(
            url + endpoint, data=json.dumps(user), headers=headers)
        return uuid
    except Exception as e:
        logging.error("API error: %s" % e)
        return None
