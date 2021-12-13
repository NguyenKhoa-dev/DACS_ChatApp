from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "Chat"

urlpatterns = [
    path('', views.index, name='index'),
    path('user', views.UserLoginRegister, name='user'),
    path('logout/',views.logoutUser,name='logout'),
    path('info/<str:user_name>/',views.account_view,name='viewinfo'),
    path('info/<str:user_name>/edit/',views.edit_account_view,name='edit_account'),
    path('chatroom/<int:room_id>', views.room,name='room'),
    path('myrooms/', views.myrooms, name='myrooms'),
    path('delete_room/<int:room_id>', views.deleteRoom, name='deleteroom'),
    path('escape_room/<int:room_id>', views.escapeRoom, name='escaperoom'),
    path('update_room/<int:room_id>', views.updateRoom, name='updateroom')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)