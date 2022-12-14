from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ReadOnlyModelViewSet,ModelViewSet

from shop.models import Article, Category, Product
from shop.serializers import CategoryDetailSerialiser,CategoryListSerializer, ArticleSerializer,ProductDetailSerializer,ProductListSerializer

class MultipleSerializerMixin:
    # Un mixin est une classe qui ne fonctionne pas de façon autonome
    # Elle permet d'ajouter des fonctionnalités aux classes qui les étendent
    detail_serializer_class = None

    def get_serializer_class(self):
        # Notre mixin détermine quel serializer à utiliser
        # même si elle ne sait pas ce que c'est ni comment l'utiliser
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
             # Si l'action demandée est le détail alors nous retournons le serializer de détail
            return self.detail_serializer_class
        return super().get_serializer_class()

#endpoint d’administration
class AdminCategoryViewset(MultipleSerializerMixin, ModelViewSet):
     
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerialiser
 
    def get_queryset(self):
        return Category.objects.all()
    
    
class AdminProductViewset(MultipleSerializerMixin, ModelViewSet):
    
    serializer_class=ProductListSerializer
    detail_serializer_class=ProductDetailSerializer
    
    def get_queryset(self):
        return Product.objects.all()
    
    
class AdminArticleViewset(MultipleSerializerMixin, ModelViewSet):
    
    serializer_class=ArticleSerializer
    #detail_serializer_class=ArticleDetailSerializer
    queryset = Article.objects.all()
        


class CategoryViewset(MultipleSerializerMixin,ReadOnlyModelViewSet):
    
    serializer_class=CategoryListSerializer
    detail_serializer_class=CategoryDetailSerialiser
    
    def get_queryset(self):
        return Category.objects.filter(active=True)

    
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        # Nous pouvons maintenant simplement appeler la méthode disable
        self.get_object().disable()
        return Response()
    
    def get_serializer_class(self):
        #si l'action  est detail:retrieve
        if self.action == 'retrieve':
            return self.detail_serializer_class
        #par default return serializer_class
        return super().get_serializer_class()
    

class ProductViewset(MultipleSerializerMixin,ReadOnlyModelViewSet):
    
    serializer_class = ProductListSerializer
    detail_serializer_class = ProductDetailSerializer

    
    def get_queryset(self):
        # Nous récupérons tous les produits dans une variable nommée queryset
        queryset = Product.objects.filter(active=True)
        # Vérifions la présence du paramètre ‘category_id’ dans l’url et si oui alors appliquons notre filtre
        category_id = self.request.GET.get('category_id')
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset

    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()

class ArticleViewset(ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer
    
    def get_queryset(self):
        queryset =  Article.objects.filter(active=True)
        product_id = self.request.GET.get('product_id')
        
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset
    
       
# class CategoryAPIView(APIView):
    
#     def get(self, *args, **kwargs):
#         #queryset
#         categories = Category.objects.all()
#         serializer= CategorySerialiser(categories, many=True)#many: pour qu'il puisse generer pusieur
#         return Response(serializer.data)


# class ProductAPIView(APIView):
    
#     def get(self, *args, **kwargs):
#         #queriset
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data) 
    

# class ArticleAPIView(APIView):
#      def get(self, *args, **kwargs):
#         #queriset
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)