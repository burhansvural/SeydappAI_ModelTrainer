# src/ui/views/models_view.py
"""
🧠 Models View - Model management
"""

import flet as ft


def create_models_view(log_system):
    """Models view oluşturur"""

    def load_model(e):
        log_system.add_event_log("🧠 Loading StarCoder2-3B base model...", "SYSTEM")

    def apply_lora(e):
        log_system.add_event_log("🎯 Applying LoRA adapter...", "SYSTEM")

    return ft.Container(
        key="models_view",
        content=ft.Column([
            ft.Text("🧠 Model Management", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Container(height=20),
            ft.Text("StarCoder2-3B checkpoint management", color=ft.Colors.GREY_400),
            ft.Container(height=30),

            # Model cards
            ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Icon(name=ft.Icons.PSYCHOLOGY, size=48, color=ft.Colors.PURPLE_400),
                        ft.Text("StarCoder2-3B", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text("Base Model", size=12, color=ft.Colors.GREY_400),
                        ft.Container(height=10),
                        ft.ElevatedButton("Load Model", bgcolor=ft.Colors.PURPLE_600, color=ft.Colors.WHITE,
                                          on_click=load_model)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=30,
                    width=250,
                    bgcolor=ft.Colors.GREY_900,
                    border_radius=15
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Icon(name=ft.Icons.TUNE, size=48, color=ft.Colors.GREEN_400),
                        ft.Text("LoRA Adapter", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text("Fine-tuned", size=12, color=ft.Colors.GREY_400),
                        ft.Container(height=10),
                        ft.ElevatedButton("Apply LoRA", bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE,
                                          on_click=apply_lora)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=30,
                    width=250,
                    bgcolor=ft.Colors.GREY_900,
                    border_radius=15
                )
            ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
        padding=50,
        expand=True
    )
