
import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from app.models import Category


@method_decorator(csrf_exempt, name="dispatch")
class CategoryCreateView(CreateView):
    model = Category
    fields = "__all__"

    @staticmethod
    def post(request, *args, **kwargs):
        data = json.loads(request.body)
        new_cats = Category.objects.create(**data)
        return JsonResponse({"id": new_cats.id, "name": new_cats.name})


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        try:
            cats = self.get_object()
        except:
            return JsonResponse({"error": "Not found"})
        return JsonResponse({"id": cats.id, "name": cats.name})


class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return JsonResponse([{"id": cats.id,
                              "name": cats.name} for cats in self.object_list.order_by("name")], safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Category
    fields = "__all__"

    def patch(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.name = data.get("name")
        self.object.save()
        return JsonResponse({"id": self.object.id, "name": self.object.name}, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        data = self.get_object()
        super().delete(request, *args, **kwargs)
        return JsonResponse({"id": data.id})
