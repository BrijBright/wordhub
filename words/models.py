from django.db import models

class Word(models.Model):
    word = models.CharField(max_length=100)
    meaning = models.TextField(blank=True, null=True)
    revised_count = models.PositiveIntegerField(default=0)
    need_improvement = models.BooleanField(default=False)
    is_mastered = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)  # This will store the creation date

    def __str__(self):
        return self.word
