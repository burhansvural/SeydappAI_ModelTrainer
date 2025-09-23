# src/ui/views/chat_view.py
"""
💬 Chat View - AI chat interface
Search results [2] pattern: Component separation[2]
"""

import flet as ft
import asyncio
import threading


def create_chat_view(log_system):
    """Chat view oluşturur"""
    
    # Chat messages list
    chat_messages = []
    messages_listview = None
    selected_model = "bigcode/starcoder2-3b"  # Default model

    def handle_chat_message(e):
        message = e.control.value.strip()
        if message:
            # Add user message
            add_user_message(message)
            log_system.add_event_log(f"💬 User asked: {message}", "CHAT")
            
            # Clear input
            e.control.value = ""
            e.control.update()
            
            # Show typing indicator
            add_ai_message("🤔 Thinking...")
            
            # Start async processing in background
            import threading
            def process_ai_response():
                try:
                    import asyncio
                    
                    # Create new event loop for this thread
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    try:
                        from src.ui.ai_chat_interface import AIChatInterface
                        ai_chat = AIChatInterface(e.page)
                        # Pass selected model to AI chat
                        ai_response = loop.run_until_complete(ai_chat.get_ai_response(message, model=selected_model))
                        
                        # Remove typing indicator and add response
                        def update_ui():
                            if messages_listview and len(messages_listview.controls) > 0:
                                messages_listview.controls.pop()
                            add_ai_message(ai_response)
                        
                        # Schedule UI update on main thread
                        e.page.run_thread(update_ui)
                        
                    finally:
                        loop.close()
                        
                except Exception as ex:
                    # Handle error
                    error_message = str(ex)
                    def update_error():
                        if messages_listview and len(messages_listview.controls) > 0:
                            messages_listview.controls.pop()
                        add_ai_message(f"❌ Sorry, I encountered an error: {error_message}")
                    
                    e.page.run_thread(update_error)
                    log_system.add_event_log(f"❌ Chat error: {ex}", "ERROR")
            
            # Start background thread
            thread = threading.Thread(target=process_ai_response, daemon=True)
            thread.start()

    def add_user_message(message: str):
        """Add user message to chat"""
        if messages_listview:
            user_msg = ft.Container(
                content=ft.Row([
                    ft.Container(expand=True),
                    ft.Container(
                        content=ft.Text(message, size=14, color=ft.Colors.WHITE, selectable=True),
                        padding=15,
                        bgcolor=ft.Colors.PURPLE_600,
                        border_radius=ft.border_radius.only(
                            top_left=15, top_right=15, bottom_left=15, bottom_right=5
                        ),
                        width=600  # Fixed max width
                    )
                ]),
                animate=ft.Animation(300, ft.AnimationCurve.EASE_IN)
            )
            messages_listview.controls.append(user_msg)
            messages_listview.update()

    def add_ai_message(message: str):
        """Add AI message to chat"""
        if messages_listview:
            ai_msg = ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.SMART_TOY, size=20, color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.PURPLE_400,
                        border_radius=15,
                        width=30,
                        height=30,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=ft.Text(message, size=14, color=ft.Colors.WHITE, selectable=True),
                        padding=15,
                        bgcolor=ft.Colors.GREY_700,
                        border_radius=ft.border_radius.only(
                            top_left=5, top_right=15, bottom_left=15, bottom_right=15
                        ),
                        width=600  # Fixed max width
                    )
                ], spacing=10),
                animate=ft.Animation(300, ft.AnimationCurve.EASE_IN)
            )
            messages_listview.controls.append(ai_msg)
            messages_listview.update()

    def send_chat_message(e):
        # Use the chat_input directly since it's in scope
        if chat_input and chat_input.value.strip():
            handle_chat_message(type('Event', (), {'control': chat_input, 'page': e.page})())
        
        log_system.add_event_log("💬 Chat message sent", "CHAT")

    def on_model_change(e):
        """Model seçimi değiştiğinde çağrılır"""
        nonlocal selected_model
        selected_model = e.control.value
        log_system.add_event_log(f"🤖 Model changed to: {selected_model}", "CHAT")
        
        # Model değişikliğini chat'e bildir
        add_ai_message(f"🔄 Model değiştirildi: {selected_model}")

    def show_learning_dashboard(e):
        """Show learning dashboard"""
        try:
            from src.ui.ai_chat_interface import AIChatInterface
            ai_chat = AIChatInterface(e.page)
            dashboard = ai_chat.get_learning_dashboard()
            
            # Create dialog
            dialog = ft.AlertDialog(
                title=ft.Text("🧠 Self-Learning Dashboard"),
                content=dashboard,
                actions=[
                    ft.TextButton("Close", on_click=lambda e: close_dialog(e))
                ],
                modal=True
            )
            
            def close_dialog(e):
                dialog.open = False
                e.page.update()
            
            e.page.dialog = dialog
            dialog.open = True
            e.page.update()
            
        except Exception as ex:
            log_system.add_event_log(f"❌ Learning dashboard error: {ex}", "ERROR")

    # Model seçenekleri
    model_options = [
        ft.dropdown.Option("bigcode/starcoder2-3b", "StarCoder2-3B (Hızlı)"),
        ft.dropdown.Option("bigcode/starcoder2-7b", "StarCoder2-7B (Güçlü)"),
        ft.dropdown.Option("microsoft/DialoGPT-medium", "DialoGPT-Medium"),
        ft.dropdown.Option("microsoft/DialoGPT-large", "DialoGPT-Large"),
        ft.dropdown.Option("gpt2", "GPT-2 (Temel)")
    ]

    return ft.Container(
        key="chat_view",
        content=ft.Column([
       # Header - En üstte sabit
                 ft.Container(
                content=ft.Row([
                    # Başlık
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(name=ft.Icons.SMART_TOY, size=32, color=ft.Colors.PURPLE_400),
                            ft.Text("🤖 AI Assistant Chat", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                        ], spacing=10),
                        expand=True
                    ),
                    # Controls
                    ft.Row([
                        # Learning Dashboard Button
                        ft.IconButton(
                            icon=ft.Icons.PSYCHOLOGY,
                            tooltip="🧠 Self-Learning Dashboard",
                            on_click=show_learning_dashboard,
                            icon_color=ft.Colors.AMBER,
                            bgcolor=ft.Colors.AMBER_100
                        ),
                        # Model Seçici
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Model Seçimi:", size=12, color=ft.Colors.GREY_400),
                                ft.Dropdown(
                                    value=selected_model,
                                    options=model_options,
                                    on_change=on_model_change,
                                    width=200,
                                    bgcolor=ft.Colors.GREY_800,
                                    border_color=ft.Colors.PURPLE_400,
                                    focused_border_color=ft.Colors.PURPLE_300,
                                    text_style=ft.TextStyle(color=ft.Colors.WHITE, size=12)
                                )
                            ], spacing=5)
                        )
                    ], spacing=10)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.only(left=20, right=20, top=20, bottom=10),
                bgcolor=ft.Colors.GREY_900,
                border_radius=ft.border_radius.only(top_left=15, top_right=15)
            ),

            # Chat Area - Kalan alanı kaplar
            ft.Container(
                content=ft.Column([
                    # Messages Area - Expand ile kalan alanı kaplar
                    ft.Container(
                        content=(messages_listview := ft.ListView(
                            expand=True,  # Kalan alanı kaplar
                            spacing=10,
                            padding=15,
                            auto_scroll=True,
                            controls=[
                                ft.Container(
                                    content=ft.Row([
                                        ft.Container(
                                            content=ft.Icon(name=ft.Icons.SMART_TOY, size=20, color=ft.Colors.WHITE),
                                            bgcolor=ft.Colors.PURPLE_400,
                                            border_radius=15,
                                            width=30,
                                            height=30,
                                            alignment=ft.alignment.center
                                        ),
                                        ft.Container(
                                            content=ft.Text(
                                                "🤖 Merhaba! AI asistanınım. Android, Java, Python ve diğer programlama konularında sorularınızı yanıtlayabilirim. Bilgim yoksa internetten araştırıp en güncel bilgileri getiririm!",
                                                size=14, color=ft.Colors.WHITE, selectable=True
                                            ),
                                            padding=15,
                                            bgcolor=ft.Colors.GREY_700,
                                            border_radius=15,
                                            expand=True
                                        )
                                    ], spacing=10)
                                )
                            ]
                        )),
                        bgcolor=ft.Colors.BLACK87,
                        expand=True  # Kalan alanı kaplar
                    ),

                    # Chat Input - Alt kısımda sabit
                    ft.Container(
                        content=ft.Row([
                            (chat_input := ft.TextField(
                                hint_text="Android ListView, Python, Java... herhangi bir programlama sorusu sorun!",
                                border_color=ft.Colors.PURPLE_400,
                                focused_border_color=ft.Colors.PURPLE_300,
                                multiline=True,
                                min_lines=1,
                                max_lines=3,
                                expand=True,
                                on_submit=handle_chat_message
                            )),
                            ft.Container(
                                content=ft.Icon(name=ft.Icons.SEND, size=24, color=ft.Colors.WHITE),
                                bgcolor=ft.Colors.PURPLE_400,
                                border_radius=25,
                                width=50,
                                height=50,
                                alignment=ft.alignment.center,
                                ink=True,
                                on_click=send_chat_message,
                                animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT)
                            )
                        ], spacing=10),
                        padding=15,
                        bgcolor=ft.Colors.GREY_800,
                        border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15)
                    )
                ], spacing=0),
                expand=True,  # Ana container'ın kalan alanını kaplar
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=25,
                    color=ft.Colors.BLACK54,
                    offset=ft.Offset(0, 15)
                )
            )
        ], spacing=0),
        padding=20,
        expand=True  # Tüm ekranı kaplar
    )
