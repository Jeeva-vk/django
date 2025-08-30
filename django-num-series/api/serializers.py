from rest_framework import serializers

class UrlsSerializer(serializers.Serializer):
    urls = serializers.ListField(
        child=serializers.URLField(), allow_empty=False
    )
