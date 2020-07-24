from rest_framework import serializers

class CategoryModelSerializer(serializers.Serializer):
    id          = serializers.IntegerField(read_only=True)
    name        = serializers.CharField(read_only=True)
