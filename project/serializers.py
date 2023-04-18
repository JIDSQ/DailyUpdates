from rest_framework import serializers
from .models import Profile, Account, DailyUpdate
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken



class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = ['user','firstName', 'lastName', 'position']
        
        


class AccountSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer() 
    class Meta:
        model = Account
        fields = ['userID', 'email', 'password', 'role', 'profile']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        account = Account(**validated_data)
        account.set_password(password)
        account.save()
        return account
                                                                        

class DailyUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyUpdate
        fields = ['account','accomplishedTask','inProgressTask','blocker', 'datetime']



class RegisterSerializer(serializers.ModelSerializer):
    repassword = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ['userID','email','password', 'repassword', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data.get('password') != data.get('repassword'):
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        repassword = validated_data.pop('repassword')
        if password != repassword:
            raise serializers.ValidationError("Passwords do not match.")
        email = validated_data['email']
        account, created = Account.objects.get_or_create(email=email, defaults=validated_data)
        if not created:
            raise serializers.ValidationError("User with this email already exists.")
        account.set_password(password)
        account.save()
        return account

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        repassword = validated_data.pop('repassword', None)
        if password:
            if password != repassword:
                raise serializers.ValidationError("Passwords do not match.")
            instance.set_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance



class LoginSerializer(serializers.Serializer):
 
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ['userID','email', 'password']

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            account = Account.objects.filter(email=email).first()
            if account:
                if account.check_password(password):
                    refresh = RefreshToken.for_user(account)
                    data['refresh_token'] = str(refresh)
                    data['access_token'] = str(refresh.access_token)
                else:
                    raise serializers.ValidationError("Invalid password.")
            else:
                raise serializers.ValidationError("Account with this email does not exist.")
        else:
            raise serializers.ValidationError("Please provide both email and password.")
        return data

