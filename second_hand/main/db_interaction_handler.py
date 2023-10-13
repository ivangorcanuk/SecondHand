from .models import Stores, PromotionsRegister
from django.db.models import Q


class DBInteractionHandler:
    def __init__(self):
        self.base_shop = Stores.objects.all()
        self.base_sale = PromotionsRegister.objects.all()
        self.base_non_repeat_sale = PromotionsRegister.objects.filter(discount_type='акция').values_list('general_promotions', flat=True).distinct()

    def get_sale_similar(self, sale):
        return PromotionsRegister.objects.filter(general_promotions=sale)

    def get_shop(self, shop_id):
        return Stores.objects.get(id=shop_id)

    def get_sale_id(self, id_sale):
        return PromotionsRegister.objects.get(id=id_sale)