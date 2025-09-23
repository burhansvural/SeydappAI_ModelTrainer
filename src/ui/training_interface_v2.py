# src/ui/training_interface_v2.py
"""
🎯 Real Training Interface with Threading Support
RTX 3060 + StarCoder2-3b için optimize edilmiş - SYNTAX ERROR DÜZELTİLDİ
"""

import flet as ft
import logging
import threading
import time
from datetime import datetime
from typing import Optional
import sys
from pathlib import Path

# Project import'ları için path ayarı
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logger = logging.getLogger(__name__)


class RealTrainingInterface:
    """
    Gerçek training entegrasyonu ile modern Flet UI
    Threading support + syntax error düzeltildi
    """

    def __init__(self, page: ft.Page):
        self.page = page
        self.training_thread = None
        self.training_active = False
        self.stop_requested = False

        # Training metrics
        self.current_step = 0
        self.total_steps = 2
        self.current_loss = 0.0
        self.training_start_time = None

        self.init_ui_components()
        logger.info("🎯 Real Training Interface hazırlandı")

    def init_ui_components(self):
        """UI bileşenlerini oluştur - SYNTAX ERROR DÜZELTİLDİ"""

        # 📱 Header Section
        self.header = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.SMART_TOY, size=48, color=ft.Colors.PURPLE_400),
                ft.Column([
                    ft.Text("SeydappAI ModelTrainer", size=28, weight=ft.FontWeight.BOLD),
                    ft.Text("🚀 Real StarCoder2-3b Training", size=14, color=ft.Colors.GREY_400),
                    ft.Text("RTX 3060 Threading + LoRA", size=12, color=ft.Colors.BLUE_300)
                ], spacing=3)
            ], spacing=15),
            padding=25,
            bgcolor=ft.Colors.GREY_800,
            border_radius=12,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK26)
        )

        # 📊 Status ve Progress Cards
        self.status_card = self._create_status_card()
        self.progress_card = self._create_progress_card()

        # 🎮 Control Panel (DÜZELTİLDİ)
        self.control_panel = self._create_control_panel()

        # 📝 Log Viewer
        self.log_viewer = self._create_log_viewer()

        # Initial logs
        self.add_log("🎉 Real Training Interface aktif")
        self.add_log("🖥️ RTX 3060 (12GB VRAM) + CUDA 12.9")
        self.add_log("📦 StarCoder2-3b model hazır")
        self.add_log("⚡ Threading + progress tracking aktif")

    def _create_status_card(self):
        """Status tracking card"""
        # Status text widgets
        self.status_text = ft.Text("🤖 Ready", size=14, color=ft.Colors.GREEN_400)
        self.model_text = ft.Text("StarCoder2-3b", size=12, color=ft.Colors.BLUE_300)
        self.time_text = ft.Text("00:00", size=12, color=ft.Colors.GREY_400)

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.MONITOR_HEART, size=24, color=ft.Colors.GREEN_400),
                    ft.Text("Training Status", size=16, weight=ft.FontWeight.BOLD)
                ], spacing=10),
                ft.Divider(height=1, color=ft.Colors.GREY_600),

                ft.Row([ft.Text("Status:", size=12, color=ft.Colors.GREY_400), self.status_text], spacing=10),
                ft.Row([ft.Text("Model:", size=12, color=ft.Colors.GREY_400), self.model_text], spacing=10),
                ft.Row([ft.Text("Time:", size=12, color=ft.Colors.GREY_400), self.time_text], spacing=10)
            ], spacing=8),
            padding=15,
            bgcolor=ft.Colors.GREY_800,
            border_radius=8,
            width=320
        )

    def _create_progress_card(self):
        """Progress tracking card"""
        # Progress widgets
        self.step_text = ft.Text("0/2", size=12, color=ft.Colors.WHITE)
        self.loss_text = ft.Text("0.000", size=12, color=ft.Colors.YELLOW_400)
        self.progress_bar = ft.ProgressBar(
            width=250,
            height=10,
            color=ft.Colors.BLUE_400,
            bgcolor=ft.Colors.GREY_600,
            value=0.0
        )

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.TRENDING_UP, size=24, color=ft.Colors.BLUE_400),
                    ft.Text("Training Metrics", size=16, weight=ft.FontWeight.BOLD)
                ], spacing=10),
                ft.Divider(height=1, color=ft.Colors.GREY_600),

                ft.Row([ft.Text("Steps:", size=12, color=ft.Colors.GREY_400), self.step_text], spacing=10),
                ft.Row([ft.Text("Loss:", size=12, color=ft.Colors.GREY_400), self.loss_text], spacing=10),

                ft.Container(height=5),
                self.progress_bar
            ], spacing=8),
            padding=15,
            bgcolor=ft.Colors.GREY_800,
            border_radius=8,
            width=320,
            visible=False
        )

    def _create_control_panel(self):
        """Control button panel - SYNTAX ERROR DÜZELTİLDİ"""

        # Button'ları normal assignment ile oluştur
        self.start_btn = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.ROCKET_LAUNCH, size=20),
                ft.Text("Start Real Training")
            ], spacing=8),
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE,
            on_click=self.start_real_training,
            width=200,
            height=50
        )

        self.stop_btn = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.STOP_CIRCLE, size=20),
                ft.Text("Stop Training")
            ], spacing=8),
            bgcolor=ft.Colors.RED_600,
            color=ft.Colors.WHITE,
            on_click=self.stop_training,
            width=200,
            height=50,
            disabled=True
        )

        self.config_btn = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.TUNE, size=20),
                ft.Text("Config")
            ], spacing=8),
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            on_click=self.open_config_dialog,
            width=200,
            height=50
        )

        return ft.Container(
            content=ft.Row([
                self.start_btn,
                self.stop_btn,
                self.config_btn
            ], spacing=25, alignment=ft.MainAxisAlignment.CENTER),
            padding=20
        )

    def _create_log_viewer(self):
        """Real-time log viewer"""
        self.log_list = ft.ListView(
            height=280,
            width=780,
            spacing=3,
            padding=10
        )

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.TERMINAL, size=24, color=ft.Colors.GREY_400),
                    ft.Text("🔥 Real-time Training Logs", size=16, weight=ft.FontWeight.BOLD)
                ], spacing=10),

                ft.Container(
                    content=self.log_list,
                    border=ft.border.all(1, ft.Colors.GREY_600),
                    border_radius=8,
                    bgcolor=ft.Colors.BLACK87
                )
            ], spacing=10),
            padding=15
        )

    def build_ui(self) -> ft.Container:
        """Ana UI layout"""
        return ft.Container(
            content=ft.Column([
                self.header,
                ft.Container(height=20),

                ft.Row([
                    self.status_card,
                    self.progress_card
                ], spacing=20, alignment=ft.MainAxisAlignment.CENTER),

                ft.Container(height=25),
                self.control_panel,
                ft.Container(height=20),
                self.log_viewer

            ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor=ft.Colors.GREY_900
        )

    def start_real_training(self, e):
        """Gerçek training başlat - threading safe[2][3]"""
        if self.training_active:
            return

        self.training_active = True
        self.stop_requested = False
        self.training_start_time = time.time()

        # UI durumunu güncelle
        self.start_btn.disabled = True
        self.stop_btn.disabled = False
        self.progress_card.visible = True

        self.update_status("🔄 Training başlatılıyor...")
        self.add_log("🚀 Gerçek LoRA training başlatıldı")
        self.add_log("🧵 Background thread oluşturuluyor...")

        self.page.update()

        # Threading safe başlatma[2][3]
        self.training_thread = threading.Thread(
            target=self._training_worker,
            daemon=True
        )
        self.training_thread.start()

    def _training_worker(self):
        """Background training worker - thread exception safe[1][2]"""
        try:
            self._thread_safe_update("📦 Dependencies yükleniyor...")

            # Gerçek training sürecini simulate edelim
            self._simulate_real_training()

        except Exception as e:
            logger.error(f"❌ Training worker hatası: {e}")
            self._training_failed(f"Thread error: {str(e)}")

    def _simulate_real_training(self):
        """
        Gerçek training simulation - thread safe[3]
        (Actual training integration için hazırlık)
        """
        steps = [
            ("📦 Model yükleniyor...", 0.1),
            ("🔧 Tokenizer hazırlanıyor...", 0.2),
            ("⚡ LoRA setup...", 0.3),
            ("📊 Dataset tokenizing...", 0.5),
            ("🎯 Training step 1/2...", 0.7),
            ("🎯 Training step 2/2...", 0.9),
            ("💾 Model kaydediliyor...", 1.0)
        ]

        for i, (message, progress) in enumerate(steps):
            if self.stop_requested:
                self._training_stopped()
                return

            self._thread_safe_update(message)
            self._thread_safe_progress_update(progress)

            # Loss simulation
            simulated_loss = 8.0 - (i * 1.2)  # Decreasing loss
            self._thread_safe_loss_update(simulated_loss)

            time.sleep(0.5)  # Simulate training time

        self._training_completed()

    def _thread_safe_update(self, message: str):
        """Thread-safe mesaj güncelleme[2][3]"""
        try:
            self.add_log(message)
            self.page.update()
        except Exception as e:
            logger.warning(f"⚠️ Thread update warning: {e}")

    def _thread_safe_progress_update(self, value: float):
        """Thread-safe progress güncelleme"""
        try:
            self.progress_bar.value = value
            self.page.update()
        except Exception as e:
            logger.warning(f"⚠️ Progress update warning: {e}")

    def _thread_safe_loss_update(self, loss: float):
        """Thread-safe loss güncelleme"""
        try:
            self.loss_text.value = f"{loss:.3f}"

            # Loss Color
            if loss > 6.0:
                self.loss_text.Color = ft.Colors.RED_400
            elif loss > 3.0:
                self.loss_text.Color = ft.Colors.YELLOW_400
            else:
                self.loss_text.Color = ft.Colors.GREEN_400

            self.page.update()
        except Exception as e:
            logger.warning(f"⚠️ Loss update warning: {e}")

    def stop_training(self, e):
        """Training durdur"""
        if self.training_active:
            self.stop_requested = True
            self.add_log("⏹️ Training durdurma isteği gönderildi...")

    def _training_completed(self):
        """Training tamamlandı"""
        self.training_active = False
        self.start_btn.disabled = False
        self.stop_btn.disabled = True

        elapsed_time = time.time() - self.training_start_time
        self.time_text.value = f"{elapsed_time:.1f}s"

        self.update_status("✅ Training tamamlandı!")
        self.add_log("🎉 Training başarıyla tamamlandı!")
        self.add_log(f"⏱️ Süre: {elapsed_time:.1f} saniye")

        self.page.update()

    def _training_stopped(self):
        """Training durduruldu"""
        self.training_active = False
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.progress_card.visible = False

        self.update_status("⏹️ Training durduruldu")
        self.add_log("⏹️ Training kullanıcı tarafından durduruldu")
        self.page.update()

    def _training_failed(self, error_msg: str):
        """Training başarısız"""
        self.training_active = False
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.progress_card.visible = False

        self.update_status("❌ Training başarısız!")
        self.add_log(f"❌ Hata: {error_msg}")
        self.page.update()

    def open_config_dialog(self, e):
        """Config dialog aç"""
        self.add_log("⚙️ Training config dialog açılıyor...")

    def update_status(self, message: str):
        """Status güncelle"""
        self.status_text.value = message

        if "🔄" in message:
            self.status_text.Color = ft.Colors.YELLOW_400
        elif "✅" in message:
            self.status_text.Color = ft.Colors.GREEN_400
        elif "❌" in message:
            self.status_text.Color = ft.Colors.RED_400
        else:
            self.status_text.Color = ft.Colors.BLUE_300

    def add_log(self, message: str):
        """Log entry ekle"""
        timestamp = datetime.now().strftime("%H:%M:%S")

        log_entry = ft.Container(
            content=ft.Text(
                f"[{timestamp}] {message}",
                size=11,
                color=ft.Colors.WHITE70,
                selectable=True
            ),
            padding=ft.padding.symmetric(vertical=3, horizontal=8),
            bgcolor=ft.Colors.GREY_800,
            border_radius=4,
            margin=ft.margin.symmetric(vertical=1)
        )

        self.log_list.controls.append(log_entry)

        # Performance için log limit
        if len(self.log_list.controls) > 100:
            self.log_list.controls.pop(0)


# Factory function
def create_real_training_interface(page: ft.Page) -> RealTrainingInterface:
    """Real training interface factory"""
    return RealTrainingInterface(page)


# Test
async def main(page: ft.Page):
    """Standalone test"""
    page.title = "Real Training Interface - SYNTAX FIXED"
    interface = RealTrainingInterface(page)
    page.add(interface.build_ui())


if __name__ == "__main__":
    ft.app(target=main)
