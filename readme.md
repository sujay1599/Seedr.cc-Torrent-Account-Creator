# Seedr.cc Account Creator

## Overview

This Python script automates the process of creating an account on Seedr.cc using a temporary email from 1secmail.com. The script handles the entire process, including email generation, account registration, CAPTCHA handling, email verification, and final account activation.

## Features

- **Temporary Email Generation**: Automatically generates a temporary email using 1secmail.com.
- **Automated Registration**: Uses the generated email to register a new account on Seedr.cc.
- **CAPTCHA Handling**: Pauses the script to allow manual CAPTCHA solving during registration.
- **Email Verification**: Automatically checks the inbox for the Seedr.cc verification email, opens it, and clicks the verification link.
- **Account Activation**: After clicking the verification link, the script handles the final account activation on the Seedr.cc website.
- **Logging**: Logs the generated username (email), password, and the creation timestamp to a CSV file for future reference.

## Prerequisites

- **Python 3.x**: Ensure Python is installed on your machine.
- **Selenium**: The script uses the Selenium library to automate browser interactions.
- **Chrome WebDriver**: Required to control the Chrome browser.

### Python Libraries

You need to install the following Python libraries:

```bash
pip install -r requirements.txt
```

## Setup

1. **Clone the Repository**: Clone this repository to your local machine.

   ```bash
   git clone https://github.com/sujay1599/Seedr.cc-Torrent-Account-Creator.git
   cd Seedr.cc-Torrent-Account-Creator
   ```

2. **Download ChromeDriver**: Ensure you have the correct version of ChromeDriver for your Chrome browser. Place the `chromedriver.exe` file in the same directory as your script or add it to your system PATH.

3. **Install Dependencies**: Install the required Python libraries as mentioned above.

4. **Run the Script**: Execute the script using Python.

   ```bash
   python main.py
   ```

## Usage

1. **Temporary Email Generation**: The script starts by generating a temporary email using 1secmail.com.
2. **Account Registration**: It then opens the Seedr.cc registration page in a new browser tab and automatically fills out the registration form using the generated email and a predefined password.
3. **CAPTCHA Handling**: After pressing the "Continue" button, the script pauses and waits for you to complete the CAPTCHA.
4. **Email Verification**: Once you solve the CAPTCHA and press "Enter", the script resumes. It switches back to the 1secmail inbox, awaits the verification email from Seedr.cc, and automatically opens it.
5. **Final Activation**: The script clicks the "Start" button in the email, switches to the new tab, and clicks the "Activate Account" button to complete the registration.

### Logging

- The generated username (email), password, and timestamp are stored in a CSV file named `credentials.csv` in the same directory as the script.

### File Structure

```plaintext
.
├── credentials.csv         # Stores generated emails, passwords, and timestamps.
├── main.py                 # Main script file.
├── requirements.txt        # Python dependencies.
└── README.md               # This documentation file.
```

## Notes

- **Manual CAPTCHA Solving**: The CAPTCHA needs to be solved manually. The script will wait for user input before continuing.
- **Browser Support**: The script currently supports the Chrome browser via Selenium.
- **Email Verification**: Ensure that the browser window is not refreshed or closed after receiving the verification email, as this could cause the email address to change, leading to a loss of the verification link.

## Troubleshooting

- **ChromeDriver Issues**: Ensure that the ChromeDriver version matches your installed Chrome browser version.
- **Element Not Found Errors**: If the script fails to locate elements, ensure the website structure hasn't changed. Update the XPath selectors in the script if necessary.
- **CAPTCHA Handling**: Since the CAPTCHA is solved manually, ensure you complete it promptly to avoid session timeouts.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
