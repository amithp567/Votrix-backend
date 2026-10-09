
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/voters/', include('voters.urls')),
    path('api/users/',include('users.urls')),
    path('api/voting/', include('voting.urls')),
    path("api/elections/", include("elections.urls")),
    path("api/panchayats/", include("locations.urls")),

]

