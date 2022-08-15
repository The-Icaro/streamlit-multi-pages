from requests import get


def get_address_by_zipcode(zipcode: str):
    return get(f"https://viacep.com.br/ws/{zipcode}/json/").json()
