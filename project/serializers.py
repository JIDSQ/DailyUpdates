from rest_framework import serializers
from .models import Profile, Account, DailyUpdate, Announcement




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




#Creating Profile
class ProfileCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.userID')   
    
    class Meta:
        model = Profile
        fields = '__all__'  
        

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'      


#Creating Daily Update                                                                        
class UpdateCreateSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source= 'owner.userID')   
    
    class Meta:
        model = DailyUpdate
        fields = '__all__'
        
class UpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyUpdate
        fields ='__all__'



class AnnouncementCreateSerializer(serializers.ModelSerializer):
    adminID = serializers.ReadOnlyField(source= 'adminID.announcementID')

    class Meta:
        model = Announcement
        fields = '__all__'

class AnnouncementSerialier(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields = '__all__'     