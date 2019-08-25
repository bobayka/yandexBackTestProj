from django.urls import path

from marketAnalysis import views

app_name = 'marketanalysis'
urlpatterns = [
    path('imports', views.importCitizens),
    path('imports/<import_id>/citizens/<citizen_id>', views.updateCitizens),
    path('imports/<import_id>/citizens/', views.getCitizens)

]
