from django.urls import path
from .views import PostList, PostSearch, PostCreateView, PostDetailView, PostDeleteView, PostUpdateView

urlpatterns = [path('', PostList.as_view()),
               path('search/', PostSearch.as_view(), name='search'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('create/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
               ]

