from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    context_items = {
        'search': search,
    }
    return render(request, 'my_app/new_search.html', context_items)
