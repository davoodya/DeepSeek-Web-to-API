from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headless=False تا پنجره کروم را ببینید
    page = browser.new_page()
    page.goto("https://www.google.com")
    print(f"Page title: {page.title()}")
    input("Press Enter to close browser...")  # تا ببینید کروم باز شده
    browser.close()