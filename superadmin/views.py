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
from django.shortcuts import get_object_or_404

 
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
    
class BankingListCreateView(APIView):
    def get(self, request):
        accounts = Banking.objects.all()
        serializer = BankingSerializer(accounts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BankingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BankingDetailView(APIView):
    def get(self, request, pk):
        try:
            account = Banking.objects.get(pk=pk)
            serializer = BankingSerializer(account)
            return Response(serializer.data)
        except Banking.DoesNotExist:
            return Response({"error": "Banking record not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            account = Banking.objects.get(pk=pk)
            serializer = BankingSerializer(account, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Banking.DoesNotExist:
            return Response({"error": "Banking record not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            account = Banking.objects.get(pk=pk)
            account.delete()
            return Response({"message": "Banking record deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Banking.DoesNotExist:
            return Response({"error": "Banking record not found"}, status=status.HTTP_404_NOT_FOUND)
        
class SalesStaffListAPIView(APIView):
    def get(self, request):
        sales_staff = Staff.objects.filter(staff_role='Sales Staff')
        serializer = StaffSerializer(sales_staff, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)       
        
class InvoiceListCreateAPIView(APIView):
    def post(self, request):
        data = request.data
   
        item = Subscription.objects.get(id=data.get('item'))  
        quantity = data.get('quantity', 1) 
        sub_total = item.rate * quantity 

 
        tax_percentage = data.get('tax', 0)  
        discount = data.get('discount', 0)  
        tax_amount = sub_total * (tax_percentage / 100) 
        total = sub_total - discount + tax_amount 

   
        sales_person_id = data.get('sales_person')
        if sales_person_id:
            sales_person = Staff.objects.get(id=sales_person_id)
            if sales_person.staff_role != "Sales Staff":
                return Response({"sales_person": "The selected staff member is not a Sales Staff."},
                                status=status.HTTP_400_BAD_REQUEST)

     
        invoice_data = {
            **data,  
            'sub_total': sub_total,
            'total': total
        }

        serializer = InvoiceSerializer(data=invoice_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def get(self, request):
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InvoiceDetailAPIView(APIView):
   
    
    def get_object(self, invoice_id):
        try:
            return Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            return None
    
    def get(self, request, invoice_id):
        invoice = self.get_object(invoice_id)
        if not invoice:
            return Response({"detail": "Invoice not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, invoice_id):
        invoice = self.get_object(invoice_id)
        if not invoice:
            return Response({"detail": "Invoice not found."}, status=status.HTTP_404_NOT_FOUND)

 
        data = request.data
        item = Subscription.objects.get(id=data.get('item'))
        quantity = data.get('quantity', invoice.quantity)
        sub_total = item.rate * quantity

        tax_percentage = data.get('tax', invoice.tax)
        discount = data.get('discount', invoice.discount)
        tax_amount = sub_total * (tax_percentage / 100)
        total = sub_total - discount + tax_amount

        sales_person_id = data.get('sales_person', invoice.sales_person.id)
        if sales_person_id:
            sales_person = Staff.objects.get(id=sales_person_id)
            if sales_person.staff_role != "Sales Staff":
                return Response({"sales_person": "The selected staff member is not a Sales Staff."},
                                status=status.HTTP_400_BAD_REQUEST)

        invoice_data = {
            **data,
            'sub_total': sub_total,
            'total': total
        }
        
        serializer = InvoiceSerializer(invoice, data=invoice_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, invoice_id):
        invoice = self.get_object(invoice_id)
        if not invoice:
            return Response({"detail": "Invoice not found."}, status=status.HTTP_404_NOT_FOUND)
        
        invoice.delete()
        return Response({"detail": "Invoice deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class UnpaidInvoicesByUserAPIView(APIView):
  
    def get(self, request, user_id):
      
        user = get_object_or_404(Users, id=user_id)
 
        unpaid_invoices = Invoice.objects.filter(customer_name=user, status='unpaid')

        if not unpaid_invoices:
            return Response({"detail": "No unpaid invoices found for this user."}, status=status.HTTP_404_NOT_FOUND)

     
        serializer = InvoiceSerializer(unpaid_invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

from django.db.models import Sum

class PaymentReceivedAPIView(APIView):

    def post(self, request):
        data = request.data

        user_id = data.get('customer_name')
        amount_received = data.get('amount_received')
        deposit_to_id = data.get('deposit_to')

        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            deposit_to = Banking.objects.get(id=deposit_to_id)
        except Banking.DoesNotExist:
            return Response({"detail": "Banking account not found."}, status=status.HTTP_404_NOT_FOUND)

      
        invoices = Invoice.objects.filter(customer_name=user, status__in=['unpaid', 'partially paid']).order_by('due_date')

        if not invoices:
            return Response({"detail": "No unpaid invoices found."}, status=status.HTTP_404_NOT_FOUND)

        remaining_payment = amount_received
        payment_details = []

        for invoice in invoices:
           
            previous_payments = PaymentReceived.objects.filter(invoice_no=invoice)
            total_paid = previous_payments.aggregate(Sum('amount_received'))['amount_received__sum'] or 0

          
            invoice_remaining_due = invoice.total - total_paid

            if remaining_payment >= invoice_remaining_due:
            
                payment = PaymentReceived.objects.create(
                    customer_name=user,
                    amount_received=invoice_remaining_due,
                    payment_date=data.get('payment_date'),
                    payment_mode=data.get('payment_mode'),
                    payment_number=data.get('payment_number'),
                    deposit_to=deposit_to,
                    reference=data.get('reference'),
                    date=invoice.due_date,
                    invoice_no=invoice,
                    invoice_amount=invoice.total,
                    amount_due=0,
                    total=invoice_remaining_due
                )
                invoice.status = 'paid'
                remaining_payment -= invoice_remaining_due
                payment_details.append(f"Paid full amount for Invoice {invoice.invoice_number}.")
            elif remaining_payment > 0:
         
                payment = PaymentReceived.objects.create(
                    customer_name=user,
                    amount_received=remaining_payment,
                    payment_date=data.get('payment_date'),
                    payment_mode=data.get('payment_mode'),
                    payment_number=data.get('payment_number'),
                    deposit_to=deposit_to,
                    reference=data.get('reference'),
                    date=invoice.due_date,
                    invoice_no=invoice,
                    invoice_amount=invoice.total,
                    amount_due=invoice_remaining_due - remaining_payment,
                    total=remaining_payment
                )
                invoice.status = 'partially paid'
                payment_details.append(f"Paid partial amount for Invoice {invoice.invoice_number}.")
                remaining_payment = 0

           
            invoice.save()

         
            if remaining_payment <= 0:
                break

        if remaining_payment > 0:
        
            PaymentReceived.objects.create(
                customer_name=user,
                amount_received=remaining_payment,
                payment_date=data.get('payment_date'),
                payment_mode=data.get('payment_mode'),
                payment_number=data.get('payment_number'),
                deposit_to=deposit_to,
                reference=data.get('reference'),
                date=None,   
                invoice_no=None,
                invoice_amount=0,
                amount_due=remaining_payment,
                total=remaining_payment
            )
            payment_details.append(f"Remaining balance payment of {remaining_payment} recorded without an invoice.")

        return Response({
            "detail": f"Payment received and applied. Details: {', '.join(payment_details)}",
            "remaining_due": remaining_payment
        }, status=status.HTTP_201_CREATED)


class PaymentReceivedListAPIView(APIView):
    def get(self, request):
        payments = PaymentReceived.objects.all()   
        serializer = PaymentReceivedSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PaymentReceivedDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            payment = PaymentReceived.objects.get(id=pk)
        except PaymentReceived.DoesNotExist:
            return Response({"detail": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PaymentReceivedSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PaymentReceived, Invoice
from .serializers import PaymentReceivedSerializer


from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PaymentReceived, Invoice
from .serializers import PaymentReceivedSerializer

class PaymentReceivedUpdateAPIView(APIView):
    def put(self, request, pk):
        try:
            payment = PaymentReceived.objects.get(id=pk)
        except PaymentReceived.DoesNotExist:
            return Response({"detail": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        new_amount_received = data.get("amount_received", payment.amount_received)

        if not new_amount_received:
            return Response({"detail": "Amount received is required."}, status=status.HTTP_400_BAD_REQUEST)

        invoice = payment.invoice_no
        if invoice:
            # Calculate the previous total paid for the invoice
            previous_payments = PaymentReceived.objects.filter(invoice_no=invoice).exclude(id=payment.id)
            total_paid = previous_payments.aggregate(Sum('amount_received'))['amount_received__sum'] or 0

            invoice_remaining_due = invoice.total - total_paid
            if new_amount_received > invoice_remaining_due:
                return Response({"detail": "Amount received exceeds the remaining due for the invoice."}, 
                                status=status.HTTP_400_BAD_REQUEST)

            # Update invoice and payment details based on new_amount_received
            payment.amount_due = invoice_remaining_due - new_amount_received
            payment.total = new_amount_received

            if payment.amount_due == 0:
                invoice.status = 'paid'
            else:
                invoice.status = 'partially paid'

            invoice.save()
        else:
            # If no invoice is linked, just update the payment fields
            payment.total = new_amount_received
            payment.amount_due = 0

        # Update all fields dynamically from request data
        serializer = PaymentReceivedSerializer(payment, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentReceivedDeleteAPIView(APIView):
    def delete(self, request, pk):
        try:
            payment = PaymentReceived.objects.get(id=pk)
        except PaymentReceived.DoesNotExist:
            return Response({"detail": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)
        
        payment.delete()   
        return Response({"detail": "Payment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class VendorListCreateAPIView(APIView):
    def get(self, request):
        vendors = Vendors.objects.all()
        serializer = VendorsSerializer(vendors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VendorsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorRetrieveUpdateDeleteAPIView(APIView):
    def get(self, request, pk):
        try:
            vendor = Vendors.objects.get(pk=pk)
            serializer = VendorsSerializer(vendor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Vendors.DoesNotExist:
            return Response({"detail": "Vendor not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            vendor = Vendors.objects.get(pk=pk)
        except Vendors.DoesNotExist:
            return Response({"detail": "Vendor not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = VendorsSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            vendor = Vendors.objects.get(pk=pk)
            vendor.delete()
            return Response({"detail": "Vendor deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Vendors.DoesNotExist:
            return Response({"detail": "Vendor not found."}, status=status.HTTP_404_NOT_FOUND)
        
class ExpensesListCreateAPIView(APIView):
    def get(self, request):
        expenses = Expenses.objects.all()
        serializer = ExpensesSerializer(expenses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExpensesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpensesDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            expense = Expenses.objects.get(pk=pk)
        except Expenses.DoesNotExist:
            return Response({"detail": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExpensesSerializer(expense)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            expense = Expenses.objects.get(pk=pk)
        except Expenses.DoesNotExist:
            return Response({"detail": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExpensesSerializer(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            expense = Expenses.objects.get(pk=pk)
        except Expenses.DoesNotExist:
            return Response({"detail": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)

        expense.delete()
        return Response({"detail": "Expense deleted."}, status=status.HTTP_204_NO_CONTENT)
    
class UserCountAPIView(APIView):
    def get(self, request):
        total_users = Users.objects.count()   
        data = {'user_count': total_users}
        return Response(data, status=status.HTTP_200_OK)
    
class AdminCountAPIView(APIView):
    def get(self, request):
        total_admins = Admin.objects.count()   
        data = {'admin_count': total_admins}
        return Response(data, status=status.HTTP_200_OK)