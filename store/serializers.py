from rest_framework import serializers

class ProductSerializer(serializers.Serializer):
    """
    This class serializes the Product model.
    """
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    quantity = serializers.IntegerField()