from django.shortcuts import render
from rest_framework import permissions,generics,views
from  rest_framework.response import Response
from . import serializers
from .models import Order


class CreateOrderView(generics.CreateAPIView):
    serializer_class = serializers.OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

class UserOrderListView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        user = request.user
        orders = user.orders.all()
        #orders = Order.objects.filter(user=user) #Еще один способ
        serializer = serializers.OrderSerializer(orders,many=True).data
        return Response(serializer,status=200)

class UpdateOrderStatusView(views.APIView):
    permission_classes = (permissions.IsAdminUser,)

    def patch(self,request,pk):
        status = request.data['status']
        if status not in ['in_process','closed']:
            return Response('Invalid Status',status=400)
        order = Order.objects.get(pk=pk)
        order.status =status
        order.save()
        serializer =serializers.OrderSerializer(order).data
        return Response(serializer,status=206)