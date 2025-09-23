# src/ui/training_interface.py
"""
🎯 Training Interface - SeydappAI ModelTrainer
Ana training arayüzü modülü
Python 3.12.10 + RTX 3060 + CUDA 12.9 için optimize edilmiş
"""

import flet as ft
import logging
from typing import Optional, Callable
from pathlib import Path

logger = logging.getLogger(__name__)


class ModelTrainingApp:
    """
    Ana model training uygulaması sınıfı
    main.py tarafından beklenen sınıf adı
    RTX 3060 + Python 3.12.10 için optimize edilmiş
    """

    def __init__(self):
        """
        Model training app başlatıcısı
        """
        self.app_name = "SeydappAI ModelTrainer"
        self.version = "1.0.0"
        self.is_running = False
        self.training_interface = None

        logger.info("🤖 ModelTrainingApp başlatıldı")

    def build(self, page: ft.Page) -> ft.Container:
        """
        ✅ Flet custom control build method[5]
        main.py tarafından çağrılır

        Args:
            page: Flet page objesi

        Returns:
            ft.Container: Ana UI container
        """
        try:
            # Page referansını sakla
            self.page = page

            # Sayfa ayarları
            self.initialize_page(page)

            # Training interface oluştur
            self.training_interface = TrainingInterface(page)

            # Ana UI container'ı döndür
            ui_container = self.training_interface.build_ui()

            logger.info("✅ ModelTrainingApp build() başarıyla tamamlandı")
            return ui_container

        except Exception as e:
            logger.error(f"❌ ModelTrainingApp build() hatası: {e}")

            # Hata durumunda basit error UI döndür
            return ft.Container(
                content=ft.Column([
                    ft.Text("❌ UI Build Hatası", size=20, color=ft.Colors.RED_400),
                    ft.Text(f"Hata: {str(e)}", size=12, color=ft.Colors.GREY_400),
                    ft.ElevatedButton(
                        "🔄 Yeniden Dene",
                        on_click=lambda _: self.page.update()
                    )
                ]),
                padding=20
            )

    def initialize_page(self, page: ft.Page):
        """
        Sayfa temel ayarlarını yapılandır
        RTX 3060 + Python 3.12.10 için optimize
        """
        # Sayfa ayarları (sisteminize özel)
        page.title = f"{self.app_name} v{self.version}"
        page.theme_mode = ft.ThemeMode.DARK
        page.window.width = 1200
        page.window.height = 900
        page.window_resizable = True
        page.padding = 0  # Container kendi padding'ini yönetir
        page.bgcolor = ft.Colors.GREY_900

        # Window ayarları
        page.window_min_width = 800
        page.window_min_height = 600
        page.window.center()

        logger.info("🎯 Page ayarları yapılandırıldı")

    def run(self):
        """
        Ana uygulamayı çalıştır
        Flet app başlatma method'u
        """
        try:
            logger.info(f"🚀 {self.app_name} v{self.version} başlatılıyor...")
            self.is_running = True

            # Flet uygulamasını başlat (build method ile)[4]
            ft.app(target=self.build)

        except Exception as e:
            logger.error(f"❌ Uygulama başlatma hatası: {e}")
            self.is_running = False
        finally:
            logger.info("⏹️ Uygulama sonlandırıldı")

    def get_app_info(self) -> dict[str, str]:
        """
        Uygulama bilgilerini döndür
        """
        return {
            "name": self.app_name,
            "version": self.version,
            "python_version": "3.12.10",
            "gpu": "RTX 3060 12GB",
            "cuda": "12.9",
            "pytorch": "2.8.0+cu128"
        }


