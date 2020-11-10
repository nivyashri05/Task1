from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from newapp.models import User

class UserSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model=User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True},'first_name':{'required':True}}


    def create(self, validated_data):
        print (validated_data)
        email = validated_data.pop('email')
        phone = validated_data.pop('phoneno')
        password = validated_data.pop('password')
        user = User.objects.create(email=email)
        user.set_password(password)
        user.save()
        return user
