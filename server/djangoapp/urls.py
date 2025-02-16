from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    path(route='dealerships/', view=views.get_dealership_list, name='dealerships'),
    path(route='', view=views.get_dealerships, name='index'),
    # path for about view
    # path(route='about/',view=AboutPageView.as_view(), name='about'),
    path(route='about/',view=views.about, name='about'),
    # path for contact us view
    # path(route='contact/',view=ContactPageView.as_view(), name='contact'),
    path(route='contact/',view=views.contact, name='contact'),
    # path for home view
    path(route='index/', view=views.get_dealerships, name='index'),
    # path for registration
    path(route='registration/', view=views.registration_request, name='registration'),
    # path for login
    path(route='login/', view=views.login_request, name='login'),
    # path for logout
    path(route='logout/', view=views.logout_request, name='logout'),
    # path for dealer reviews view
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),
    # path for add a review view
    path('addreviewdealer/<int:dealer_id>/', views.add_review, name='add_dealer_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)