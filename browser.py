import sys
import os
import json
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
from db import get_users, update_profile_name
from dotenv import load_dotenv

load_dotenv()

def navigate_and_update_profile(page, ident):
    try:
        # Now you are logged in, you can navigate to another page
        page.goto('https://x.com/i/user/' + ident)

        timeout = 0
        while "i/user" in page.url:
            page.wait_for_timeout(100)
            timeout += 100
            if timeout > 10000:  # Wait up to 10 seconds for the profile to become available
                raise Exception("Timeout exceeded while waiting for the profile to become available.")
            
            
        # Now you are logged in, you can get the URL segments
        current_url = page.url
        parsed_url = urlparse(current_url)

        username = parsed_url.path[1:]

        # Check if the username includes the identifier
        if ident not in username and username != '404':
            # If the identifier is not found in the username
            update_profile_name(ident, username)
            return username

        json_response = json.dumps({"status": False, "data": "", "message": f"Username not updated in browser tab URL for ident {ident}"})
        print(json_response)
        return False

    except Exception as e:
        # Constructing the JSON response
        json_response = json.dumps({"status": False, "data": "", "message": f"An error occurred while navigating and updating profile for {ident}: {e}"})
        print(json_response)
        return False
 

def update_twitter_profile_names( ident = None):
    browser = None
    with sync_playwright() as p:
        try:
            browser_port = os.getenv('browser_port')
            if not browser_port:
                json_response = json.dumps({"status": False, "data": "", "message": "browser_port environment variable is not set."})
                print(json_response)
                return False
            
            # browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:9222")
            browser = p.chromium.connect_over_cdp(f"http://172.19.0.1:9222")
            
        except Exception as e:
            print(e)
            json_response = json.dumps({"status": False, "data": "400", "message": e})
            return False            
        
        try:
            context = browser.contexts[0]       
            page = context.pages[0]
            page.goto('https://x.com/home')
            
            # parsed_url = urlparse(page.url)
            
            # path = parsed_url.path.strip('/')

            # print(browser.contexts)
            # print(path)
            
            if "home" not in page.url:
                browser.close()
                json_response = json.dumps({"status": False, "data": "400", "message": "Browser is not opened."})
                print(json_response)
                return False
                
            
            if( ident ):
                username = navigate_and_update_profile(page, ident)
                if(username):
                    return username
                
            else:
                print("Okay you are in !")
                users = get_users()
                if(users):
                    for user in users:
                        navigate_and_update_profile(page, user)
                        
        except Exception as e:
            json_response = json.dumps({"status": False, "data": "", "message": f"An error occurred: {e}"})
            print(json_response)
            return False

if __name__ == "__main__":
    
    # Check if a command-line argument is provided
    if len(sys.argv) > 1:
        parameter = sys.argv[1]  # First command-line argument after the script name
        username = update_twitter_profile_names(parameter)
        if( username ):
            json_response = json.dumps({"status": True, "data": f"{username}", "message": f"User Name Fetched for Ident {parameter}"})
            print(json_response)
    else:
        username = update_twitter_profile_names()
        if( username ):
            json_response = json.dumps({"status": True, "data": "", "message": f"username has been updated !"})
            print(json_response)