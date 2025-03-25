from csv import Error
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from dj_rest_auth.registration.views import RegisterView
from property.models import Property
from .serializers import CustomRegisterSerializer, UserDetailsSerializer
from useraccount.models import User

class CustomRegisterView(RegisterView):
  serializer_class = CustomRegisterSerializer
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_host_details(request, pk):
  try: 
    host = User.objects.get(pk=pk)
    serializer = UserDetailsSerializer(host, many=False)
    print("====host===", serializer.data)
  except User.DoesNotExist:
    return JsonResponse({
      'error': 'User not found'
    }, status=404)

  return JsonResponse({
    'data': serializer.data
  })

@api_view(['POST'])
def toggle_favorite(request, pk):
  try:
    user = User.objects.get(pk=request.user.id)
    has_property = user.favorite.filter(id=pk).exists()
    if has_property:
      user.favorite.remove(pk)
      return JsonResponse({'message': 'Removed favorite property'}, status=200) 
    else:
      user.favorite.add(pk)
      return JsonResponse({'message': 'Added favorite property'}, status=200)
  except Error:
    return JsonResponse({'error': 'failed to create favorite'}, status=500)

  