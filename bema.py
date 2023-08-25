import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL of the Billboard Hot 100 chart
url = 'https://www.billboard.com/charts/hot-100'

# Configure Selenium options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in headless mode
driver = webdriver.Chrome(options=chrome_options)

try:
    # Navigate to the URL using Selenium
    driver.get(url)
    
    # Wait for the page to load and the content to be visible
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'chart-element__information'))
    )
    
    # Extract the page source after dynamic content has loaded
    page_source = driver.page_source
    
    # Continue with BeautifulSoup for parsing
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Find the elements that contain the song information
    song_elements = soup.find_all('div', class_='chart-element__information')
    
    # Extract the song names and artists
    songs = []
    for element in song_elements:
        song_name = element.find('span', class_='chart-element__information__song').get_text()
        artist = element.find('span', class_='chart-element__information__artist').get_text()
        songs.append((song_name, artist))
    
    # Define the directory to save the file
    save_directory = 'YOUR_ABSOLUTE_PATH'  # Replace with the actual absolute path
    
    # Create the directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    # Create and write to the download list file
    file_path = os.path.join(save_directory, 'download_list.txt')
    with open(file_path, 'w') as file:
        file.write("Songs to Download:\n")
        for song in songs:
            song_name, artist = song
            file.write(f"{song_name} - {artist}\n")
    
    print(f"Download list saved to '{file_path}'")
    
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the Selenium driver
    driver.quit()
