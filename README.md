# Kittysint

Kittysint is a Python-based tool designed to check if a username is available across multiple social media platforms and websites. It utilizes **Selenium** in headless mode to interact with web pages, ensuring accurate username checks even on platforms that rely on JavaScript to load content.

## Features

- **Automated Username Check**: Check if a username is available across various social media and website platforms.
- **Headless Browser Mode**: Uses Selenium's headless Chrome mode to ensure browser windows don't appear during execution.
- **Threaded Execution**: Multiple websites can be checked concurrently, reducing the time it takes to check usernames.
- **Customizable**: Add or remove platforms by editing the `socials.txt` file.
- **Log Results**: Outputs found usernames, not found usernames, and any errors encountered during the process.

## Requirements

- **Python 3.x**
- **Selenium**
- **Google Chrome** and **ChromeDriver** (or an alternative browser and its corresponding WebDriver)
