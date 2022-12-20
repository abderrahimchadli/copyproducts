from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='post_list'),
    #jason response
    path("json/", views.getdata, name = "senddata"),
    path("multi-json/", views.getmultidata),

    
    #path("one-product/", views.importoneproduct),
    path("one-product/", views.create_product),
    path("multi-product/", views.create_multi_product),
    #billing activation
    path("activate/",views.activate_billing),
    path("handle-charge/",views.handle_billing),
    path("stop-process/",views.stop_process),
    path("read_progress/",views.read_progress),
    path('logout/',views.logoutview),
    path('privacy-policy/',views.privacyPview),
    path('webhooks/Customer-data-request-endpoint/',views.gdprCustomerdatarequest),
    path('webhooks/Customer-data-erasure-endpoint/',views.customerErasurendpoint),
    path('webhooks/Shop-data-erasure-endpoint/',views.shopErasurendpoint)

]
