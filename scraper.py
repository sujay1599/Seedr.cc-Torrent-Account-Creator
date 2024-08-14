import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from urllib.parse import urlencode
import subprocess


# Base URLs
BASE_URL_1337X = 'https://1337x.to'
API_BASE_URL_PIRATEBAY = 'https://apibay.org'

# Function to perform a search query on The Pirate Bay
def search_piratebay(search_term):
    search_url = f"{API_BASE_URL_PIRATEBAY}/q.php?q={search_term}"
    response = requests.get(search_url)
    response.raise_for_status()
    return response.json()

# Function to perform a search query on 1337x with category selection
def search_1337x(search_term, category="all"):
    category_urls = {
        "all": f"/search/{search_term}/1/",
        "movies": f"/category-search/{search_term}/Movies/1/",
        "tv": f"/category-search/{search_term}/TV/1/",
        "games": f"/category-search/{search_term}/Games/1/",
        "music": f"/category-search/{search_term}/Music/1/",
        "applications": f"/category-search/{search_term}/Apps/1/",
        "documentaries": f"/category-search/{search_term}/Documentaries/1/",
        "anime": f"/category-search/{search_term}/Anime/1/",
        "other": f"/category-search/{search_term}/Other/1/"
    }

    # Build the search URL
    search_url = BASE_URL_1337X + category_urls.get(category, category_urls["all"])
    response = requests.get(search_url)
    response.raise_for_status()

    # Parse the search results page
    soup = BeautifulSoup(response.text, 'html.parser')
    return parse_1337x_results(soup)

# Function to parse 1337x search results
def parse_1337x_results(soup):
    torrents = []
    rows = soup.select('tbody tr')
    for row in rows:
        name_tag = row.select_one('.coll-1.name a:nth-child(2)')
        seeders = row.select_one('.coll-2').text.strip()
        leeches = row.select_one('.coll-3').text.strip()
        time = row.select_one('.coll-date').text.strip()
        size = row.select_one('.coll-4.size').text.strip()
        uploader = row.select_one('.coll-5').text.strip()

        title = name_tag.text.strip()
        details_url = f"{BASE_URL_1337X}{name_tag['href']}"

        # Fetch the magnet link from the details page
        magnet_link = fetch_magnet_link(details_url)

        # Store the extracted data
        torrents.append({
            'Title': title,
            'Size': size,
            'Seeders': seeders,
            'Leeches': leeches,
            'Date Uploaded': time,
            'Uploader': uploader,
            'Magnet Link': magnet_link
        })

    return torrents

# Function to fetch the magnet link from a 1337x torrent details page
def fetch_magnet_link(details_url):
    response = requests.get(details_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    magnet_link_tag = soup.select_one('#openPopup')
    return magnet_link_tag['href'] if magnet_link_tag else 'N/A'

# Function to sort torrents by seeders and date uploaded (descending)
def sort_torrents(torrents):
    sorted_torrents = sorted(torrents, key=lambda x: (int(x['Seeders']), x.get('Date Uploaded', '')), reverse=True)
    return sorted_torrents

# Function to display torrents in batches and prompt the user to continue
def display_torrents(torrents):
    index = 0
    while index < len(torrents):
        for torrent in torrents[index:index + 25]:
            title = torrent.get('Title', 'N/A')
            size = torrent.get('Size', 'N/A')
            seeders = torrent.get('Seeders', 'N/A')
            leeches = torrent.get('Leeches', 'N/A')
            upload_date = torrent.get('Date Uploaded', 'N/A')
            uploader = torrent.get('Uploader', 'N/A')
            print(f"{title:<50} {size:<10} {seeders:<8} {leeches:<8} {upload_date:<15} {uploader:<10}")

        index += 25
        if index < len(torrents):
            more = input("Do you want to see 25 more results? (yes/no): ").strip().lower()
            if more != 'yes':
                break

# Main function
def main():
    search_term = input("Enter the search term (e.g., movie name): ").strip()
    category = input("Enter the category (all/movies/tv/games/music/applications/documentaries/anime/other): ").strip().lower()

    all_torrents = []

    print(f"Searching torrents for '{search_term}' in category '{category}' on 1337x...")
    # Scrape torrents from 1337x
    all_torrents += search_1337x(search_term, category)

    print(f"Searching torrents for '{search_term}' on The Pirate Bay...")
    # Search torrents on The Pirate Bay
    piratebay_torrents = search_piratebay(search_term)
    for torrent in piratebay_torrents:
        all_torrents.append({
            'Title': torrent['name'],
            'Size': format_size(torrent['size']),
            'Seeders': torrent['seeders'],
            'Leeches': torrent['leechers'],
            'Date Uploaded': format_date(torrent['added']),
            'Magnet Link': create_magnet_link(torrent['info_hash'], torrent['name']),
            'Uploader': 'N/A'  # The Pirate Bay API does not provide uploader information
        })

    min_seeders = int(input("Enter the minimum number of seeders required for the CSV file: ").strip())

    filtered_torrents = [torrent for torrent in all_torrents if int(torrent['Seeders']) >= min_seeders]
    sorted_torrents = sort_torrents(filtered_torrents)

    print(f"\n{'Title':<50} {'Size':<10} {'Seeders':<8} {'Leeches':<8} {'Date Uploaded':<15} {'Uploader':<10}")
    print("=" * 100)
    display_torrents(sorted_torrents)

    with open("sorted_torrents.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Title", "Size", "Seeders", "Leeches", "Date Uploaded", "Uploader", "Magnet Link"])
        for torrent in sorted_torrents:
            writer.writerow([torrent['Title'], torrent['Size'], torrent['Seeders'], torrent['Leeches'], torrent['Date Uploaded'], torrent['Uploader'], torrent['Magnet Link']])

    print(f"\nScraping completed. Torrents with more than {min_seeders} seeders were saved to 'sorted_torrents.csv'.")

# Function to format the size from bytes to a readable format with whole numbers
def format_size(size_bytes):
    size_bytes = int(size_bytes)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size_bytes < 1024:
            return f"{round(size_bytes)} {unit}"
        size_bytes /= 1024

# Function to convert UNIX timestamp to a readable date
def format_date(unix_timestamp):
    return datetime.utcfromtimestamp(int(unix_timestamp)).strftime('%Y-%m-%d')

# Function to create a properly formatted magnet link
def create_magnet_link(info_hash, name):
    encoded_name = urlencode({"dn": name})
    return f"magnet:?xt=urn:btih:{info_hash}&{encoded_name}"

if __name__ == "__main__":
    main()

    # After completing the scraping, run the verify script
    print("Running the verify script...")
    subprocess.run(["python", "verify.py"])

