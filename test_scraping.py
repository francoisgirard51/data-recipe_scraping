"""
File for testing the scraping.py file.
"""
# pylint: disable=missing-docstring, invalid-name

from bs4 import BeautifulSoup

with open("pages/carrot.html", encoding='utf-8') as file:
    soup = BeautifulSoup(file, "html.parser")

for recipe in soup.find_all('p', class_='recipe-name'):
    print(recipe.text)
