from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
import random
import json
from .serializers import *
from django.http import Http404
from rest_framework.generics import GenericAPIView
from datetime import datetime, timedelta
import jwt
import boto3
from rest_framework.parsers import MultiPartParser, FileUploadParser
import io
from .decorators import *
# Create your views here.


class SendOtpViews(GenericAPIView):
    serializer_class = SendOtpSerializer  # Set the serializer class

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = random.randrange(100000, 999999)
        
        user_type = serializer.validated_data["user_type"]
        print(user_type)
        if user_type == "login":
            try:
                customer = Customer.objects.get(contact_number=serializer.validated_data["number"])
                user_data = UserOTP(user = customer, otp = otp)
                user_data.save()
                numbers = "91" + customer.contact_number
                sendSMS(numbers)
                response_data = {
                    "data": {
                        "number": customer.contact_number,
                        "otp": otp,
                    },
                    "status": True,
                    "code": 200,
                }
                return Response(response_data)
            except Customer.DoesNotExist:
                response_data = {
                    "data": None,
                    "status": False,
                    "code": 401,
                    "message": "User Not Registered.",
                }
                return Response(response_data)
        else:
            try:
                customer = Customer.objects.get(contact_number=serializer.validated_data["number"])
            except:
                customer = None
            if customer:
                response_data = {
                  "data": None,
                  "status": False,
                  "code": 401,
                  "message": "User already exists."
                }
                return Response(response_data)
            else:
                data = Customer(image_url = None, first_name = None, last_name = None ,gender = None,location = None, address = None, contact_number = serializer.validated_data["number"],email = None, date_of_birth = None, age = None , height = None,height_unit=None, weight_unit=None, weight = None, health_issue = None, other_issue = None, any_medication = None, veg_nonveg = None, profession = None , help=None)
                data.save()
                customer = Customer.objects.get(contact_number=serializer.validated_data["number"])
                user_data = UserOTP(user = customer, otp = otp)
                user_data.save()
                print("juwe")
                response_data = {
                    "data": {
                        "number": serializer.validated_data["number"],
                        "otp": otp,
                    },
                    "status": True,
                    "code": 200,
                }
                return Response(response_data)

class VerifyOtpViews(GenericAPIView):
    serializer_class = VerifyOtpSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
 
        try:
            otp = UserOTP.objects.get(otp= serializer.validated_data["otp"])
        except:
            otp = None
        if otp:
            otp.delete()         
            customer = Customer.objects.get(contact_number=otp.user.contact_number)
            print(customer)
            access_token_expiry = datetime.utcnow() + timedelta(minutes=30)
            refresh_token_expiry = datetime.utcnow() + timedelta(minutes=30)
            # Generate the access token
            access_token_payload = {
                'client_id': customer.contact_number,
                'exp': access_token_expiry,
                'iat': datetime.utcnow(),
            }
            access_token = jwt.encode(access_token_payload, str(customer.id), algorithm='HS256')
            # Generate the refresh token
            refresh_token_payload = {
                'client_id': customer.email,
                'exp': refresh_token_expiry,
                'iat': datetime.utcnow(),
            }
            refresh_token = jwt.encode(refresh_token_payload, customer.contact_number, algorithm='HS256')
            print(access_token)
            print(refresh_token)
            # Serialize the customer object
            serializer = CustomerSerializer(customer)
            response_data = {
                "data": {
                    "accessToken": access_token,
                    "user":serializer.data
                },
                "status": True,
                "code": 200
            }
            return Response(response_data)
        else:
            response_data ={
                "data": None,
                "status": False,
                "code": 401,
                "message": "Invalid OTP.",
            }
            return Response(response_data)

