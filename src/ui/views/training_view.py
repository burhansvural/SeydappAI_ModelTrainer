# src/ui/views/training_view.py
"""
🚀 Training View - Ana dashboard
Search results [1] pattern: View as top container[1]
"""

import flet as ft


def create_training_view(log_system, dashboard_cards, control_panel):
    """Training view oluşturur - Search results [2] reusable component pattern[2]"""

    return ft.Container(
        key="training_view",
        content=ft.ListView([
            # Header section
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(name=ft.Icons.AUTO_AWESOME, size=45, color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.PURPLE_400,
                        border_radius=50,
                        width=80,
                        height=80,
                        alignment=ft.alignment.center,
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=20,
                            color=ft.Colors.PURPLE_400,
                            offset=ft.Offset(0, 0)
                        )
                    ),
                    ft.Container(width=20),
                    ft.Column([
                        ft.Text("SeydappAI ModelTrainer", size=32, weight=ft.FontWeight.W_900, color=ft.Colors.WHITE),
                        ft.Text("🚀 Next-Gen AI Training Platform", size=16, color=ft.Colors.GREY_300, italic=True),
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(name=ft.Icons.MEMORY, size=16, color=ft.Colors.CYAN_400),
                                ft.Text("RTX 3060", size=12, color=ft.Colors.CYAN_400),
                                ft.VerticalDivider(width=1, color=ft.Colors.GREY_600),
                                ft.Icon(name=ft.Icons.FLASH_ON, size=16, color=ft.Colors.YELLOW_400),
                                ft.Text("CUDA 12.9", size=12, color=ft.Colors.YELLOW_400),
                                ft.VerticalDivider(width=1, color=ft.Colors.GREY_600),
                                ft.Icon(name=ft.Icons.PSYCHOLOGY, size=16, color=ft.Colors.PURPLE_400),
                                ft.Text("StarCoder2-3b", size=12, color=ft.Colors.PURPLE_400)
                            ], spacing=8),
                            padding=ft.padding.symmetric(vertical=8, horizontal=15),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                            border_radius=20
                        )
                    ], spacing=8)
                ], alignment=ft.MainAxisAlignment.START),
                padding=30,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=[ft.Colors.PURPLE_900, ft.Colors.INDIGO_900, ft.Colors.BLUE_900]
                ),
                border_radius=20,
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=30,
                    color=ft.Colors.BLACK38,
                    offset=ft.Offset(0, 10)
                )
            ),

            ft.Container(height=30),

            # Dashboard cards
            dashboard_cards.get_cards(),

            ft.Container(height=25),

            # Control panel
            control_panel.get_controls(),

            ft.Container(height=30),

            # Log viewer
            log_system.get_log_container()

        ], spacing=0, padding=ft.padding.only(left=20, top=20, bottom=20, right=40)),  # ✅ ListView padding çalışır[2]
        expand=True
    )
