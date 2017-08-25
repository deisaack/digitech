from rest_framework.generics import (
        ListAPIView, RetrieveAPIView,
        DestroyAPIView, UpdateAPIView,
        CreateAPIView, RetrieveUpdateAPIView,
    )

from digitech.apply.models import Application
from .serializers import ApplicationSerializer, ApplicationCreateUpdateSerializer,\
    ApplicationDetailSerializer


class ApplicationDetailApiView(RetrieveAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationDetailSerializer
    # lookup_field = 'slug'
    # lookup_url_kwarg = 'abc'


class ApplicationUpdateApiView(RetrieveUpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationDetailSerializer


class ApplicationDeleteApiView(DestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationDetailSerializer


class ApplicationListApiView(ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class ApplicationCreateApiView(CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationCreateUpdateSerializer

    def perfom_create(self, serializer):
        serializer.save(user=self.request.user, amount=5000)
