from django.urls import path
from .views import index, word_list,mark_revised,add_words_api,add_words_page,improvement_list
from . import views

urlpatterns = [
    path('', index, name='home'),          
    path('api/words/', word_list, name='word-list'),
    path('api/words/<int:word_id>/mark_revised/', mark_revised, name='mark-revised'),
    path("api/add_words/", add_words_api, name="add_words_api"),
    path("add-words/", add_words_page, name="add_words_page"),

    path('improvement/', improvement_list, name='improvement_list'),
    path('api/words/<int:pk>/mark_improvement/', views.mark_improvement, name='mark_improvement'),

    path('mastered/', views.mastered_list, name='mastered_list'),
    path('api/words/<int:pk>/toggle_mastered/', views.toggle_mastered, name='toggle_mastered'),
    

]
