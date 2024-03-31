from django.shortcuts import render,redirect
from .models import URL

def shorten_url(request):
    if request.method == 'POST':
        long_url = request.POST.get('long_url')
        url = URL.objects.create(long_url=long_url)
        urls = URL.objects.all()
        return render(request, 'shorten_url.html', {'short_url': url.short_url, 'urls':urls})
    urls = URL.objects.all()
    return render(request, 'shorten_url.html', {'urls': urls})


def su(request,short_url):
    try:
        url = URL.objects.get(short_url=short_url)
        url.visited += 1
        url.save()
        return redirect(url.long_url)
    except:
        return HttpResponse("URL not found")



from django.http import HttpResponse
def redirect_to_long_url(request, short_url):
    try:
        url = URL.objects.get(short_url=short_url)
        url.visited = url.visited+1
        return redirect(url.long_url)
    except URL.DoesNotExist:
        return HttpResponse("URL not found")