from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from .models import Green, Purple, Fertilizer, Milk, Employee, Reports, Pruning, Weeding, VetCosts


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]


class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class GreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Green
        fields = '__all__'


class PurpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purple
        fields = '__all__'


class FertilizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fertilizer
        fields = '__all__'


class PruningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pruning
        fields = '__all__'


class WeedingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weeding
        fields = '__all__'


class MilkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milk
        fields = '__all__'


class VetCostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VetCosts
        fields = '__all__'
