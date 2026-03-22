import flet as ft

class Colors:
    BG = "blue"
    DANGER = "red"

class Textos_estilos:
    H4 = ft.TextStyle(size=20, weight="bold")

class Card:
    tarjeta = {
        "bgcolor": "#1e1e1e",
        "padding": 20,
        "border_radius": 15,
        "shadow": ft.BoxShadow(blur_radius=10, color="black"),
    }