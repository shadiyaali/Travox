from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
import logging
logger = logging.getLogger(__name__) 
from rest_framework import status
from .serializers import *
from django.core.mail import send_mail
from django.conf import settings


 
class AdminLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        logger.info(f"Attempting to login user with email: {email}")

        if email is None or password is None:
            return Response({'error': 'Email and password must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_staff and user.is_superuser:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)

        logger.warning(f"Failed login attempt for user: {email}")
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)


class AdminCreateView(APIView):
    def post(self, request, *args, **kwargs):
     
        print("Request Data:", request.data)

   
        serializer = AdminSerializer(data=request.data)
        
 
        print("Serialized Data (before validation):", serializer.initial_data)

        if serializer.is_valid():
            admin = serializer.save()

       
            print("Admin Data (after validation and save):", AdminSerializer(admin).data)

       
            subject = "Your Admin Account Information"
            message = f"Hello {admin.username},\n\nYour admin account has been created successfully.\n\nUsername: {admin.username}\nPassword: {request.data['password']}\n\nPlease change your password after logging in."
            from_email = settings.EMAIL_HOST_USER   
            recipient_list = [admin.email_address]   

            try:
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

          
            return Response(AdminSerializer(admin).data, status=status.HTTP_201_CREATED)

        
        print("Validation Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class AdminListView(APIView):
    def get(self, request, *args, **kwargs):
        admins = Admin.objects.all()
        serializer = AdminSerializer(admins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AdminDetailView(APIView):
    def get(self, request, *args, **kwargs):
 
        admin_id = kwargs.get('id')
        try:
            admin = Admin.objects.get(id=admin_id)
        except Admin.DoesNotExist:
            return Response({"error": "Admin not found"}, status=status.HTTP_404_NOT_FOUND)
 
        serializer = AdminSerializer(admin)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AdminUpdateView(APIView):
    def put(self, request, pk, *args, **kwargs):   
        try:
            admin = Admin.objects.get(pk=pk)
        except Admin.DoesNotExist:
            return Response({"error": "Admin not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AdminSerializer(admin, data=request.data, partial=True)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class BlockUnblockAdminView(APIView):
    def post(self, request, pk, *args, **kwargs): 
        try:
            admin = Admin.objects.get(pk=pk)
        except Admin.DoesNotExist:
            return Response({"error": "Admin not found"}, status=status.HTTP_404_NOT_FOUND)     
        new_status = request.data.get('status')
        if not new_status:
            return Response({"error": "Status is required."}, status=status.HTTP_400_BAD_REQUEST)
        new_status = new_status.lower()
        if new_status not in ['active', 'blocked']:
            return Response({"error": "Invalid status value. Use 'active' or 'blocked'."}, status=status.HTTP_400_BAD_REQUEST)    
        admin.status = new_status
        admin.save()
        return Response(AdminSerializer(admin).data, status=status.HTTP_200_OK)


class AdminDeleteView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        try: 
            admin = Admin.objects.get(pk=pk)
        except Admin.DoesNotExist:
            return Response({"error": "Admin not found"}, status=status.HTTP_404_NOT_FOUND)
        admin.delete()
        return Response({"message": "Admin deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class SubscriptionCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            subscription = serializer.save()
            return Response(SubscriptionSerializer(subscription).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SubscriptionListView(APIView):
    def get(self, request, *args, **kwargs):
        subscriptions = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)
    
class SubscriptionDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            subscription = Subscription.objects.get(pk=pk)
            serializer = SubscriptionSerializer(subscription)
            return Response(serializer.data)
        except Subscription.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
class SubscriptionUpdateView(APIView):
    def put(self, request, pk, *args, **kwargs):
        try:
            subscription = Subscription.objects.get(pk=pk)
            serializer = SubscriptionSerializer(subscription, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Subscription.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
class SubscriptionDeleteView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        try:
            subscription = Subscription.objects.get(pk=pk)
            subscription.delete()
            return Response({"detail": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Subscription.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
class UsersCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            # Save the new Traventry request
            traventry_request = serializer.save()
            return Response(UsersSerializer(traventry_request).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UsersListView(APIView):
    def get(self, request, *args, **kwargs):
        users = Users.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UsersDetailView(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            user = Users.objects.get(id=id)
        except Users.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UsersSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UsersUpdateView(APIView):
    def put(self, request, id, *args, **kwargs):
        try:
            user = Users.objects.get(id=id)
        except Users.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UsersSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UsersDeleteView(APIView):
    def delete(self, request, id, *args, **kwargs):
        try:
            user = Users.objects.get(id=id)
        except Users.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        user.delete()
        return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class BlockUnblockUsersView(APIView):
    def post(self, request, pk, *args, **kwargs): 
        try:
            admin = Users.objects.get(pk=pk)
        except Users.DoesNotExist:
            return Response({"error": "Admin not found"}, status=status.HTTP_404_NOT_FOUND)     
        new_status = request.data.get('status')
        if not new_status:
            return Response({"error": "Status is required."}, status=status.HTTP_400_BAD_REQUEST)
        new_status = new_status.lower()
        if new_status not in ['active', 'blocked']:
            return Response({"error": "Invalid status value. Use 'active' or 'blocked'."}, status=status.HTTP_400_BAD_REQUEST)    
        admin.status = new_status
        admin.save()
        return Response(UsersSerializer(admin).data, status=status.HTTP_200_OK)
    
    
class StaffCreateView(APIView):
    def post(self, request, *args, **kwargs):
     
        print("Request Data:", request.data)

   
        serializer = StaffSerializer(data=request.data)
        
 
        print("Serialized Data (before validation):", serializer.initial_data)

        if serializer.is_valid():
            staff = serializer.save()

       
            print("Staff Data (after validation and save):", StaffSerializer(staff).data)

       
            subject = "Your Staff Account Information"
            message = f"Hello {staff.username},\n\nYour staff account has been created successfully.\n\nUsername: {staff.username}\nPassword: {request.data['password']}\n\nPlease change your password after logging in."
            from_email = settings.EMAIL_HOST_USER   
            recipient_list = [staff.email]   

            try:
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

          
            return Response(StaffSerializer(staff).data, status=status.HTTP_201_CREATED)

        
        print("Validation Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class StaffListView(APIView):
    def get(self, request, *args, **kwargs):
        admins = Staff.objects.all()
        serializer = StaffSerializer(admins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class StaffDetailView(APIView):
    def get(self, request, *args, **kwargs):
 
        admin_id = kwargs.get('id')
        try:
            admin = Staff.objects.get(id=admin_id)
        except Staff.DoesNotExist:
            return Response({"error": "Admin not found"}, status=status.HTTP_404_NOT_FOUND)
 
        serializer = StaffSerializer(admin)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class StaffUpdateView(APIView):
    def put(self, request, pk, *args, **kwargs):   
        try:
            admin = Staff.objects.get(pk=pk)
        except Staff.DoesNotExist:
            return Response({"error": "Admin not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StaffSerializer(admin, data=request.data, partial=True)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class BlockUnblockStaffView(APIView):
    def post(self, request, pk, *args, **kwargs): 
        try:
            admin = Staff.objects.get(pk=pk)
        except Staff.DoesNotExist:
            return Response({"error": "Admin not found"}, status=status.HTTP_404_NOT_FOUND)     
        new_status = request.data.get('status')
        if not new_status:
            return Response({"error": "Status is required."}, status=status.HTTP_400_BAD_REQUEST)
        new_status = new_status.lower()
        if new_status not in ['active', 'blocked']:
            return Response({"error": "Invalid status value. Use 'active' or 'blocked'."}, status=status.HTTP_400_BAD_REQUEST)    
        admin.status = new_status
        admin.save()
        return Response(StaffSerializer(admin).data, status=status.HTTP_200_OK)


class StaffDeleteView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        try: 
            admin = Staff.objects.get(pk=pk)
        except Staff.DoesNotExist:
            return Response({"error": "Admin not found"}, status=status.HTTP_404_NOT_FOUND)
        admin.delete()
        return Response({"message": "Admin deleted successfully"}, status=status.HTTP_204_NO_CONTENT)