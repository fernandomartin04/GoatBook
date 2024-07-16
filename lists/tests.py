from django.test import TestCase
from lists.models import Item

# Create your tests here.

class HomePageTest(TestCase) :
    def test_home_page_returns_correct_html(self) :
        # Simulo solicitud GET al servidor en la raíz
        response = self.client.get("/")
        # Verifico si la plantilla usada es la de home.html
        self.assertTemplateUsed(response, "home.html")

    def test_can_save_a_POST_request(self) :
        self.client.post("/", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self) :
        # Simulo una solicitud POST que guardo en la variable respuesta
        response = self.client.post("/", data={"item_text": "A new list item"})
        self.assertRedirects(response, "/lists/the-only-list-in-the-world/")  # Redirecciono la respuesta a la URL raiz

    def test_only_saves_items_when_necessary(self) :
        self.client.get("/")  # Obtengo datos con metodo GET 
        # Me aseguro q como resultado del GET no se guarda ninguna instancia de Item en el servior
        self.assertEqual(Item.objects.count(), 0)  


class ListViewTests(TestCase) :
    def test_uses_list_templates(self) :
        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_all_list_items(self) :
        # Hago en el objeto Item insert del siguiente texto
        Item.objects.create(text="itemey 1")
        Item.objects.create(text="itemey 2")
        response = self.client.get("/lists/the-only-list-in-the-world/")
        # Compruebo con el metodo GET que se han añadido
        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")

class ItemModelTest(TestCase) :
    def test_saving_and_retrieving_items(self) :
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(second_saved_item.text, "Item the second")

