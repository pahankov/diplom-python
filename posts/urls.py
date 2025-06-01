from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'likes', views.LikeViewSet)

urlpatterns = [
    # path('', views.index, name='index'),  # если не нужен второй раз
    path('', include(router.urls)),  # <-- БЕЗ 'api/'!
    path('posts/<int:post_pk>/comments/', views.CommentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('posts/<int:post_pk>/comments/<int:pk>/', views.CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
] 