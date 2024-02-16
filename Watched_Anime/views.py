from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt
from .models import WatchedAnime

@csrf_exempt
def upload_anime(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            rating = data.get('rating')
            site = data.get('site')
            link = data.get('link')
            if title and rating and site and link:
                anime = WatchedAnime(title=title, rating=rating, site=site, link=link)
                anime.save()
                return JsonResponse({'message': 'Data uploaded successfully'})
            else:
                return JsonResponse({'error': 'Title, site and rating are required.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    else:
        return JsonResponse({'error': 'POST request required.'}, status=400)

# get all watched anime
def get_watched_anime(request):
    watched_anime = WatchedAnime.objects.all()
    watched_anime_list = list(watched_anime.values('title', 'rating', 'site', 'link'))
    return JsonResponse(watched_anime_list, safe=False)

