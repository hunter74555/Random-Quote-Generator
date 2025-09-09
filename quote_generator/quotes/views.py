from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import random
from .models import Quote
from .forms import QuoteForm
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages


def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Цитата успешно добавлена!')
            return redirect('index')
    else:
        form = QuoteForm()

    return render(request, 'quotes/add_quote.html', {'form': form})

@require_POST
def like_quote(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    quote.likes += 1
    quote.save()
    return JsonResponse({'likes': quote.likes, 'dislikes': quote.dislikes})

@require_POST
def dislike_quote(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    quote.dislikes += 1
    quote.save()
    return JsonResponse({'likes': quote.likes, 'dislikes': quote.dislikes})


def get_random_quote():
    quotes = list(Quote.objects.all())
    if not quotes:
        return None

    weights = [quote.weight for quote in quotes]
    return random.choices(quotes, weights=weights, k=1)[0]


def index(request):
    quote = get_random_quote()
    if quote:
        quote.views += 1
        quote.save()

    return render(request, 'quotes/index.html', {
        'quote': quote,
        'total_quotes': Quote.objects.count()
    })


def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = QuoteForm()

    return render(request, 'quotes/add_quote.html', {'form': form})

def top_quotes(request):
    """Топ-10 цитат по лайкам"""
    top_quotes = Quote.objects.all().order_by('-likes')[:10]
    return render(request, 'quotes/top_quotes.html', {'quotes': top_quotes})