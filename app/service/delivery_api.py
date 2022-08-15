from requests import get


def get_all_deliveryman():
    return get("https://cybersecurity-fiap.herokuapp.com/v1/deliveryman").json()


def get_all_buyers():
    return get("https://cybersecurity-fiap.herokuapp.com/v1/buyer").json()


def get_all_deliveries():
    return get("https://cybersecurity-fiap.herokuapp.com/v1/delivery").json()


def find_deliveryman_by_id(id: int):
    return get(f"https://cybersecurity-fiap.herokuapp.com/v1/deliveryman/{id}").json()


def find_buyer_by_id(id: int):
    return get(f"https://cybersecurity-fiap.herokuapp.com/v1/buyer/{id}").json()
