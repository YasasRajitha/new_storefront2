from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product,Collection
from .serializers import ProductSerializer,CollectionSerializer

# Create your views here.

@api_view(['GET','POST'])
def product_list(request):
    # return HttpResponse('ok')
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all().order_by('id')
        serializer = ProductSerializer(queryset, many=True, context={'request': request})

    # return Response('ok')
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response('ok')
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        return Response('ok')

@api_view()
def product_detail(request,id):
    # try:
    #     product = Product.objects.get(pk=id)
    #     serializer = ProductSerializer(product)
    #     # return Response(id)
    #     return Response(serializer.data)
    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    product = get_object_or_404(Product,pk=id)
    serializer = ProductSerializer(product, context={'request': request})

    return Response(serializer.data)

@api_view()
def collection_detail(request,pk):

    collection = Collection.objects.get(pk=pk)
    serializer = CollectionSerializer(collection)

    return Response(serializer.data)