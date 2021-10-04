from django.views import generic
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Shop

longitude = 1
latitude = 1

user_location = Point(longitude, latitude, srid=4326)

class Home(generic.ListView):
    
    def post(self, request, *args, **kwargs):
        try:
            latitude = float(request.POST.get("latitude"))
            longitude = float(request.POST.get("longtitude"))

            user_location = Point(longitude, latitude, srid=4326)
            queryset = Shop.objects.annotate( 
                distance=Distance("location",user_location)
                ).order_by("distance")[0:10]
            context = {'shops':queryset}
            
            return render(request, 'index.html',context)

            
        except:
            return redirect('/')    
        


    model = Shop
    context_object_name = "shops"
    queryset = Shop.objects.annotate(
         distance=Distance("location",user_location)
    ).order_by("distance")[0:10]
    template_name = "index.html"

    


home = Home.as_view()