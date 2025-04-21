from csv import Error
from datetime import datetime

from django.db import IntegrityError
from django.forms import ValidationError
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.db.models import Q
from useraccount.models import User

from .forms import PropertyModelForm
from .models import Property, PropertyImage, Reservations
from .serializers import PropertyListSerializer, PropertyDetailsSerializer, ReservationListSerializer


@api_view(['POST', 'FILES'])
def create_property(request):
  data = PropertyModelForm(request.POST, request.FILES)
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
  where = Q()
  # filter by host_id
  host_id = request.GET.get('host_id', '')

  # filter by search parameters
  country = request.GET.get('country', '')
  check_in = request.GET.get('check_in', '')
  check_out = request.GET.get('check_out', '')
  guests = request.GET.get('guests', '')
  bedrooms = request.GET.get('bedrooms', '')
  bathrooms = request.GET.get('bathrooms', '')
  category = request.GET.get('category', '')

  reserved_property_ids = []

  if host_id:
    where |= Q(landlord=host_id)
  if country:
    where |= Q(country_code=country)
  if check_in and check_out:
    check_in = datetime.strptime(check_in, '%m/%d/%Y %H:%M:%S')
    check_out = datetime.strptime(check_out, '%m/%d/%Y %H:%M:%S')
    
    reservations = Reservations.objects.all().filter(start_date__lte=check_in).filter(end_date__gte=check_out)
    if reservations:
      for reservation in reservations:
        reserved_property_ids.append(reservation.property_id)
  if guests:
    where |= Q(guests=guests)
  if bedrooms:
    where |= Q(bedrooms=bedrooms)
  if bathrooms:
    where |= Q(bathrooms=bathrooms)
  if category:
    where |= Q(category=category)

  properties = properties.filter(where)
  if len(reserved_property_ids) > 0:
    properties = properties.exclude(id__in=reserved_property_ids)

  serializer = PropertyDetailsSerializer(properties, many=True)
  
  return JsonResponse({
    'data': serializer.data
  })

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def get_property_details(request, pk):
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