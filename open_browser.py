from playwright.sync_api import sync_playwright
import time
import json
import os
from dotenv import load_dotenv
import logging
browser = None

load_dotenv()

def open_browser():
    try:
        with sync_playwright() as p:
            browser_port = os.getenv('browser_port')
            if not browser_port:
                json_response = json.dumps({"status": False, "data": "", "message": "browser_port environment variable is not set."})
                print(json_response)
                return False
                
            
            print("starting browser")
            
            # browser = p.chromium.launch(headless=True)   # Default is Chromium
            browser = p.chromium.launch(
                headless=True,
                args=[
                    f"--remote-debugging-port={browser_port}",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-gpu"  # May also help with Docker compatibility
                ]
            )
            page = browser.new_page()
            page.goto('https://x.com/i/flow/login')
            print('inside the browser')
            # Fill in the input field with autocomplete="username"
            page.fill('[autocomplete="username"]', os.getenv('twitter_email'))

            # Check if the button with text "Next" exists
            if page.inner_text('text="Next"'):
                # Click on the button
                page.click('text="Next"')
            else:
                logging.error("Button with text 'Next' not found.")
                json_response = json.dumps({"status": False, "data": "", "message": "Button with text 'Next' not found."})
                print(json_response)
                
            page.wait_for_timeout(7000)
            
            try:
                input_field = page.wait_for_selector('[data-testid="ocfEnterTextTextInput"]')
                if input_field:
                    logging.warning("nput field found, filling with Twitter username...")
                    page.fill('[data-testid="ocfEnterTextTextInput"]', os.getenv('twitter_user'))
                    next_button = page.wait_for_selector('[data-testid="ocfEnterTextNextButton"]')
                    if next_button:
                        logging.warning("Next button found, clicking...")
                        page.click('[data-testid="ocfEnterTextNextButton"]')
                    else:
                        logging.warning("Button with text 'Next' not found.")
                else:
                    logging.warning("Input field with data-testid 'ocfEnterTextTextInput' not found.")
            except Exception as e:
                print("")
            
            logging.warning("filling password...")
            page.fill('[name="password"]', os.getenv('twitter_pass'))

            if page.inner_text('text="Log in"'):
                # Click on the button
                page.click('text="Log in"')
                logging.warning("clicked login...")
            else:
                json_response = json.dumps({"status": False, "data": "", "message": "Button with text 'Log in' not found."})
                print(json_response)
            
            logging.warning("you are loggedin...")
            json_response = json.dumps({"status": True, "data": "200", "message": "Browser opened!."})
            print(json_response)
            
            time.sleep(24 * 60 * 60)
            
    except Exception as e:
        json_response = json.dumps({"status": False, "data": "", "message": f"An error occurred: {e}"})
        print(json_response)
        return False



if __name__ == "__main__":
    browser = open_browser()
    
