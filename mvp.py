import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service # Not needed if Chrome installed via packages.txt
from selenium_stealth import stealth
from PIL import Image
import time
import os # Import os to handle potential file cleanup

# Streamlit UI
st.title("Website Screenshot App")
url = st.text_input("Enter website URL", "https://www.kayak.es/flights/BCN-HAN/2025-06-13/2025-06-29?ucs=ernz75&sort=bestflight_a")

if st.button("Capture Screenshot"):
    options = Options()
    options.add_argument("--headless")
    # --- Essential arguments for Streamlit Cloud ---
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu") # Often necessary for headless stability
    # --- End essential arguments ---

    options.add_argument("--window-size=1920,1080") # Set window size via argument

    # Proxy setting (keep as is)
    options.add_argument("--proxy-server=https://scraperapi.screenshot=true:a9755f0a02aa82bb4eed7c5698527196@proxy-server.scraperapi.com:8001")

    driver = None # Initialize driver to None
    try:
        # Selenium 4+ should find chromedriver automatically if google-chrome-stable is installed
        driver = webdriver.Chrome(options=options)
        # driver.set_window_size(1920, 1080) # Already set via options argument

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
        time.sleep(5)  # Keep original sleep time

        # Take Screenshot
        screenshot_path = "screenshot.png"
        driver.get_screenshot_as_file(screenshot_path)


        # Display screenshot
        image = Image.open(screenshot_path)
        st.image(image, caption="Captured Screenshot", use_container_width=True)

        # Optional clean up screenshot file after displaying
        if os.path.exists(screenshot_path):
             os.remove(screenshot_path)

    except Exception as e:
        st.error(f"An error occurred: {e}") # Basic error display

    finally:
        # Ensure the driver is closed even if an error occurs
        if driver:
            driver.quit()
