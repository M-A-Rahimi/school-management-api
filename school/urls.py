from django.urls import path
from .views import SchoolListCreateView,SchoolUpdateView,SchoolDetailListView,ClassRoomCreateView,\
    ListLessonTeacherView,ClassRoomUpdateView,SchoolClassRoomView

urlpatterns = [    
    path("list-create/",SchoolListCreateView.as_view(),name = "school_list_create"),
    path("update/<int:pk>/",SchoolUpdateView.as_view(),name = "school_update"),
    path("detail/<int:id>/",SchoolDetailListView.as_view(),name = "school_detail"),
    path("create-class-room/",ClassRoomCreateView.as_view(),name = "school_create"),
    path("list-lesson-teacher/",ListLessonTeacherView.as_view(),name = "lesson_teacher"),
    path("update-class-room/<int:pk>/",ClassRoomUpdateView.as_view(),name = "lesson_teacher"),
    path("class-rooms/<int:id>/",SchoolClassRoomView.as_view(),name = "school_class_room"),
]
    
