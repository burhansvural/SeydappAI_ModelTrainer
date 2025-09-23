# src/ui/builder/control_panel.py

import flet as ft
import logging
import asyncio
import time
from pathlib import Path

logger = logging.getLogger(__name__)


class ControlPanel:
    """Kontrol butonları ve paneli"""

    def __init__(self, log_system, dashboard_cards):
        """✅ INIT: Log ve dashboard referanslarını al sadece - UI oluştur"""
        self.log_system = log_system
        self.dashboard_cards = dashboard_cards
        self.controls_row = None
        self.start_btn = None
        self.stop_btn = None
        self.config_btn = None
        self.research_btn = None
        self.rag_test_btn = None
        self.autonomous_btn = None
        self.force_train_btn = None
        self.running = False
        self.autonomous_running = False



    def create_controls(self, page):
        """✅ UI OLUŞTUR: Sayfa referansı ile UI oluştur
        """
        logger.info("🔧 Creating control panel UI components")

        # Start button
        self.start_btn = ft.Container(
            key="start_btn",
            content=ft.Row([
                ft.Icon(name=ft.Icons.ROCKET_LAUNCH, size=24, color=ft.Colors.WHITE),
                ft.Text("Start Training", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
            ], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
            padding=20,
            width=220,
            height=60,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.GREEN_500, ft.Colors.GREEN_700, ft.Colors.GREEN_900]
            ),
            border_radius=30,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.Colors.with_opacity(0.4, ft.Colors.GREEN_400),
                offset=ft.Offset(0, 5)
            ),
            on_click=self.start_training,
            ink=True,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            visible=True
        )

        # Stop button
        self.stop_btn = ft.Container(
            key="stop_btn",
            content=ft.Row([
                ft.Icon(name=ft.Icons.STOP_CIRCLE, size=24, color=ft.Colors.WHITE),
                ft.Text("Stop Training", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
            ], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
            padding=20,
            width=220,
            height=60,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.RED_500, ft.Colors.RED_700, ft.Colors.RED_900]
            ),
            border_radius=30,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.Colors.with_opacity(0.4, ft.Colors.RED_400),
                offset=ft.Offset(0, 5)
            ),
            on_click=self.stop_training,
            visible=True,
            disabled=True,
            ink=True,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT)
        )

        # Config button
        self.config_btn = ft.Container(
            key="config_btn",
            content=ft.Row([
                ft.Icon(name=ft.Icons.TUNE, size=24, color=ft.Colors.WHITE),
                ft.Text("Advanced Config", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
            ], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
            padding=20,
            width=220,
            height=60,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.BLUE_500, ft.Colors.BLUE_700, ft.Colors.INDIGO_900]
            ),
            border_radius=30,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=ft.Colors.with_opacity(0.4, ft.Colors.BLUE_400),
                offset=ft.Offset(0, 5)
            ),
            on_click=self.show_config_dialog,
            ink=True,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT)
        )

        self.research_btn = ft.Container(
            key="research_btn",
            content=ft.Row([
                ft.Icon(name=ft.Icons.SEARCH, size=24, color=ft.Colors.WHITE),
                ft.Text("Start Research", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
            ], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
            padding=20,
            width=220,
            height=60,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.CYAN_500, ft.Colors.CYAN_700, ft.Colors.BLUE_900]
            ),
            border_radius=30,
            on_click=self.start_research,
            ink=True,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT)
        )

        # RAG system test button
        self.rag_test_btn = ft.Container(
            key="rag_test_btn",
            content=ft.Row([
                ft.Icon(name=ft.Icons.PSYCHOLOGY, size=24, color=ft.Colors.WHITE),
                ft.Text("Test Knowledge RAG", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
            ], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
            padding=20,
            width=220,
            height=60,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.PURPLE_500, ft.Colors.PURPLE_700, ft.Colors.INDIGO_900]
            ),
            border_radius=30,
            on_click=self.test_rag_system,
            ink=True,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT)
        )

        # Autonomous Learning Control Button
        self.autonomous_btn = ft.Container(
            key="autonomous_btn",
            content=ft.Row([
                ft.Icon(name=ft.Icons.SMART_TOY, size=24, color=ft.Colors.WHITE),
                ft.Text("Start Autonomous", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
            ], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
            padding=20,
            width=220,
            height=60,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.CYAN_500, ft.Colors.CYAN_700, ft.Colors.BLUE_900]
            ),
            border_radius=30,
            on_click=self.toggle_autonomous_learning,
            ink=True,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT)
        )

        self.force_train_btn = ft.Container(
            key="force_train_btn",
            content=ft.Row([
                ft.Icon(name=ft.Icons.FLASH_ON, size=24, color=ft.Colors.WHITE),
                ft.Text("Force Training", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
            ], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
            padding=20,
            width=220,
            height=60,
            gradient=ft.LinearGradient(
                colors=[ft.Colors.ORANGE_500, ft.Colors.ORANGE_700, ft.Colors.DEEP_ORANGE_900]
            ),
            border_radius=30,
            on_click=self.force_training,
            ink=True,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT)
        )

        # Responsive container - tüm butonları içeren container
        self.controls_row = ft.Container(
            key="controls_container",
            content=ft.ResponsiveRow([
                ft.Container(content=self.start_btn, col={"sm": 12, "md": 6, "lg": 4, "xl": 2}),
                ft.Container(content=self.stop_btn, col={"sm": 12, "md": 6, "lg": 4, "xl": 2}),
                ft.Container(content=self.config_btn, col={"sm": 12, "md": 6, "lg": 4, "xl": 2}),
                ft.Container(content=self.research_btn, col={"sm": 12, "md": 6, "lg": 4, "xl": 2}),
                ft.Container(content=self.rag_test_btn, col={"sm": 12, "md": 6, "lg": 4, "xl": 2}),
                ft.Container(content=self.autonomous_btn, col={"sm": 12, "md": 6, "lg": 4, "xl": 2}),
                ft.Container(content=self.force_train_btn, col={"sm": 12, "md": 6, "lg": 4, "xl": 2})
            ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            padding=25
        )

        self.log_system.add_event_log("🎮 Control panel initialized", "SYSTEM")
        logger.info("✅ Control panel UI components created")

    def get_controls(self) -> ft.Container:
        """
        Tüm
        kontrol
        elemanlarını
        döndürür
        """
        if not self.controls_row:
            logger.warning("⚠️ Control panel UI not created yet")
        return self.controls_row

    async def _delayed_click(self, e, original_function):
        """
        Search
        results[5]
        pattern: Thread - safe
        update
        """
        # UI'nin yanıt vermesi için biraz zaman ver
        await asyncio.sleep(0.1)
        # Orijinal fonksiyonu çağır
        await original_function(e)

    def _training_worker_sync(self):
        """✅ Real-time worker with live system monitoring - Search results [1] pattern[1]"""
        import time

        # ✅ Real-time monitoring başlat[1]
        self.dashboard_cards.start_real_time_monitoring()

        for step in range(1, 101):
            if not self.running:
                break

            loss = max(2.5 - (step * 0.025), 0.001)

            # ✅ Her adımda training status güncelle[1]
            self.dashboard_cards.update_real_training_status(is_training=True)

            # Progress güncelle
            self.dashboard_cards.update_training_stats(
                step / 100,
                step,
                round(loss, 3),
                f"{(100 - step) * 0.4:.0f}s"
            )

            time.sleep(0.05)

        # ✅ Training bittiğinde monitoring durdur[1]
        self.dashboard_cards.stop_real_time_monitoring()

        if self.running:
            # ✅ Auto-completion - user action değil
            logger.info("🎉 Training completed automatically")

            # UI state güncelle - stop_training() kullanma
            self.start_btn.disabled = False
            self.stop_btn.disabled = True
            self.controls_row.update()

            # Monitoring durdur
            self.dashboard_cards.update_real_training_status(is_training=False)
            self.dashboard_cards.stop_real_time_monitoring()

            # State güncelle
            self.running = False

            # ✅ Doğru completion messages
            self.log_system.add_event_log("🎉 Training completed successfully!", "SUCCESS")
            self.log_system.add_event_log("✨ Model ready for use!", "SYSTEM")

    def start_training(self, e):
        """
        Training
        başlama
        fonksiyonu - SEARCH
        RESULTS[4]
        pattern
        """
        logger.info("🚀 Training started by user")

        # Buton görünürlüklerini güncelle - Önce text değerlerini güncelle
        self.start_btn.disabled = True
        self.stop_btn.disabled = False


        # UI güncelle - SEARCH RESULTS [5] - Flet'in Thread-safe update'i
        self.controls_row.update()

        # Log kaydı
        self.log_system.add_event_log("🚀 Training started", "TRAINING")

        # Trainingi başlatacak thread'i tetikle
        self.running = True
        import threading
        threading.Thread(target=self._training_worker_sync, daemon=True).start()

    def stop_training(self, e):
        """
        Training
        durdurma
        fonksiyonu
        """
        logger.info("⏹️ Training stopped by user")

        # Buton görünürlüklerini güncelle - Önce text değerlerini güncelle
        self.start_btn.disabled = False
        self.stop_btn.disabled = True

        # UI güncelle
        self.controls_row.update()

        # Log kaydı
        self.log_system.add_event_log("⏹️ Training stopped", "TRAINING")

        # Training durdur
        self.running = False

    def show_config_dialog(self, e):
        """
        Config
        dialog
        göster
        """
        logger.info("⚙️ Advanced config dialog opened")

        config_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("⚙️ Advanced Training Configuration"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("🔧 Advanced settings will be available in next update"),
                    ft.Divider(),
                    ft.Text("Current optimal settings for RTX 3060:"),
                    ft.Text("• Model: StarCoder2-3b", size=12),
                    ft.Text("• Batch Size: 2", size=12),
                    ft.Text("• Sequence Length: 4096", size=12),
                    ft.Text("• LoRA Rank: 16", size=12),
                ], spacing=10),
                width=400,
                height=200
            ),
            actions=[
                ft.TextButton("Close", on_click=self.close_config_dialog)
            ]
        )

        self.config_dialog = config_dialog
        self.log_system.page.overlay.append(config_dialog)
        config_dialog.open = True
        self.log_system.page.update()

        # Log kaydı
        self.log_system.add_event_log("⚙️ Advanced config dialog opened", "CONFIG")

    def close_config_dialog(self, e):
        """
        Config
        dialog
        kapatma
        fonksiyonu
        """
        if hasattr(self, 'config_dialog'):
            self.config_dialog.open = False
            self.log_system.page.update()
            self.log_system.add_event_log("⚙️ Advanced config dialog closed", "CONFIG")

    def start_research(self, e):
        """✅ FIXED: Research başlatma - Search results [3] named logger[3]"""
        logger.info("🔍 Research started by user")
        logger.debug("🔧 Research button clicked - initializing worker thread")  # ✅ EKLE

        self.log_system.add_event_log("🔍 Starting research cycle...", "RESEARCH")

        # ✅ Threading kullan - detailed logging[1]
        import threading
        research_thread = threading.Thread(target=self._research_worker_sync, daemon=True)
        logger.debug(f"🧵 Research thread created: {research_thread.name}")  # ✅ EKLE
        research_thread.start()
        logger.info("✅ Research worker thread started successfully")  # ✅ EKLE

    def test_rag_system(self, e):
        """
        RAG
        sistemini
        test
        etme
        fonksiyonu
        """
        logger.info("🧠 Testing RAG system")
        self.log_system.add_event_log("🧠 Testing Knowledge Graph RAG system...", "RAG")
        import threading
        threading.Thread(target=self._rag_test_worker_sync, daemon=True).start()

    def toggle_autonomous_learning(self, e):
        """
        Autonomous
        learning
        'i toggle etme fonksiyonu"""
        if self.autonomous_running:
            self._stop_autonomous_learning(e)
        else:
            self._start_autonomous_learning(e)

    def _start_autonomous_learning(self, e):
        """Autonomous learning'i başlatma"""
        logger.info("🤖 Starting autonomous learning")

        # Button appearance update
        if self.autonomous_btn:
            self.autonomous_btn.content = ft.Row([
                ft.Icon(name=ft.Icons.STOP, size=24, color=ft.Colors.WHITE),
                ft.Text("Stop Autonomous", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
            ], spacing=12, alignment=ft.MainAxisAlignment.CENTER)

            self.autonomous_btn.gradient = ft.LinearGradient(
                colors=[ft.Colors.RED_500, ft.Colors.RED_700, ft.Colors.RED_900]
            )
            self.autonomous_btn.update()

        # State update
        self.autonomous_running = True

        # Log and start
        self.log_system.add_event_log("🤖 Autonomous learning system STARTED!", "AUTO")
        asyncio.create_task(self._autonomous_worker())

    def _stop_autonomous_learning(self, e):
        """Autonomous learning'i durdurma"""
        logger.info("🛑 Stopping autonomous learning")

        # Button appearance update
        if self.autonomous_btn:
            self.autonomous_btn.content = ft.Row([
                ft.Icon(name=ft.Icons.SMART_TOY, size=24, color=ft.Colors.WHITE),
                ft.Text("Start Autonomous", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
            ], spacing=12, alignment=ft.MainAxisAlignment.CENTER)

            self.autonomous_btn.gradient = ft.LinearGradient(
                colors=[ft.Colors.CYAN_500, ft.Colors.CYAN_700, ft.Colors.BLUE_900]
            )
            self.autonomous_btn.update()

        # State update
        self.autonomous_running = False

        # Log update
        self.log_system.add_event_log("🛑 Autonomous learning system STOPPED!", "AUTO")

    def force_training(self, e):
        """Scheduled training'i zorla başlatma"""
        logger.info("🔥 Forcing training cycle now")
        self.log_system.add_event_log("🔥 FORCING training cycle NOW...", "TRAINING")
        import threading
        threading.Thread(target=self._force_training_worker_sync, daemon=True).start()

    async def _training_worker(self):
        """Reel training process (simulated)"""
        for step in range(1, 201):
            if not self.running:
                break

            loss = max(2.5 - (step * 0.012), 0.001)
            eta = int((100 - step) * 0.4)

            # Training istatistiklerini güncelle
            self.dashboard_cards.update_training_stats(
                step / 200,
                step,
                round(loss, 4),
                f"{(200 - step) * 0.05:.1f}s"
            )

            # 100ms bekle
            await asyncio.sleep(0.1)

        if self.running:
            self.log_system.add_event_log("🎉 Training completed!", "SUCCESS")

            # ✅ Manual stop değil, auto-complete - Search results [1] pattern[1]
            self.start_btn.disabled = False
            self.stop_btn.disabled = True
            self.controls_row.update()
            self.dashboard_cards.update_real_training_status(is_training=False)
            self.dashboard_cards.stop_real_time_monitoring()
            self.running = False

    def _research_worker_sync(self):
        """✅ SYNC research worker - Search results [1] best practices[1]"""
        import time

        # ✅ DETAYLI LOGGING - Search results [1] application details[1]
        logger.info("🔍 Research worker thread başlatıldı")
        logger.debug("🔧 Research worker: Initializing research pipeline")

        try:
            self.log_system.add_event_log("🔍 Starting web research task...", "RESEARCH")
            logger.debug("📝 Research log event added to system")

            # Research steps - Search results [1] structured logging[1]
            research_steps = [
                ("🌐 Initializing crawler...", 10),
                ("🔍 Analyzing topic structures...", 25),
                ("📚 Indexing technical documentation...", 45),
                ("💡 Extracting key concepts...", 70),
                ("📊 Building knowledge graph...", 90),
                ("✅ Research complete!", 100)
            ]

            logger.info(f"📊 Research pipeline: {len(research_steps)} steps planned")  # ✅ EKLE

            for i, (message, progress) in enumerate(research_steps):
                logger.debug(f"🔄 Research Step {i + 1}/{len(research_steps)}: {message} ({progress}%)")  # ✅ EKLE

                # Progress güncelle - Search results [1] sync update[1]
                self.log_system.add_event_log(message, "RESEARCH")

                # ✅ Dashboard card güncelleme - detaylı logging[3]
                research_stats = {
                    "topics_researched": min(progress // 20, 5),  # ✅ Realistic progression
                    "knowledge_nodes": progress // 2,
                    "last_scan": "Just now",
                    "quality_score": progress / 100,
                    "status": "Active" if progress < 100 else "Complete"
                }

                logger.debug(f"📊 Updating research stats: {research_stats}")  # ✅ EKLE
                self.dashboard_cards.update_research_stats(research_stats)

                time.sleep(1.5)  # Sync sleep
                logger.debug(f"⏱️ Research step {i + 1} completed, waiting 1.5s")  # ✅ EKLE

            logger.info("✅ Research worker completed successfully")  # ✅ EKLE
            self.log_system.add_event_log("✨ A total of 5 topics researched!", "SUCCESS")

        except Exception as e:
            # ✅ Search results [1] exception logging best practice[1]
            logger.error(f"❌ Research worker error: {str(e)}", exc_info=True)  # ✅ EKLE: exc_info=True
            self.log_system.add_event_log(f"❌ Research error: {str(e)}", "ERROR")
            logger.debug("🔧 Research worker thread terminated due to error")  # ✅ EKLE

    def _rag_test_worker_sync(self):
        """Simulated RAG test process"""
        try:
            self.log_system.add_event_log("🧠 Initializing Knowledge Graph RAG...", "RAG")

            # Simulated RAG system steps
            rag_steps = [
                ("📊 Loading knowledge base...", 15),
                ("🔍 Building entity relations...", 35),
                ("💡 Calculating embedding vectors...", 60),
                ("✨ Optimizing retrieval efficiency...", 85),
                ("✅ RAG system ready!", 100)
            ]

            for message, progress in rag_steps:
                self.log_system.add_event_log(message, "RAG")
                self.dashboard_cards.update_research_stats({
                    "knowledge_entities": progress,
                    "status": "Active" if progress < 100 else "Ready"
                })
                time.sleep(1.2)

            self.log_system.add_event_log("🧪 RAG system test completed successfully!", "SUCCESS")

        except Exception as e:
            self.log_system.add_event_log(f"❌ RAG error: {str(e)}", "ERROR")

    async def _autonomous_worker(self):
        """Autonomous learning simulator"""
        try:
            cycle = 1
            while self.autonomous_running:
                self.log_system.add_event_log(f"🤖 Starting Autonomous Cycle #{cycle}", "AUTO")

                # Research phase
                self.log_system.add_event_log("🔍 Phase 1: Web research", "AUTO")
                await self._simulated_research_task()

                # Knowledge processing
                self.log_system.add_event_log("🧠 Phase 2: Knowledge processing", "AUTO")
                await self._simulated_knowledge_process()

                # Training phase
                self.log_system.add_event_log("🚀 Phase 3: Model training", "AUTO")
                await self._simulated_training_task()

                cycle += 1
                # Sonraki cycle için 5 saniye bekle
                for i in range(5, 0, -1):
                    status = f"⏰ Autonomous cycle will start in {i} seconds..."
                    self.dashboard_cards.update_research_stats({
                        "status": status,
                        "completed_cycles": cycle,
                        "next_training": f"in {i} sec"
                    })
                    await asyncio.sleep(1)

        except Exception as e:
            self.log_system.add_event_log(f"❌ Autonomous error: {str(e)}", "ERROR")
            self.autonomous_running = False

    async def _simulated_research_task(self):
        """Simulated research task for autonomous cycle"""
        # Simulate incremental progress
        for p in range(0, 101, 10):
            self.dashboard_cards.update_research_stats({
                "status": f"Web crawling ({p}%)",
                "knowledge_nodes": p * 5,
                "last_scan": "Now"
            })
            await asyncio.sleep(0.3)

    async def _simulated_knowledge_process(self):
        """Simulated knowledge process for autonomous cycle"""
        # Simulate incremental progress
        for p in range(0, 101, 5):
            self.dashboard_cards.update_research_stats({
                "status": f"Knowledge processing ({p}%)",
                "quality_score": p / 100.0
            })
            await asyncio.sleep(0.1)

    async def _simulated_training_task(self):
        """Simulated training task for autonomous cycle"""
        # Simulate incremental progress
        for step in range(0, 101, 2):
            self.dashboard_cards.update_training_stats(
                step / 100,
                step,
                round(5.0 - (step * 0.04), 3),
                f"{(100 - step) * 0.2:.0f}:00"
            )
            await asyncio.sleep(0.1)

        self.log_system.add_event_log("🎉 Autonomous training cycle completed!", "SUCCESS")
        self.dashboard_cards.update_research_stats({
            "status": "Cycle completed!",
            "next_training": "in 5 sec"
        })

    def _force_training_worker_sync(self):
        """Forced training immediately"""
        try:
            self.log_system.add_event_log("🔥 Executing immediate training cycle...", "TRAINING")

            # Kişisel training steps
            training_steps = [
                ("📦 Preparing training data...", 20),
                ("🔧 Loading neural architecture...", 40),
                ("🧠 Initializing quantum weights...", 60),
                ("⚡ Optimizing parameter space...", 80),
                ("✅ Training complete!", 100)
            ]

            for message, progress in training_steps:
                self.log_system.add_event_log(message, "TRAINING")
                self.dashboard_cards.update_training_stats(
                    progress / 100,
                    progress,
                    round(1.0 - (progress * 0.008), 3),
                    f"{(100 - progress) // 2}:00"
                )
                time.sleep(1.0)

            self.log_system.add_event_log("✨ AI skill level improved!", "SUCCESS")

        except Exception as e:
            self.log_system.add_event_log(f"❌ Force training failed: {str(e)}", "ERROR")
