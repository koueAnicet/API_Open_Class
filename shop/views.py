from django.shortcuts import render, redirect

from django.views.generic import View
from shop import models



       
class CategoryView(View):
    form = models.Category
    def get(self, request):
        form = self.form()
        return render(request, locals)
    
class ProductView(View):
    form = models.Product
    def get(self, request):
        form = self.form()
        return render(request, locals)
    
class ArticleView(View):
    form = models.Article
    def get(self, request):
        form = self.form()
        return render(request, locals)
    
    
