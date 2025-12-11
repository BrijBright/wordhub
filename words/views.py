from django.shortcuts import render
from django.http import JsonResponse
from .models import Word
from django.views.decorators.csrf import csrf_exempt
import json



def word_list(request):
    words = Word.objects.all().values(
        'id', 'word', 'meaning', 
        'category__name', 'subcategory__name'
    )
    return JsonResponse(list(words), safe=False)



def index(request):
    # Optionally, filter by category or subcategory via GET parameters
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')

    words = Word.objects.exclude(is_mastered=True).order_by('revised_count')

    if category_id:
        words = words.filter(category_id=category_id)
    if subcategory_id:
        words = words.filter(subcategory_id=subcategory_id)

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
        category_id = data.get("category")  # required
        subcategory_id = data.get("subcategory")  # optional
    except:
        return JsonResponse({"message": "Invalid JSON"}, status=400)

    if not text.strip():
        return JsonResponse({"message": "No data provided"}, status=400)

    # Check if category exists
    from .models import Category, Subcategory
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return JsonResponse({"message": "Category not found"}, status=400)

    subcategory = None
    if subcategory_id:
        try:
            subcategory = Subcategory.objects.get(id=subcategory_id)
            if subcategory.category != category:
                return JsonResponse({"message": "Subcategory does not belong to the category"}, status=400)
        except Subcategory.DoesNotExist:
            return JsonResponse({"message": "Subcategory not found"}, status=400)

    # Split by ;
    entries = [e.strip() for e in text.split(";") if e.strip()]

    added = 0
    skipped = 0

    for item in entries:
        if "," in item:
            parts = item.split(",", 1)
            word_text = parts[0].strip()
            meaning = parts[1].strip()
        else:
            word_text = item
            meaning = None

        if not word_text:
            continue

        obj, created = Word.objects.get_or_create(
            word=word_text,
            defaults={
                "meaning": meaning,
                "category": category,
                "subcategory": subcategory
            }
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


@csrf_exempt
def mark_improvement(request, pk):
    if request.method == 'POST':
        try:
            word = Word.objects.get(pk=pk)

            # Toggle need_improvement
            word.need_improvement = not word.need_improvement

            # If need_improvement becomes True → force mastered False
            if word.need_improvement:
                word.is_mastered = False

            word.save()

            return JsonResponse({
                'success': True,
                'need_improvement': word.need_improvement,
                'is_mastered': word.is_mastered
            })

        except Word.DoesNotExist:
            return JsonResponse({'error': 'Word not found'}, status=404)

    return JsonResponse({'error': 'Invalid method'}, status=400)





def improvement_list(request):
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')

    words = Word.objects.filter(need_improvement=True)

    # Optional category filter
    if category_id:
        if category_id.lower() == 'null':
            words = words.filter(category__isnull=True)
        else:
            words = words.filter(category_id=category_id)

    # Optional subcategory filter
    if subcategory_id:
        if subcategory_id.lower() == 'null':
            words = words.filter(subcategory__isnull=True)
        else:
            words = words.filter(subcategory_id=subcategory_id)

    return render(request, "index.html", {"words": words})



@csrf_exempt
def toggle_mastered(request, pk):
    if request.method == 'POST':
        try:
            word = Word.objects.get(pk=pk)

            # Toggle is_mastered
            word.is_mastered = not word.is_mastered

            # If mastered becomes True -> force need_improvement = False
            if word.is_mastered:
                word.need_improvement = False

            word.save()

            return JsonResponse({
                'success': True,
                'is_mastered': word.is_mastered,
                'need_improvement': word.need_improvement
            })

        except Word.DoesNotExist:
            return JsonResponse({'error': 'Word not found'}, status=404)

    return JsonResponse({'error': 'Invalid method'}, status=400)



def mastered_list(request):
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')

    words = Word.objects.filter(is_mastered=True)

    # Optional category filter
    if category_id:
        if category_id.lower() == 'null':
            words = words.filter(category__isnull=True)
        else:
            words = words.filter(category_id=category_id)

    # Optional subcategory filter
    if subcategory_id:
        if subcategory_id.lower() == 'null':
            words = words.filter(subcategory__isnull=True)
        else:
            words = words.filter(subcategory_id=subcategory_id)

    return render(request, "index.html", {"words": words})
