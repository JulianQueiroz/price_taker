from django.core.management.base import BaseCommand
from decimal import Decimal
import requests
from bs4 import BeautifulSoup
from backend.models import Store, Product, History
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help = 'Obtém preços dos produtos da loja e os salva no banco de dados'

    def handle(self, *args, **kwargs):
        url_alimentosbasicos = "https://www.amigao.com/maringa/alimentos-basicos"
        payload = {
            "stateCode": "maringa",
            "loggedIn": "false"
        }

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

        response = requests.get(url_alimentosbasicos, json=payload, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        product_items = soup.find_all('li', class_='product-item')

        # categoria e loja
        category = "alimentos-basicos"
        store, _ = Store.objects.get_or_create(description="Amigao")

        for item in product_items:
            a_tag = item.find('a', class_='product-item-link')
            if a_tag:
                name_product = a_tag.get_text(strip=True)
            else:
                name_product = "Nome não encontrado"

            # ID do produto
            form_tag = item.find('form', attrs={'data-product-sku': True})
            if not form_tag:
                continue 
            sku = form_tag.get('data-product-sku')

            # preços
            special_price_tag = item.find('span', class_='special-price')
            if special_price_tag:
                special_price_str = special_price_tag.find('span', class_='price').get_text(strip=True)
                special_price = Decimal(special_price_str.replace("R$", "").replace(",", ".").strip())
            else:
                special_price = None

            old_price_tag = item.find('span', class_='old-price')
            if old_price_tag:
                old_price_str = old_price_tag.find('span', class_='price').get_text(strip=True)
                old_price = Decimal(old_price_str.replace("R$", "").replace(",", ".").strip())
            else:
                old_price = None

            final_price_tag = item.find('span', class_='price-wrapper')
            if final_price_tag:
                final_price_str = final_price_tag.find('span', class_='price').get_text(strip=True)
                final_price = Decimal(final_price_str.replace("R$", "").replace(",", ".").strip())
            else:
                final_price = None

            # lógica de preços
            if special_price:
                default_price = old_price 
                offer_price = special_price 
                offer = True 
            else:
                default_price = final_price if final_price else old_price 
                offer_price = None  
                offer = False 

            try:
                product, created = Product.objects.get_or_create(
                    id=sku,
                    defaults={
                        "description": name_product,
                        "store": store,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Produto criado --> {name_product} (SKU: {sku})"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Produto já existe: {name_product} (SKU: {sku})"))
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f"Erro ao criar produto: {e}"))
                continue

            # Criar histórico para o produto
            History.objects.create(
                default_price=default_price,
                offer_price=offer_price,
                offer=offer,
                category=category,
            )
        
        self.stdout.write(self.style.SUCCESS('Preços dos produtos atualizados com sucesso!'))
