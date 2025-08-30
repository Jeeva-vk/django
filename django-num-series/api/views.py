from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

from .serializers import UrlsSerializer

def extract_numbers(data):
    """Extract numbers from JSON data (list or dict with 'numbers')."""
    items = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        for key in ("numbers", "data", "items", "values"):
            if key in data and isinstance(data[key], list):
                items = data[key]
                break
    out = []
    for v in items:
        if isinstance(v, bool):
            continue
        try:
            f = float(v)
            out.append(int(f) if f.is_integer() else f)
        except:
            continue
    return out

class NumbersView(APIView):
    def post(self, request):
        serializer = UrlsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        urls = serializer.validated_data["urls"]
        numbers = []
        errors = {}

        for url in urls:
            try:
                resp = requests.get(url, timeout=5)
                resp.raise_for_status()
                data = resp.json()
                nums = extract_numbers(data)
                numbers.extend(nums)
            except Exception as e:
                errors[url] = str(e)

        # remove duplicates
        seen = set()
        deduped = []
        for n in numbers:
            key = float(n)
            if key not in seen:
                seen.add(key)
                deduped.append(n)

        # sort
        deduped_sorted = sorted(deduped, key=lambda x: float(x))

        return Response({"numbers": deduped_sorted, "errors": errors})
