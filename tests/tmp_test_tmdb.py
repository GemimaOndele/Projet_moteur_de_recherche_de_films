import os, requests, json
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_API_TOKEN = os.getenv('TMDB_API_TOKEN')
print('TMDB_API_KEY set:', bool(TMDB_API_KEY))
print('TMDB_API_TOKEN set:', bool(TMDB_API_TOKEN))
for movie_id in [205596, 6016, 323677]:
    url = f'https://api.themoviedb.org/3/movie/{movie_id}'
    params = {'api_key': TMDB_API_KEY, 'language':'fr-FR', 'append_to_response':'videos,watch/providers'}
    headers = {'Authorization': f'Bearer {TMDB_API_TOKEN}'} if TMDB_API_TOKEN else {}
    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        print('\nMovie ID:', movie_id, 'Status:', r.status_code)
        try:
            d = r.json()
            print('overview len:', len(d.get('overview','')))
            print('poster_path:', d.get('poster_path'))
            print('backdrop_path:', d.get('backdrop_path'))
            print('videos count:', len(d.get('videos', {}).get('results', [])))
            print('watch providers keys:', list(d.get('watch/providers', {}).get('results', {}).keys())[:5])
            if 'status_message' in d:
                print('status_message:', d.get('status_message'))
        except Exception as ex:
            print('json parse failed', ex)
    except Exception as e:
        print('Request error:', e)
