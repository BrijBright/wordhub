from django.core.exceptions import ValidationError
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories"
    )

    def __str__(self):
        return f"{self.category.name} -> {self.name}"


class Word(models.Model):
    word = models.CharField(max_length=100)
    meaning = models.TextField(blank=True, null=True)
    revised_count = models.PositiveIntegerField(default=0)
    need_improvement = models.BooleanField(default=False)
    is_mastered = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)

    # New fields
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="words"
    )
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.SET_NULL, blank=True, null=True, related_name="words"
    )

    def __str__(self):
        return self.word

    def clean(self):
        """
        Ensure that if a subcategory is provided, it belongs to the selected category.
        """
        if self.subcategory and self.subcategory.category != self.category:
            raise ValidationError(
                {
                    "subcategory": "Subcategory must belong to the selected category."
                }
            )

    def save(self, *args, **kwargs):
        # Run validation before saving
        self.clean()
        super().save(*args, **kwargs)
