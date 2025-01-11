#!/usr/bin/python3

from playwright.sync_api import sync_playwright

LIST_OF_STATES = "https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States"
TARGET_STATE = "greenland"

with sync_playwright() as p:
    browser = p.firefox.launch()
    page = browser.new_page()
    page.goto(LIST_OF_STATES)

    # Find all links, but only from tables
    locator = (
        page.locator("tr")
        .filter(has=page.get_by_role("link"))
        .filter(has_text=TARGET_STATE)
    )
    links = locator.all()

    # Just take first link
    for link in links[:1]:
        # Update status
        with open("status.txt", "w") as f:
            f.write("YES")

        # Take screenshot containing link
        link.scroll_into_view_if_needed(timeout=2000)
        link.hover()
        page.screenshot(path="proof.png")

        # htmx expects an HTML fragment - not just the image.
        # So we need a wrapper here.
        with open("proof", "w") as f:
            f.write("<img alt='Screenshot proof' src='/proof.png'>")

    browser.close()