class UploadImageView(GenericAPIView):
    parser_classes = [MultiPartParser]  # Allow file uploads
    
    def post(self, request):
        data = request.data
        print(data)

        try:
            uploaded_image = request.data.get("image")
            print(uploaded_image)
            if uploaded_image:
                uploaded_image = data["image"]
                aws_access_key_id = 'AKIAU62W7KNUZ4DKGRU3'
                aws_secret_access_key = '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'
                aws_region = 'us-east-2'
                bucket_name = 'appstacklabs'
                s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
                object_key = f"images/{uploaded_image}"  # Adjust the path in the bucket as needed
                image_data = uploaded_image.read()
                # Upload the image data to S3 using put_object
                s3.put_object(Body=image_data, Bucket=bucket_name, Key=object_key)
                s3_image_url = f"https://{bucket_name}.s3.{aws_region}.amazonaws.com/{object_key}"
                print(s3_image_url)
                response_data = {
                    "data": s3_image_url,
                    "status": True,
                    "code": 200,
                    "message": "Image Successfully uploaded.",
                }
                return Response(response_data)
            else:
                response_data ={
                "data": None,
                "status": False,
                "code": 400,
                "message": "Image Not Found.",
            }
        except Exception as e:
            print(e)
            response_data ={
                "data": None,
                "status": False,
                "code": 500,
                "message": "Something Wrong, Try again.",
            }
            return Response(response_data)
    




class UpdateUserDetailViews(APIView):   
    def post(self, request):
        auth_header = request.headers.get('Authorization')
        data = request.data
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
            try:
                decoded_payload = jwt.decode(token, algorithms=['HS256'], options={"verify_signature": False})
                try:
                    customer = Customer.objects.get(contact_number=decoded_payload['client_id'])
                    for key, value in data.items():
                        if isinstance(value, list):
                            value = ', '.join(value)  # Convert list to comma-separated string
                        if hasattr(customer, key):
                            setattr(customer, key, value)
                        else:
                            response_data ={
                                "data": None,
                                "status": False,
                                "code": 400,
                                "message": f"Invalid field name: {key}",
                            }
                            return Response(response_data)
                    customer.save()
                    
                    serializer = CustomerSerializer(customer)
                    serialized_data = serializer.data

                    response_data = {
                        "data": serialized_data,
                        "status": True,
                        "code": 200,
                        "message": "User Detail Successfully updated.",
                    }
                    return Response(response_data)
                    
                except Customer.DoesNotExist:
                    response_data ={
                        "data": None,
                        "status": False,
                        "code": 401,
                        "message": "User Doesn't exist.",
                    }
                    return Response(response_data)
                except Exception as e:
                    response_data ={
                        "data": None,
                        "status": False,
                        "code": 500,
                        "message": "An error occurred.",
                    }
                    return Response(response_data)
            except jwt.ExpiredSignatureError:
                response_data ={
                    "data": None,
                    "status": False,
                    "code": 401,
                    "message": "Token has expired.",
                }
                return Response(response_data)
            except jwt.DecodeError:
                response_data ={
                    "data": None,
                    "status": False,
                    "code": 498,
                    "message": "Invalid token.",
                }
                return Response(response_data)
        else:
            response_data ={
                "data": None,
                "status": False,
                "code": 400,
                "message": "No token provided.",
            }
            return Response(response_data)



