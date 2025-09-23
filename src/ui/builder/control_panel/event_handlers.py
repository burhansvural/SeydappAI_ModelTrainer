# src/ui/builder/control_panel/event_handlers.py
"""
🎯 Event Handlers - Kullanıcı Etkileşim Yönetici
Bu dosya tüm button click ve user interaction event'lerini yönetir
Python class yapısını kullanarak organized event handling sağlar[1][4]
"""

import logging
import threading
import time
import json
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class EventHandlers:
    """
    Control Panel event handler'larını yöneten sınıf

    Bu sınıf Python'ın nesne tabanlı programlama özelliklerini kullanır[1]
    - self parametresi ile instance method'ları tanımlar
    - __init__ constructor'da başlangıç durumunu ayarlar
    - Encapsulation ile event logic'i organize eder
    """

    def __init__(self, control_panel_instance):
        """
        Event Handler sınıfının constructor'ı[1]

        Args:
            control_panel_instance: Ana control panel referansı

        Python sınıf yapısına göre:
        - __init__ metodu obje oluşturulurken çağrılır[4]
        - self parametresi instance'a referans verir[1]
        - Instance nitelikleri (self.variable) tanımlanır
        """
        logger.info("🎯 Initializing EventHandlers")

        # Ana control panel referansı - composition pattern
        self.control_panel = control_panel_instance

        # Event durumlarını takip eden instance nitelikleri[1]
        self._event_lock = threading.Lock()  # Thread-safe event handling
        self._last_click_time = 0.0  # Double-click koruması
        self._click_cooldown = 1.0  # Minimum click aralığı (saniye)
        
        # ✅ Model ve profil seçimi state'leri
        self.selected_model = "bigcode/starcoder2-3b"  # Default model
        self.selected_profile = "rtx3060_optimized"    # Default profile
        self.profile_descriptions = {
            "micro_test": "Hızlı test için minimal ayarlar",
            "rtx3060_optimized": "RTX 3060 için optimize edilmiş ayarlar", 
            "production": "Tam kapsamlı production training"
        }

        logger.info("✅ EventHandlers initialized with thread safety")

    def toggle_autonomous_learning(self, event):
        """
        Otonom öğrenme toggle event handler'ı

        Args:
            event: Flet click event object'i

        Bu method[1]:
        - Instance method olarak tanımlanmıştır (self parametresi ile)
        - Click event'ini handle eder
        - State management yapar
        - Thread-safe operations sağlar
        """
        # Double-click koruması - RTX 3060 için önemli
        current_time = time.time()
        if current_time - self._last_click_time < self._click_cooldown:
            logger.debug("🛡️ Click ignored - too fast")
            return

        self._last_click_time = current_time

        try:
            logger.info("🔄 Autonomous learning toggle requested")

            # Thread-safe state check
            with self._event_lock:
                if self.control_panel.autonomous_running:
                    self._handle_stop_autonomous()
                    # ✅ Button'u Start moduna çevir
                    self._update_button_to_start_mode()
                else:
                    self._handle_start_autonomous()
                    # ✅ Button'u Stop moduna çevir
                    self._update_button_to_stop_mode()

        except Exception as ex:
            logger.error(f"❌ Toggle event failed: {ex}")
            self._handle_event_error("Toggle hatası", str(ex))

    def _update_button_to_stop_mode(self):
        """Button'u Stop moduna çevir - Flet best practices[1][2]"""
        try:
            logger.debug("🔄 Updating button to STOP mode")

            # ✅ Search results[5]: Proper disabled state management
            if hasattr(self.control_panel, 'ui_components_manager'):
                manager = self.control_panel.ui_components_manager

                # ✅ Button reference kontrolü
                if hasattr(manager, 'button_references'):
                    autonomous_btn = manager.button_references.get('autonomous_button')

                    if autonomous_btn:
                        # ✅ Search results[2]: Control state management
                        try:
                            # Text ve icon değiştir
                            if hasattr(autonomous_btn, 'text'):
                                autonomous_btn.text = "⏹️ Stop Training"

                            # ✅ Search results[5]: Color state management
                            if hasattr(autonomous_btn, 'bgcolor'):
                                autonomous_btn.bgcolor = ft.Colors.RED_500

                            if hasattr(autonomous_btn, 'color'):
                                autonomous_btn.color = ft.Colors.WHITE

                            # ✅ Search results[2]: Disabled state
                            autonomous_btn.disabled = False  # Keep enabled for stop

                            logger.debug("✅ Button properties updated")

                        except Exception as btn_error:
                            logger.error(f"❌ Button property update failed: {btn_error}")
                            # ✅ Fallback: Update via content structure
                            self._update_button_content_fallback(autonomous_btn, "stop")

                        # ✅ Search results[1]: Essential page.update() call
                        self.control_panel.safe_page_update()
                        logger.debug("✅ Button updated to STOP mode successfully")

                    else:
                        logger.error("❌ Button reference not found!")
                        self._debug_available_references(manager)
                else:
                    logger.error("❌ Button references not available!")

        except Exception as e:
            logger.error(f"❌ Button update to stop mode failed: {e}")

    def _update_button_content_fallback(self, button, mode: str):
        """Fallback method for button update[1]"""
        try:
            if mode == "stop":
                # Try different content structures
                if hasattr(button, 'content'):
                    if hasattr(button.content, 'controls'):
                        # Container with controls
                        for control in button.content.controls:
                            if hasattr(control, 'value') and "Start" in str(control.value):
                                control.value = "⏹️ Stop Training"
                    elif hasattr(button.content, 'value'):
                        # Direct text content
                        button.content.value = "⏹️ Stop Training"

            elif mode == "start":
                # Similar logic for start mode
                if hasattr(button, 'content'):
                    if hasattr(button.content, 'controls'):
                        for control in button.content.controls:
                            if hasattr(control, 'value') and "Stop" in str(control.value):
                                control.value = "🤖 Start Autonomous Training"
                    elif hasattr(button.content, 'value'):
                        button.content.value = "🤖 Start Autonomous Training"

            logger.debug(f"✅ Fallback content update completed for {mode} mode")

        except Exception as e:
            logger.error(f"❌ Fallback content update failed: {e}")

    def _debug_available_references(self, manager):
        """Debug available button references[3]"""
        try:
            if hasattr(manager, 'button_references'):
                available = list(manager.button_references.keys())
                logger.debug(f"Available button references: {available}")

                # Try to find autonomous button with different keys
                for key in available:
                    if 'autonomous' in key.lower() or 'start' in key.lower():
                        logger.debug(f"Found potential autonomous button: {key}")
            else:
                logger.debug("No button_references attribute found")

        except Exception as e:
            logger.error(f"❌ Debug references failed: {e}")


    def _update_button_to_start_mode(self):
        """Button'u Start moduna çevir - SYNC VERSION[1][5]"""
        try:
            if hasattr(self.control_panel, 'ui_components_manager'):
                manager = self.control_panel.ui_components_manager
                autonomous_btn = manager.button_references.get('autonomous_button')

                if autonomous_btn:
                    logger.debug("🔄 Updating button to START mode")

                    # Text değiştir
                    try:
                        if hasattr(autonomous_btn, 'content') and autonomous_btn.content:
                            if hasattr(autonomous_btn.content, 'content'):
                                content_items = autonomous_btn.content.content
                                if len(content_items) > 1:
                                    # İkon text
                                    if hasattr(content_items, 'value'):
                                        content_items.value = "🤖"

                                    # Ana text container
                                    if hasattr(content_items[1], 'content') and len(content_items[1].content) > 0:
                                        content_items[1].content.value = "Start Autonomous Training"
                                        if len(content_items[1].content) > 1:
                                            content_items[1].content[1].value = "AI will learn automatically"

                        # ✅ Search results[1]: Success state visual feedback
                        autonomous_btn.gradient = ft.LinearGradient(
                            colors=[ft.Colors.PURPLE_500, ft.Colors.PURPLE_700, ft.Colors.INDIGO_900]
                        )

                        # ✅ Button enabled[2]
                        autonomous_btn.disabled = False

                        logger.debug("✅ Button updated to START mode")

                    except Exception as content_error:
                        logger.error(f"❌ Button content update failed: {content_error}")

                    # Page update
                    self.control_panel.safe_page_update()

        except Exception as e:
            logger.error(f"❌ Button update to start mode failed: {e}")

    def _handle_start_autonomous(self) -> bool:
        """Start autonomous - return success status[1]"""
        logger.info("🚀 Starting autonomous learning process")

        try:
            # 1. Topic'leri yükle
            topics = self._load_learning_topics()
            if not topics:
                self._show_no_topics_warning()
                return False

            # 2. Autonomous manager'ı başlat
            success = self.control_panel.autonomous_manager.start_learning(topics)

            if success:
                # 2.5. ✅ Training coordinator'ı başlat - EKSİK OLAN BU!
                if hasattr(self.control_panel, 'training_coordinator'):
                    coordinator_started = self.control_panel.training_coordinator.start_coordinator()
                    if not coordinator_started:
                        logger.warning("⚠️ Training coordinator failed to start")
                    else:
                        logger.info("✅ Training coordinator started successfully")
                else:
                    logger.error("❌ Training coordinator not available")

                # 3. Progress monitoring başlat
                self.control_panel.progress_monitor.start_monitoring()

                # 4. Success logging
                self.control_panel.log_system.add_event_log(
                    f"🚀 {len(topics)} konu için öğrenme başlatıldı",
                    "AUTO"
                )

                logger.info(f"✅ Autonomous learning started with {len(topics)} topics")
                return True
            else:
                self._handle_start_failure()
                return False

        except Exception as e:
            logger.error(f"❌ Start autonomous failed: {e}")
            self._handle_event_error("Başlatma hatası", str(e))
            return False

    def _handle_stop_autonomous(self):
        """
        Otonom öğrenme durdurma işlemlerini yöneten private method

        Güvenli shutdown sequence:
        1. Manager'a stop sinyali gönder
        2. Thread'leri bekle
        3. UI'ı inactive state'e güncelle
        4. Resources temizle
        """
        logger.info("⏹️ Stopping autonomous learning")

        try:
            # 1. Manager'ı durdur
            self.control_panel.autonomous_manager.stop_learning()

            if hasattr(self.control_panel, 'training_coordinator'):
                self.control_panel.training_coordinator.stop_coordinator()
                logger.info("✅ Training coordinator stopped")

            # 2. Monitoring'i durdur
            self.control_panel.progress_monitor.stop_monitoring()

            # 3. UI'ı inactive state'e güncelle
            self._update_ui_to_inactive_state()

            # 4. Success logging
            self.control_panel.log_system.add_event_log(
                "⏹️ Otonom öğrenme durduruldu",
                "WARNING"
            )

            logger.info("✅ Autonomous learning stopped successfully")

        except Exception as e:
            logger.error(f"❌ Stop autonomous failed: {e}")
            self._handle_event_error("Durdurma hatası", str(e))

    def _debug_button_structure(self):
        """Button structure'ını debug et"""
        try:
            if hasattr(self.control_panel, 'ui_components_manager'):
                manager = self.control_panel.ui_components_manager
                autonomous_btn = manager.button_references.get('autonomous_button')

                if autonomous_btn:
                    logger.debug(f"Button found: {type(autonomous_btn)}")
                    logger.debug(f"Button content: {hasattr(autonomous_btn, 'content')}")

                    if hasattr(autonomous_btn, 'content'):
                        logger.debug(f"Content type: {type(autonomous_btn.content)}")
                        if hasattr(autonomous_btn.content, 'content'):
                            logger.debug(f"Content items: {len(autonomous_btn.content.content)}")
                else:
                    logger.error("❌ Button reference not found!")
                    # List all available references
                    logger.debug(f"Available references: {list(manager.button_references.keys())}")

        except Exception as e:
            logger.error(f"❌ Button debug failed: {e}")

    def start_quick_research(self, event):
        """
        Hızlı araştırma başlatma event handler'ı

        Args:
            event: Flet click event

        Bu method quick research workflow'unu manage eder:
        - User feedback sağlar
        - Background process başlatır
        - Progress updates verir
        """
        logger.info("🔍 Quick research event triggered")

        try:
            # Double-click koruması
            current_time = time.time()
            if current_time - self._last_click_time < self._click_cooldown:
                return

            self._last_click_time = current_time

            # Research workflow başlat
            self._execute_quick_research_workflow()

        except Exception as e:
            logger.error(f"❌ Quick research event failed: {e}")
            self._handle_event_error("Araştırma hatası", str(e))

    def _execute_quick_research_workflow(self):
        """
        Hızlı araştırma workflow'unu execute eden private method

        Workflow steps:
        1. UI feedback başlat
        2. Background research thread başlat
        3. Progress updates sağla
        4. Results handle et
        """

        def research_worker():
            """
            Background research worker function
            Nested function olarak tanımlanmış - closure kullanır
            """
            try:
                # Research simulation steps
                research_steps = [
                    ("🌐 Web kaynakları taranıyor...", 1.5),
                    ("📚 Bilgi çıkarılıyor...", 2.0),
                    ("🧠 Bilgi işleniyor...", 1.5),
                    ("💾 Araştırma verisi kaydediliyor...", 1.0),
                    ("✅ Hızlı araştırma tamamlandı!", 0.5)
                ]

                for step_text, duration in research_steps:
                    # Her adımı logla
                    self.control_panel.log_system.add_event_log(step_text, "RESEARCH")

                    # Simulated processing time
                    time.sleep(duration)

                    # UI progress update
                    self._update_research_progress(step_text)

                logger.info("✅ Quick research workflow completed")

            except Exception as e:
                logger.error(f"❌ Research worker failed: {e}")
                self.control_panel.log_system.add_event_log(
                    f"❌ Araştırma hatası: {e}",
                    "ERROR"
                )

        # Background thread başlat
        research_thread = threading.Thread(
            target=research_worker,
            name="QuickResearchWorker",
            daemon=True
        )

        # Thread'i active threads listesine ekle
        self.control_panel.active_threads.append(research_thread)
        research_thread.start()

        logger.info("✅ Quick research thread started")

    def stop_all_processes(self, event):
        """
        Tüm işlemleri durdurma event handler'ı

        Args:
            event: Flet click event

        Emergency stop functionality:
        - Tüm running processes'leri durdurur
        - Thread'leri terminate eder
        - UI'ı safe state'e resetler
        - Resources temizler
        """
        logger.info("🛑 Stop all processes event triggered")

        try:
            # Double-click koruması
            current_time = time.time()
            if current_time - self._last_click_time < self._click_cooldown:
                return

            self._last_click_time = current_time

            # Emergency shutdown sequence
            self._execute_emergency_shutdown()

        except Exception as e:
            logger.error(f"❌ Stop all processes failed: {e}")
            self._handle_event_error("Durdurma hatası", str(e))

    def _execute_emergency_shutdown(self):
        """
        Emergency shutdown sequence'ını execute eden method

        Shutdown order (önemli sıralama):
        1. Autonomous learning durdur
        2. Research processes durdur
        3. Progress monitoring durdur
        4. UI'ı reset et
        5. Memory cleanup
        """
        logger.info("🚨 Executing emergency shutdown sequence")

        try:
            # 1. Tüm boolean flag'leri false yap
            self.control_panel.autonomous_running = False
            self.control_panel.research_running = False

            # 2. Manager'ları durdur
            if hasattr(self.control_panel, 'autonomous_manager'):
                self.control_panel.autonomous_manager.emergency_stop()

            if hasattr(self.control_panel, 'progress_monitor'):
                self.control_panel.progress_monitor.emergency_stop()

            # 3. UI'ı inactive state'e resetle
            self._reset_all_ui_states()

            # 4. Thread cleanup
            self.control_panel.cleanup_threads()

            # 5. Success logging
            self.control_panel.log_system.add_event_log(
                "⏹️ Tüm işlemler emergency stop ile durduruldu",
                "SYSTEM"
            )

            logger.info("✅ Emergency shutdown completed")

        except Exception as e:
            logger.error(f"❌ Emergency shutdown failed: {e}")

    def _load_learning_topics(self) -> List[str]:
        """
        Öğrenme konularını dosyadan yükleyen utility method

        Returns:
            List[str]: Topic'lerin listesi

        File handling pattern:
        - Path kullanarak modern dosya işlemleri
        - JSON parsing ile structured data
        - Exception handling ile error tolerance
        """
        try:
            topics_file = Path("datasets/conversations/user_topics.jsonl")
            topics = []

            if topics_file.exists():
                with open(topics_file, 'r', encoding='utf-8') as f:
                    for line_number, line in enumerate(f, 1):
                        if line.strip():
                            try:
                                data = json.loads(line.strip())
                                if data.get('topic'):
                                    topics.append(data['topic'])
                            except json.JSONDecodeError as json_error:
                                logger.debug(f"JSON parse error at line {line_number}: {json_error}")
                                continue

            logger.info(f"📚 Loaded {len(topics)} learning topics")
            return topics

        except Exception as e:
            logger.error(f"❌ Topic loading failed: {e}")
            return []

    def _update_ui_to_active_state(self):
        """UI'ı active state'e güncelleyen method"""
        try:
            if hasattr(self.control_panel, 'autonomous_btn') and self.control_panel.autonomous_btn:
                # Button'ı active görünüme güncelle (implementation UI'da)
                pass

            if hasattr(self.control_panel, 'stop_btn') and self.control_panel.stop_btn:
                self.control_panel.stop_btn.disabled = False
                self.control_panel.stop_btn.update()

            # Page update
            self.control_panel.safe_page_update()

        except Exception as e:
            logger.debug(f"UI update error: {e}")

    def _update_ui_to_inactive_state(self):
        """UI'ı inactive state'e güncelleyen method"""
        try:
            if hasattr(self.control_panel, 'stop_btn') and self.control_panel.stop_btn:
                self.control_panel.stop_btn.disabled = True
                self.control_panel.stop_btn.update()

            # Page update
            self.control_panel.safe_page_update()

        except Exception as e:
            logger.debug(f"UI update error: {e}")

    def _reset_all_ui_states(self):
        """Tüm UI elemanlarını initial state'e resetleyen method"""
        try:
            self._update_ui_to_inactive_state()

            # Status text reset
            if hasattr(self.control_panel, 'status_text') and self.control_panel.status_text:
                self.control_panel.status_text.value = "⏹️ Tüm işlemler durduruldu"
                self.control_panel.status_text.color = "red"

            # Progress bar reset
            if hasattr(self.control_panel, 'progress_bar') and self.control_panel.progress_bar:
                self.control_panel.progress_bar.value = 0.0

            self.control_panel.safe_page_update()

        except Exception as e:
            logger.debug(f"UI reset error: {e}")

    def _handle_event_error(self, error_type: str, error_message: str):
        """Event error'larını handle eden utility method"""
        self.control_panel.log_system.add_event_log(
            f"❌ {error_type}: {error_message}",
            "ERROR"
        )

    def _show_no_topics_warning(self):
        """Topic bulunamadığında warning gösteren method"""
        self.control_panel.log_system.add_event_log(
            "⚠️ Öğrenme konuları bulunamadı!",
            "WARNING"
        )

    def _handle_start_failure(self):
        """Başlatma başarısızlığını handle eden method"""
        self.control_panel.log_system.add_event_log(
            "❌ Otonom öğrenme başlatılamadı",
            "ERROR"
        )

    def _update_research_progress(self, step_text: str):
        """Research progress'ini güncelleyen method"""
        try:
            if hasattr(self.control_panel, 'status_text') and self.control_panel.status_text:
                self.control_panel.status_text.value = step_text
                self.control_panel.safe_page_update()
        except Exception as e:
            logger.debug(f"Progress update error: {e}")

    # ✅ Yeni Event Handler Metodları - Model ve Profil Seçimi

    def on_model_change(self, event):
        """Model seçimi değiştiğinde çağrılan event handler"""
        try:
            new_model = event.control.value
            logger.info(f"🤖 Model changed: {self.selected_model} -> {new_model}")
            
            self.selected_model = new_model
            
            # Log event
            self.control_panel.log_system.add_event_log(
                f"🤖 Model seçildi: {new_model}",
                "SYSTEM"
            )
            
            # Status güncelle
            if hasattr(self.control_panel, 'status_text') and self.control_panel.status_text:
                self.control_panel.status_text.value = f"Model: {new_model.split('/')[-1]}"
                self.control_panel.safe_page_update()
                
        except Exception as e:
            logger.error(f"❌ Model change event failed: {e}")
            self._handle_event_error("Model seçim hatası", str(e))

    def on_profile_change(self, event):
        """Training profil seçimi değiştiğinde çağrılan event handler"""
        try:
            new_profile = event.control.value
            logger.info(f"⚙️ Profile changed: {self.selected_profile} -> {new_profile}")
            
            self.selected_profile = new_profile
            
            # Profile description güncelle
            description = self.profile_descriptions.get(new_profile, "Bilinmeyen profil")
            
            # Log event
            self.control_panel.log_system.add_event_log(
                f"⚙️ Profil seçildi: {new_profile} - {description}",
                "SYSTEM"
            )
            
            # Status güncelle
            if hasattr(self.control_panel, 'status_text') and self.control_panel.status_text:
                self.control_panel.status_text.value = f"Profil: {new_profile}"
                self.control_panel.safe_page_update()
                
        except Exception as e:
            logger.error(f"❌ Profile change event failed: {e}")
            self._handle_event_error("Profil seçim hatası", str(e))

    def start_training(self, event):
        """Training başlatma event handler"""
        try:
            logger.info(f"🚀 Training start requested - Model: {self.selected_model}, Profile: {self.selected_profile}")
            
            # Double-click koruması
            current_time = time.time()
            if current_time - self._last_click_time < self._click_cooldown:
                logger.debug("🛡️ Training start ignored - too fast")
                return
            
            self._last_click_time = current_time
            
            # Training config hazırla
            training_config = {
                "model_name": self.selected_model,
                "profile": self.selected_profile,
                "timestamp": current_time
            }
            
            # Training state'i başlat
            from src.utils.training_state import training_state
            training_state.start_training(training_config)
            
            # Dashboard monitoring'i başlat
            if hasattr(self.control_panel, 'dashboard_cards'):
                self.control_panel.dashboard_cards.start_training_monitoring()
            
            # Log event
            self.control_panel.log_system.add_event_log(
                f"🚀 Training başlatıldı - Model: {self.selected_model.split('/')[-1]}, Profil: {self.selected_profile}",
                "TRAINING"
            )
            
            # Status güncelle
            if hasattr(self.control_panel, 'status_text') and self.control_panel.status_text:
                self.control_panel.status_text.value = "🔥 Training Active"
                self.control_panel.safe_page_update()
            
            logger.info("✅ Training started successfully")
            
        except Exception as e:
            logger.error(f"❌ Start training event failed: {e}")
            self._handle_event_error("Training başlatma hatası", str(e))

    def get_current_config(self) -> Dict[str, Any]:
        """Mevcut model ve profil konfigürasyonunu döndürür"""
        return {
            "selected_model": self.selected_model,
            "selected_profile": self.selected_profile,
            "profile_description": self.profile_descriptions.get(self.selected_profile, "")
        }
