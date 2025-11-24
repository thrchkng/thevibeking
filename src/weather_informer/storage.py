# Простое временное хранилище в памяти
_user_settings = {}

def get_user_settings(user_id: int):
    return _user_settings.get(user_id, {})

def set_user_city(user_id: int, city: str):
    if user_id not in _user_settings:
        _user_settings[user_id] = {}
    _user_settings[user_id]["city"] = city

def set_user_interval(user_id: int, interval_hours: int):
    if user_id not in _user_settings:
        _user_settings[user_id] = {}
    _user_settings[user_id]["interval_hours"] = interval_hours

def get_user_city(user_id: int):
    return _user_settings.get(user_id, {}).get("city")

def has_user_city(user_id: int):
    return bool(get_user_city(user_id))
