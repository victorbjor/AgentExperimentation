from playwright.sync_api import sync_playwright

# Start Playwright and launch the browser
playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False)  # Set headless=True if you don't want the UI
page = browser.new_page()

page.goto('localhost:3000')

browser.close()
playwright.stop()


from playwright.sync_api import sync_playwright

def extract_page_elements(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        # Extract images
        images = page.query_selector_all('img')
        image_data = [img.get_attribute('src') for img in images]

        # Extract buttons
        buttons = page.query_selector_all('button')
        button_data = [btn.inner_text() for btn in buttons]

        # Extract links
        links = page.query_selector_all('a')
        link_data = [(link.inner_text(), link.get_attribute('href')) for link in links]

        # Optionally extract text content
        text = page.content()

        browser.close()

    return {
        'images': image_data,
        'buttons': button_data,
        'links': link_data,
        'text': text[:500],  # Limit to the first 500 characters for brevity
    }

# Example usage
url = 'https://example.com'
page_info = extract_page_elements(url)
print(page_info)