class AllDishesViews(APIView):   
    def post(self, request):
        auth_header = request.headers.get('Authorization')
        data = request.data
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
            try:
                decoded_payload = jwt.decode(token, algorithms=['HS256'], options={"verify_signature": False})
                try:
                    customer = Customer.objects.get(contact_number=decoded_payload['client_id'])
                    breakfast_instances = Breakfast.objects.all()  # Retrieve all Breakfast instances
                    breakfastserializer = BreakfastSerializer(breakfast_instances, many=True)
                    print(breakfastserializer.data)
                    
                    launch_instances = Launch.objects.all()  # Retrieve all Launch instances
                    launchserializer = LaunchSerializer(launch_instances, many=True)
                    
                    dinner_instances = Dinner.objects.all()  # Retrieve all Dinner instances
                    dinnerserializer = DinnerSerializer(dinner_instances, many=True)
                    
                    snacks_instances = Snacks.objects.all()  # Retrieve all Snacks instances
                    snacksserializer = SnacksSerializer(snacks_instances, many=True)
                    response_data = {
                        "Breakfast": breakfastserializer.data,
                        "Launch": launchserializer.data,
                        "Dinner": dinnerserializer.data,
                        "Snacks": snacksserializer.data,
                        "status": True,
                        "code": 200
                    }
                    print(response_data)
                    return Response(response_data)
                except Customer.DoesNotExist:
                    response_data ={
                        "data": None,
                        "status": False,
                        "code": 401,
                        "message": "Invalid Authentication.",
                    }
                    return Response(response_data)
                except Exception as e:
                    print
                    response_data ={
                        "data": None,
                        "status": False,
                        "code": 500,
                        "message": "An error occurred.",
                    }
                    return Response(response_data)
            except jwt.ExpiredSignatureError:
                response_data ={
                    "data": None,
                    "status": False,
                    "code": 401,
                    "message": "Token has expired.",
                }
                return Response(response_data)
            except jwt.DecodeError:
                response_data ={
                    "data": None,
                    "status": False,
                    "code": 498,
                    "message": "Invalid token.",
                }
                return Response(response_data)
        else:
            response_data ={
                "data": None,
                "status": False,
                "code": 400,
                "message": "No token provided.",
            }
            return Response(response_data)


class GetDisheViews(APIView):   
    def post(self, request):
        auth_header = request.headers.get('Authorization')
        data = request.data
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
            try:
                decoded_payload = jwt.decode(token, algorithms=['HS256'], options={"verify_signature": False})
                try:
                    customer = Customer.objects.get(contact_number=decoded_payload['client_id'])
                    try:
                        if data["type_of_meal"] == "Breakfast":
                            breakfast_instances = Breakfast.objects.get(food=data["type_of_food"])  # Retrieve all Breakfast instances
                            serializer = BreakfastSerializer(breakfast_instances)
                        elif data["type_of_meal"] == "Lunch":                   
                            launch_instances = Launch.objects.get(food=data["type_of_food"])  # Retrieve all Launch instances
                            serializer = LaunchSerializer(launch_instances)
                        elif data["type_of_meal"] == "Dinner":
                            dinner_instances = Dinner.objects.get(food=data["type_of_food"])  # Retrieve all Dinner instances
                            serializer = DinnerSerializer(dinner_instances)
                        elif data["type_of_meal"] == "Snacks":
                            snacks_instances = Snacks.objects.all()  # Retrieve all Snacks instances
                            serializer = SnacksSerializer(snacks_instances)
                        response_data = {
                            "data":  {
                                "caloriesUsed": 650,
                                "calorieBreakdown": {
                                "calories": 100,
                                "pral": 100,
                                "calcium": 450
                                },
                                "breakfast": [
                                {
                                    "dishName": "idli",
                                    "ingredients": "Idli 100 gms idly Ravva, Water",
                                    "calories": 400
                                },
                                {
                                    "dishName": "idli",
                                    "ingredients": "Idli 100 gms idly Ravva, Water",
                                    "calories": 400
                                }
                              ],
                              "lunch": [
                                {
                                  "dishName": "idli",
                                  "ingredients": "Idli 100 gms idly Ravva, Water",
                                  "calories": 400
                                },
                                {
                                  "dishName": "idli",
                                  "ingredients": "Idli 100 gms idly Ravva, Water",
                                  "calories": 400
                                }
                              ],
                              "eveningSnacks": [
                                {
                                  "dishName": "idli",
                                  "ingredients": "Idli 100 gms idly Ravva, Water",
                                  "calories": 400
                                },
                                {
                                  "dishName": "idli",
                                  "ingredients": "Idli 100 gms idly Ravva, Water",
                                  "calories": 400
                                }
                              ],
                              "dinner": [
                                {
                                  "dishName": "idli",
                                  "ingredients": "Idli 100 gms idly Ravva, Water",
                                  "calories": 400
                                },
                                {
                                  "dishName": "idli",
                                  "ingredients": "Idli 100 gms idly Ravva, Water",
                                  "calories": 400
                                }
                              ]
                            },
                            "status": True,
                            "code": 200
                        }
                        print(response_data)
                        return Response(response_data)
                    except:
                        response_data ={
                            "data": None,
                            "status": False,
                            "code": 401,
                            "message": "Meal or Food Not Foud.",
                        }
                        return Response(response_data)
                except Customer.DoesNotExist:
                    response_data ={
                        "data": None,
                        "status": False,
                        "code": 401,
                        "message": "Invalid Authentication.",
                    }
                    return Response(response_data)
                except Exception as e:
                    print
                    response_data ={
                        "data": None,
                        "status": False,
                        "code": 500,
                        "message": "An error occurred.",
                    }
                    return Response(response_data)
            except jwt.ExpiredSignatureError:
                response_data ={
                    "data": None,
                    "status": False,
                    "code": 401,
                    "message": "Token has expired.",
                }
                return Response(response_data)
            except jwt.DecodeError:
                response_data ={
                    "data": None,
                    "status": False,
                    "code": 498,
                    "message": "Invalid token.",
                }
                return Response(response_data)
        else:
            response_data ={
                "data": None,
                "status": False,
                "code": 400,
                "message": "No token provided.",
            }
            return Response(response_data)


