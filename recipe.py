# pylint: disable=missing-docstring, line-too-long, missing-timeout
import sys
from os import path

from bs4 import BeautifulSoup


def parse(html):
    ''' return a list of dict {name, difficulty, prep_time} '''
    list_dicts = []
    soup = BeautifulSoup(open("pages/carrot.html"), "html.parser")
    for recipe_name in soup.find_all('p', class_= 'recipe-name'):
        article = soup.find(text=recipe_name.text).parent.parent
        list_dicts.append(parse_recipe(article))
    return list_dicts

    pass  # YOUR CODE HERE

def parse_recipe(article):
    ''' return a dict {name, difficulty, prep_time} modeling a recipe'''
    dict_recipe = {'name':'', 'difficulty':'', 'prep_time':''}

    #for recipe_name in article.find_all('p', class_= 'recipe-name'):
    dict_recipe['name'] = article.find_all('p', class_= 'recipe-name')
    dict_recipe['difficulty'] = article.find_all('span', class_= 'recipe-difficulty')[0].text
    dict_recipe['prep_time'] = article.find_all('span', class_= 'recipe-cooktime')[0].text
    return dict_recipe

    pass  # YOUR CODE HERE

def write_csv(ingredient, recipes):
    ''' dump recipes to a CSV file `recipes/INGREDIENT.csv` '''
    pass  # YOUR CODE HERE

def scrape_from_internet(ingredient, start=1):
    ''' Use `requests` to get the HTML page of search results for given ingredients. '''
    pass  # YOUR CODE HERE

def scrape_from_file(ingredient):
    file = f"pages/{ingredient}.html"

    if path.exists(file):
        return open(file, encoding='utf-8')

    print("Please, run the following command first:")
    print(f'curl -g "https://recipes.lewagon.com/?search[query]={ingredient}" > pages/{ingredient}.html')

    sys.exit(1)


def main():
    if len(sys.argv) > 1:
        ingredient = sys.argv[1]

        # TODO: Replace scrape_from_file with scrape_from_internet and implement pagination (more than 2 pages needed)
        recipes = parse(scrape_from_file(ingredient))

        pass  # YOUR CODE HERE
        write_csv(ingredient, recipes)
        print(f"Wrote recipes to recipes/{ingredient}.csv")
    else:
        print('Usage: python recipe.py INGREDIENT')
        sys.exit(0)


if __name__ == '__main__':
    main()
