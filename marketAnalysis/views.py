# Create your views here.

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from marketAnalysis.models import Citizen
from marketAnalysis.serializers import ImportCreateSerializer, CitizenGetUpdateSerializer, GiftDistributionSerializer, \
    AgePercentileSerializer


@api_view(['POST'])
def importCitizens(request):
    if request.method == 'POST':
        serializer = ImportCreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response({'data': {'import_id': data.pk}}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def updateCitizens(request, import_id, citizen_id):
    if request.method == 'PATCH':
        try:
            if len(request.data) == 0:
                return Response({'error': "Body is empty"}, status=status.HTTP_400_BAD_REQUEST)
            instance = Citizen.objects.get(imports_id=import_id, citizen_id=citizen_id)
            serializer = CitizenGetUpdateSerializer(instance, data=request.data, partial=True,
                                                    context={'import_id': import_id})
            if serializer.is_valid():
                serializer.save()
                return Response({'data': serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            print(err)
            return Response({'error': err.__str__()}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getCitizens(request, import_id):
    if request.method == 'GET':
        instance = Citizen.objects.filter(imports=import_id)
        if len(instance) == 0:
            return Response("unknown id", status=status.HTTP_400_BAD_REQUEST)
        serializer = CitizenGetUpdateSerializer(instance, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def getGifsCount(request, import_id):
    if request.method == 'GET':
        data = {'data': ""}
        serializer = GiftDistributionSerializer(data, context={'import_id': import_id})
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getPercentileAge(request, import_id):
    if request.method == 'GET':
        data = {'data': []}
        serializer = AgePercentileSerializer(data, context={'import_id': import_id})
        return Response(serializer.data, status=status.HTTP_200_OK)
