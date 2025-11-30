from django.db import models

class Word(models.Model):
    word = models.CharField(max_length=100)
    meaning = models.TextField(blank=True, null=True)
    revised_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.word
