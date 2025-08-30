import random, string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ShortURL
from .serializers import ShortURLSerializer

def generate_short_code(length=6):
    """Generate a random short code"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@api_view(['POST'])
def shorten_url(request):
    """Create a short code for a given URL"""
    original_url = request.data.get("url")
    if not original_url:
        return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Generate unique short code
    code = generate_short_code()
    while ShortURL.objects.filter(short_code=code).exists():
        code = generate_short_code()

    short_obj = ShortURL.objects.create(original_url=original_url, short_code=code)
    serializer = ShortURLSerializer(short_obj)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def expand_url(request, code):
    """Expand a short code to original URL"""
    try:
        short_obj = ShortURL.objects.get(short_code=code)
        short_obj.usage_count += 1
        short_obj.save()
        return Response({"original_url": short_obj.original_url, "usage_count": short_obj.usage_count})
    except ShortURL.DoesNotExist:
        return Response({"error": "Short code not found"}, status=status.HTTP_404_NOT_FOUND)
