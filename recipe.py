"""Scrapper for recipes from https://recipes.lewagon.com/"""

import csv
import sys
import requests
from bs4 import BeautifulSoup

def parse(html):
    ''' Retourne une liste de dictionnaires {name, difficulty, prep_time} '''
    soup = BeautifulSoup(html, 'html.parser')
    recipes = []
    recipe_articles = soup.find_all("div", class_="recipe")
    for article in recipe_articles:
        recipe_data = parse_recipe(article)
        recipes.append(recipe_data)
    return recipes

def parse_recipe(article):
    ''' Retourne un dictionnaire {name, difficulty, prep_time} modélisant une recette'''
    recipe_data = {}

    # Extraction du nom de la recette
    recipe_name = article.find("p", class_="recipe-name")
    if recipe_name:
        recipe_data["name"] = recipe_name.get_text()

    # Extraction du niveau de difficulté
    recipe_difficulty = article.find("span", class_="recipe-difficulty")
    if recipe_difficulty:
        recipe_data["difficulty"] = recipe_difficulty.get_text()

    # Extraction du temps de préparation
    recipe_cooktime = article.find("span", class_="recipe-cooktime")
    if recipe_cooktime:
        recipe_data["prep_time"] = recipe_cooktime.get_text()
    return recipe_data

def write_csv(ingredient, recipes):
    ''' Écrit les recettes dans un fichier CSV `recipes/INGREDIENT.csv` '''
    with open(f'recipes/{ingredient}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'difficulty', 'prep_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for recipe in recipes:
            writer.writerow(recipe)

def scrape_from_internet(ingredient, page=1):
    ''' Utilise `requests` pour obtenir la page HTML des résultats de
    recherche pour l'ingrédient donné. '''
    url = f'https://recipes.lewagon.com/?search[query]={ingredient}&page={page}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    print(f"Failed to retrieve page {page}.")
    return None

def scrape_all_pages(ingredient):
    """Scrape all pages for a given ingredient."""
    page = 1
    recipes = []
    while True:
        html = scrape_from_internet(ingredient, page)
        if html is None:
            break
        new_recipes = parse(html)
        if not new_recipes:
            break
        recipes.extend(new_recipes)
        page += 1
    return recipes

def main():
    """This is the main function."""
    if len(sys.argv) > 1:
        ingredient = sys.argv[1]
        recipes = scrape_all_pages(ingredient)
        write_csv(ingredient, recipes)
        print(f"Wrote recipes to recipes/{ingredient}.csv")
    else:
        print('Usage: python recipe.py INGREDIENT')
        sys.exit(0)

if __name__ == '__main__':
    main()
