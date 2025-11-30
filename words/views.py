from django.shortcuts import render
from django.http import JsonResponse
from .models import Word
from django.views.decorators.csrf import csrf_exempt
import json



def word_list(request):
    words = Word.objects.all().values('id', 'word', 'meaning')
    return JsonResponse(list(words), safe=False)


def index(request):
    # Order by revised_count ascending (lowest first)
    words = Word.objects.all().order_by('revised_count')
    return render(request, 'index.html', {'words': words})



@csrf_exempt
def mark_revised(request, word_id):
    if request.method == 'POST':
        word = Word.objects.get(id=word_id)
        data = json.loads(request.body)
        increment = data.get('increment', 1)
        word.revised_count += increment
        word.save()
        return JsonResponse({'revised_count': word.revised_count})


# app/views.py

@csrf_exempt
def add_words_api(request):
    if request.method != "POST":
        return JsonResponse({"message": "Invalid request"}, status=400)

    try:
        data = json.loads(request.body)
        text = data.get("text", "")
    except:
        return JsonResponse({"message": "Invalid JSON"}, status=400)

    if not text.strip():
        return JsonResponse({"message": "No data provided"}, status=400)

    # Split by ;
    entries = [e.strip() for e in text.split(";") if e.strip()]

    added = 0
    skipped = 0

    for item in entries:
        if "," in item:
            # Format: word,meaning
            parts = item.split(",", 1)  # only split first comma
            word = parts[0].strip()
            meaning = parts[1].strip()
        else:
            # Format: only word
            word = item
            meaning = None

        if not word:
            continue

        obj, created = Word.objects.get_or_create(
            word=word,
            defaults={"meaning": meaning}
        )

        if not created:
            skipped += 1
        else:
            added += 1

    return JsonResponse({
        "message": f"Added {added} words, skipped {skipped} duplicates."
    })


def add_words_page(request):
    # Just render the add_words.html template
    return render(request, "add_words.html")
