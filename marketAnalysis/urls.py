from django.urls import path

from marketAnalysis import views

app_name = 'marketanalysis'
urlpatterns = [
    path('imports', views.importCitizens),
    path('imports/<int:import_id>/citizens/<int:citizen_id>', views.updateCitizens),
    path('imports/<int:import_id>/citizens', views.getCitizens),
    path('imports/<int:import_id>/citizens/birthdays', views.getGifsCount),
    path('imports/<int:import_id>/towns/stat/percentile/age', views.getPercentileAge)

]
