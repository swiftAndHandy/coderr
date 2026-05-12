from django.db.models import Min
from rest_framework import serializers

from offers_app.models import OfferDetail, Offer

class OfferDetailSerializer(serializers.ModelSerializer):
    features = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = OfferDetailSerializer(many=True, source="offerdetail_set")
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time'
        ]

    def validate(self, data):
        offer_types = {detail['offer_type'] for detail in data['offerdetail_set']}
        if offer_types != {'basic', 'standard', 'premium'}:
            raise serializers.ValidationError('An offer must have exactly one basic, standard and premium detail.')
        return data

    def get_min_price(self, obj):
        return obj.offerdetail_set.aggregate(Min('price'))['price__min']

    def get_min_delivery_time(self, obj):
        return obj.offerdetail_set.aggregate(Min('delivery_time_in_days'))['delivery_time_in_days__min']

    def create(self, validated_data):
        details = validated_data.pop('offerdetail_set')
        offer = Offer.objects.create(user=self.context['request'].user, **validated_data)
        for detail in details:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer

    def update(self, instance, validated_data):
        details = validated_data.pop('offerdetail_set', [])
        instance = super().update(instance, validated_data)
        for detail in details:
            offer_type = detail.get('offer_type')
            OfferDetail.objects.filter(offer=instance, offer_type=offer_type).update(**detail)
        return instance


class OfferDetailURLSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='offerdetails-list', lookup_field='pk')

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']


class OfferListSerializer(serializers.ModelSerializer):
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    details = OfferDetailURLSerializer(many=True, source="offerdetail_set")
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time',
            'user_details'
        ]

    def get_min_price(self, obj):
        return obj.offerdetail_set.aggregate(Min('price'))['price__min']

    def get_min_delivery_time(self, obj):
        return obj.offerdetail_set.aggregate(Min('delivery_time_in_days'))['delivery_time_in_days__min']

    def get_user_details(self, obj):
        return {
            'first_name': obj.user.profile.first_name,
            'last_name': obj.user.profile.last_name,
            'username': obj.user.username,
        }