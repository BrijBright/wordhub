from django.shortcuts import render
from django.http import JsonResponse
from .models import Word
from django.views.decorators.csrf import csrf_exempt
from .models import Word, Category, Subcategory
import json

def word_list(request):
    words = Word.objects.all().values(
        'id', 'word', 'meaning', 
        'category__name', 'subcategory__name'
    )
    return JsonResponse(list(words), safe=False)




def index(request):
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')

    words = Word.objects.exclude(is_mastered=True).order_by('revised_count')

    if category_id:
        words = words.filter(category_id=category_id)
    if subcategory_id:
        words = words.filter(subcategory_id=subcategory_id)

    context = {
        'words': words,
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'active_category': int(category_id) if category_id else None,
        'active_subcategory': int(subcategory_id) if subcategory_id else None,
    }
    return render(request, 'index.html', context)






@csrf_exempt
def mark_revised(request, word_id):
    if request.method == 'POST':
        word = Word.objects.get(id=word_id)
        data = json.loads(request.body)
        increment = data.get('increment', 1)
        word.revised_count += increment
        word.save()
        return JsonResponse({'revised_count': word.revised_count})



@csrf_exempt
def add_words_api(request):
    if request.method != "POST":
        return JsonResponse({"message": "Invalid request"}, status=400)

    try:
        data = json.loads(request.body)
        text = data.get("text", "").strip()

        category_id = data.get("category")
        subcategory_id = data.get("subcategory")

        new_category = data.get("newCategory", "").strip()
        new_subcategory = data.get("newSubcategory", "").strip()

    except:
        return JsonResponse({"message": "Invalid JSON"}, status=400)

    if not text:
        return JsonResponse({"message": "No data provided"}, status=400)

    # --- CATEGORY HANDLING ---
    if new_category:
        category, _ = Category.objects.get_or_create(name=new_category)
    elif category_id:
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return JsonResponse({"message": "Category not found"}, status=400)
    else:
        return JsonResponse({"message": "Category is required"}, status=400)

    # --- SUBCATEGORY HANDLING ---
    subcategory = None

    if new_subcategory:
        subcategory, _ = Subcategory.objects.get_or_create(
            name=new_subcategory,
            category=category
        )
    elif subcategory_id:
        try:
            subcategory = Subcategory.objects.get(id=subcategory_id)
            if subcategory.category != category:
                return JsonResponse({
                    "message": "Subcategory does not belong to the selected category"
                }, status=400)
        except Subcategory.DoesNotExist:
            return JsonResponse({"message": "Subcategory not found"}, status=400)

    # --- PROCESS BULK TEXT ---
    entries = [e.strip() for e in text.split(";") if e.strip()]

    added = 0
    skipped = 0

    for item in entries:
        if "," in item:
            word_text, meaning = item.split(",", 1)
            word_text = word_text.strip()
            meaning = meaning.strip()
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
                "subcategory": subcategory,
            }
        )

        if created:
            added += 1
        else:
            skipped += 1

    return JsonResponse({
        "message": f"Added {added} words, skipped {skipped} duplicates."
    })

    if request.method != "POST":
        return JsonResponse({"message": "Invalid request"}, status=400)

    try:
        data = json.loads(request.body)
        text = data.get("text", "").strip()
        category_id = data.get("category")        # selected existing category
        subcategory_id = data.get("subcategory")  # selected existing subcategory
        new_category = data.get("newCategory", "").strip()      # new category input
        new_subcategory = data.get("newSubcategory", "").strip()  # new subcategory input
    except:
        return JsonResponse({"message": "Invalid JSON"}, status=400)

    if not text:
        return JsonResponse({"message": "No data provided"}, status=400)

    # Handle category
    if new_category:
        category, _ = Category.objects.get_or_create(name=new_category)
    elif category_id:
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return JsonResponse({"message": "Category not found"}, status=400)
    else:
        return JsonResponse({"message": "Category is required"}, status=400)

    # Handle subcategory
    subcategory = None
    if new_subcategory:
        # Create new subcategory linked to selected/created category
        subcategory, _ = Subcategory.objects.get_or_create(name=new_subcategory, category=category)
    elif subcategory_id:
        try:
            subcategory = Subcategory.objects.get(id=subcategory_id)
            if subcategory.category != category:
                return JsonResponse({"message": "Subcategory does not belong to the selected category"}, status=400)
        except Subcategory.DoesNotExist:
            return JsonResponse({"message": "Subcategory not found"}, status=400)

    # Split bulk words by ;
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

        if created:
            added += 1
        else:
            skipped += 1

    return JsonResponse({
        "message": f"Added {added} words, skipped {skipped} duplicates."
    })

def add_words_page(request):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()

    return render(request, "add_words.html", {
        "categories": categories,
        "subcategories": subcategories
    })


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
