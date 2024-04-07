
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
import json

User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView:
    def post(self, request):
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        referral_code = data.get('referral_code')

        if not all([name, email, password]):
            return JsonResponse({'error': 'Name, email, and password are required'}, status=400)

        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        if referral_code:
            referring_user = User.objects.filter(referral_code=referral_code).first()
            if referring_user:
                Referral.objects.create(referring_user=referring_user, referred_user=user)
                referring_user.save()

        return JsonResponse({'user_id': user.id, 'message': 'User created successfully'}, status=201)

@method_decorator(csrf_exempt, name='dispatch')
class UserDetailsView:
    def get(self, request):
        user = request.user
        return JsonResponse({'username': user.username, 'email': user.email, 'referral_code': user.referral_code})

@method_decorator(csrf_exempt, name='dispatch')
class ReferralsView:
    def get(self, request):
        referrals = Referral.objects.filter(referring_user=request.user)
        referrals_data = [{'referring_user': referral.referring_user.username,
                           'referred_user': referral.referred_user.username,
                           'timestamp': referral.timestamp} for referral in referrals]
        return JsonResponse({'referrals': referrals_data})