class TrainingInterface:
    """
    Training arayüzü sınıfı
    RTX 3060 sistemi için optimize edilmiş training UI
    """

    def __init__(self, page: ft.Page):
        """
        Training interface başlatıcısı

        Args:
            page: Flet page objesi
        """
        self.page = page

        # UI state
        self.training_active = False
        self.current_model = "bigcode/starcoder2-3b"

        # UI bileşenleri
        self.init_ui_components()

        logger.info("🎯 Training interface hazırlandı")

    def init_ui_components(self):
        """UI bileşenlerini başlat"""

        # Header bileşenleri
        self.app_icon = ft.Icon(ft.Icons.SMART_TOY, size=40, color=ft.Colors.BLUE_400)
        self.app_title = ft.Text("SeydappAI ModelTrainer", size=24, weight=ft.FontWeight.BOLD)

        # Status bileşenleri
        self.status_text = ft.Text("🤖 RTX 3060 + Python 3.12.10 Ready", size=16, color=ft.Colors.GREEN_400)
        self.model_info = ft.Text(f"📦 Model: {self.current_model}", size=12, color=ft.Colors.BLUE_300)

        # Progress bileşenleri
        self.progress_bar = ft.ProgressBar(width=800, visible=False)
        self.progress_text = ft.Text("", size=12, visible=False)

        # Control buttons
        self.start_btn = ft.ElevatedButton(
            "🚀 Start Training",
            on_click=self.start_training,
            bgcolor=ft.Colors.GREEN_600,
            width=150
        )

        self.stop_btn = ft.ElevatedButton(
            "⏹️ Stop Training",
            on_click=self.stop_training,
            bgcolor=ft.Colors.RED_600,
            width=150,
            disabled=True
        )

        self.settings_btn = ft.ElevatedButton(
            "⚙️ Settings",
            on_click=self.open_settings,
            bgcolor=ft.Colors.BLUE_600,
            width=150
        )

        # Log area
        self.log_area = ft.ListView(
            height=300,
            width=800,
            spacing=2
        )

        # Initial log message
        self.add_log("🎉 SeydappAI ModelTrainer başlatıldı")
        self.add_log(f"🖥️ GPU: RTX 3060 (11.6GB VRAM)")
        self.add_log(f"⚡ CUDA: 12.9 + PyTorch 2.8.0+cu128")

    def build_ui(self) -> ft.Container:
        """
        Ana UI layout'unu oluştur

        Returns:
            ft.Container: Tam UI container
        """
        return ft.Container(
            content=ft.Column([
                # Header Section
                ft.Container(
                    content=ft.Row([
                        self.app_icon,
                        ft.Column([
                            self.app_title,
                            ft.Text("StarCoder2 Conversation Training Toolkit", size=12, color=ft.Colors.GREY_400)
                        ], spacing=5)
                    ]),
                    padding=ft.padding.all(20),
                    bgcolor=ft.Colors.GREY_900,
                    border_radius=10
                ),

                # Status Section
                ft.Container(
                    content=ft.Column([
                        self.status_text,
                        self.model_info,
                        ft.Divider()
                    ]),
                    padding=10
                ),

                # Progress Section
                ft.Container(
                    content=ft.Column([
                        self.progress_bar,
                        self.progress_text
                    ]),
                    padding=10
                ),

                # Control Buttons
                ft.Container(
                    content=ft.Row([
                        self.start_btn,
                        self.stop_btn,
                        self.settings_btn
                    ], spacing=20),
                    padding=10
                ),

                # Log Section
                ft.Container(
                    content=ft.Column([
                        ft.Text("📝 Training Logs", size=16, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=self.log_area,
                            border=ft.border.all(1, ft.Colors.GREY_600),
                            border_radius=5,
                            padding=10
                        )
                    ]),
                    padding=10
                )
            ], spacing=10),
            padding=20
        )

    def start_training(self, e):
        """Training başlat"""
        if not self.training_active:
            self.training_active = True
            self.start_btn.disabled = True
            self.stop_btn.disabled = False
            self.progress_bar.visible = True
            self.progress_text.visible = True

            self.update_status("🔄 Training başlatılıyor...")
            self.add_log("🚀 StarCoder2-3b training başlatıldı")
            self.add_log("🎯 RTX 3060 optimized settings aktif")

            # UI güncelle
            self.page.update()

            logger.info("🚀 Training başlatıldı")

    def stop_training(self, e):
        """Training durdur"""
        if self.training_active:
            self.training_active = False
            self.start_btn.disabled = False
            self.stop_btn.disabled = True
            self.progress_bar.visible = False
            self.progress_text.visible = False

            self.update_status("⏹️ Training durduruldu")
            self.add_log("⏹️ Training işlemi kullanıcı tarafından durduruldu")

            # UI güncelle
            self.page.update()

            logger.info("⏹️ Training durduruldu")

    def open_settings(self, e):
        """Ayarlar penceresini aç"""
        self.add_log("⚙️ Ayarlar menüsü açılıyor...")
        logger.info("⚙️ Settings penceresi açıldı")

    def update_status(self, message: str):
        """Status mesajını güncelle"""
        self.status_text.value = message
        self.status_text.Color = ft.Colors.YELLOW_400 if "🔄" in message else ft.Colors.GREEN_400
        self.page.update()

    def add_log(self, message: str):
        """Log mesajı ekle"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")

        log_entry = ft.Text(
            f"[{timestamp}] {message}",
            size=11,
            color=ft.Colors.WHITE70
        )

        self.log_area.controls.append(log_entry)

        # Maksimum 100 log mesajı tut (performance için)
        if len(self.log_area.controls) > 100:
            self.log_area.controls.pop(0)

        # Auto-scroll en alta
        if hasattr(self.log_area, 'scroll_to'):
            self.log_area.scroll_to(offset=-1)


# ===============================================================================
# 🏁 EXPORT FUNCTIONS (main.py uyumluluğu için)
# ===============================================================================

def create_training_interface(page: ft.Page) -> TrainingInterface:
    """
    Training interface factory function

    Args:
        page: Flet page objesi

    Returns:
        TrainingInterface: Hazırlanmış training interface
    """
    return TrainingInterface(page)


def create_model_training_app() -> ModelTrainingApp:
    """
    Model training app factory function
    main.py tarafından kullanılır

    Returns:
        ModelTrainingApp: Hazırlanmış training app
    """
    return ModelTrainingApp()


# Ana çalıştırma fonksiyonu (standalone test için)
def main(page: ft.Page):
    """
    Standalone Flet uygulaması (test için)
    """
    try:
        app = ModelTrainingApp()
        app.initialize_ui(page)
        logger.info("🎉 Standalone training interface başlatıldı")
    except Exception as e:
        logger.error(f"❌ Training interface hatası: {e}")


# ===============================================================================
# 🔧 MODULE EXPORTS (main.py için gerekli)
# ===============================================================================

# main.py'nin import edebilmesi için sınıfları export et
__all__ = [
    'ModelTrainingApp',
    'TrainingInterface',
    'create_training_interface',
    'create_model_training_app',
    'main'
]

if __name__ == "__main__":
    """
    Development test için - dosyayı direkt çalıştırabilirsiniz
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    logger.info("🔍 Training interface standalone test...")

    # Flet uygulamasını başlat
    ft.app(target=main)

