import flet as ft
from app.views.mostrar_productos import products_view

def main(page:ft.Page):
    page.title="Aplicacion con estilos"
    page.scroll=ft.ScrollMode.ADAPTIVE
    page.add(products_view(page))

if __name__=="__main__":
    ft.app(target=main)