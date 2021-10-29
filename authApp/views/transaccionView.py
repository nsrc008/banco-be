from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.permissions import IsAuthenticated

from authApp.models.account import Account
from authApp.models.transaccion import Transaccion
from authApp.serializers.transaccionSerializer import TransaccionSerializer

class transaccionDetailView(generics.RetrieveAPIView):
    queryset             = Transaccion.objects.all()
    serializer_class     = TransaccionSerializer
    permission_classes   = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)

        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        return super().get(request, *args, **kwargs)

class transaccionAccountView(generics.ListAPIView):
    queryset             = Transaccion.objects.all()
    serializer_class     = TransaccionSerializer
    permission_classes   = (IsAuthenticated,)

    def get_queryset(self):
        token = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)

        if valid_data['user_id'] != self.kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        queryset = Transaccion.objects.filter(origin_account_id=self.kwargs['account'])
        return queryset

class transaccionCreateView(generics.CreateAPIView):
    queryset             = Transaccion.objects.all()
    serializer_class     = TransaccionSerializer
    permission_classes   = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)

        if valid_data['user_id'] != kwargs['user_id']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        origin_account = Account.objects.get(id=request.data['transaccion_data']['origin_account'])
        if origin_account.balance < request.data['transaccion_data']['amount']:
            stringResponse = {'detail':'Slado Insuficiente'}
            return Response(stringResponse, status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = TransaccionSerializer(data=request.data['transaccion_data'])
        serializer.is_valid(raise_exception=True)
        serializer.save()

        origin_account.balance -= request.data['transaccion_data']['amount']
        origin_account.save()

        destiny_account = Account.objects.get(id=request.data['transaccion_data']['destiny_account'])
        destiny_account.balance += request.data['transaccion_data']['amount']
        destiny_account.save()

        return  Response("Transaccion Exitosa", status=status.HTTP_201_CREATED)

class transaccionUpdateView(generics.UpdateAPIView):
    queryset             = Transaccion.objects.all()
    serializer_class     = TransaccionSerializer
    permission_classes   = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)

        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        
        return super().update(request, *args, **kwargs)

class transaccionDeleteView(generics.DestroyAPIView):
    queryset             = Transaccion.objects.all()
    serializer_class     = TransaccionSerializer
    permission_classes   = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)

        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        return super().destroy(request, *args, **kwargs)