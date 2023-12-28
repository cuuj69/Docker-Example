import os
import random
import requests
import logging
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
logging.basicConfig(level=logging.INFO)

def fetch_top_movies(url):
    try:
        response = requests.get(url)
        response.raise_for_status() #Raises an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.RequestException as e:
        logging.error(f"Error fetching data from {url}: {e}")
        return None
    
def get_movies_info(soup):
    movietags = soup.select('td.titleColumn')
    inner_movietags = soup.select('td.titleColumn a')
    ratingtags = soup.select('td.posterColumn span[name=ir]')

    def get_year(movie_tag):
        moviesplit = movie_tag.text.split()
        year = moviesplit[-1]
        return year

    years = [get_year(tag) for tag in movietags]
    actors_list = [tag['title'] for tag in inner_movietags]
    titles = [tag.text for tag in inner_movietags]
    ratings = [float(tag['data-value']) for tag in ratingtags]

    return titles, years, actors_list, ratings

def main():
    # Access the SITE_URL directly from the environment variables
    url = os.getenv('SITE_URL')

    soup = fetch_top_movies(url)
    if soup is None:
        print("Failed to fetch data. Check the URL and your internet connection.")
        return
    
    titles, years, actors_list, ratings = get_movies_info(soup)
    n_movies = len(titles)

    while True:
        idx = random.randrange(0, n_movies)
        print(f"{titles[idx]} {years[idx]}, Rating: {ratings[idx]:.1f}, Starring: {actors_list[idx]}")

        user_input = input('Do you want another movie (y/[n])? ')
        if user_input.lower() != 'y':
            break

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.exception(f"An unexpected error occured: {e}")
        exit(1) #Exit with a non-zero code to indicate an error
