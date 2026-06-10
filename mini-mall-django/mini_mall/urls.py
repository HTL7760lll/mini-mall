from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API
    path('api/member/', include('apps.member.urls')),
    path('api/goods/', include('apps.goods.urls')),
    path('api/cart/', include('apps.cart.urls')),
    path('api/order/', include('apps.order.urls')),
    path('api/banner/', include('apps.banner.urls')),
    path('api/comment/', include('apps.comment.urls')),

    # Token refresh
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
