from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from config import LOGIN, PASSWORD

def get_online_girl():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. LOGIN PAGE
        page.goto("https://findbride.com/login", timeout=60000)

        # 2. FILL LOGIN FORM (селекторы могут отличаться, но обычно такие)
        page.fill('input[name="email"]', LOGIN)
        page.fill('input[name="password"]', PASSWORD)

        page.click('button[type="submit"]')

        page.wait_for_timeout(5000)

        # 3. GO TO MEMBERS PAGE
        page.goto(
            "https://findbride.com/members?age%5Bfrom%5D=25&age%5Bto%5D=40",
            timeout=60000
        )

        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        profiles = soup.select(".member-item")

        for profile in profiles:
            if "online" not in str(profile):
                continue

            name = profile.select_one(".member-name")
            age = profile.select_one(".member-age")
            country = profile.select_one(".member-country")
            link_tag = profile.select_one("a")
            img_tag = profile.select_one("img")

            if name and age and country and link_tag and img_tag:
                browser.close()
                return {
                    "name": name.text.strip(),
                    "age": age.text.strip(),
                    "country": country.text.strip(),
                    "link": "https://findbride.com" + link_tag["href"],
                    "img": img_tag["src"]
                }

        browser.close()
        return None
