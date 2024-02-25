from rest_framework import serializers


class PolygonBoundarySerializer(serializers.Serializer):
    type = serializers.CharField()
    coordinates = serializers.ListField(
        child=serializers.ListField(child=serializers.ListField(child=serializers.FloatField())))


class FeatureSerializer(serializers.Serializer):
    type = serializers.CharField()
    geometry = PolygonBoundarySerializer()


class MarketShareRequestSerializer(serializers.Serializer):
    city_boundary = FeatureSerializer()
    points = serializers.ListField(child=serializers.ListField(child=serializers.FloatField()))
