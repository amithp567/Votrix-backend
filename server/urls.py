from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/voters/', include('apps.voters.urls')),
    path('api/users/',include('apps.users.urls')),
    path('api/voting/', include('apps.voting.urls')),
    path("api/elections/", include("apps.elections.urls")),
    path("api/panchayats/", include("apps.locations.urls")),

    path("api/token/refresh/", TokenRefreshView.as_view()),
    path("api/logout/", TokenBlacklistView.as_view())

]

