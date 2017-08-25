from rest_framework.serializers import (
        ModelSerializer,
        HyperlinkedIdentityField,
        SerializerMethodField,
    )


from digitech.apply.models import Application


class ApplicationSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='apply-api:detail',
        lookup_field='pk',
    )
    class Meta:
        model = Application
        fields = [
            'url',
            'date',
            'amount',
        ]


class ApplicationCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = [
            "user",
            "my_location",
            "payment_method",
            'receipt_no',
            'amount'
        ]


class ApplicationDetailSerializer(ModelSerializer):
    delete_url = HyperlinkedIdentityField(
        view_name='apply-api:delete',
        lookup_field='pk',
    )
    user = SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            'user',
            'my_location',
            'payment_method',
            'receipt_no',
            'amount',
            'date',
            'delete_url'
        ]

    def get_user(self, obj):
        u = ('%s %s (%s)' % (obj.user.last_name, obj.user.first_name, obj.user.username ))
        return u
