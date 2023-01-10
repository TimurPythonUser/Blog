from django.urls import path
from .views import *


urlpatterns = [
    path('', PostHome.as_view(), name='home'),
    path('detail/<int:post_id>/', show_detail_post, name='detail'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('addpage/', AddPage.as_view(), name='addpost'),
    path('showauthorpost/', ShowPost.as_view(), name='my_posts'),
    path('searchres/', SearchResult.as_view(), name='search'),
    path('like/<int:pk>', LikeView, name='like_post')
]