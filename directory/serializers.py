from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from .models import Company, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    company = SlugRelatedField(slug_field='name', queryset=Company.objects.all())
    phone_numbers = serializers.SerializerMethodField()
    work = serializers.CharField(write_only=True)
    private = serializers.CharField(write_only=True, required=False)
    fax = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Employee
        fields = ('id', 'full_name', 'position', 'phone_numbers', 'work', 'private', 'fax', 'company')
        read_only_fields = ('id',)

        validators = [
            UniqueTogetherValidator(queryset=Employee.objects.all(),
                                    fields=('full_name', 'company'),
                                    message='Сотрудник с таким именем уже существует в этой компании'),
        ]

    def get_phone_numbers(self, obj):
        result = {'work': obj.work}
        result = dict(**result, private=obj.private) if obj.private else result
        result = dict(**result, fax=obj.fax) if obj.fax else result
        return result


class CompanySerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    employees = EmployeeSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Company
        fields = ('id', 'address', 'name', 'description', 'employees', 'owner')
        read_only_fields = ('id', 'owner',)


class CompanySearchSerializer(serializers.ModelSerializer):
    employees = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ('name', 'employees')

    def get_employees(self, obj):
        employees = obj.employees.all()[:5]
        result = list(employees.values('full_name', 'position'))

        # Добавляю к каждому сотруднику телефонные номера
        for val, employee in enumerate(employees):
            phone_numbers = dict(work=employee.work)
            if employee.private:
                phone_numbers = dict(**phone_numbers, private=employee.private)
            elif employee.fax:
                phone_numbers = dict(**phone_numbers, fax=employee.fax)
            result[val].update(**phone_numbers)
        return result