class UpdateDailyRecipeViews(APIView):   
    def post(self, request):
        auth_header = request.headers.get('Authorization')
        data = request.data
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
            try:
                decoded_payload = jwt.decode(token, algorithms=['HS256'], options={"verify_signature": False})
                try:
                    customer = Customer.objects.get(contact_number=decoded_payload['client_id'])
                    try:
                        customer_id = request.data.get('customer')  # Get customer ID from the request data
                        print(customer_id)
                        customer_instance = get_object_or_404(Customer, id=customer_id)
                        
                        # Create a DailyRecipe instance and populate its fields
                        daily_recipe_instance = DailyRecipe(
                            customer=customer_instance,
                            food=request.data.get('food'),
                            quantity=request.data.get('quantity'),
                            oil=request.data.get('oil'),
                            gl=request.data.get('gl'),
                            usable_cals=request.data.get('usable_cals'),
                            # ... populate other fields ...
                        )
                        print(daily_recipe_instance)
                        daily_recipe_instance.save()  # Save the instance
                        
                        serializer = DailyRecipeSerializer(daily_recipe_instance)
                        response_data = {
                            "data": serializer.data,
                            "status": True,
                            "code": 200
                        }
                        return Response(response_data)
                    except Exception as e:
                        response_data ={
                            "data": None,
                            "status": False,
                            "code": 401,
                            "message": "Meal or Food Not Found.",
                        }
                        return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
                except Customer.DoesNotExist:
                    response_data ={
                        "data": None,
                        "status": False,
                        "code": 401,
                        "message": "Invalid Authentication.",
                    }
                    return Response(response_data)
                except Exception as e:
                    print
                    response_data ={
                        "data": None,
                        "status": False,
                        "code": 500,
                        "message": "An error occurred.",
                    }
                    return Response(response_data)
            except jwt.ExpiredSignatureError:
                response_data ={
                    "data": None,
                    "status": False,
                    "code": 401,
                    "message": "Token has expired.",
                }
                return Response(response_data)
            except jwt.DecodeError:
                response_data ={
                    "data": None,
                    "status": False,
                    "code": 498,
                    "message": "Invalid token.",
                }
                return Response(response_data)
        else:
            response_data ={
                "data": None,
                "status": False,
                "code": 400,
                "message": "No token provided.",
            }
            return Response(response_data)