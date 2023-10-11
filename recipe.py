# pylint: disable=missing-docstring, line-too-long, missing-timeout
import csv
import sys
from os import path
from bs4 import BeautifulSoup
import requests


def parse(html):
    ''' return a list of dict {name, difficulty, prep_time} '''
    list_dicts = []
    soup = BeautifulSoup(html, "html.parser")
    for div in soup.find_all("div", class_="col-12 col-sm-6 col-md-4 col-lg-3"):
        list_dicts.append(parse_recipe(div))
    return list_dicts


def parse_recipe(article):
    ''' return a dict {name, difficulty, prep_time} modeling a recipe'''
    dict_recipe = {'name':'', 'difficulty':'', 'prep_time':''}
    dict_recipe['name'] = article.find_all('p', class_= 'recipe-name')[0].text
    dict_recipe['difficulty'] = article.find_all('span', class_= 'recipe-difficulty')[0].text
    dict_recipe['prep_time'] = article.find_all('span', class_= 'recipe-cooktime')[0].text
    return dict_recipe


def write_csv(ingredient, recipes):
    ''' dump recipes to a CSV file `recipes/INGREDIENT.csv` '''
    with open(f'recipes/{ingredient}.csv', 'w', encoding='utf-8') as csv_file:
        keys = recipes[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(recipes)


def scrape_from_internet(ingredient, start=1):
    ''' Use `requests` to get the HTML page of search results for given ingredients. '''
    url_params = {'search[query]': ingredient,'page': start}
    response = requests.get("https://recipes.lewagon.com/", params = url_params)
    return response.text

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

        #recipes = parse(scrape_from_file(ingredient))
        #Replace scrape_from_file with scrape_from_internet and implement pagination (more than 2 pages needed)
        recipes = []
        for i in range(3):
            output = parse(scrape_from_internet(ingredient, i+1))
            if output:
                recipes.append(output)
            else:
                break

        write_csv(ingredient, recipes)
        print(f"Wrote recipes to recipes/{ingredient}.csv")
    else:
        print('Usage: python recipe.py INGREDIENT')
        sys.exit(0)


if __name__ == '__main__':
    main()
