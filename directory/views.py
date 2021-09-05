from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Company, Employee
from .permissions import OwnerOrAdmin
from .serializers import CompanySerializer, EmployeeSerializer, CompanySearchSerializer


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = (OwnerOrAdmin,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Company.objects.all()
        return Company.objects.filter(owner=self.request.user)

    @action(methods=['get'], detail=False)
    def search(self, request):
        result = Company.objects.all()
        q = request.query_params.get('q')
        if q is not None:
            result = Company.objects.filter(
                Q(name__icontains=q) | Q(employees__full_name__icontains=q) | Q(employees__work__icontains=q)
            ).distinct()
        result = result[:5]
        serializer = CompanySearchSerializer(result, many=True)
        return Response(serializer.data)


class EmployeeViewSet(ModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = (OwnerOrAdmin,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Employee.objects.all()
        return Employee.objects.filter(owner=self.request.user)
