from django.urls import path

from app.views.cat import CategoryDetailView, CategoryCreateView, CategoryListView, CategoryUpdateView, \
    CategoryDeleteView

urlpatterns = [
    path("create/", CategoryCreateView.as_view()),
    path("<int:pk>/", CategoryDetailView.as_view()),
    path("", CategoryListView.as_view()),
    path("<int:pk>/update/", CategoryUpdateView.as_view()),
    path("<int:pk>/delete/", CategoryDeleteView.as_view()),
]