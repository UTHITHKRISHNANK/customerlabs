from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Account, Destination
from .sequent import AccountSerializer, DestinationSerializer
from requests import request  

class AccountListCreate(APIView):
  def get(self, request):
    accounts = Account.objects.all()
    serializer = AccountSerializer(accounts, many=True)
    return Response(serializer.data)

  def post(self, request):
    serializer = AccountSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountDetailDelete(APIView):
  def get_object(self, pk):
    try:
      return Account.objects.get(pk=pk)
    except Account.DoesNotExist:
      raise status.HTTP_404_NOT_FOUND

  def get(self, request, pk):
    account = self.get_object(pk)
    serializer = AccountSerializer(account)
    return Response(serializer.data)

  def delete(self, request, pk):
    account = self.get_object(pk)
    account.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class DestinationListCreate(APIView):
  def get(self, request, pk):
    account = Account.objects.get(pk=pk)
    destinations = Destination.objects.filter(account=account)
    serializer = DestinationSerializer(destinations, many=True)
    return Response(serializer.data)

  def post(self, request, pk):
    account = Account.objects.get(pk=pk)
    serializer = DestinationSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(account=account)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IncomingDataView(APIView):
  def post(self, request):
    if not request.is_json():
      return Response({"message": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    if 'CL-X-TOKEN' not in request.headers:
      return Response({"message": "Un Authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
      secret_token = request.headers['CL-X-TOKEN']
      try:
        account = Account.objects.get(app_secret_token=secret_token)
      except Account.DoesNotExist:
        return Response({"message": "Invalid Token"}, status=status.HTTP_401)

      # Get incoming data
      data = request.data

      # Send data to destinations
      for destination in Destination.objects.filter(account=account):
        self.send_data(destination.url, destination.http_method, destination.headers, data)

      return Response({"message": "Data received successfully"}, status=status.HTTP_200_OK)

  def send_data(self, url, method, headers, data):
    # Use requests library to send data to destination
    response = request(method, url, headers=headers, json=data if method in ('POST', 'PUT') else data)

