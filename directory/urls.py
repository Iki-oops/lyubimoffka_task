from django.urls import path, include
from rest_framework.routers import DefaultRouter

from directory.views import CompanyViewSet, EmployeeViewSet

router = DefaultRouter()
router.register('company', CompanyViewSet, basename='company')
router.register('employee', EmployeeViewSet, basename='employee')


urlpatterns = [
    path('', include(router.urls)),
]
