from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .serializers import UserSerializer
from .models import User


@api_view(['PATCH'])
def update_profile(request,id):
    data = request.data
    user = User.objects.get(id=id)
    user.first_name = data.get('first_name',user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    email = data.get('email', user.email)
    user.email = email.lower()
    user.dob = data.get('dob',user.dob)
    user.height = data.get('height', user.height)
    user.weight = data.get('weight',user.weight)
    user.allergies = data.get('allergies',user.allergies)
    user.blood_type = data.get('blood_type', user.blood_type)
    user.emergency_contact = data.get('emergency_contact',user.emergency_contact)

    user.save()

    serializer = UserSerializer(user)

    return Response(serializer.data)


