import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config import HEADERS, LOGIN_URL, LOGIN, PASSWORD


BASE_URL = "https://findbride.com"


def login(session):
    payload = {
        "email": LOGIN,
        "password": PASSWORD
    }

    resp = session.post(LOGIN_URL, data=payload, headers=HEADERS)

    # более реалистичная проверка логина
    if resp.status_code != 200:
        print("Login failed: bad status")
        return False

    text = resp.text.lower()

    if "logout" in text or "sign out" in text:
        return True

    print("Login might have failed (no logout marker)")
    return False


def is_online(profile):
    classes = profile.get("class", [])
    return (
        "online" in classes
        or profile.select_one(".online") is not None
        or "online" in profile.text.lower()
    )


def get_img(img_tag):
    if not img_tag:
        return None
    return (
        img_tag.get("data-src")
        or img_tag.get("src")
    )


def get_online_girl():
    with requests.Session() as session:

        # LOGIN
        if not login(session):
            return None

        url = f"{BASE_URL}/members?age[from]=25&age[to]=40"
        resp = session.get(url, headers=HEADERS)

        if resp.status_code != 200:
            print("Failed to load members page:", resp.status_code)
            return None

        soup = BeautifulSoup(resp.text, "html.parser")
        profiles = soup.select(".member-item")

        if not profiles:
            print("No profiles found (HTML structure may have changed)")
            return None

        # перебираем профили
        for profile in profiles:

            if not is_online(profile):
                continue

            name = profile.select_one(".member-name")
            age = profile.select_one(".member-age")
            country = profile.select_one(".member-country")
            link_tag = profile.select_one("a")
            img_tag = profile.select_one("img")

            if not all([name, age, country, link_tag]):
                continue

            img = get_img(img_tag)
            if not img:
                continue

            return {
                "name": name.text.strip(),
                "age": age.text.strip(),
                "country": country.text.strip(),
                "link": urljoin(BASE_URL, link_tag["href"]),
                "img": img
            }

    return None
