import flet as ft
from typing import Any
from app.services.transacciones_api_productos import list_products 
from app.styles.estilos import Colors, Textos_estilos

def products_view(page: ft.Page) -> ft.Control:
    try:
        response = list_products() 
        productos = response.get("items", [])
    except Exception as e:
        print(f"Error al traer datos: {e}")
        productos = []

    columnas = [
        ft.DataColumn(label=ft.Text("Nombre", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Cantidad", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Ingreso", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Min", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Max", style=Textos_estilos.H4))
    ]

    data = []
    for p in productos:
        data.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(p.get("name", "N/A"))),
                    ft.DataCell(ft.Text(str(p.get("quantity", 0)))),
                    ft.DataCell(ft.Text(p.get("ingreso_date", ""))),
                    ft.DataCell(ft.Text(str(p.get("min_stock", 0)))),
                    ft.DataCell(ft.Text(str(p.get("max_stock", 0)))),
                ]
            )
        )

    if not data:
        data.append(ft.DataRow(cells=[ft.DataCell(ft.Text("No hay datos disponibles")) for _ in columnas]))

    tabla = ft.DataTable(
        columns=columnas,
        rows=data,
        width=900,
        heading_row_height=60,
        heading_row_color=Colors.BG,
        data_row_max_height=60,
        data_row_min_height=48
    )

    return tabla