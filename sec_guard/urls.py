# from django.urls import path

# from . import views

# app_name='sec_guard'

# urlpatterns=[
# 		path('', views.index, name='index'),
# 		path('new_entry', views.new_entry, name='new_entry'),
# 		path('search_by_phone', views.search_by_phone, name='search_by_phone'),
# 		path('detail', views.detail, name='detail'),
# ]




from django.urls import path
from .apiviews import PackageCreate, PackageDetailId, PackageListPhone, PackageUpdate

urlpatterns = [
    path("sec_guard/", PackageCreate.as_view(), name="package_create"),
    path("sec_guard/<int:pk>/", PackageDetailId.as_view(), name="package_detail_id"),
    path("sec_guard/search/<phone>/", PackageListPhone.as_view(), name="package_list_phone"),
    path("sec_guard/update/<int:pk>/", PackageUpdate.as_view(), name="package_update"),
]