# src/ui/builder/control_panel/ui_helpers.py
"""
🛠️ UI Helpers - Control Panel için Yardımcı UI Fonksiyonları
Bu dosya UI update'leri ve error handling için utility fonksiyonları sağlar
"""

import flet as ft
import logging
from typing import Optional, Callable, Any

logger = logging.getLogger(__name__)


class UIHelpers:
    """
    UI operations için static helper method'lar sağlayan sınıf[1]

    Static method'lar[1]:
    - Sınıf instance'ına ihtiyaç duymaz
    - @staticmethod dekoratörü ile tanımlanır
    - Utility functions için idealdir
    """

    @staticmethod
    def safe_update_text(text_widget: Optional[ft.Text], new_value: str, color: Optional[str] = None):
        """
        Text widget'ını güvenli şekilde güncelleyen static method[1]

        Args:
            text_widget: Güncellenecek text widget
            new_value: Yeni text değeri
            color: Yeni renk (isteğe bağlı)
        """
        try:
            if text_widget:
                text_widget.value = new_value
                if color:
                    text_widget.color = color
                if hasattr(text_widget, 'update'):
                    text_widget.update()
        except Exception as e:
            logger.debug(f"Text update error: {e}")

    @staticmethod
    def safe_update_progress(progress_widget: Optional[ft.ProgressBar], value: float):
        """
        Progress bar'ı güvenli şekilde güncelleyen static method

        Args:
            progress_widget: Güncellenecek progress bar
            value: Yeni progress değeri (0.0 - 1.0)
        """
        try:
            if progress_widget:
                # Value validation
                clamped_value = max(0.0, min(1.0, value))
                progress_widget.value = clamped_value
                if hasattr(progress_widget, 'update'):
                    progress_widget.update()
        except Exception as e:
            logger.debug(f"Progress update error: {e}")

    @staticmethod
    def safe_enable_disable_button(button_widget: Optional[ft.Container], enabled: bool):
        """
        Button'ı güvenli şekilde enable/disable eden static method

        Args:
            button_widget: Güncellenecek button container
            enabled: Enable durumu (True/False)
        """
        try:
            if button_widget:
                button_widget.disabled = not enabled
                if hasattr(button_widget, 'update'):
                    button_widget.update()
        except Exception as e:
            logger.debug(f"Button update error: {e}")

    @staticmethod
    def create_error_dialog(page: ft.Page, title: str, message: str) -> ft.AlertDialog:
        """
        Error dialog oluşturan static method

        Args:
            page: Flet page referansı
            title: Dialog başlığı
            message: Error mesajı

        Returns:
            ft.AlertDialog: Oluşturulan error dialog
        """
        try:
            dialog = ft.AlertDialog(
                title=ft.Text(title),
                content=ft.Text(message),
                actions=[
                    ft.TextButton(
                        "Tamam",
                        on_click=lambda e: page.close_dialog()
                    )
                ]
            )
            return dialog
        except Exception as e:
            logger.error(f"Error dialog creation failed: {e}")
            return None

    @staticmethod
    def show_success_snackbar(page: ft.Page, message: str):
        """
        Success snackbar gösteren static method

        Args:
            page: Flet page referansı
            message: Success mesajı
        """
        try:
            snackbar = ft.SnackBar(
                content=ft.Text(message, color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_400
            )
            page.snack_bar = snackbar
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            logger.debug(f"Success snackbar error: {e}")

    @staticmethod
    def show_error_snackbar(page: ft.Page, message: str):
        """
        Error snackbar gösteren static method

        Args:
            page: Flet page referansı
            message: Error mesajı
        """
        try:
            snackbar = ft.SnackBar(
                content=ft.Text(message, color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_400
            )
            page.snack_bar = snackbar
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            logger.debug(f"Error snackbar error: {e}")


class UIAnimations:
    """
    UI animasyonları için helper sınıfı[1]
    """

    @staticmethod
    def create_pulse_animation() -> ft.Animation:
        """Pulse animasyonu oluşturan static method"""
        return ft.Animation(1000, ft.AnimationCurve.EASE_IN_OUT)

    @staticmethod
    def create_fade_animation() -> ft.Animation:
        """Fade animasyonu oluşturan static method"""
        return ft.Animation(500, ft.AnimationCurve.EASE_IN)
