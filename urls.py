from django.urls import path
from . import views

urlpatterns = [
    path("register/",views.regist,name ="register"),
    path("",views.login,name ="login"),
    path("index/" ,views.index,name="index"),
    path("about/",views.about,name="about"),
    path("contact/",views.contact,name="contact"),
    path("myaccount/",views.myaccount,name= "myaccount"),
    path("find/",views.find,name= "find"),
    path("deep/",views.deep,name= "deep"),
    path("otp/",views.verify_otp_view,name= "verify_otp_view"),
    path("resend_otp/",views.resend_otp,name= "resend_otp"),
    path("user_commands/",views.user_commands,name= "user_commands"),
    path("water/",views.water,name ="water"),

]
