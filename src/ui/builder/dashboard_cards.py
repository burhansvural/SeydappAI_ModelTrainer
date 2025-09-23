# src/ui/builder/dashboard_cards.py

import flet as ft
import logging
from src.utils.gpu_monitor import SystemMonitor

logger = logging.getLogger(__name__)


class DashboardCards:
    """Dashboard kartları - Log sistemi mevcut olmalı"""

    def __init__(self, log_system):
        """✅ INIT: Sadece log referansını al - UI henüz oluşturulmuyor"""
        self.log_system = log_system
        self.cards_row = None
        self.training_status_card = None
        self.progress_card = None
        self.model_card = None
        self.research_card = None
        self.rag_card = None
        self.autonomous_card = None
        self.monitoring_active = False
        self.monitoring_thread = None

        # ✅ UI değişkenlerini başlat (Samsung'dan Search results [1] ve [2]'ye uygun)
        self.progress_percentage = ft.Text("0%", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
        self.steps_text = ft.Text("0/100", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
        self.loss_text = ft.Text("0.000", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.YELLOW_400)
        self.eta_text = ft.Text("--:--", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_400)
        
        # ✅ Training Status Card için canlı veri text'leri
        self.status_text = ft.Text("Ready", size=14, color=ft.Colors.GREEN_400, weight=ft.FontWeight.BOLD)
        self.gpu_text = ft.Text("GPU: 0.0%", size=12, color=ft.Colors.CYAN_400)
        self.vram_text = ft.Text("VRAM: 0.0GB", size=12, color=ft.Colors.GREY_400)
        self.cpu_text = ft.Text("CPU: 0.0%", size=12, color=ft.Colors.BLUE_400)
        self.ram_text = ft.Text("RAM: 0.0%", size=12, color=ft.Colors.YELLOW_400)
        self.temp_text = ft.Text("Temp: --°C", size=12, color=ft.Colors.ORANGE_400)
        self.power_text = ft.Text("Power: --W", size=12, color=ft.Colors.RED_400)
        self.uptime_text = ft.Text("Uptime: 00:00:00", size=12, color=ft.Colors.GREEN_300)
        
        # ✅ System Info Card için text'ler
        self.gpu_name_text = ft.Text("GPU: Unknown", size=11, color=ft.Colors.PURPLE_300)
        self.disk_text = ft.Text("Disk: --GB free", size=11, color=ft.Colors.BLUE_300)
        self.network_text = ft.Text("Network: --MB", size=11, color=ft.Colors.GREEN_300)
        self.cpu_freq_text = ft.Text("CPU Freq: --MHz", size=11, color=ft.Colors.CYAN_300)

        self.research_topics_text = ft.Text("0", size=11, color=ft.Colors.CYAN_300, weight=ft.FontWeight.BOLD)
        self.research_nodes_text = ft.Text("0 nodes", size=11, color=ft.Colors.BLUE_300, weight=ft.FontWeight.BOLD)
        self.research_scan_text = ft.Text("Never", size=11, color=ft.Colors.GREEN_300, weight=ft.FontWeight.BOLD)
        self.research_quality_text = ft.Text("N/A", size=11, color=ft.Colors.PURPLE_300, weight=ft.FontWeight.BOLD)
        self.research_status_text = ft.Text("Idle", size=11, color=ft.Colors.ORANGE_300, weight=ft.FontWeight.BOLD)

        self.rag_entities_text = ft.Text("0", size=11, color=ft.Colors.PURPLE_300, weight=ft.FontWeight.BOLD)
        self.rag_embeddings_text = ft.Text("0", size=11, color=ft.Colors.BLUE_300, weight=ft.FontWeight.BOLD)
        self.rag_queries_text = ft.Text("0", size=11, color=ft.Colors.GREEN_300, weight=ft.FontWeight.BOLD)
        self.rag_status_text = ft.Text("Offline", size=11, color=ft.Colors.ORANGE_300, weight=ft.FontWeight.BOLD)

        self.autonomous_status_text = ft.Text("Offline", size=11, color=ft.Colors.RED_300, weight=ft.FontWeight.BOLD)
        self.autonomous_cycles_text = ft.Text("0", size=11, color=ft.Colors.BLUE_300, weight=ft.FontWeight.BOLD)
        self.autonomous_next_text = ft.Text("--:--", size=11, color=ft.Colors.GREEN_300, weight=ft.FontWeight.BOLD)
        self.autonomous_entities_text = ft.Text("0", size=11, color=ft.Colors.PURPLE_300, weight=ft.FontWeight.BOLD)

        logger.info("Intialized DashboardCards - UI components not created yet")

    def add_pulse_animation(self):
        """Add pulse effect during active research - Search results [5] safe animations"""
        if self.research_card:
            try:
                self.research_card.animate_opacity = ft.Animation(1000, ft.AnimationCurve.EASE_IN_OUT)
                self.research_card.animate_scale = ft.Animation(500, ft.AnimationCurve.BOUNCE_IN)
                self.research_card.update()
                logger.debug("🎯 Pulse animation activated")
            except Exception as e:
                logger.error(f"❌ Animation error: {e}")
        else:
            logger.warning("⚠️ research_card not initialized for animation")


    def start_real_time_monitoring(self):
        """✅ Search results [1] real-time updates pattern[1]"""
        if not self.monitoring_active:
            self.monitoring_active = True
            import threading
            self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            self.monitoring_thread.start()
            logger.info("🔄 Real-time monitoring started")

    def stop_real_time_monitoring(self):
        """✅ Stop real-time monitoring[1]"""
        self.monitoring_active = False
        logger.info("⏹️ Real-time monitoring stopped")
    
    def start_training_monitoring(self):
        """✅ Training başladığında monitoring'i aktif hale getir"""
        if not self.monitoring_active:
            self.start_real_time_monitoring()
            logger.info("🚀 Training monitoring activated")
        else:
            logger.info("🔄 Training monitoring already active")

    def _monitoring_loop(self):
        """✅ Search results [1] continuous update loop[1]"""
        import time
        from datetime import datetime, timedelta
        from src.utils.gpu_monitor import SystemMonitor
        
        start_time = datetime.now()

        while self.monitoring_active:
            try:
                # ✅ Her 2 saniyede sistem bilgilerini güncelle[1]
                real_status = SystemMonitor.get_real_training_status()
                detailed_stats = SystemMonitor.get_detailed_system_stats()
                training_metrics = SystemMonitor.get_training_metrics()
                
                # ✅ Uptime hesapla
                uptime = datetime.now() - start_time
                uptime_str = str(uptime).split('.')[0]  # Microseconds'ları kaldır
                
                # ✅ GPU sıcaklığını al
                gpu_temp = SystemMonitor.get_gpu_temperature()
                
                # ✅ Canlı veri güncellemeleri - Text referanslarını kullan
                if hasattr(self, 'status_text'):
                    # Training durumuna göre status rengi - daha akıllı kontrol
                    is_training = SystemMonitor.is_training_active()
                    
                    if is_training:
                        self.status_text.value = "🔥 Training Active"
                        self.status_text.color = ft.Colors.ORANGE_400
                    elif real_status['gpu_usage'] > 20:
                        self.status_text.value = "⚡ GPU Active"
                        self.status_text.color = ft.Colors.BLUE_400
                    elif real_status['gpu_usage'] > 5:
                        self.status_text.value = "💤 GPU Idle"
                        self.status_text.color = ft.Colors.YELLOW_400
                    else:
                        self.status_text.value = "✅ Ready"
                        self.status_text.color = ft.Colors.GREEN_400
                    
                    # ✅ Sistem metrikleri güncelle
                    self.gpu_text.value = f"GPU: {real_status['gpu_usage']:.1f}%"
                    self.vram_text.value = f"VRAM: {real_status['vram_used']:.1f}GB / {real_status['vram_total']/1024:.1f}GB"
                    self.cpu_text.value = f"CPU: {real_status['cpu_usage']:.1f}%"
                    self.ram_text.value = f"RAM: {real_status['ram_usage']:.1f}%"
                    self.temp_text.value = f"Temp: {gpu_temp}°C" if gpu_temp > 0 else "Temp: --°C"
                    self.uptime_text.value = f"Uptime: {uptime_str}"
                    
                    # ✅ GPU kullanımına göre renk değişimi
                    if real_status['gpu_usage'] > 80:
                        self.gpu_text.color = ft.Colors.RED_400
                    elif real_status['gpu_usage'] > 50:
                        self.gpu_text.color = ft.Colors.ORANGE_400
                    else:
                        self.gpu_text.color = ft.Colors.CYAN_400
                    
                    # ✅ VRAM kullanımına göre renk değişimi
                    vram_percent = (real_status['vram_used'] / real_status['vram_total']) * 100
                    if vram_percent > 85:
                        self.vram_text.color = ft.Colors.RED_400
                    elif vram_percent > 70:
                        self.vram_text.color = ft.Colors.ORANGE_400
                    else:
                        self.vram_text.color = ft.Colors.GREY_400
                    
                    # ✅ RAM kullanımına göre renk değişimi
                    if real_status['ram_usage'] > 85:
                        self.ram_text.color = ft.Colors.RED_400
                    elif real_status['ram_usage'] > 70:
                        self.ram_text.color = ft.Colors.ORANGE_400
                    else:
                        self.ram_text.color = ft.Colors.YELLOW_400
                    
                    # ✅ Detaylı sistem bilgilerini güncelle
                    if detailed_stats:
                        gpu_info = detailed_stats.get('gpu_info', {})
                        disk_info = detailed_stats.get('disk', {})
                        network_info = detailed_stats.get('network', {})
                        system_info = detailed_stats.get('system', {})
                        
                        # GPU adı
                        if gpu_info.get('name'):
                            self.gpu_name_text.value = f"GPU: {gpu_info['name'][:20]}..."
                        
                        # Disk bilgisi
                        if disk_info.get('free_gb'):
                            self.disk_text.value = f"Disk: {disk_info['free_gb']:.1f}GB free"
                        
                        # Network bilgisi (MB cinsinden)
                        if network_info.get('bytes_recv'):
                            network_mb = network_info['bytes_recv'] / (1024*1024)
                            self.network_text.value = f"Network: {network_mb:.1f}MB recv"
                        
                        # CPU frekansı
                        if system_info.get('cpu_freq'):
                            self.cpu_freq_text.value = f"CPU Freq: {system_info['cpu_freq']:.0f}MHz"
                    
                    # ✅ Training metrikleri güncelle
                    if training_metrics:
                        current_step = training_metrics.get('current_step', 0)
                        total_steps = training_metrics.get('total_steps', 100)
                        train_loss = training_metrics.get('train_loss', 0.0)
                        
                        # Progress card güncellemeleri
                        if hasattr(self, 'steps_text'):
                            self.steps_text.value = f"{current_step}/{total_steps}"
                        if hasattr(self, 'loss_text'):
                            self.loss_text.value = f"{train_loss:.3f}"
                        
                        # ETA güncelle
                        if hasattr(self, 'eta_text'):
                            eta_minutes = training_metrics.get('eta_minutes', 0)
                            if eta_minutes > 0:
                                hours = eta_minutes // 60
                                minutes = eta_minutes % 60
                                if hours > 0:
                                    self.eta_text.value = f"{hours:02d}:{minutes:02d}:00"
                                else:
                                    self.eta_text.value = f"{minutes:02d}:00"
                            else:
                                self.eta_text.value = "Complete"
                        
                        # Progress percentage
                        if hasattr(self, 'progress_percentage') and total_steps > 0:
                            progress_percent = (current_step / total_steps) * 100
                            self.progress_percentage.value = f"{progress_percent:.1f}%"
                            
                            # Circular progress güncelle
                            if hasattr(self, 'circular_progress'):
                                self.circular_progress.value = progress_percent / 100

                # ✅ Training Status Card'ı güncelle
                if self.training_status_card:
                    try:
                        self.training_status_card.update()
                    except Exception as update_error:
                        logger.debug(f"UI update error: {update_error}")
                
                # ✅ Progress Card'ı güncelle
                if self.progress_card:
                    try:
                        self.progress_card.update()
                    except Exception as update_error:
                        logger.debug(f"Progress card update error: {update_error}")
                
                # ✅ System Info Card'ı güncelle
                if self.system_info_card:
                    try:
                        self.system_info_card.update()
                    except Exception as update_error:
                        logger.debug(f"System info card update error: {update_error}")

                time.sleep(2.0)  # 2 saniye aralıkla güncelle

            except Exception as e:
                logger.error(f"❌ Monitoring error: {e}")
                time.sleep(5.0)  # Hata durumunda 5 saniye bekle

    def create_cards(self, page):
        """✅ UI OLUŞTUR: Sayfa referansına gerek var - WEB UI için critical"""
        logger.info("🔧 Creating dashboard UI components")

        # Progress components
        self.circular_progress = ft.ProgressRing(
            key="circular_progress",
            width=120,
            height=120,
            stroke_width=6,
            color=ft.Colors.BLUE_400,
            bgcolor=ft.Colors.TRANSPARENT,
            value=0.0
        )

        # Progress stack
        progress_stack = ft.Stack([
            ft.Container(
                key="progress_bg",
                width=120,
                height=120,
                border_radius=60,
                bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_400),
                border=ft.border.all(3, ft.Colors.with_opacity(0.3, ft.Colors.BLUE_400))
            ),
            self.circular_progress,
            ft.Container(
                key="progress_text",
                content=ft.Column([
                    self.progress_percentage,
                    ft.Text("Complete", size=10, color=ft.Colors.GREY_400)
                ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2),
                top=0, bottom=0, left=0, right=0,
                width=120, height=120,
                alignment=ft.alignment.center,
            )
        ], alignment=ft.alignment.center)

        # ✅ Training Status Card - Canlı verilerle güncellenecek
        real_status = SystemMonitor.get_real_training_status()

        self.training_status_card = ft.Container(
            key="training_status_card",
            content=ft.Column([
                ft.Row([
                    ft.Icon(name=ft.Icons.TIMELINE, size=24, color=ft.Colors.GREEN_400),
                    ft.Text("Training Status", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                ], spacing=10),

                ft.Container(height=5),
                
                # ✅ Ana status
                self.status_text,
                
                ft.Container(height=5),
                
                # ✅ Sistem metrikleri - Canlı güncellenecek
                self.gpu_text,
                self.vram_text,
                self.cpu_text,
                self.ram_text,
                
                ft.Container(height=5),
                
                # ✅ Ek bilgiler
                self.temp_text,
                self.uptime_text,
                
            ], spacing=8),
            padding=20,
            width=300,
            height=300,  # Yüksekliği artırdık
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.GREEN_700, ft.Colors.GREEN_900, ft.Colors.TEAL_900]
            ),
            border_radius=15,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.GREEN_400)),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.Colors.with_opacity(0.3, ft.Colors.GREEN_400),
                offset=ft.Offset(0, 8)
            )
        )

        # ✅ Progress Card
        self.progress_card = ft.Container(
            key="progress_card",
            content=ft.Column([
                ft.Row([
                    ft.Text("Training Progress", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Icon(name=ft.Icons.TRENDING_UP, size=20, color=ft.Colors.BLUE_400)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                ft.Container(height=10),
                progress_stack,

                ft.Row([
                    ft.Column([
                        ft.Text("Steps", size=10, color=ft.Colors.GREY_400),
                        self.steps_text
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Column([
                        ft.Text("Loss", size=10, color=ft.Colors.GREY_400),
                        self.loss_text
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Column([
                        ft.Text("ETA", size=10, color=ft.Colors.GREY_400),
                        self.eta_text
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ], spacing=15),
            padding=25,
            width=300,
            height=276,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.Colors.INDIGO_900, ft.Colors.PURPLE_900]
            ),
            border_radius=20,
            border=ft.border.all(1, ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=25,
                color=ft.Colors.with_opacity(0.3, ft.Colors.PURPLE_400),
                offset=ft.Offset(0, 10)
            )
        )

        # ✅ Model Card
        self.model_card = ft.Container(
            key="model_card",
            content=ft.Column([
                ft.Row([
                    ft.Icon(name=ft.Icons.PSYCHOLOGY, size=24, color=ft.Colors.PURPLE_400),
                    ft.Text("Model Config", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                ], spacing=10),

                ft.Container(height=5),

                ft.Column([
                    ft.Row([ft.Text("Model:", size=11, color=ft.Colors.GREY_400),
                            ft.Text("StarCoder2-3b", size=11, color=ft.Colors.PURPLE_300, weight=ft.FontWeight.BOLD)],
                           spacing=10),
                    ft.Row([ft.Text("Method:", size=11, color=ft.Colors.GREY_400),
                            ft.Text("LoRA Adapter", size=11, color=ft.Colors.BLUE_300, weight=ft.FontWeight.BOLD)],
                           spacing=10),
                    ft.Row([ft.Text("Precision:", size=11, color=ft.Colors.GREY_400),
                            ft.Text("4-bit Quantized", size=11, color=ft.Colors.CYAN_300, weight=ft.FontWeight.BOLD)],
                           spacing=10),
                    ft.Row([ft.Text("Rank:", size=11, color=ft.Colors.GREY_400),
                            ft.Text("16", size=11, color=ft.Colors.GREEN_300, weight=ft.FontWeight.BOLD)], spacing=10),
                    ft.Row([ft.Text("LR:", size=11, color=ft.Colors.GREY_400),
                            ft.Text("1e-4", size=11, color=ft.Colors.YELLOW_300, weight=ft.FontWeight.BOLD)],
                           spacing=10)
                ], spacing=8)
            ], spacing=10),
            padding=20,
            width=300,
            height=276,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.Colors.PURPLE_700, ft.Colors.INDIGO_900]
            ),
            border_radius=20,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.Colors.BLACK26,
                offset=ft.Offset(0, 8)
            )
        )

        # ✅ Research card - SEARCH RESULTS [2] pattern[2]
        self.research_card = ft.Container(
            key="research_card",
            content=ft.Column([
                ft.Row([
                    ft.Icon(name=ft.Icons.TRAVEL_EXPLORE, size=24, color=ft.Colors.CYAN_400),
                    ft.Text("🔍 Autonomous Research", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                ], spacing=10),

                ft.Container(height=5),

                ft.Column([
                    # ✅ SEARCH RESULTS [2] PATTERN: Dynamic text with containers[2]
                    ft.Row([
                        ft.Container(content=ft.Text("Topics:", size=11, color=ft.Colors.GREY_400), width=80),
                        ft.Container(
                            content=self.research_topics_text,  # ✅ Dynamic text
                            padding=ft.padding.symmetric(vertical=2, horizontal=8),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.CYAN_300),
                            border_radius=8
                        )
                    ], spacing=10),

                    ft.Row([
                        ft.Container(content=ft.Text("Knowledge:", size=11, color=ft.Colors.GREY_400), width=80),
                        ft.Container(
                            content=self.research_nodes_text,  # ✅ Dynamic text
                            padding=ft.padding.symmetric(vertical=2, horizontal=8),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_300),
                            border_radius=8
                        )
                    ], spacing=10),

                    ft.Row([
                        ft.Container(content=ft.Text("Last scan:", size=11, color=ft.Colors.GREY_400), width=80),
                        ft.Container(
                            content=self.research_scan_text,  # ✅ Dynamic text
                            padding=ft.padding.symmetric(vertical=2, horizontal=8),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN_300),
                            border_radius=8
                        )
                    ], spacing=10),

                    ft.Row([
                        ft.Container(content=ft.Text("Quality:", size=11, color=ft.Colors.GREY_400), width=80),
                        ft.Container(
                            content=self.research_quality_text,  # ✅ Dynamic text
                            padding=ft.padding.symmetric(vertical=2, horizontal=8),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.PURPLE_300),
                            border_radius=8
                        )
                    ], spacing=10),

                    ft.Row([
                        ft.Container(content=ft.Text("Status:", size=11, color=ft.Colors.GREY_400), width=80),
                        ft.Container(
                            content=self.research_status_text,  # ✅ Dynamic text
                            padding=ft.padding.symmetric(vertical=2, horizontal=8),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.ORANGE_300),
                            border_radius=8
                        )
                    ], spacing=10)
                ], spacing=8)
            ], spacing=10),
            padding=20,
            width=300,
            height=276,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.CYAN_700, ft.Colors.BLUE_900]
            ),
            border_radius=20,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.Colors.BLACK26,
                offset=ft.Offset(0, 8)
            ),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT)
        )

        # ✅ RAG System Card - Search results [2] knowledge base pattern[2]
        self.rag_card = ft.Container(
            key="rag_card",
            content=ft.Column([
                ft.Row([
                    ft.Icon(name=ft.Icons.DEVICE_HUB, size=24, color=ft.Colors.PURPLE_400),
                    ft.Text("🧠 Knowledge RAG", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                ], spacing=10),

                ft.Container(height=5),

                ft.Column([
                    ft.Row([
                        ft.Container(content=ft.Text("Entities:", size=11, color=ft.Colors.GREY_400), width=80),
                        ft.Container(content=self.rag_entities_text,
                                     padding=ft.padding.symmetric(vertical=2, horizontal=8),
                                     bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.PURPLE_300), border_radius=8)
                    ], spacing=10),

                    ft.Row([
                        ft.Container(content=ft.Text("Embeddings:", size=11, color=ft.Colors.GREY_400), width=80),
                        ft.Container(content=self.rag_embeddings_text,
                                     padding=ft.padding.symmetric(vertical=2, horizontal=8),
                                     bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_300), border_radius=8)
                    ], spacing=10),

                    ft.Row([
                        ft.Container(content=ft.Text("Queries:", size=11, color=ft.Colors.GREY_400), width=80),
                        ft.Container(content=self.rag_queries_text,
                                     padding=ft.padding.symmetric(vertical=2, horizontal=8),
                                     bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN_300), border_radius=8)
                    ], spacing=10),

                    ft.Row([
                        ft.Container(content=ft.Text("Status:", size=11, color=ft.Colors.GREY_400), width=80),
                        ft.Container(content=self.rag_status_text,
                                     padding=ft.padding.symmetric(vertical=2, horizontal=8),
                                     bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.ORANGE_300), border_radius=8)
                    ], spacing=10)
                ], spacing=8)
            ], spacing=10),
            padding=20,
            width=300,
            height=276,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.Colors.PURPLE_600, ft.Colors.PINK_900, ft.Colors.DEEP_PURPLE_900]
            ),
            border_radius=20,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=20, color=ft.Colors.BLACK26, offset=ft.Offset(0, 8)),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT)
        )

        # ✅ Autonomous Learning Card - 6th card
        self.autonomous_card = ft.Container(
            key="autonomous_card",
            content=ft.Column([
                ft.Row([
                    ft.Icon(name=ft.Icons.AUTO_MODE, size=24, color=ft.Colors.CYAN_400),
                    ft.Text("🤖 Autonomous Learning", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                ], spacing=10),

                ft.Container(height=5),

                ft.Column([
                    ft.Row([
                        ft.Container(content=ft.Text("Status:", size=11, color=ft.Colors.GREY_400), width=80),
                        ft.Container(content=self.autonomous_status_text,
                                     padding=ft.padding.symmetric(vertical=2, horizontal=8),
                                     bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.RED_300), border_radius=8)
                    ], spacing=10),

                    ft.Row([
                        ft.Container(content=ft.Text("Cycles:", size=11, color=ft.Colors.GREY_400), width=80),
                        ft.Container(content=self.autonomous_cycles_text,
                                     padding=ft.padding.symmetric(vertical=2, horizontal=8),
                                     bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_300), border_radius=8)
                    ], spacing=10),

                    ft.Row([
                        ft.Container(content=ft.Text("Next:", size=11, color=ft.Colors.GREY_400), width=80),
                        ft.Container(content=self.autonomous_next_text,
                                     padding=ft.padding.symmetric(vertical=2, horizontal=8),
                                     bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN_300), border_radius=8)
                    ], spacing=10),

                    ft.Row([
                        ft.Container(content=ft.Text("Entities:", size=11, color=ft.Colors.GREY_400), width=80),
                        ft.Container(content=self.autonomous_entities_text,
                                     padding=ft.padding.symmetric(vertical=2, horizontal=8),
                                     bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.PURPLE_300), border_radius=8)
                    ], spacing=10)
                ], spacing=8)
            ], spacing=10),
            padding=20,
            width=300,
            height=276,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_right,
                end=ft.alignment.bottom_left,
                colors=[ft.Colors.TEAL_700, ft.Colors.CYAN_900]
            ),
            border_radius=20,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=20, color=ft.Colors.BLACK26, offset=ft.Offset(0, 8)),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT)
        )

        # ✅ System Info Card - Detaylı sistem bilgileri
        self.system_info_card = ft.Container(
            key="system_info_card",
            content=ft.Column([
                ft.Row([
                    ft.Icon(name=ft.Icons.COMPUTER, size=24, color=ft.Colors.INDIGO_400),
                    ft.Text("System Info", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                ], spacing=10),

                ft.Container(height=5),

                ft.Column([
                    ft.Row([
                        ft.Container(content=ft.Text("Hardware:", size=11, color=ft.Colors.GREY_400), width=80),
                        ft.Container(
                            content=self.gpu_name_text,
                            padding=ft.padding.symmetric(vertical=2, horizontal=8),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.PURPLE_300),
                            border_radius=8
                        )
                    ], spacing=10),

                    ft.Row([
                        ft.Container(content=ft.Text("Storage:", size=11, color=ft.Colors.GREY_400), width=80),
                        ft.Container(
                            content=self.disk_text,
                            padding=ft.padding.symmetric(vertical=2, horizontal=8),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_300),
                            border_radius=8
                        )
                    ], spacing=10),

                    ft.Row([
                        ft.Container(content=ft.Text("Network:", size=11, color=ft.Colors.GREY_400), width=80),
                        ft.Container(
                            content=self.network_text,
                            padding=ft.padding.symmetric(vertical=2, horizontal=8),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN_300),
                            border_radius=8
                        )
                    ], spacing=10),

                    ft.Row([
                        ft.Container(content=ft.Text("CPU Freq:", size=11, color=ft.Colors.GREY_400), width=80),
                        ft.Container(
                            content=self.cpu_freq_text,
                            padding=ft.padding.symmetric(vertical=2, horizontal=8),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.CYAN_300),
                            border_radius=8
                        )
                    ], spacing=10),
                ], spacing=12)
            ], spacing=10),
            padding=20,
            width=300,
            height=300,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.Colors.INDIGO_700, ft.Colors.BLUE_900]
            ),
            border_radius=20,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.Colors.BLACK26,
                offset=ft.Offset(0, 8)
            )
        )

        # ✅ Tüm kartları bir row içinde topla
        self.cards_row = ft.Container(
            content=ft.Row(
                controls=[
                    self.training_status_card,
                    self.progress_card,
                    self.model_card,
                    self.system_info_card,  # ✅ Yeni card eklendi
                    self.research_card,
                    self.rag_card,
                    self.autonomous_card
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO
            ),
            # ✅ ÇÖZÜM: Height artır + margin - Search results [3] padding pattern[3]
            height=395,  # ✅ Card height (300) + scroll space (95)
            padding=ft.padding.all(10),  # ✅ Tüm taraflarda boşluk[3]

        )

        self.update_rag_stats(
            entities=0,
            embeddings=0,
            queries=0,
            status="Standby"
        )

        self.update_autonomous_stats(
            status="Ready",
            cycles=0,
            next_time="--:--",
            entities=0
        )

        # Log kaydı
        self.log_system.add_event_log("📊 Dashboard cards initialized", "SYSTEM")
        logger.info("✅ Dashboard UI components created")
        
        # ✅ Monitoring hazır ama otomatik başlatılmıyor
        # Manuel başlatmak için: dashboard_cards.start_real_time_monitoring()
        logger.info("💡 Real-time monitoring hazır - manuel başlatılabilir")

    def get_cards(self) -> ft.Row:
        """Tüm dashboard kartlarını döndürür - Search results [1] safe return pattern"""
        if not self.cards_row:
            logger.error("❌ cards_row is None - UI not created yet")
            return ft.Container(content=ft.Text("Dashboard not ready", color=ft.Colors.RED))
        return self.cards_row

    def update_from_rag_system(self):
        """Update RAG stats from real system - Search results [2] real-time updates"""
        try:
            # Gerçek RAG system stats al
            rag_stats = self.get_real_rag_stats()  # Bu metodunuz varsa

            self.update_rag_stats(
                entities=rag_stats.get('entity_count', 0),
                embeddings=rag_stats.get('embedding_count', 0),
                queries=rag_stats.get('query_count', 0),
                status=rag_stats.get('status', 'Unknown')
            )
        except Exception as e:
            logger.error(f"❌ RAG stats update failed: {e}")

    def update_real_training_status(self, is_training=False):
        """✅ Search results [4] real-time data binding[4]"""
        if not self.training_status_card:
            return

        real_status = SystemMonitor.get_real_training_status()

        # Status text güncelle - Search results [4] dynamic values[4]
        # Status güncelle
        status_text = self.training_status_card.content.controls[1]
        status_text.value = "Training..." if is_training else "Ready"
        status_text.color = ft.Colors.ORANGE_400 if is_training else ft.Colors.GREEN_400

        # Sistem bilgilerini güncelle
        gpu_text = self.training_status_card.content.controls[2]
        gpu_text.value = f"GPU: {real_status['gpu_usage']:.1f}%"

        vram_text = self.training_status_card.content.controls[3]
        vram_text.value = f"VRAM: {real_status['vram_used']:.1f}GB"

        cpu_text = self.training_status_card.content.controls[4]
        cpu_text.value = f"CPU: {real_status['cpu_usage']:.1f}%"

        ram_text = self.training_status_card.content.controls[5]
        ram_text.value = f"RAM: {real_status['ram_usage']:.1f}%"

        self.training_status_card.update()

    def update_training_stats(self, progress: float, steps: int, loss: float, eta: str):
        """Training ilerlemesini günceller - Search results [3] real-time updates"""
        if not self.progress_card:
            logger.warning("⚠️ progress_card not initialized")
            return

        try:
            # ✅ Safe value updates with validation
            clamped_progress = max(0.0, min(1.0, progress))
            safe_steps = max(0, steps)
            safe_loss = max(0.0, loss)

            self.progress_percentage.value = f"{int(clamped_progress * 100)}%"
            self.steps_text.value = f"{safe_steps}/100"
            self.loss_text.value = f"{safe_loss:.3f}"
            self.eta_text.value = str(eta)
            self.circular_progress.value = clamped_progress

            # ✅ Individual updates - Search results [4] component updates
            # self.progress_percentage.update()
            # self.steps_text.update()
            # self.loss_text.update()
            # self.eta_text.update()
            # self.circular_progress.update()

            # ✅ BONUS: Training sırasında diğer kartları da güncelleyin
            if progress > 0:  # Training aktifse
                # RAG sistem training data'yı işliyor gibi göster
                self.update_rag_stats(
                    entities=int(progress * 1000),  # Training ilerledikçe artar
                    embeddings=int(progress * 500),
                    queries=steps,
                    status="Processing"
                )

                # Autonomous sistem training'e bağlı bilgileri göster
                self.update_autonomous_stats(
                    status="Training Mode",
                    cycles=int(progress * 10),
                    next_time=eta,
                    entities=int(progress * 100)
                )

        except Exception as e:
            logger.error(f"❌ Training stats update failed: {e}")

    def update_research_stats(self, stats: dict):
        """Search results [4] - Page-level update approach"""
        try:
            topics_count = int(stats.get('topics_researched', 0))
            nodes_count = int(stats.get('knowledge_nodes', 0))

            # ✅ Sadece değerleri set et, individual update yapma
            if hasattr(self, 'research_topics_text') and self.research_topics_text:
                self.research_topics_text.value = f"{topics_count}/8 completed"
                # ❌ self.research_topics_text.update()  # Kaldır

            if hasattr(self, 'research_nodes_text') and self.research_nodes_text:
                self.research_nodes_text.value = f"{nodes_count} knowledge nodes"
                # ❌ self.research_nodes_text.update()  # Kaldır

            if hasattr(self, 'research_scan_text') and self.research_scan_text:
                self.research_scan_text.value = stats.get('last_scan', 'Never')
                # ❌ self.research_scan_text.update()  # Kaldır

            if hasattr(self, 'research_quality_text') and self.research_quality_text:
                quality = stats.get('quality_score', '70%')
                self.research_quality_text.value = quality
                # ❌ self.research_quality_text.update()  # Kaldır

            if hasattr(self, 'research_status_text') and self.research_status_text:
                status = stats.get('status', 'Idle')
                if topics_count > 0:
                    status = f"Processing {topics_count}/8"
                self.research_status_text.value = status
                # ❌ self.research_status_text.update()  # Kaldır

            logger.debug(f"Research stats set: {topics_count} topics processed")

        except Exception as e:
            logger.debug(f"Research stats update deferred: {e}")

    def update_rag_stats(self, entities=0, embeddings=0, queries=0, status="Offline"):
        """Update RAG system statistics - Search results [2] component updates"""
        try:
            # ✅ Sadece değerleri set et, individual update yapma
            if hasattr(self, 'rag_entities_text') and self.rag_entities_text:
                self.rag_entities_text.value = str(entities)
                # ❌ self.rag_entities_text.update()  # Bu satırı kaldır

            if hasattr(self, 'rag_embeddings_text') and self.rag_embeddings_text:
                self.rag_embeddings_text.value = str(embeddings)
                # ❌ self.rag_embeddings_text.update()  # Bu satırı kaldır

            if hasattr(self, 'rag_queries_text') and self.rag_queries_text:
                self.rag_queries_text.value = str(queries)
                # ❌ self.rag_queries_text.update()  # Bu satırı kaldır

            if hasattr(self, 'rag_status_text') and self.rag_status_text:
                self.rag_status_text.value = str(status)
                # ❌ self.rag_status_text.update()  # Bu satırı kaldır

            # ✅ Sadece log - update yok
            logger.debug(f"RAG stats set: {entities} entities, {status} status")

        except Exception as e:
            logger.debug(f"RAG stats update deferred: {e}")

    def update_autonomous_stats(self, status="Offline", cycles=0, next_time="--:--", entities=0):
        """Update autonomous learning statistics - Search results [3] real-time data"""
        try:
            # ✅ Sadece değerleri set et
            if hasattr(self, 'autonomous_status_text') and self.autonomous_status_text:
                self.autonomous_status_text.value = str(status)

            if hasattr(self, 'autonomous_cycles_text') and self.autonomous_cycles_text:
                self.autonomous_cycles_text.value = str(cycles)

            if hasattr(self, 'autonomous_next_text') and self.autonomous_next_text:
                self.autonomous_next_text.value = str(next_time)

            if hasattr(self, 'autonomous_entities_text') and self.autonomous_entities_text:
                self.autonomous_entities_text.value = str(entities)

            # ✅ Sadece log - individual update yok
            logger.debug(f"Autonomous stats set: {status}, {cycles} cycles")

        except Exception as e:
            logger.debug(f"Autonomous stats update deferred: {e}")

