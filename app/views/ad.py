
import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from app.models import Ad, Category
from users.models import User


class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("-price")

        paginator = Paginator(self.object_list, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        total = page_obj.paginator.count
        num_page = page_obj.paginator.num_pages
        response = []
        data = {"total": total, "num_pages": num_page, "item": response}
        for ad in page_obj:
            response.append(
                {
                    "id": ad.id,
                    "name": ad.name,
                    "author": ad.author_id.username,
                    "price": ad.price,
                    "description": ad.description,
                    "is_published": ad.is_published,
                    "category": ad.category_id.name,
                    "image": ad.image.url if ad.image else None
                }
            )

        return JsonResponse(data, safe=False)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except:
            return JsonResponse({"error": "Not found"})
        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author_id.username,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category": ad.category_id.name,
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        author = get_object_or_404(User, pk=data.pop("author_id"))
        category = get_object_or_404(Category, pk=data.pop("category_id"))

        # ad = Ad.objects.create(
        #     name=data.get("name"),
        #     author_id=author,
        #     price=data.get("price"),
        #     description=data.get("description"),
        #     is_published=data.get("is_published"),
        #     category_id=category,
        # )

        ad = Ad.objects.create(
            author_id=author,
            category_id=category,
            **data
        )

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author_id.username,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category": ad.category_id.name,
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ad
    fields = "__all__"

    def patch(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        data = json.loads(request.body)
        if "name" in data:
            self.object.name = data.get("name")
        if "author_id" in data:
            author = get_object_or_404(User, pk=data.get("author_id"))
            self.object.author_id = author
        if "price" in data:
            self.object.price = data.get("price")
        if "description" in data:
            self.object.description = data.get("description")
        if "is_published" in data:
            self.object.is_published = data.get("is_published")
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author_id.username,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category": self.object.category_id.name,
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        data = self.get_object()
        super().delete(request, *args, **kwargs)
        return JsonResponse({"id": data.id})


@method_decorator(csrf_exempt, name="dispatch")
class AdImageView(UpdateView):
    model = Ad
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get("image")
        self.object.save()

        return JsonResponse({"id": self.object.id,
                             "image": self.object.image.url})
