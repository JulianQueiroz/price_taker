from django.core.management.base import BaseCommand
from decimal import Decimal
import requests
from bs4 import BeautifulSoup
from backend.models import Store, Product, History
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help = 'Obtém preços dos produtos da loja e os salva no banco de dados'

    def get_price(self, price_tag):
        # converte o preço de string pra decimal
        if price_tag:
            price_str = price_tag.find('span', class_='price').get_text(strip=True)
            if price_str:
                try:
                    return Decimal(price_str.replace("R$", "").replace(",", ".").strip())
                except (ValueError, TypeError):
                    return None
        return None

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

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f"Falha na requisição: {response.status_code}"))
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        product_items = soup.find_all('li', class_='product-item')

        if not product_items:
            self.stdout.write(self.style.WARNING("Nenhum produto encontrado na página."))
            return

        # categoria e loja
        category = "alimentos-basicos"
        store, _ = Store.objects.get_or_create(description="Amigao")

        for item in product_items:
            a_tag = item.find('a', class_='product-item-link')
            name_product = a_tag.get_text(strip=True) if a_tag else "Nome não encontrado"

            form_tag = item.find('form', attrs={'data-product-sku': True})
            if not form_tag:
                continue
            sku = form_tag.get('data-product-sku')

            # extração de preços
            special_price = self.get_price(item.find('span', class_='special-price'))
            old_price = self.get_price(item.find('span', class_='old-price'))
            final_price = self.get_price(item.find('span', class_='price-wrapper'))

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
                # verifica se o produto ja existe 
                product, created = Product.objects.get_or_create(
                    id=sku,
                    defaults={"description": name_product, "store": store}
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Produto criado --> {name_product} (SKU: {sku})"))
                else:
                    # atualiza o produto se necessario
                    product.description = name_product
                    product.store = store
                    product.save()
                    self.stdout.write(self.style.SUCCESS(f"Produto atualizado --> {name_product} (SKU: {sku})"))

            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f"Erro ao criar ou atualizar produto: {e}"))
                continue

            # save
            History.objects.create(
                default_price=default_price,
                offer_price=offer_price,
                offer=offer,
                category=category,
            )

        self.stdout.write(self.style.SUCCESS('Preços dos produtos atualizados com sucesso!'))
