from django.contrib import admin
from .models import Word, Category, Subcategory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "word",
        "category",
        "subcategory",
        "revised_count",
        "need_improvement",
        "is_mastered",
        "created_date",
    )
    list_filter = ("category", "subcategory", "need_improvement", "is_mastered")
    search_fields = ("word", "meaning")
