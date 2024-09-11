import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from colorama import Fore, Style, init
import time

init(autoreset=True)

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless")

webdriver_path = "/usr/bin/chromedriver"

try:
    with open("socials.txt", "r") as file:
        social_sites = set(line.strip() for line in file if line.strip())
    print(f"{Fore.CYAN}Loaded {len(social_sites)} unique URLs from socials.txt{Style.RESET_ALL}")
except FileNotFoundError:
    print(f"{Fore.RED}Error: socials.txt file not found!{Style.RESET_ALL}")
    exit(1)

found_file = "found.txt"
not_found_file = "notfound.txt"
error_file = "errors.txt"

with open(found_file, "w") as f:
    f.write("")
with open(not_found_file, "w") as f:
    f.write("")
with open(error_file, "w") as f:
    f.write("")

not_found_keywords = [
    "does not exist", "user does not exist", "content unavailable",
    "not found", "page not found", "404 error", "that content is unavailable",
    "we couldn’t find", "this account doesn’t exist", "no longer available", 
    "this channel is unavailable", "Sorry. Unless you've got a time machine, that content is unavailable.",
    "this page isn't available", "username is incorrect", "that page is gone", "lost this page",
    "There is no one by the name", "something isn’t here", "start at the beginning", "We can't find that page",
    "The page you're looking for doesn't exist", "doesn't exist", "We couldn't find that page", "404",
    "This account may have been banned or the username is incorrect", "you seem to have stumbled on a bad link",
    "We couldn't find anything", "Unregistered", "This account may have been banned or the username is incorrect", "This user cannot be found",

]

def check_username_selenium(username, url):
    driver = None
    try:
        url_to_check = url.replace("{USERNAME}", username)
        print(f"{Fore.YELLOW}Checking {url_to_check}...{Style.RESET_ALL}")

        service = Service(executable_path=webdriver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(15)

        driver.get(url_to_check)

        time.sleep(2)

        html_content = driver.page_source.lower()

        if any(keyword.lower() in html_content for keyword in not_found_keywords):
            with threading.Lock():
                with open(not_found_file, "a") as f:
                    f.write(f"{url_to_check}\n")
            print(f"{Fore.RED}[NOT FOUND] {url_to_check} (HTML Keyword){Style.RESET_ALL}")
        else:
            with threading.Lock():
                with open(found_file, "a") as f:
                    f.write(f"{url_to_check}\n")
            print(f"{Fore.GREEN}[FOUND] {url_to_check}{Style.RESET_ALL}")

    except TimeoutException:
        with threading.Lock():
            with open(error_file, "a") as f:
                f.write(f"{url_to_check}: TimeoutException\n")
        print(f"{Fore.YELLOW}[ERROR] {url_to_check} - TimeoutException{Style.RESET_ALL}")
    
    except WebDriverException as e:
        with threading.Lock():
            with open(error_file, "a") as f:
                f.write(f"{url_to_check}: {str(e)}\n")
        print(f"{Fore.YELLOW}[ERROR] {url_to_check} - {str(e)}{Style.RESET_ALL}")

    finally:
        if driver:
            driver.quit()

def main():
    username = input("Enter the username to check: ")
    thread_count = int(input("Enter the number of threads to use: "))

    threads = []
    for url in social_sites:
        if len(threads) >= thread_count:
            for t in threads:
                t.join()
            threads = []

        thread = threading.Thread(target=check_username_selenium, args=(username, url))
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()

    print(f"{Fore.CYAN}Username check complete.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
