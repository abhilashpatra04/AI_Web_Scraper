from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
import time
import traceback

def select_makemytrip_date(driver, date_str):
    """Handles MakeMyTrip's complex date picker"""
    try:
        # Parse input date (format: DD-MM-YYYY)
        day = date_str.split('-')[0]
        month_year = datetime.strptime(date_str, '%d-%m-%Y').strftime('%b %Y')

        # Click to open date picker
        date_picker = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='travelDate']"))
        )
        date_picker.click()
        time.sleep(3)

        # Wait for calendar to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "DayPicker-Month"))
        )

        # Navigate to correct month/year
        while True:
            current_month = driver.find_element(By.CSS_SELECTOR, ".DayPicker-Caption > div").text
            if month_year in current_month:
                break

            next_btn = driver.find_element(By.CSS_SELECTOR, ".DayPicker-NavButton--next")
            ActionChains(driver).move_to_element(next_btn).click().perform()
            time.sleep(0.5)

        # Select specific day
        day_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class,'DayPicker-Day') and not(contains(@class,'disabled'))]//p[contains(text(),'{day}')]"))
        )
        day_element.click()

        # Verify selection
        selected_date = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p[data-cy='departureDate']"))
        ).text
        print(f"✅ Selected date: {selected_date}")

    except Exception as e:
        print(f"❌ Date selection failed: {str(e)}")
        driver.save_screenshot("date_error.png")
        raise

def scrape_makemytrip_schedule(source, destination, travel_date):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.makemytrip.com/railways/")
        time.sleep(3)

        # Close login modal if it appears
        try:
            driver.find_element(By.CLASS_NAME, "modalClose").click()
        except:
            pass

        # Hide interfering slider if it exists
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "sliderItemContent"))
            )
            driver.execute_script("""
                let popup = document.querySelector('.sliderItemContent');
                if (popup) { popup.style.display = 'none'; }
            """)
            print("🧹 Popup slider hidden.")
        except:
            pass

        # Select source station
        from_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "fromCity"))
        )
        from_input.click()
        from_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='From']"))
        )
        from_field.clear()
        from_field.send_keys(source + Keys.ARROW_DOWN + Keys.RETURN)

        # Select destination station
        to_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "toCity"))
        )
        to_input.click()
        to_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='To']"))
        )
        to_field.clear()
        to_field.send_keys(destination + Keys.ARROW_DOWN + Keys.RETURN)

        # Select date
        select_makemytrip_date(driver, travel_date)

        # Click search button
        search_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-cy='submit']"))
        )
        search_btn.click()

        print("🔄 Waiting for train list...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".train-heading "))
        )

        train_elements = driver.find_elements(By.CSS_SELECTOR, ".train-heading")
        trains = [train.text for train in train_elements]
        return trains

    except Exception as e:
        print("❌ Error:", str(e))
        traceback.print_exc()
        driver.save_screenshot("scrape_error.png")
        return []

    finally:
        driver.quit()
