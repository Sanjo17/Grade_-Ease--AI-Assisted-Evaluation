from django.urls import path
from papergrading import views
from django.contrib.auth.views import LoginView


urlpatterns = [
path('papergradingclick', views.papergradingclick_view,name='papergradingclick'),
path('papergrade',views.papergrade,name='papergrade'),
path('paperresult/<int:paper_id>/',views.paperresult,name='paperresult'),
path('generate-report-card', views.generate_report_card, name='generate_report_card'),
]       