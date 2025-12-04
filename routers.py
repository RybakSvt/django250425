from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from library.views.books import BookViewSet
from library.views.publishers import PublisherViewSet


router = SimpleRouter()
# router = DefaultRouter()
router.register('publisher', PublisherViewSet)  # /api/v1/publishers/
                                                      # /api/v1/publishers/<pk>

router.register('books', BookViewSet)

urlpatterns = [
    # path('books/', include('library.urls.books')),
    path('users/', include('library.urls.users')),
    path('categories/', include('library.urls.categories')),
    path('token-auth/', obtain_auth_token),
    path('jwt-auth/', TokenObtainPairView.as_view()),
    path('jwt-refresh/', TokenRefreshView.as_view()),
] + router.urls



# from django.urls import path, include
# from rest_framework.routers import DefaultRouter, SimpleRouter
# from rest_framework.authtoken.views import obtain_auth_token
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
#
# from library.views.books import BookListCreateAPIView
# from library.views.publishers import PublisherViewSet
# from library.views.posts import PostViewSet
# from library.views.events import EventViewSet
#
#
# #router = SimpleRouter()
# router = DefaultRouter()
# router.register('publisher', PublisherViewSet)  # /api/v1/publishers/
# router.register('posts', PostViewSet, basename='posts')                                                      # /api/v1/publishers/<pk>
# router.register('events', EventViewSet, basename='events')
#
#
#
# urlpatterns = [
#     path('books/', include('library.urls.books')),
#     path('users/', include('library.urls.users')),
#     path('categories/', include('library.urls.categories')),
#     path('token-auth/', obtain_auth_token),
#     path('jwt-auth/', TokenObtainPairView.as_view()),
#     path('jwt-refresh/', TokenRefreshView.as_view()),
# ] + router.urls
