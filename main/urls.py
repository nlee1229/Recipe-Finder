from django.urls import path
from . import views

from recipe_finder import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [

	# ************************************************************** ADMIN

	path('admin', views.admin),
	path('edit/<id>', views.edit),
	path('edit_proc/<id>', views.edit_proc),
	path('input', views.inputinformation),
	path('process_recipe', views.add_recipe),
	path('recipe_profile/<id>', views.recipe_profile),
	path('process_ingredient/<id>', views.add_ingredient),
	path('addimg/<id>', views.add_image),
	path('delimg/<id>/<recipe_id>', views.del_image),
	path('del/<id>', views.del_ing),
	path('del_rec/<id>', views.del_recipe),
	path('del_ing/<ing_id>/<recipe_id>', views.del_ingredient),

	# ************************************************************** USER
	
	path('searching', views.searching),
	path('clearsearching', views.clearsearching),
	path('search', views.search),
	path('clear', views.clearsearch),
	path('account_user', views.account_user),
	path('home', views.home),
	path('list_ingredients', views.list_ingredients),
	path('process_ing', views.process_ing),
	path('recipeinfo/<id>', views.recipeinfo),
	path('fav/<recipe_id>', views.addfav),
	path('unfav/<recipe_id>', views.removefav),
	path('addfavfromrecipe/<recipe_id>', views.addfavfromrecipe),

]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)