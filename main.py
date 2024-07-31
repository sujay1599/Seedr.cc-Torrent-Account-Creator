import requests
from bs4 import BeautifulSoup
import time
import config

# Function to generate a temporary email using 1secmail API
def generate_temp_email():
    domain = "1secmail.com"
    response = requests.get(f"https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
    email = response.json()[0]
    return email

# Function to extract login credentials from email
def get_login_from_email(email):
    login = email.split("@")[0]
    domain = email.split("@")[1]
    return login, domain

# Function to sign up on Seedr.cc using the generated email
def signup_seedr(email, password):
    session = requests.Session()
    signup_url = "https://www.seedr.cc/signup"
    signup_data = {
        "email": email,
        "password": password,
        "confirm_password": password,
        "referrer": "",
    }
    response = session.post(signup_url, data=signup_data)
    if response.status_code == 200:
        print("Signup successful!")
    else:
        print("Signup failed!")
    return session

# Function to check for confirmation email and extract confirmation link
def check_confirmation_email(login, domain):
    while True:
        response = requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}")
        messages = response.json()
        if messages:
            for message in messages:
                mail_id = message["id"]
                mail_response = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={mail_id}")
                mail_content = mail_response.json()
                soup = BeautifulSoup(mail_content["body"], 'html.parser')
                link = soup.find('a')['href']
                return link
        time.sleep(10)

# Function to confirm email using the confirmation link
def confirm_email(session, confirmation_link):
    response = session.get(confirmation_link)
    if response.status_code == 200:
        print("Email confirmed successfully!")
    else:
        print("Email confirmation failed!")

# Function to log account details
def log_account_details(email, password):
    with open("account_details.txt", "a") as file:
        file.write(f"Email: {email}, Password: {password}\n")
    print("Account details logged successfully!")

# Main script
if __name__ == "__main__":
    temp_email = generate_temp_email()
    password = config.PASSWORD

    login, domain = get_login_from_email(temp_email)

    print(f"Temporary Email: {temp_email}")

    session = signup_seedr(temp_email, password)
    confirmation_link = check_confirmation_email(login, domain)
    confirm_email(session, confirmation_link)
    log_account_details(temp_email, password)
