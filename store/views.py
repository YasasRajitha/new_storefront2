from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.db.models.aggregates import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import ListModelMixin,CreateModelMixin
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework import status
from .models import Product,Collection,Review
from .serializers import ProductSerializer,CollectionSerializer,ReviewSerializer

# Create your views here.

# class ProductList(ListCreateAPIView):
class ProductViewSet(ModelViewSet):

    # queryset = Product.objects.select_related('collection').all().order_by('id')
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer

    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all().order_by('id')
    
    # def get_serializer(self, *args, **kwargs):
    #     return ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        product = get_object_or_404(Product,pk=kwargs['pk'])
        if product.orderitems.count() > 0:
            return Response({'error' : 'Product cannot be deleted because it is associated with an order item.'}
                            , status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)

    # def perform_destroy(self, instance):
    #     return super().perform_destroy(instance)
    # def get(self, request):
    #     queryset = Product.objects.select_related('collection').all().order_by('id')
    #     serializer = ProductSerializer(queryset, many=True, context={'request': request})

    # # return Response('ok')
    #     return Response(serializer.data)
    
    # def post(self, request):
    #     serializer = ProductSerializer(data=request.data)
    #     # if serializer.is_valid():
    #     #     serializer.validated_data
    #     #     return Response('ok')
    #     # else:
    #     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     # print(serializer.validated_data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET','POST'])
# def product_list(request):
#     # return HttpResponse('ok')
#     if request.method == 'GET':
#         queryset = Product.objects.select_related('collection').all().order_by('id')
#         serializer = ProductSerializer(queryset, many=True, context={'request': request})

#     # return Response('ok')
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         # if serializer.is_valid():
#         #     serializer.validated_data
#         #     return Response('ok')
#         # else:
#         #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # print(serializer.validated_data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class ProductDetail(APIView):
# class ProductDetail(RetrieveUpdateDestroyAPIView):

#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
    # lookup_field = 'id'

    # def get(self, request, id):
    #     product = get_object_or_404(Product,pk=id)
    #     serializer = ProductSerializer(product, context={'request': request})
    #     return Response(serializer.data)

    # def put(self, request, id):
    #     product = get_object_or_404(Product,pk=id)
    #     serializer = ProductSerializer(product, data = request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)

    # def delete(self, request, pk):
    #     product = get_object_or_404(Product,pk=pk)
    #     if product.orderitems.count() > 0:
    #         return Response({'error' : 'Product cannot be deleted because it is associated with an order item.'}
    #                         , status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     print(product.delete())
 
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def product_detail(request,id):
#     # try:
#     #     product = Product.objects.get(pk=id)
#     #     serializer = ProductSerializer(product)
#     #     # return Response(id)
#     #     return Response(serializer.data)
#     # except Product.DoesNotExist:
#     #     return Response(status=status.HTTP_404_NOT_FOUND)
#     product = get_object_or_404(Product,pk=id)

#     if request.method == 'GET':
#         serializer = ProductSerializer(product, context={'request': request})
#         return Response(serializer.data)
    
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data) 
    
#     elif request.method == 'DELETE':
#         if product.orderitems.count() > 0:
#             return Response({'error' : 'Product cannot be deleted because it is associated with an order item.'}
#                             , status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         print(product.delete())

#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def collection_detail(request,pk):

class CollectionViewSet(ModelViewSet):

    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')),pk=kwargs['pk'])
        if collection.products.count() > 0:
            return Response({"error": "Collection cannot be deleted because it includes one or more products"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        # print(collection.delete())

        # return Response(status=status.HTTP_204_NO_CONTENT vb )
        return super().destroy(request, *args, **kwargs)

# class CollectionDetail(RetrieveUpdateDestroyAPIView):

#     queryset = Collection.objects.annotate(products_count=Count('products'))
#     serializer_class = CollectionSerializer

    # collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')),pk=pk)
    # if request.method == 'GET':
    #     serializer = CollectionSerializer(collection)

    #     return Response(serializer.data)
    
    # elif request.method == 'PUT':
    #     serializer = CollectionSerializer(collection, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response(serializer.data)
    
    # def delete(self, request, pk):
    #     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')),pk=pk)
    #     if collection.products.count() > 0:
    #         return Response({"error": "Collection cannot be deleted because it includes one or more products"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     print(collection.delete())

    #     return Response(status=status.HTTP_204_NO_CONTENT)

    # elif request.method == 'DELETE':
    #     if collection.products.count() > 0:
    #         return Response({"error": "Collection cannot be deleted because it includes one or more products"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     print(collection.delete())

    #     return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# class CollectionList(ListCreateAPIView):

#     queryset = Collection.objects.annotate(products_count=Count('products')).all().order_by('id')
#     serializer_class = CollectionSerializer

    # if request.method == 'GET':
    #     queryset = Collection.objects.annotate(products_count=Count('products')).all().order_by('id')
    #     serializer = CollectionSerializer(queryset,many=True)

    #     return Response(serializer.data)
    
    # elif request.method == 'POST':
    #     serializer = CollectionSerializer(data = request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

        # for key,value in self.kwargs.items():
        #     print(key)

        # return {}

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}