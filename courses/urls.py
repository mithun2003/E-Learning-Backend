from django.urls import path
from .views import *
from django.urls import path

urlpatterns = [

    path('category-create', CreateCategory.as_view()),
    path('category-list', ViewCategory.as_view()),
    path('category/publish/<id>', PublishCategory.as_view()),
    path('category/delete/<id>', DeleteCategory.as_view()),
    path('category-wise/list/<cat_id>', ViewCourseCategoryWise.as_view()),
    path('category/<cat_id>', ViewOneCategory.as_view()),

    path('publish/<id>', PublishCourse.as_view()),
    path('course-create', CourseCreate.as_view()),
    path('course-list', ViewCourse.as_view()),
    path('user/course-list', UserCourseView.as_view()),
    path('course-detail/<id>', ViewOneCourse.as_view()),
    path('admin/course-detail/<id>', AdminViewOneCourse.as_view()),
    path('course-delete/<id>', DeleteCourse.as_view()),
    path('course-edit/<id>', CourseUpdate.as_view()),
    path('teacher/course-list/<id>', TeacherViewCourse.as_view()),

    path('chapter-add', CreateChapter.as_view()),
    path('chapter-delete/<id>', DeleteChapter.as_view()),
    path('<int:course_id>/chapter-list/', ViewAllChapter.as_view()),
    path('admin/<int:course_id>/chapter-list/', ViewAllChapterAdmin.as_view()),
    path('chapter/<chapter_id>', ViewOneChapter.as_view()),
    path('chapters/<int:chapter_id>/complete/', Progress.as_view(), name='complete-video'),

    path('enroll/<course_id>', Enroll.as_view()),
    path('enroll/check/<course_id>', CheckEnroll.as_view()),

    path('unenroll/<course_id>', Unenroll.as_view()),

    path('enrollment/<course_id>', ViewEnrolled.as_view()),
    path('enrollment/user/<user_id>', CourseEnrolled.as_view()),
    path('enrollment/course/<course_id>', EnrolledStudents.as_view()),

    path('wishlist/', WishlistView.as_view()),
    path('wishlist/get/<course_id>', WishlistView.as_view()),
    path('wishlist/remove/<id>', WishlistView.as_view()),
    path('wishlist-list-all/', WishlistAll.as_view()),

    path('<course_id>/reviews/', Review.as_view()),

    path('category-view/<cat_id>', Course_By_Category.as_view()),
    
    
    path('search/<query>', Search.as_view()),
    

]




