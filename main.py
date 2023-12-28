import random
import requests
from bs4 import BeautifulSoup

# crawl IMDB Top 250 and randomly select a movie

#how about we use a .env file to get the url instead of plainly stating it in the main code
URL = 'http://www.imdb.com/chart/top'

#this function aims to scrap the endpoint and fetch the content and the
def main():
    #firstly we ping the url and then save the response into the response variable
    response = requests.get(URL)

    soup = BeautifulSoup(response.text, 'html.parser')
    #we curtail the response by parsing it to the BeautifulSoup method with the mode, html.parser
    #soup = BeautifulSoup(response.text, 'lxml') # faster

    # print(soup.prettify())

    #with the movie tags_variable we are selecting
    movietags = soup.select('td.titleColumn')

    inner_movietags = soup.select('td.titleColumn a')
    ratingtags = soup.select('td.posterColumn span[name=ir]')

    def get_year(movie_tag):
        moviesplit = movie_tag.text.split() #splits the movie names into a list
        year = moviesplit[-1] #we can access the year at the end of the movie split lists
        return year

    years = [get_year(tag) for tag in movietags]
    actors_list =[tag['title'] for tag in inner_movietags] # access attribute 'title'
    titles = [tag.text for tag in inner_movietags]
    ratings = [float(tag['data-value']) for tag in ratingtags] # access attribute 'data-value'

    n_movies = len(titles)

    #we also implement this feature where we are able to suggest random movies
    while(True):
        idx = random.randrange(0, n_movies)
        
        print(f'{titles[idx]} {years[idx]}, Rating: {ratings[idx]:.1f}, Starring: {actors_list[idx]}')

        #user input to prevent script from running perpetually
        user_input = input('Do you want another movie (y/[n])? ')
        if user_input != 'y':
            break
    
#python idiom that is going to run the main function in the advent that the 
if __name__ == '__main__':
    main()