# Seedr.cc Torrent Account Creator, Scraper, and Magnet Link Verifier

This repository contains scripts to automate the creation of a Seedr.cc account, scrape torrent links from popular sources, and verify magnet links by placing them in Seedr.cc for downloading.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [How It Works](#how-it-works)
  - [main.py](#mainpy)
  - [verify.py](#verifypy)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

The project is divided into two main components:

1. **`main.py`**: Automates the creation of a Seedr.cc account, logs in, scrapes torrent links from 1337x and The Pirate Bay, and saves the results to a CSV file.
2. **`verify.py`**: Verifies available storage on Seedr.cc and places magnet links from the CSV file into Seedr.cc for downloading.

## Prerequisites

- **Python 3.6+**
- **Google Chrome** (latest version)
- **Chromedriver** compatible with your version of Chrome

### Required Python Packages

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Contents of `requirements.txt`:

```
selenium
beautifulsoup4
requests
pyperclip
```

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/sujay1599/Seedr.cc-Torrent-Account-Creator.git
   cd Seedr.cc-Torrent-Account-Creator
   ```

2. **Configure Chromedriver**

   Make sure the path to `chromedriver.exe` is correctly set in the `chrome_driver_path` variable in both `main.py` and `verify.py`.

3. **Run `main.py`**

   This script handles creating a Seedr.cc account, logging in, and scraping torrent links.

   ```bash
   python main.py
   ```

   After the script completes:
   - The browser will automatically close.
   - The scraped torrent links with the required number of seeders will be saved in `sorted_torrents.csv`.

4. **Run `verify.py`**

   After `main.py` completes, you can manually run `verify.py` to:

   - Open a new browser session.
   - Log in to Seedr.cc using the credentials saved during the `main.py` process.
   - Place magnet links from `sorted_torrents.csv` into Seedr.cc for downloading.
   - Manage storage on Seedr.cc if needed.

   ```bash
   python verify.py
   ```

## How It Works

### `main.py`

1. **Account Creation and Login**
   - Generates a temporary email using `1secmail`.
   - Creates a Seedr.cc account and logs in.
   - Navigates to the Seedr.cc dashboard.

2. **Torrent Scraping**
   - Scrapes torrent links from 1337x and The Pirate Bay based on user-defined search terms and categories.
   - Saves torrents with more than the specified number of seeders to `sorted_torrents.csv`.

3. **Automated Browsing**
   - Automates browsing and interaction with Seedr.cc.

### `verify.py`

1. **Storage Management**
   - Verifies available storage in Seedr.cc.
   - Deletes files if storage exceeds the defined limit.

2. **Magnet Link Verification**
   - Reads `sorted_torrents.csv`.
   - Randomly selects and places magnet links into Seedr.cc for download.
   - Verifies if more magnet links can be placed based on available storage.

## Troubleshooting

- **Module Not Found Errors**: Ensure all required Python packages are installed using `pip install -r requirements.txt`.
- **Chromedriver Issues**: Verify that the `chromedriver.exe` path matches your local setup and is compatible with your version of Chrome.
- **Deprecation Warnings**: Update your code to handle any deprecated methods if you encounter warnings.

## Contributing

Contributions, bug reports, and feature requests are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
