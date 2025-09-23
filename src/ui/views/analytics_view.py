# src/ui/views/analytics_view.py
"""
📊 Analytics View - Metrics dashboard
"""

import flet as ft


def create_analytics_view(log_system):
    """Analytics view oluşturur"""

    return ft.Container(
        key="analytics_view",
        content=ft.Column([
            ft.Text("📊 Analytics Dashboard", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Container(height=20),
            ft.Text("Training metrics and performance analysis", color=ft.Colors.GREY_400),
            ft.Container(height=30),

            # Analytics cards
            ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Text("Training Sessions", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text("12", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400),
                        ft.Text("Total completed", size=12, color=ft.Colors.GREY_400)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20,
                    width=200,
                    bgcolor=ft.Colors.GREY_900,
                    border_radius=15
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Average Loss", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text("0.234", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                        ft.Text("Lower is better", size=12, color=ft.Colors.GREY_400)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20,
                    width=200,
                    bgcolor=ft.Colors.GREY_900,
                    border_radius=15
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Training Time", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text("4.2h", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_400),
                        ft.Text("Total elapsed", size=12, color=ft.Colors.GREY_400)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20,
                    width=200,
                    bgcolor=ft.Colors.GREY_900,
                    border_radius=15
                )
            ], spacing=20, alignment=ft.MainAxisAlignment.CENTER),

            ft.Container(height=30),
            ft.ProgressRing(width=100, height=100, value=0.75, color=ft.Colors.BLUE_400),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
        padding=50,
        expand=True
    )
