from rest_framework import generics

from .models import Employee, Reports, Green, Purple, Milk, Fertilizer, Pruning, Weeding, VetCosts
from .serializer import EmployeeSerializer, ReportsSerializer, GreenSerializer, PurpleSerializer, \
    MilkSerializer, FertilizerSerializer, PruningSerializer, WeedingSerializer, VetCostsSerializer


class ReportsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer


class ReportsRetrtieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer


class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeRetrtieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class GreenListCreateAPIView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = GreenSerializer


class GreenRetrtieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Green.objects.all()
    serializer_class = GreenSerializer


class PurpleListCreateAPIView(generics.ListCreateAPIView):
    queryset = Purple.objects.all()
    serializer_class = PurpleSerializer


class PurpleRetrtieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Purple.objects.all()
    serializer_class = PurpleSerializer


class FertilizerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Fertilizer.objects.all()
    serializer_class = FertilizerSerializer


class FertilizerRetrtieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fertilizer.objects.all()
    serializer_class = FertilizerSerializer


class PruningListCreateAPIView(generics.ListCreateAPIView):
    queryset = Pruning.objects.all()
    serializer_class = PruningSerializer


class PruningRetrtieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pruning.objects.all()
    serializer_class = PruningSerializer


class WeedingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Weeding.objects.all()
    serializer_class = WeedingSerializer


class WeedingRetrtieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Weeding.objects.all()
    serializer_class = WeedingSerializer


class MilkListCreateAPIView(generics.ListCreateAPIView):
    queryset = Milk.objects.all()
    serializer_class = MilkSerializer


class MilkRetrtieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Milk.objects.all()
    serializer_class = MilkSerializer


class VetCostsListCreateAPIView(generics.ListCreateAPIView):
    queryset = VetCosts.objects.all()
    serializer_class = VetCostsSerializer


class VetCostsRetrtieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VetCosts.objects.all()
    serializer_class = VetCostsSerializer
