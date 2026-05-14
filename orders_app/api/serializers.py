from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from offers_app.models import OfferDetail
from orders_app.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    Read-Only serializer for the full Order model.
    """
    features = serializers.ListField(child=serializers.CharField())

    customer_user = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'customer_user',
            'business_user',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'status',
            'created_at',
            'updated_at',
        ]

class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Accepts a single offer_detail_id and creates an order.
    Offer detail fields are snapshotted so later edits to the offer don't affect existing orders.
    """
    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = ['offer_detail_id']

    def create(self, validated_data):
        offer_detail_id = validated_data.pop('offer_detail_id')
        offer_detail = get_object_or_404(
            OfferDetail.objects.select_related('offer__user'),
            pk=offer_detail_id
        )

        return Order.objects.create(
            customer_user=self.context['request'].user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
        )

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """Restricts PATCH updates to the status field only."""
    class Meta:
        model = Order
        fields = ['status']
