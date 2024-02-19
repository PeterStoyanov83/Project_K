# from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import Group
# from django.core.mail import send_mail
# from django.urls import reverse
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_text
# from django.template.loader import render_to_string
# from .tokens import account_activation_token  # You need to create this token
# from .models import CustomUser
#
# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False  # Don't activate until email is verified
#             user.save()
#             # Add logic here to assign to a default group if necessary
#             # Send verification email
#             current_site = get_current_site(request)
#             subject = 'Activate Your Account'
#             message = render_to_string('account_activation_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user),
#             })
#             user.email_user(subject, message)
#             return redirect('account_activation_sent')
#     else:
#         form = UserCreationForm()
#     return render(request, 'registration/register.html', {'form': form})
