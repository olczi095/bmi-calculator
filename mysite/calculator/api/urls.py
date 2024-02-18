from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CalculatedDataDetailView, CalculatedDataListView, PersonViewSet

router = routers.SimpleRouter()
router.register('persons', PersonViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('calculateddata/', CalculatedDataListView.as_view(), name='calculateddata-list'),
    path('calculateddata/<int:pk>/', CalculatedDataDetailView.as_view(),
         name='calculateddata-detail'),
]

urlpatterns += router.urls
