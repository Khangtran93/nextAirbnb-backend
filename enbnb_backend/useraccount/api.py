from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from .serializers import UserDetailsSerializer
from useraccount.models import User


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