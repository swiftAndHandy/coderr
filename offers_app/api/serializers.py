from django.db.models import Min
from rest_framework import serializers

from offers_app.models import OfferDetail, Offer
from profile_app.api.serializers import ProfileSerializer


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
        if len(data['offerdetail_set']) != 3:
            raise serializers.ValidationError('An offer must have exactly three details.')
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