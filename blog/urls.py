from django.urls import path
from .import views

# Application namespace, allows to organize urls by application.
# <int:year> these all are path converters.
# if path converters is not sufficient use re_path.

app_name = 'blog'

urlpatterns = [
    #path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share', views.post_share, name='post_share'),
]
