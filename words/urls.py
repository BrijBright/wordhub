from django.urls import path
from .views import index, word_list,mark_revised,add_words_api,add_words_page
 
urlpatterns = [
    path('', index, name='home'),           # Home page
    path('api/words/', word_list, name='word-list'),  # JSON API
    path('api/words/<int:word_id>/mark_revised/', mark_revised, name='mark-revised'),
    #   path("add-words/", add_words_api, name="add_words_api"),
    path("api/add_words/", add_words_api, name="add_words_api"),
    path("add-words/", add_words_page, name="add_words_page"),
]
