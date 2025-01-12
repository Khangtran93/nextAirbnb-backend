from csv import Error
import json
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from useraccount.models import User

from .forms import PropertyModelForm
from .models import Property, Reservations
from .serializers import PropertyListSerializer, PropertyDetailsSerializer

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def property_list(request):
  properties = Property.objects.all()
  serializer = PropertyDetailsSerializer(properties, many=True)
  
  return JsonResponse({
    'data': serializer.data
  })

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_property(request, pk):
  print("=============pk============", pk)
  property = Property.objects.get(pk=pk)
  serializer = PropertyDetailsSerializer(property, many=False)

  if property:
    return JsonResponse({
      'data': serializer.data
    })
  else:
    return JsonResponse({
      'error': 'Property not found'
    }, status=404)

@api_view(['POST'])
def create_reservation(request,pk):
  # data = json.loads(request.body)
  data = request.data
  print(request.POST)
  print('===============data=======================', data)
  property = Property.objects.get(pk=pk)
  user = User.objects.get(pk=request.user.pk)
  user = request.user
  total = data.get('total')
  start_date = data.get('start_date')
  end_date = data.get('end_date')
  number_of_nights = data.get('number_of_nights')
  guest = data.get('guest')
  try:
    Reservations.objects.create(
      property=property, 
      customer=user, 
      total=total, 
      start_date=start_date, 
      end_date=end_date, 
      number_of_nights=number_of_nights, 
      guest=guest
      )

  except Error as e:
    return JsonResponse({"error": e})
  return JsonResponse({"message": "Booking created successfully", "status_code": 400})

  
@api_view(['POST', 'FILES'])
def create_property(request):
  # print("==========POST==============", request.body)
  # data = json.loads(request.body)
  # print("==========POST==============", request.body)
  data = PropertyModelForm(request.POST, request.FILES)
  # data = request.data
  print("===============data type===========", type(data))
  print("===============data=============", data)
  # return JsonResponse({"success": "success"})
  try:
    if data.is_valid():
      property = data.save(commit=False)
      property.landlord = request.user
      property.save()
    else:
      print("=========errors==========", data.errors)
      return JsonResponse({
        'errors': data.errors
      }, status=400)
    return JsonResponse({
      'message': 'Property created successfully',
    })
  except:
    return JsonResponse({
      'error': 'Failed to create property'
    }, status=500)
  
  