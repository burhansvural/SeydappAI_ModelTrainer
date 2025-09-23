# src/ui/builder/control_panel.py
"""
🎮 Control Panel - Refactored with Facade Pattern
Bu dosya Facade Pattern[1] kullanarak complex subsystems'i unified interface ile yönetir
Eski 700+ satırlık kod şimdi 60 satır - modular architecture ile
"""

import flet as ft
import logging
from typing import Dict, Optional

# Parçalı yapıyı import et - Composition Pattern[4]
from .control_panel import (
    ControlPanel as ModularControlPanel,
    ControlPanelConfig
)

logger = logging.getLogger(__name__)


class ControlPanel:
    """
    Facade Pattern[1] implementation - Complex subsystems için unified interface

    Bu sınıf restaurant manager gibi çalışır[1]:
    - Client code chef, cashier, waiter ile ayrı ayrı uğraşmaz
    - Manager (Facade) her şeyi handle eder
    - Simplified interaction ve reduced coupling[1]
    """

    def __init__(self, log_system, dashboard_cards, config: Optional[Dict] = None):
        """
        Facade constructor - Complex subsystem'leri initialize eder[1]

        Args:
            log_system: Event loglama sistemi
            dashboard_cards: Dashboard widget'ları
            config: Konfigürasyon dictionary'si

        Facade Pattern Benefits[1]:
        - Client code'un complex internal structure bilmesine gerek yok
        - Simplified interface ile improved usability
        - Reduced coupling between client and subsystem
        """
        logger.info("🎮 Initializing Control Panel with Facade Pattern")

        # Facade Pattern - Complex subsystem'i gizle[1]
        self._modular_control_panel = ModularControlPanel(
            log_system,
            dashboard_cards,
            config
        )

        # Client interface için basit referanslar
        self.page = None

        logger.info("✅ Control Panel Facade initialized - Complex subsystems hidden")

    def create_controls(self, page: ft.Page) -> None:
        """
        Unified interface[1] - UI creation complexity'sini gizler

        Args:
            page: Flet page referansı

        Facade Pattern[1]:
        - Client code UI creation details'leri bilmiyor
        - Internal complexity (UI components, event handlers, etc.) gizli
        - Simple method call ile complex operations
        """
        self.page = page
        logger.info("🔧 Creating UI through Facade interface")

        try:
            # Facade Pattern - Complex UI creation'ı delegate et[1]
            self._modular_control_panel.create_controls(page)

            logger.info("✅ UI created successfully through Facade")

        except Exception as e:
            logger.error(f"❌ Facade UI creation failed: {e}")
            # Facade Pattern - Error handling de simplified[1]
            self._handle_ui_creation_error(page, str(e))

    def get_controls(self) -> ft.Container:
        """
        Facade getter method[1] - Complex control retrieval'ı simplify eder

        Returns:
            ft.Container: UI controls container

        Client code bu method ile complex internal structure'a erişir
        ama internal complexity'yi bilmek zorunda değil[1]
        """
        try:
            # Delegate to complex subsystem[1]
            return self._modular_control_panel.get_controls()

        except Exception as e:
            logger.error(f"❌ Facade get_controls failed: {e}")
            # Facade Pattern - Fallback handling simplified[1]
            return self._create_emergency_fallback()

    # Facade Pattern[1] - Simplified client interface methods
    def toggle_autonomous_learning(self, event) -> None:
        """Unified interface for autonomous learning toggle[1]"""
        try:
            self._modular_control_panel.event_handlers.toggle_autonomous_learning(event)
        except Exception as e:
            logger.error(f"❌ Facade autonomous toggle failed: {e}")

    def start_quick_research(self, event) -> None:
        """Unified interface for quick research[1]"""
        try:
            self._modular_control_panel.event_handlers.start_quick_research(event)
        except Exception as e:
            logger.error(f"❌ Facade research failed: {e}")

    def stop_all_processes(self, event) -> None:
        """Unified interface for stopping all processes[1]"""
        try:
            self._modular_control_panel.event_handlers.stop_all_processes(event)
        except Exception as e:
            logger.error(f"❌ Facade stop failed: {e}")

    def cleanup_threads(self) -> None:
        """Simplified thread cleanup interface[1]"""
        try:
            self._modular_control_panel.cleanup_threads()
        except Exception as e:
            logger.debug(f"Facade cleanup error: {e}")

    def safe_page_update(self) -> None:
        """Simplified page update interface[1]"""
        try:
            self._modular_control_panel.safe_page_update()
        except Exception as e:
            logger.debug(f"Facade page update error: {e}")

    # Facade Pattern[1] - Property-like access to complex state
    @property
    def autonomous_running(self) -> bool:
        """Simplified access to autonomous state[1]"""
        try:
            return self._modular_control_panel.autonomous_manager.is_running
        except Exception:
            return False

    @property
    def training_queue_size(self) -> int:
        """Simplified access to training queue state[1]"""
        try:
            status = self._modular_control_panel.training_coordinator.get_queue_status()
            return status.get('queue_size', 0)
        except Exception:
            return 0

    def get_system_status(self) -> Dict:
        """
        Facade Pattern[1] - Unified interface for complex system status

        Returns:
            Dict: Comprehensive system status from multiple subsystems

        Client code tek method ile tüm subsystem status'larını alır[1]
        Internal complexity completely hidden
        """
        try:
            status = {
                'autonomous_running': self.autonomous_running,
                'queue_size': self.training_queue_size,
                'progress_info': {},
                'memory_status': {}
            }

            # Gather status from complex subsystems[1]
            try:
                status['progress_info'] = self._modular_control_panel.autonomous_manager.get_progress_info()
            except Exception:
                status['progress_info'] = {'error': 'unavailable'}

            try:
                status['queue_status'] = self._modular_control_panel.training_coordinator.get_queue_status()
            except Exception:
                status['queue_status'] = {'error': 'unavailable'}

            return status

        except Exception as e:
            logger.debug(f"Facade status error: {e}")
            return {'error': 'system_unavailable'}

    # Private helper methods - Facade Pattern internal implementation[1]
    def _handle_ui_creation_error(self, page: ft.Page, error_message: str) -> None:
        """Facade Pattern - Simplified error handling[1]"""
        try:
            # Create minimal fallback UI - complexity hidden from client[1]
            fallback_container = ft.Container(
                content=ft.Column([
                    ft.Text("🎮 Control Panel - Safe Mode", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Error: {error_message}", size=12, color=ft.Colors.RED_400),
                    ft.ElevatedButton(
                        "Reload",
                        on_click=lambda e: self.create_controls(page),
                        width=200
                    )
                ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20
            )

            # Set fallback in modular system
            self._modular_control_panel.controls_container = fallback_container

        except Exception as e:
            logger.critical(f"❌ Facade fallback creation failed: {e}")

    def _create_emergency_fallback(self) -> ft.Container:
        """Facade Pattern - Emergency fallback when everything fails[1]"""
        return ft.Container(
            content=ft.Text(
                "🚨 Control Panel Emergency Mode\nPlease restart application",
                color=ft.Colors.RED_400,
                text_align=ft.TextAlign.CENTER
            ),
            padding=20,
            alignment=ft.alignment.center
        )


# Facade Pattern[1] - Convenience factory function
def create_control_panel(log_system, dashboard_cards, config: Optional[Dict] = None) -> ControlPanel:
    """
    Factory function - Facade Pattern[1] ile simplified object creation

    Args:
        log_system: Loglama sistemi
        dashboard_cards: Dashboard widgets
        config: Configuration dictionary

    Returns:
        ControlPanel: Facade instance

    Client code factory function ile complex initialization'dan kurtulur[1]
    """
    logger.info("🏭 Creating Control Panel through Factory")

    try:
        # Configuration preprocessing - complexity hidden[1]
        processed_config = ControlPanelConfig() if not config else None

        # Facade instance creation[1]
        facade = ControlPanel(log_system, dashboard_cards, config)

        logger.info("✅ Control Panel Facade created successfully")
        return facade

    except Exception as e:
        logger.error(f"❌ Factory creation failed: {e}")
        # Return minimal facade even on error[1]
        return ControlPanel(log_system, dashboard_cards, {})


# Export sadece Facade interface[1] - Internal complexity gizli
__all__ = ['ControlPanel', 'create_control_panel']
