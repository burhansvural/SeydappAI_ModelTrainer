# src/ui/builder/view_manager.py - SADECE IMPORT VE MANAGER

import flet as ft
import logging
from ..views import *

logger = logging.getLogger(__name__)


class ViewManager:
    """✅ Basit view manager - Search results [2] component coordination[2]"""

    def __init__(self, page, log_system, dashboard_cards, control_panel):
        self.page = page
        self.log_system = log_system
        self.dashboard_cards = dashboard_cards
        self.control_panel = control_panel
        self.current_view = "training"
        self.views = {}
        self.view_container = None
        logger.info("Initialized ViewManager")

    def create_views(self):
        """✅ View'ları ayrı dosyalardan oluştur - Search results [2] pattern[2]"""
        logger.info("🔧 Creating views from separate modules")

        # ✅ Ayrı dosyalardan view'ları oluştur
        self.views["training"] = create_training_view(self.log_system, self.dashboard_cards, self.control_panel)
        self.views["chat"] = create_chat_view(self.log_system)
        self.views["analytics"] = create_analytics_view(self.log_system)
        self.views["settings"] = create_settings_view(self.log_system)
        self.views["models"] = create_models_view(self.log_system)

        self.view_container = ft.Container(
            key="view_container",
            content=self.views[self.current_view],
            expand=True,
            padding= 10
        )

        logger.info("✅ All views created from separate modules")

    def switch_view(self, view_key: str):
        """View değiştir"""
        if view_key in self.views:
            self.current_view = view_key
            self.view_container.content = self.views[view_key]
            self.view_container.update()
            self.log_system.add_event_log(f"📱 View: {view_key}", "UI")

    def get_view_container(self) -> ft.Container:
        return self.view_container
