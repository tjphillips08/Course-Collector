from django.urls import path
from . import views

# this like app.use() in express
urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('about/', views.About.as_view(), name="about"),
    path('courses/', views.CourseList.as_view(), name="course_list"),
    path('courses/new/', views.CourseCreate.as_view(), name="course_create"),
    path('courses/<int:pk>/', views.CourseDetail.as_view(), name="course_detail"),
    path('courses/<int:pk>/update',views.CourseUpdate.as_view(), name="course_update"),
    path('courses/<int:pk>/delete',views.CourseDelete.as_view(), name="course_delete"),
    path('courses/<int:pk>/members/new/', views.MemberCreate.as_view(), name="member_create"),
    path('clubs/<int:pk>/members/<int:member_pk>', views.ClubMemberAssoc.as_view(), name="club_member_assoc"),
    path('accounts/signup/', views.Signup.as_view(), name="signup"),
]