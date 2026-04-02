import flet as ft
from typing import Any
from app.services.transacciones_api_productos import list_products, update_product, create_product, delete_product
from app.components.popup import show_popup, show_snackbar
from app.components.error import ApiError, api_error_to_text
from app.styles.estilos import Colors, Textos_estilos, Card
from app.views.nuevo_editar import formulario_nuevo_editar_producto

def products_view(page: ft.Page) -> ft.Control:

    def inicio_editar_producto(p: dict[str, Any]):
        async def editar_producto(data: dict):
            try:
                payload = {
                    "name": data.get("name") if data.get("name") else p.get("name"),
                    "quantity": int(data.get("quantity")) if data.get("quantity") is not None else p.get("quantity"),
                    "ingreso_date": data.get("ingreso_date") if data.get("ingreso_date") else p.get("ingreso_date"),
                    "min_stock": int(data.get("min_stock")) if data.get("min_stock") is not None else p.get("min_stock"),
                    "max_stock": int(data.get("max_stock")) if data.get("max_stock") is not None else p.get("max_stock")
                }

                await update_product(p["id"], payload)
                
                close() 
                show_snackbar(page, "Exito: Producto actualizado correctamente")
                
                await actualizar_data() 
                
            except Exception as ex:
                print(f"Error detallado en la vista: {ex}")
                show_snackbar(page, f"Error al actualizar: {str(ex)}")

        dlg, open_, close = formulario_nuevo_editar_producto(
            page, 
            on_submit=editar_producto, 
            initial=p
        )
        open_()

    async def borrar_producto(p: dict[str, Any]):
        try:
            await delete_product(p["id"])
            # Solo dos argumentos: page y el mensaje
            show_snackbar(page, "Éxito: Producto borrado") 
            await actualizar_data()
            
        except Exception as ex:
            print(f"Error al borrar: {ex}")
            show_snackbar(page, f"Error: {str(ex)}")

    def inicio_borrar_producto(p: dict[str, Any]):
        async def tarea():
            await borrar_producto(p)

        page.run_task(tarea)

    async def inicio_nuevo_producto(_e):
        async def crear_nuevo_producto(data: dict):
            try:
                await create_product(data)
                show_snackbar(page, "Éxito: Producto creado")
                await actualizar_data()
            except Exception as ex:
                show_snackbar(page, f"Error: {str(ex)}")

        dlg, open_, close = formulario_nuevo_editar_producto(page, on_submit=crear_nuevo_producto, initial=None)
        open_()

    btn_nuevo = ft.Button("Nuevo producto", icon=ft.Icons.ADD, on_click=inicio_nuevo_producto)

    rows_data: list[dict[str, Any]] = []
    total_text = ft.Text("Total de productos: (cargando...)", style=Textos_estilos.H4)

    columnas = [
        ft.DataColumn(label=ft.Text("Nombre", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Cantidad", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Ingreso", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Min", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Max", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Acciones", style=Textos_estilos.H4)),
    ]

    tabla = ft.DataTable(
        columns=columnas,
        rows=[], 
        width=900,
        heading_row_color=Colors.BG,
        data_row_max_height=60,
    )

    async def actualizar_data():
        nonlocal rows_data
        try:
            data = await list_products(limit=500, offset=0)  
            total_text.value = f"Total de productos: {data.get('total', 0)}"
            rows_data = data.get("items", []) or []
            actualizar_filas()
        except Exception as ex:
            show_snackbar(page, f"Error de carga: {str(ex)}")

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
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    icon_color=ft.Colors.BLUE,
                                    tooltip="Editar producto",
                                    on_click=lambda e, prod=p: inicio_editar_producto(prod)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE, 
                                    tooltip="Borrar", 
                                    on_click=lambda e, p=p: inicio_borrar_producto(p)
                                ),
                            ])
                        ),
                    ]
                )
            )
        tabla.rows = nuevas_filas
        page.update()

    page.run_task(actualizar_data)

    # Construcción final de la UI
    contenido = ft.Column(
        controls=[btn_nuevo, total_text, ft.Container(content=tabla)],
        spacing=30,
        scroll=ft.ScrollMode.AUTO
    )
    
    tarjeta = ft.Container(content=contenido, **Card.tarjeta)
    
    return ft.Container(
        expand=True, 
        alignment=ft.Alignment(0, -1), 
        content=tarjeta
    )