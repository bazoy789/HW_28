
import json

from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from users.models import User, Location


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        try:
            user = self.get_object()
        except:
            return JsonResponse({"error": "Not found"})
        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "password": user.password,
            "role": user.role,
            "age": user.age,
            "location": [loc.name for loc in user.location.all()]
        })


class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = []
        for user in self.object_list.annotate(total_ad=Count("ad", filter=Q(ad__is_published=True))):
            response.append(
                {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "role": user.role,
                    "age": user.age,
                    "location": [loc.name for loc in user.location.all()],
                    "total_ad": user.total_ad
                }
            )
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        locations = data.pop("locations")
        user = User.objects.create(**data)
        for loc_name in locations:
            loc, _ = Location.objects.get_or_create(name=loc_name)

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "location": [loc.name for loc in user.location.all()]
        })


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = "__all__"

    def patch(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        data = json.loads(request.body)
        if "first_name" in data:
            self.object.name = data.get("first_name")
        if "last_name" in data:
            self.object.author_id = data.get("last_name")
        if "username" in data:
            self.object.price = data.get("username")
        if "role" in data:
            self.object.description = data.get("role")
        if "age" in data:
            self.object.is_published = data.get("age")
        if "locations" in data:
            self.object.location.clear()
            for loc_name in data.get("locations"):
                loc, _ = Location.objects.get_or_create(name=loc_name)
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "role": self.object.role,
            "age": self.object.age,
            "location": [loc.name for loc in self.object.location.all()]
        })


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        data = self.get_object()
        super().delete(request, *args, **kwargs)
        return JsonResponse({"id": data.id})
