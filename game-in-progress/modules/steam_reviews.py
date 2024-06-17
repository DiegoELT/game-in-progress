import steamreviews

from .language_comparison import pre_process

request_params = dict()
request_params['language'] = 'english'
request_params['filter'] = 'all'
request_params['day_range'] = '28'

def get_reviews(app_id, n = 15):
  review_dict, query_count = steamreviews.download_reviews_for_app_id(str(app_id), chosen_request_params = request_params)
  review_dict = review_dict['reviews']

  invalid_keys = []

  for key in review_dict:
    if review_dict[key]['language'] != 'english':
      invalid_keys.append(key)

  for key in invalid_keys:
    del review_dict[key]

  game_reviews = []
  for key in review_dict:
    review = review_dict[key]['review']
    game_reviews.append((review, review_dict[key]['votes_up']))

  game_reviews.sort(key = lambda item: -item[1])

  for i in range(len(game_reviews)):
    game_reviews[i] =  pre_process(game_reviews[i][0])

  if len(game_reviews) < n:
    return game_reviews
  return game_reviews[:n]