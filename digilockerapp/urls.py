from django.urls import path
from .views import *

urlpatterns = [
    path('',landingpageview,name = "landingpage"),
    path('login/',loginpageview,name = "loginpage"),
    path('authenticate/',authenticateuser),
    path('signup/',signupview,name = "signuppage"),
    path('signup/save/',signup,name = "signup"),
    path('homepage/',homepageview,name = "homepage"),
    path('logout/',logoutuser,name = "logout"),
    path('document/add/',adddocumentview,name = "adddocumentpage"),
    path('document/add/save/',adddocument,name = "adddocument"),
    path('document/delete/<int:id>/',deletedocument)

    # path('login/',loginpageview,name = "loginpage"),




]