class TrainingInterface:
    """
    Ana training arayüzü sınıfı
    RTX 3060 sistemi için optimize edilmiş training UI
    """

    def __init__(self, page: ft.Page):
        """
        Training interface başlatıcısı

        Args:
            page: Flet page objesi
        """
        self.page = page
        self.page.title = "SeydappAI ModelTrainer - Training Interface"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window.width = 1200
        self.page.window.height = 900

        # UI bileşenleri
        self.status_text = ft.Text("🤖 SeydappAI Model Trainer Ready", size=16)
        self.progress_bar = ft.ProgressBar(width=800, visible=False)
        self.log_area = ft.ListView(height=300, width=800)

        logger.info("🎯 Training interface başlatıldı")

    def build_ui(self) -> ft.Container:
        """
        Ana UI bileşenlerini oluştur

        Returns:
            ft.Container: Ana UI container
        """
        return ft.Container(
            content=ft.Column([
                # Header
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.SMART_TOY, size=40, color=ft.Colors.BLUE_400),
                        ft.Text("SeydappAI ModelTrainer", size=24, weight=ft.FontWeight.BOLD)
                    ]),
                    padding=20
                ),

                # Status area
                ft.Container(
                    content=self.status_text,
                    padding=10
                ),

                # Progress area
                ft.Container(
                    content=self.progress_bar,
                    padding=10,
                    visible=False
                ),

                # Control buttons
                ft.Container(
                    content=ft.Row([
                        ft.ElevatedButton(
                            "🚀 Start Training",
                            on_click=self.start_training,
                            bgcolor=ft.Colors.GREEN_600
                        ),
                        ft.ElevatedButton(
                            "⏹️ Stop Training",
                            on_click=self.stop_training,
                            bgcolor=ft.Colors.RED_600
                        ),
                        ft.ElevatedButton(
                            "📊 View Results",
                            on_click=self.view_results,
                            bgcolor=ft.Colors.BLUE_600
                        )
                    ]),
                    padding=10
                ),

                # Log area
                ft.Container(
                    content=ft.Column([
                        ft.Text("📝 Training Logs", size=16, weight=ft.FontWeight.BOLD),
                        self.log_area
                    ]),
                    padding=10
                )
            ]),
            padding=20
        )

    def start_training(self, e):
        """Training başlat"""
        logger.info("🚀 Training başlatıldı")
        self.update_status("🔄 Training başlatılıyor...")

    def stop_training(self, e):
        """Training durdur"""
        logger.info("⏹️ Training durduruldu")
        self.update_status("⏹️ Training durduruldu")

    def view_results(self, e):
        """Sonuçları görüntüle"""
        logger.info("📊 Sonuçlar görüntüleniyor")
        self.update_status("📊 Sonuçlar yükleniyor...")

    def update_status(self, message: str):
        """Status mesajını güncelle"""
        self.status_text.value = message
        self.add_log(message)
        self.page.update()

    def add_log(self, message: str):
        """Log mesajı ekle"""
        self.log_area.controls.append(
            ft.Text(f"[{ft.datetime.datetime.now().strftime('%H:%M:%S')}] {message}")
        )
        # Maksimum 100 log mesajı tut
        if len(self.log_area.controls) > 100:
            self.log_area.controls.pop(0)


def create_training_interface(page: ft.Page) -> TrainingInterface:
    """
    Training interface factory function

    Args:
        page: Flet page objesi

    Returns:
        TrainingInterface: Hazırlanmış training interface
    """
    interface = TrainingInterface(page)

    # UI'yi page'e ekle
    page.add(interface.build_ui())

    logger.info("✅ Training interface oluşturuldu")
    return interface


# Ana çalıştırma fonksiyonu
def main(page: ft.Page):
    """
    Ana Flet uygulaması
    """
    try:
        interface = create_training_interface(page)
        logger.info("🎉 Training interface başarıyla yüklendi")
    except Exception as e:
        logger.error(f"❌ Training interface hatası: {e}")


if __name__ == "__main__":
    """
    Development test için
    """
    logging.basicConfig(level=logging.INFO)
    logger.info("🔍 Training interface test başlatılıyor...")

    # Flet uygulamasını başlat
    ft.app(target=main)
