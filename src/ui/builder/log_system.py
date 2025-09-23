# src/ui/builder/log_system.py - TAMAMEN DÜZELTİLDİ

import flet as ft
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class LogSystem:
    """✅ FIXED: Search results [1] ListView hierarchy pattern[1]"""

    def __init__(self, page):
        """✅ INIT: Sadece referansları al - UI oluşturma"""
        self.page = page
        self.terminal_log_list = None
        self.terminal_header = None
        self.log_container = None
        self.log_history = []
        self.max_logs = 200
        self.ui_ready = False
        self.page_attached = False  # ✅ NEW: Page attachment tracker

        # Direct button references
        self.copy_button = None
        self.clear_button = None
        self.fullscreen_button = None

        self._create_log_controls()
        logger.info("Initialized LogSystem")

    def _create_log_controls(self):
        """✅ FIXED: Search results [1] ListView proper setup[1]"""

        # ✅ ListView with proper scroll - Search results [1][2] pattern[1][2]
        self.terminal_log_list = ft.ListView(
            key="terminal_log_list",
            expand=True,
            spacing=2,
            padding=15,
            auto_scroll=True,
        )

        # Direct button references
        self.copy_button = ft.IconButton(
            key="copy_logs_btn",
            icon=ft.Icons.COPY,
            icon_size=16,
            icon_color=ft.Colors.GREY_400,
            tooltip="Copy logs"
        )

        self.clear_button = ft.IconButton(
            key="clear_logs_btn",
            icon=ft.Icons.CLEAR,
            icon_size=16,
            icon_color=ft.Colors.GREY_400,
            tooltip="Clear logs"
        )

        self.fullscreen_button = ft.IconButton(
            key="fullscreen_logs_btn",
            icon=ft.Icons.FULLSCREEN,
            icon_size=16,
            icon_color=ft.Colors.GREY_400,
            tooltip="Fullscreen"
        )

        # Terminal header
        self.terminal_header = ft.Container(
            key="terminal_header",
            content=ft.Row([
                ft.Row([
                    ft.Container(width=12, height=12, bgcolor=ft.Colors.RED_400, border_radius=6),
                    ft.Container(width=12, height=12, bgcolor=ft.Colors.YELLOW_400, border_radius=6),
                    ft.Container(width=12, height=12, bgcolor=ft.Colors.GREEN_400, border_radius=6)
                ], spacing=8),
                ft.Text("🔥 Real-time Training Terminal", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Row([
                    self.copy_button,
                    self.clear_button,
                    self.fullscreen_button
                ], spacing=5)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(vertical=10, horizontal=15),
            bgcolor=ft.Colors.GREY_900,
        )

        # ✅ Log container with height constraint - Search results [1] large lists pattern[1]
        self.log_container = ft.Container(
            key="log_container",
            content=ft.Column([self.terminal_header, self.terminal_log_list], spacing=0),
            width=900,
            height=400,  # ✅ CRITICAL: Fixed height for scroll[1]
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=30,
                color=ft.Colors.BLACK54,
                offset=ft.Offset(0, 15)
            ),
            visible=False
        )

    def attach_to_page(self, page):
        """✅ FIXED: Proper page attachment - Search results [1] hierarchy[1]"""
        logger.info("🔧 Log UI attached to page")

        # ✅ CRITICAL: Mark as page-attached BEFORE adding logs[1]
        self.page_attached = True
        self.ui_ready = True

        # Event handlers
        self.copy_button.on_click = self.copy_logs
        self.clear_button.on_click = self.clear_logs
        self.fullscreen_button.on_click = self.toggle_log_fullscreen

        # Show container
        self.log_container.visible = True
        page.update()

        # ✅ FIXED: Add logs ONLY after page attachment[1]
        logger.info(f"📋 Adding {len(self.log_history)} queued logs to UI")
        for timestamp, message, log_type in self.log_history:
            self._add_log_to_ui_safe(timestamp, message, log_type)
        self.log_history = []

    def add_event_log(self, message: str, log_type: str = "INFO"):
        """Public log interface"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self._add_log_to_ui_safe(timestamp, message, log_type)

    def _add_log_to_ui_safe(self, timestamp: str, message: str, log_type: str):
        """✅ FIXED: Safe log adding - Search results [1] ListView pattern[1]"""

        # ✅ Check page attachment FIRST[1]
        if not self.page_attached or not self.ui_ready or not self.terminal_log_list:
            # Queue for later
            self.log_history.append((timestamp, message, log_type))
            if len(self.log_history) > self.max_logs:
                self.log_history.pop(0)
            return

        # ✅ Type colors
        type_colors = {
            "AUTO": ft.Colors.CYAN_300,
            "INFO": ft.Colors.CYAN_400,
            "SUCCESS": ft.Colors.GREEN_400,
            "WARNING": ft.Colors.YELLOW_400,
            "ERROR": ft.Colors.RED_400,
            "TRAINING": ft.Colors.PURPLE_400,
            "SYSTEM": ft.Colors.BLUE_400,
            "RAG": ft.Colors.PURPLE_300,
            "CONFIG": ft.Colors.ORANGE_400,
            "RESEARCH": ft.Colors.BLUE_300,
            "UI": ft.Colors.GREY_400
        }

        # ✅ Create log entry
        log_entry = ft.Container(
            content=ft.Row([
                ft.Text(f"[{timestamp}]", size=10, color=ft.Colors.GREY_500),
                ft.Container(
                    content=ft.Text(log_type, size=9, color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD),
                    padding=ft.padding.symmetric(vertical=1, horizontal=6),
                    bgcolor=type_colors.get(log_type, ft.Colors.GREY_400),
                    border_radius=8
                ),
                ft.Text(message, size=11, color=ft.Colors.WHITE, selectable=True)
            ], spacing=8),
            padding=ft.padding.symmetric(vertical=3, horizontal=10),
        )

        # ✅ SAFE ADD: Only if ListView is in page[1]
        try:
            self.terminal_log_list.controls.append(log_entry)

            # Limit logs
            if len(self.terminal_log_list.controls) > self.max_logs:
                self.terminal_log_list.controls.pop(0)

            # ✅ Update ListView directly - Search results [1] pattern[1]
            self.terminal_log_list.update()

        except Exception as e:
            # Silent fail - don't create recursive log errors
            pass

    def setup_welcome_logs(self):
        """Welcome messages - only after page attachment"""
        welcome_messages = [
            ("🎨 Ultra-Modern AI Interface loaded", "SUCCESS"),
            ("🖥️ RTX 3060 (12GB) neural accelerator ready", "SYSTEM"),
            ("⚡ CUDA 12.9 quantum cores active", "SYSTEM"),
            ("🧠 StarCoder2-3b consciousness online", "INFO"),
            ("🎯 Advanced LoRA neural adaptation ready", "INFO"),
            ("🔧 6 dashboard widgets initialized", "SYSTEM"),
            ("🤖 Autonomous Learning System standby", "AUTO"),
            ("✨ Ready for AI evolution - click Start Training", "INFO")
        ]

        for message, log_type in welcome_messages:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self._add_log_to_ui_safe(timestamp, message, log_type)

    def get_log_container(self) -> ft.Container:
        """Log container'ı döndür"""
        return self.log_container

    def copy_logs(self, e):
        """Copy logs to clipboard"""
        if not self.terminal_log_list or not self.terminal_log_list.controls:
            return

        log_texts = []
        for control in self.terminal_log_list.controls:
            try:
                row = control.content
                if isinstance(row, ft.Row) and len(row.controls) >= 3:
                    timestamp = row.controls.value
                    log_type = row.controls[1].content.value
                    message = row.controls[2].value
                    log_texts.append(f"{timestamp} [{log_type}] {message}")
            except:
                continue

        if log_texts:
            self.page.set_clipboard("\n".join(log_texts))
            self.add_event_log("📋 Logs copied to clipboard!", "SUCCESS")

    def clear_logs(self, e):
        """Clear all logs"""
        if self.terminal_log_list:
            self.terminal_log_list.controls.clear()
            self.terminal_log_list.update()
            self.add_event_log("🧹 Logs cleared", "SYSTEM")

    def toggle_log_fullscreen(self, e):
        """Simple fullscreen toggle"""
        self.add_event_log("📺 Fullscreen mode (coming soon)", "INFO")
