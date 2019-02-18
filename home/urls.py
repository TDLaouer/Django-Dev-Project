#home/urls.py

from django.urls import path
from home.views import *

urlpatterns = [

    path('', HomeView.as_view(), name='home'),
    path('delete_post/<int:pk>', DeletePost.as_view(), name='delete_post'),
    path('post/<int:pk>', PostView.as_view(), name='post'),
    path('comment/<int:pk>/remove/', CommentRemove.as_view(), name='comment_remove'),
    path('new_post', NewPostView.as_view(), name='new_post'),
    path('post/<int:pk>/edit', EditPostView.as_view(), name='edit_post')

]
