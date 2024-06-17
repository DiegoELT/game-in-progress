from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_title_by_id(app_id):
  url = "https://store.steampowered.com/app/" + str(app_id)
  page = urlopen(url)
  html = page.read().decode("utf-8")

  soup = BeautifulSoup(html,'html.parser')
  game_title = soup.find_all('div', {'class': 'apphub_AppName'})[0].text

  return game_title

def get_similar_games(app_id, n_similar_games):
  url = "http://store.steampowered.com/recommended/morelike/app/" + str(app_id)
  page = urlopen(url)
  html = page.read().decode("utf-8")
  
  soup = BeautifulSoup(html, 'html.parser')
  games_items = soup.find_all('div', {'class': 'similar_grid_item'})

  similar_games = []

  for i in range(n_similar_games):
    game_item = str(games_items[i])
    id_index = game_item.find('App_')
    id_end = game_item[id_index:].find('"')

    game_id = game_item[id_index + 4 : id_index + id_end]
    game_title = get_title_by_id(int(game_id))

    similar_games.append((game_id, game_title))
  
  return similar_games