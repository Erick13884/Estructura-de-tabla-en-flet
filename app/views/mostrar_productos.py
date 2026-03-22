import flet as ft
from typing import Any
from app.services.transacciones_api_productos import list_products, get_product, create_product, update_product, delete_product
from app.components.popup import show_popup, show_popup_auto_close, show_snackbar, confirm_dialog
from app.components.error import ApiError, api_error_to_text
from app.styles.estilos import Colors, Textos_estilos

def products_view(page: ft.Page) -> ft.Control:
    rows_data: list[dict[str, Any]] = []
    total_items = 0
    total_text = ft.Text("Total de productos: (cargando...)", style=Textos_estilos.H4)
    btn_nuevo = ft.ElevatedButton("Nuevo Registro", icon=ft.Icons.ADD, on_click=lambda _: print("Nuevo click"))

    # Encabezados
    columnas = [
        ft.DataColumn(label=ft.Text("Nombre", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Cantidad", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Ingreso", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Min", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Max", style=Textos_estilos.H4)),
    ]

    # Se crea la tabla con los encabezados(columnas) y los datos de prueba(data)
    tabla = ft.DataTable(
        columns=columnas,
        rows=[], 
        width=900,
        heading_row_height=60,
        heading_row_color=Colors.BG,
        data_row_max_height=60,
        data_row_min_height=48
    )

    async def actualizar_data():
        nonlocal rows_data, total_items
        try:
            data = list_products(limit=500, offset=0)  
            total_items = int(data.get("total", 0))
            total_text.value = f"Total de productos: {total_items}"
            rows_data = data.get("items", []) or []
            actualizar_filas()
        except Exception as ex:
            await show_snackbar(page, "Error", str(ex), bgcolor=Colors.DANGER)

    def actualizar_filas():
        nuevas_filas = []
        for p in rows_data:
            nuevas_filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(p.get("name", ""))),
                        ft.DataCell(ft.Text(str(p.get("quantity", "")))),
                        ft.DataCell(ft.Text(p.get("ingreso_date", "") or "")),
                        ft.DataCell(ft.Text(str(p.get("min_stock", "")))),
                        ft.DataCell(ft.Text(str(p.get("max_stock", "")))),
                    ]
                )
            )
        tabla.rows = nuevas_filas
        page.update()

    page.run_task(actualizar_data)

    contenido = ft.Column(
        spacing=30,
        scroll=ft.ScrollMode.AUTO,
        controls=[btn_nuevo, total_text, ft.Container(content=tabla)]
    )

    return contenido