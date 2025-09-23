# src/ui/builder/main_content.py
"""
🧱 Ana içerik alanı - Son bileşen olarak yüklenecek
Search results [3] pattern: UI hierarchy management
"""

import flet as ft
import logging

logger = logging.getLogger(__name__)


class MainContent:
    """Ana içerik alanı - Tüm bileşenler mevcut olmalı"""

    def __init__(self, page, log_system, dashboard_cards, control_panel, sidebar):
        """Main content initialization"""
        self.page = page
        self.log_system = log_system
        self.dashboard_cards = dashboard_cards
        self.control_panel = control_panel
        self.sidebar = sidebar
        self.view_manager = None
        self.content_container = None
        logger.info("Initialized MainContent")

    def create_content(self):
        """✅ Ana içerik yapısını oluşturur - Search results [3] hierarchy pattern"""
        logger.info("🔧 Creating main content UI structure")

        # View manager'ı oluştur
        from .view_manager import ViewManager
        self.view_manager = ViewManager(self.page, self.log_system, self.dashboard_cards, self.control_panel)
        self.view_manager.create_views()

        # Ana içerik container'ı
        self.content_container = self.view_manager.get_view_container()

        self.log_system.add_event_log("🧱 Main content structure created", "SYSTEM")
        logger.info("✅ Main content UI structure created")

    def update_view(self, view_key):
        """View'ı güncelle - Search results [1] reusable pattern"""
        if self.view_manager:
            self.view_manager.switch_view(view_key)
            # Sidebar'a da bildir
            self.sidebar.update_active_item(view_key)
        else:
            logger.error("❌ ViewManager not initialized")

    def get_content(self) -> ft.Container:
        """Ana içerik container'ını döndürür"""
        if not self.content_container:
            logger.error("❌ Content container not created yet")
            return ft.Container(
                content=ft.Text("❌ Content not ready", color=ft.Colors.RED_400),
                padding=50
            )
        return self.content_container
