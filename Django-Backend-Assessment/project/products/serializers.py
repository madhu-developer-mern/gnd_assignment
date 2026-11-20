from rest_framework import serializers

from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=12, decimal_places=2, coerce_to_string=False)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = Item
        fields = (
            "id", "name", "description", "category", "brand", "price",
            "discount_percentage", "stock_quantity", "rating", "is_available",
            "created_at", "updated_at",
        )


class PaginationSerializer(serializers.Serializer):
    # TODO: Candidate implementation
    # Declare page and page_size fields with the required bounds and defaults.
    pass


class ItemFilterSerializer(serializers.Serializer):
    # TODO: Candidate implementation
    # Declare the optional filters and validate the combined ranges.
    pass
