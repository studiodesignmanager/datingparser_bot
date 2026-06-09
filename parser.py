
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from config import LOGIN, PASSWORD


def get_online_girl():
    print("🔥 START get_online_girl")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # 1. OPEN MAIN PAGE
            print("🌍 OPENING SITE")
            page.goto("https://findbride.com", timeout=60000)

            page.wait_for_timeout(3000)

            # 2. CLICK LOGIN BUTTON
            print("🔑 CLICK LOGIN BUTTON")

            try:
                page.click("text=Login")
            except:
                try:
                    page.click("text=Log in")
                except:
                    page.click("text=Sign in")

            page.wait_for_timeout(3000)

            # 3. FILL FORM
            print("✍️ FILL LOGIN FORM")

            page.fill('input[name="email"]', LOGIN)
            page.fill('input[name="password"]', PASSWORD)

            # 4. SUBMIT
            print("🚀 SUBMIT LOGIN")

            page.click('button[type="submit"]')

            page.wait_for_timeout(7000)

            # 5. GO TO MEMBERS
            print("👥 OPEN MEMBERS PAGE")

            page.goto(
                "https://findbride.com/members?age%5Bfrom%5D=25&age%5Bto%5D=40",
                timeout=60000
            )

            html = page.content()

            print("📦 PAGE LOADED, PARSING HTML")

            soup = BeautifulSoup(html, "html.parser")
            profiles = soup.select(".member-item")

            print(f"🔎 FOUND PROFILES: {len(profiles)}")

            for profile in profiles:
                if "online" not in str(profile).lower():
                    continue

                name = profile.select_one(".member-name")
                age = profile.select_one(".member-age")
                country = profile.select_one(".member-country")
                link_tag = profile.select_one("a")
                img_tag = profile.select_one("img")

                if name and age and country and link_tag and img_tag:
                    result = {
                        "name": name.text.strip(),
                        "age": age.text.strip(),
                        "country": country.text.strip(),
                        "link": "https://findbride.com" + link_tag["href"],
                        "img": img_tag["src"]
                    }

                    print("📦 RETURN RESULT")
                    browser.close()
                    return result

            print("❌ NO ONLINE PROFILES FOUND")

            browser.close()
            return None

        except Exception as e:
            print("💥 ERROR:", e)
            browser.close()
            return None


if __name__ == "__main__":
    print("🚀 PARSER STARTED")
    result = get_online_girl()
    print("✅ RESULT:", result)
