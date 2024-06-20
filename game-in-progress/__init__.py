import os

from flask import Flask, render_template, request, redirect, url_for, session
from .db import get_db
from .modules.language_comparison import LanguageComparison
from .modules.steam_reviews import get_reviews
from .modules.depth_scraper import get_similar_games
from gensim.models import KeyedVectors

model_path = './google_model.bin'

def create_app(test_config = None):
  app = Flask(__name__, instance_relative_config = True)
  app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'game-in-progress.sqlite'),
  )

  if test_config is None:
    app.config.from_pyfile('config.py', silent = True)
  else:
    app.config.from_mapping(test_config)

  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  model = KeyedVectors.load_word2vec_format(model_path, binary = True)

  @app.route('/list/<query>/<depth>', methods = ['GET', 'POST'])
  def list_games(query, depth = 0):
    db = get_db()
    description = ' '.join(query.split('+'))

    if request.method == 'POST':
      
      score = request.form['rating']
      print(score)

      cursor = db.cursor() # We gonna use the cursor since we are going to insert in more than one table c: 

      cursor.execute(
        'INSERT INTO ranking (rating, description) VALUES (?, ?)',
        (score, description)
      )

      last_row = cursor.lastrowid

      for i, game in enumerate(session['games']):
        cursor.execute(
          'INSERT INTO list_entries (id, app_id, position) VALUES (?, ?, ?)',
          (last_row, game['app_id'], i + 1)
        )

      db.commit()
      
      return render_template('game_list.html', data = session['games']) #TODO: Update this so re-render does not occur after submitting.
    
    games = db.execute(
      'SELECT * FROM game LIMIT 5000'
    ).fetchall()

    games = [{'info': {'app_id': game['app_id'], 'name': game['name']}, 'text': game['description']} for game in games]

    comparer = LanguageComparison(model)
    similar_games = comparer.get_most_similar(description, games)

    game_data = []

    curated_games = [{'info': game[0], 'score': game[1]} for game in similar_games]
    existing_ids = [game['info']['app_id'] for game in curated_games]

    if depth:
      related_games = [get_similar_games(game['info']['app_id'], int(depth)) for game in curated_games]
      related_games = [game for game_list in related_games for game in game_list]
      related_games = list(set([ tuple(sorted(game)) for game in related_games ])) # We do not want to consider repeated games. 

      for i in range(len(related_games)):
        if int(related_games[i][0]) not in existing_ids:
          curated_games.append({'info': {'app_id': int(related_games[i][0]), 'name': related_games[i][1]}, 'score': curated_games[i]['score']})
    
    for game in curated_games:
      reviews = get_reviews(game['info']['app_id'], n = 10)
      game['score'] = (game['score'] + comparer.get_similarity_average(description, reviews)) / 2

    curated_games.sort(key = lambda item: -item['score'])
    curated_games = curated_games[:10]
      
    for game in curated_games:
      game_data.append(
        {
          'name': game['info']['name'],
          'app_id': game['info']['app_id'],
          'score': round(game['score'] * 100 + 50, 2)
        }
      )

    session['games'] = game_data

    return render_template('game_list.html', data = game_data)

  @app.route('/', methods = ['GET', 'POST'])
  def index():
    if request.method == 'POST':
      description = request.form['description'].replace(' ', '+')

      depth = 0

      if request.form.get('deep-search'):
        depth = request.form['depth']
        
      return redirect(url_for('list_games', query = description, depth = depth))
    
    session['games'] = []

    return render_template('game_query.html')
  
  from . import db
  db.init_app(app)
  
  return app
  
