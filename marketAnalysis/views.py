# Create your views here.

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from marketAnalysis.models import Citizen
from marketAnalysis.serializers import ImportCreateSerializer, CitizenUpdateSerializer


@api_view(['POST'])
def importCitizens(request):
    if request.method == 'POST':
        serializer = ImportCreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response({'data': {'import_id': data.__dict__.get('id')}}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def updateCitizens(request, import_id, citizen_id):
    if request.method == 'PATCH':
        instance = Citizen.objects.get(imports_id=import_id, citizen_id=citizen_id)
        serializer = CitizenUpdateSerializer(instance, data=request.data, partial=True,
                                             context={'import_id': import_id})
        if serializer.is_valid():
            data = serializer.save()
            print(data)
            print(serializer.data)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getCitizens(request, import_id):
    if request.method == 'GET':
        instance = Citizen.objects.filter(imports=import_id)
        if len(instance) == 0:
            return Response("unknown id", status=status.HTTP_400_BAD_REQUEST)
        # sdinst = json.dumps(list(instance), cls = DjangoJSONEncoder, ensure_ascii=False)
        # print(sdinst)
        serializer = CitizenUpdateSerializer(instance, many=True)
        # print(instance[0].)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
