import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from PIL import Image
import time

# Streamlit UI
st.title("Website Screenshot App")
url = st.text_input("Enter website URL", "https://www.kayak.es/flights/BCN-HAN/2025-06-13/2025-06-29?ucs=ernz75&sort=bestflight_a")

if st.button("Capture Screenshot"):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--proxy-server=https://scraperapi.screenshot=true:a9755f0a02aa82bb4eed7c5698527196@proxy-server.scraperapi.com:8001")

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)  # Set window size to Full HD

    # Apply stealth settings
    stealth(
        driver,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True
    )

    # Modify navigator properties using JavaScript
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """
        },
    )

    # Open the website
    driver.get(url)
    time.sleep(5)  # Ensure the page loads

    # Take Screenshot
    screenshot_path = "screenshot.png"
    driver.get_screenshot_as_file(screenshot_path)
    driver.quit()

    # Display screenshot
    image = Image.open(screenshot_path)
    st.image(image, caption="Captured Screenshot", use_container_width=True)