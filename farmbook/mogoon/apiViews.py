from rest_framework import generics

from .models import Employee, Reports, Green, Purple, Kandojobs, Milk, Fertilizer
from .serializer import EmployeeSerializer, ReportsSerializer, GreenSerializer, PurpleSerializer, KandojobsSerializer, \
    MilkSerializer, FertilizerSerializer


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


class KandojobsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Kandojobs.objects.all()
    serializer_class = KandojobsSerializer


class KandojobsRetrtieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kandojobs.objects.all()
    serializer_class = KandojobsSerializer


class MilkListCreateAPIView(generics.ListCreateAPIView):
    queryset = Milk.objects.all()
    serializer_class = MilkSerializer


class MilkRetrtieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Milk.objects.all()
    serializer_class = MilkSerializer


class FertilizerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Fertilizer.objects.all()
    serializer_class = FertilizerSerializer


class FertilizerRetrtieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fertilizer.objects.all()
    serializer_class = FertilizerSerializer

