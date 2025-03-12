from csv import Error
import json
from django.db import IntegrityError
from django.forms import ValidationError
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from useraccount.models import User

from .forms import PropertyModelForm
from .models import Property, PropertyImage, Reservations
from .serializers import PropertyListSerializer, PropertyDetailsSerializer, ReservationListSerializer


@api_view(['POST', 'FILES'])
def create_property(request):
  # print("==========POST==============", request.body)
  # data = json.loads(request.body)
  # print("==========POST==============", request.body)
  data = PropertyModelForm(request.POST, request.FILES)
  # data = request.data
  print("===============data type===========", type(data))
  print("===============data=============", data)
  images = request.FILES.getlist("image")
  print('===============images=========', images)
  print("===============images===========", type(images))
  
  # return JsonResponse({"success": "success"})
  try:
    if data.is_valid():
      property = data.save(commit=False)
      property.landlord = request.user
      property.save()
      for image in images:
        print("===============image========", type(image))
        print(image)
        image_object = PropertyImage(property=Property.objects.get(pk=property.pk), image=image)
        image_object.save()
      return JsonResponse({
      'message': 'Property created successfully',
    })
    else:
      print("=========errors==========", data.errors)
      return JsonResponse({
        'errors': data.errors
      }, status=400)
   
  except:
    return JsonResponse({
      'error': 'Failed to create property'
    }, status=500)
  
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def property_list(request):
  properties = Property.objects.all()
  host_id = request.GET.get('host_id', '')
  print("=============host_id============", host_id)
  if host_id:
    properties = properties.filter(landlord=host_id)
  for property in properties:
    print(property)
  serializer = PropertyDetailsSerializer(properties, many=True)
  
  return JsonResponse({
    'data': serializer.data
  })

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def get_property_details(request, pk):
  print("=============pk============", pk)
  print('===========request.user_id============', request.user.id)
  property = Property.objects.get(pk=pk)
  serializer = PropertyDetailsSerializer(property, context={'request': request}, many=False)

  if property:
    print("data", serializer.data)
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
  user = request.user
  print('landlord', property.landlord)
  if user == property.landlord:
    return JsonResponse({'error': 'Cannot create reservation'})
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

    # Check if the request method is POST
    # if request.method != "POST":
    #     return JsonResponse({"error": "Invalid request method. Please use POST."}, status=405)

    # data = request.data
    # print('===============data=======================', data)

    # try:
    #     # Get the property
    #     property = Property.objects.get(pk=pk)
    # except Property.DoesNotExist:
    #     return JsonResponse({"error": "Property not found."}, status=404)

    # user = request.user
    # print('landlord', property.landlord)

    # # Check if the user is the landlord of the property
    # if user == property.landlord:
    #     return JsonResponse({'error': 'Cannot create reservation for your own property'}, status=400)

    # # Extract data from the request
    # total = data.get('total')
    # start_date = data.get('start_date')
    # end_date = data.get('end_date')
    # number_of_nights = data.get('number_of_nights')
    # guest = data.get('guest')

    # # Validate the input data
    # if not all([total, start_date, end_date, number_of_nights, guest]):
    #     return JsonResponse({"error": "Missing required fields."}, status=400)

    # try:
    #     # Create the reservation
    #     reservation = Reservations.objects.create(
    #         property=property,
    #         customer=user,
    #         total=total,
    #         start_date=start_date,
    #         end_date=end_date,
    #         number_of_nights=number_of_nights,
    #         guest=guest
    #     )
    # except IntegrityError as e:
    #     return JsonResponse({"error": "Error creating reservation. Please check your data."}, status=500)
    # except ValidationError as e:
    #     return JsonResponse({"error": str(e)}, status=400)
    # except Exception as e:
    #     return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    # return JsonResponse({"message": "Booking created successfully", "reservation_id": reservation.id}, status=201)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_property_reservations(request, pk):
  property = Property.objects.get(pk=pk)
  reservation = property.reservations.all()
  serializer = ReservationListSerializer(reservation, many=True)
  return JsonResponse({
    'data': serializer.data
  })

@api_view(['GET'])
def get_user_reservations(request):
  user = request.user
  reservations = Reservations.objects.filter(customer=request.user.id).select_related('customer', 'property')
  for res in reservations:
    print('customer name', res.customer.name)
  serializer = ReservationListSerializer(reservations, many=True)
  return JsonResponse({'data': serializer.data})

@api_view(['GET'])
def get_favorite_properties(request):
  try:
    user = User.objects.get(pk=request.user.id)
    favorites = user.favorite.all()
    if favorites:
      serializer = PropertyDetailsSerializer(favorites, many=True)
      return JsonResponse({'data': serializer.data})
    else:
      return JsonResponse({'message': 'No favorite properties found.'}, status=200)

  except User.DoesNotExist:
    return JsonResponse({'error': 'User not found.'}, status=404)