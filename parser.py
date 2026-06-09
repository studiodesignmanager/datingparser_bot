
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
from config import LOGIN, PASSWORD

BASE_URL = "https://findbride.com"


def get_online_girl():
    print("🚀 START PLAYWRIGHT PARSER")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # -------------------
            # 1. OPEN SITE
            # -------------------
            print("🌍 OPEN SITE")
            page.goto(BASE_URL, timeout=60000)

            page.wait_for_timeout(3000)

            # -------------------
            # 2. CLICK LOGIN
            # -------------------
            print("🔑 CLICK LOGIN")

            try:
                page.click("text=Login")
            except:
                try:
                    page.click("text=Log in")
                except:
                    try:
                        page.click("text=Sign in")
                    except:
                        print("❌ LOGIN BUTTON NOT FOUND")

            page.wait_for_timeout(5000)

            # -------------------
            # DEBUG: SHOW HTML AFTER LOGIN CLICK
            # -------------------
            print("📸 HTML AFTER LOGIN CLICK (FIRST 1500 CHARS)")
            html = page.content()
            print(html[:1500])

            # -------------------
            # 3. TRY LOGIN (TEMP DISABLED)
            # -------------------
            print("✍️ LOGIN STEP SKIPPED FOR DEBUG")

            # page.fill('input[name="email"]', LOGIN)
            # page.fill('input[name="password"]', PASSWORD)
            # page.click('button[type="submit"]')

            page.wait_for_timeout(5000)

            # -------------------
            # 4. OPEN MEMBERS PAGE
            # -------------------
            print("👥 OPEN MEMBERS PAGE")

            page.goto(
                f"{BASE_URL}/members?age%5Bfrom%5D=25&age%5Bto%5D=40",
                timeout=60000
            )

            page.wait_for_timeout(5000)

            # -------------------
            # 5. PARSE HTML
            # -------------------
            html = page.content()

            from bs4 import BeautifulSoup
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

                if not all([name, age, country, link_tag]):
                    continue

                result = {
                    "name": name.text.strip(),
                    "age": age.text.strip(),
                    "country": country.text.strip(),
                    "link": urljoin(BASE_URL, link_tag["href"]),
                    "img": img_tag["src"] if img_tag else None
                }

                print("📦 FOUND GIRL:", result)

                browser.close()
                return result

            print("❌ NO ONLINE GIRLS FOUND")

            browser.close()
            return None

        except Exception as e:
            print("💥 ERROR:", e)
            browser.close()
            return None


# -----------------------
# ENTRY POINT
# -----------------------
if __name__ == "__main__":
    result = get_online_girl()
    print("✅ FINAL RESULT:", result)
