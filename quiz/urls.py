from django.contrib import admin
from django.urls import path, include

from base import views

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('question/<int:id>', views.question),
    path('ranking/', views.ranking),
    path('__debug__/', include('debug_toolbar.urls')),

]
