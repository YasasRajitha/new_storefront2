from django.urls import path
from rest_framework.routers import SimpleRouter,DefaultRouter
from rest_framework_nested import routers
from . import views
from pprint import pprint

# router = SimpleRouter()
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
# pprint(router.urls)

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

urlpatterns = router.urls + products_router.urls

# URLConf
# urlpatterns = [
#     # # path('products/', views.product_list),
#     # path('products/', views.ProductList.as_view()),
#     # path('products/<int:pk>/', views.ProductDetail.as_view()),
#     # path('collections/<int:pk>/', views.CollectionDetail.as_view(),name='collection-detail'),
#     # # path('collections/', views.collection_list),
#     # path('collections/', views.CollectionList.as_view()),
# ]
