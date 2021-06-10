from django.conf.urls import url, include
from .views import signup, profile, logout


urlpatterns = [
    url('signup/', signup, name='signup'),
    url('profile/', profile, name='profile'),
    url('logout/', logout, name='logout'),
    url('', include('django.contrib.auth.urls')),
    url('api/', include('accounts.api.urls')),
]