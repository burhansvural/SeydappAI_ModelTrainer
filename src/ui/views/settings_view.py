# src/ui/views/settings_view.py
"""
⚙️ Ayarlar Görünümü - Otonom Öğrenme Yapılandırması
Search results [2][4] pattern: Named loggers with getLogger(__name__)
"""

import flet as ft
import json
import logging
from pathlib import Path
from datetime import datetime

# Search results [2][4] - Module-specific named logger
logger = logging.getLogger(__name__)


def create_settings_view(log_system):
    """Create autonomous learning settings view - Search results [4] best practices[4]"""

    logger.info("🔧 Settings view creation started")

    # State management variables - Search results [1] consistent naming[1]
    current_topics = []
    topics_valid = False

    def validate_topics(e):
        """Validate topics in real-time - Search results [1] formatted strings[1]"""
        topics_text = e.control.value.strip()

        logger.debug(f"🔍 Validating topics input: {len(topics_text)} characters")

        if not topics_text:
            logger.info("⚠️ Empty topics input detected")
            update_status("⚠️ En az 3 konu girmeniz gerekiyor", ft.Colors.ORANGE_400, False)
        else:
            topics = [topic.strip() for topic in topics_text.split('\n') if topic.strip()]

            if len(topics) < 3:
                logger.info(f"⚠️ Insufficient topics: {len(topics)}/3 minimum")
                update_status(f"⚠️ {len(topics)}/3 minimum konu sayısı", ft.Colors.ORANGE_400, False)
            elif len(topics) > 10:
                logger.info(f"⚠️ Too many topics: {len(topics)}/10 maximum")
                update_status(f"⚠️ {len(topics)}/10 maksimum konu sayısı", ft.Colors.ORANGE_400, False)
            else:
                logger.info(f"✅ Topics validation successful: {len(topics)} topics ready")
                update_status(f"✅ {len(topics)} konu hazır - AI otomatik öğrenecek!", ft.Colors.GREEN_400, True)
                current_topics.clear()
                current_topics.extend(topics)

        e.page.update()

    def update_status(message: str, color: ft.Colors, valid: bool):
        """Update validation status - Search results [1] contextual information[1]"""
        nonlocal topics_valid
        topics_valid = valid

        logger.debug(f"📊 Status update: {message} (valid: {valid})")

        status_text.value = message
        status_text.color = color

        # Update save button state
        save_button.disabled = not valid
        save_button.bgcolor = ft.Colors.GREEN_600 if valid else ft.Colors.GREY_600

    def save_autonomous_config(e):
        """Save autonomous learning configuration - Search results [4] structured logging[4]"""
        try:
            logger.info("🚀 Starting autonomous config save operation")

            if not current_topics:
                logger.warning("⚠️ No topics to save")
                log_system.add_event_log("⚠️ Kaydedilecek konu bulunamadı", "WARNING")
                return

            # Create config directory
            config_dir = Path("datasets/conversations")
            config_dir.mkdir(exist_ok=True)
            logger.info(f"📁 Config directory ensured: {config_dir}")

            # Save topics to file
            topics_file = config_dir / "user_topics.jsonl"
            saved_topics = []

            with open(topics_file, 'w', encoding='utf-8') as f:
                for i, topic in enumerate(current_topics):
                    topic_data = {
                        "topic": topic,
                        "timestamp": datetime.now().isoformat(),
                        "autonomous": True,
                        "language": "tr"
                    }
                    f.write(json.dumps(topic_data, ensure_ascii=False) + '\n')
                    saved_topics.append(topic)
                    logger.debug(f"📝 Topic {i + 1} saved: {topic}")

            # Success logging - Search results [1] informative messages
            logger.info(f"✅ Successfully saved {len(saved_topics)} autonomous learning topics")
            logger.info(f"📄 Config file: {topics_file}")
            logger.debug(f"💾 Saved topics: {saved_topics}")

            # UI logging
            log_system.add_event_log(f"💾 {len(current_topics)} otonom öğrenme konusu kaydedildi", "CONFIG")
            log_system.add_event_log("🤖 AI otonom öğrenme için hazır!", "SUCCESS")

            # Update UI status
            update_status("✅ Yapılandırma kaydedildi! Eğitim panelinden otonom öğrenmeyi başlatın",
                          ft.Colors.GREEN_400, True)

        except Exception as ex:
            # Error logging - Search results [1][4] error handling with context
            logger.error(f"❌ Failed to save autonomous config: {ex}", exc_info=True)
            log_system.add_event_log(f"❌ Kaydetme hatası: {ex}", "ERROR")

    def load_default_topics(e):
        """Load default topics - Search results [2] pre-defined logging levels[2]"""
        logger.info("🔄 Loading default topics")

        default_topics = """python makine öğrenmesi
pytorch optimizasyonu
transformer fine-tuning
sinir ağları eğitimi
derin öğrenme temelleri
yapay zeka algoritmaları
veri bilimi python
makine öğrenmesi projeleri"""

        try:
            # Update TextField
            topics_input.value = default_topics
            topics_input.update()

            # Manual validation
            topics_text = default_topics.strip()
            topics = [topic.strip() for topic in topics_text.split('\n') if topic.strip()]

            logger.info(f"✅ {len(topics)} default topics loaded successfully")
            logger.debug(f"📝 Default topics: {topics}")

            if 3 <= len(topics) <= 10:
                update_status(f"✅ {len(topics)} konu hazır - AI otomatik öğrenecek!", ft.Colors.GREEN_400, True)
                current_topics.clear()
                current_topics.extend(topics)

            e.page.update()
            log_system.add_event_log("📝 Varsayılan konular yüklendi", "CONFIG")

        except Exception as ex:
            logger.error(f"❌ Failed to load default topics: {ex}", exc_info=True)
            log_system.add_event_log(f"❌ Varsayılan konu yükleme hatası: {ex}", "ERROR")

    def reset_settings(e):
        """Reset settings - Search results [4] consistent logging format[4]"""
        logger.info("🧹 Resetting settings")

        try:
            topics_input.value = ""
            topics_input.update()

            update_status("⚠️ Konuları girmeniz gerekiyor", ft.Colors.ORANGE_400, False)
            current_topics.clear()

            logger.info("✅ Settings reset completed successfully")

            e.page.update()
            log_system.add_event_log("🔄 Ayarlar sıfırlandı", "CONFIG")

        except Exception as ex:
            logger.error(f"❌ Failed to reset settings: {ex}", exc_info=True)
            log_system.add_event_log(f"❌ Ayar sıfırlama hatası: {ex}", "ERROR")

    # Main topics input field - Search results [1] contextual information[1]
    logger.debug("🎯 Creating topics input field")
    topics_input = ft.TextField(
        label="🎯 Otonom Öğrenme Konuları",
        hint_text="python makine öğrenmesi\npytorch optimizasyonu\ntransformer eğitimi\nsinir ağları\nderin öğrenme",
        multiline=True,
        min_lines=8,
        max_lines=15,
        border_color=ft.Colors.PURPLE_400,
        focused_border_color=ft.Colors.PURPLE_300,
        value="python makine öğrenmesi\npytorch optimizasyonu\ntransformer fine-tuning\nsinir ağları eğitimi\nderin öğrenme temelleri",
        on_change=validate_topics,
        text_size=14,
        helper_text="Her satıra bir konu yazın (3-10 konu arası)"
    )

    # Status text indicator
    status_text = ft.Text("⚠️ Konuları girmeniz gerekiyor", size=14, color=ft.Colors.ORANGE_400)

    # Main save button - Search results [1] consistent format[1]
    logger.debug("💾 Creating save button")
    save_button = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.SAVE, size=22, color=ft.Colors.WHITE),
            ft.Text("Otonom Öğrenme Ayarlarını Kaydet", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
        ], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
        padding=ft.padding.symmetric(horizontal=30, vertical=18),
        bgcolor=ft.Colors.GREY_600,
        border_radius=15,
        disabled=True,
        on_click=save_autonomous_config,
        ink=True,
        animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT)
    )

    # Helper buttons - Search results [2] consistent naming[2]
    logger.debug("🔧 Creating helper buttons")
    default_button = ft.ElevatedButton(
        content=ft.Row([
            ft.Icon(ft.Icons.REFRESH, size=18),
            ft.Text("Varsayılan Konuları Yükle")
        ], spacing=8),
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE,
        on_click=load_default_topics
    )

    reset_button = ft.ElevatedButton(
        content=ft.Row([
            ft.Icon(ft.Icons.CLEAR, size=18),
            ft.Text("Temizle")
        ], spacing=8),
        bgcolor=ft.Colors.ORANGE_600,
        color=ft.Colors.WHITE,
        on_click=reset_settings
    )

    logger.info("✅ Settings view components created successfully")

    return ft.Container(
        key="settings_view",
        content=ft.ListView([
            # Main header section
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.AUTO_AWESOME, size=42, color=ft.Colors.PURPLE_400),
                        ft.Column([
                            ft.Text("🤖 Otonom Öğrenme Ayarları", size=26, weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE),
                            ft.Text("AI'ınızın otomatik olarak öğrenmesi için konuları yapılandırın", size=15,
                                    color=ft.Colors.GREY_400)
                        ], spacing=5)
                    ], spacing=20),
                ], spacing=12),
                padding=35,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=[ft.Colors.PURPLE_800, ft.Colors.PURPLE_600, ft.Colors.INDIGO_700]
                ),
                border_radius=18,
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=25,
                    color=ft.Colors.with_opacity(0.3, ft.Colors.PURPLE_400),
                    offset=ft.Offset(0, 8)
                )
            ),

            ft.Container(height=35),

            # Information card - how autonomous learning works
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.LIGHTBULB_OUTLINE, size=26, color=ft.Colors.CYAN_400),
                        ft.Text("🧠 Otonom Öğrenme Nasıl Çalışır?", size=20, weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE)
                    ], spacing=12),

                    ft.Container(height=15),

                    ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.SEARCH, size=16, color=ft.Colors.CYAN_300),
                            ft.Text("AI belirlediğiniz konuları otomatik olarak araştırır", size=14,
                                    color=ft.Colors.WHITE)
                        ], spacing=10),
                        ft.Row([
                            ft.Icon(ft.Icons.WEB, size=16, color=ft.Colors.CYAN_300),
                            ft.Text("Web kaynaklarından bilgi toplar ve analiz eder", size=14, color=ft.Colors.WHITE)
                        ], spacing=10),
                        ft.Row([
                            ft.Icon(ft.Icons.AUTO_GRAPH, size=16, color=ft.Colors.CYAN_300),
                            ft.Text("Kendi eğitim örneklerini otomatik olarak oluşturur", size=14,
                                    color=ft.Colors.WHITE)
                        ], spacing=10),
                        ft.Row([
                            ft.Icon(ft.Icons.ROCKET_LAUNCH, size=16, color=ft.Colors.CYAN_300),
                            ft.Text("Sürekli olarak kendini eğiter ve geliştirir", size=14, color=ft.Colors.WHITE)
                        ], spacing=10),
                        ft.Row([
                            ft.Icon(ft.Icons.STAR, size=16, color=ft.Colors.CYAN_300),
                            ft.Text("Manuel müdahale gerektirmeden uzmanlaşır", size=14, color=ft.Colors.WHITE)
                        ], spacing=10)
                    ], spacing=12)
                ], spacing=8),
                padding=30,
                bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.CYAN_400),
                border_radius=15,
                border=ft.border.all(1, ft.Colors.with_opacity(0.3, ft.Colors.CYAN_400))
            ),

            ft.Container(height=30),

            # Topics configuration section
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.TOPIC, size=24, color=ft.Colors.PURPLE_400),
                        ft.Text("🎯 Öğrenme Konuları", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                    ], spacing=12),

                    ft.Text("AI'ınızın hangi konularda uzmanlaşmasını istediğinizi belirtin", size=14,
                            color=ft.Colors.GREY_400),

                    ft.Container(height=20),

                    # Topics input field
                    topics_input,

                    ft.Container(height=12),

                    # Status indicator
                    ft.Container(
                        content=status_text,
                        padding=12,
                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.ORANGE_400),
                        border_radius=8,
                        border=ft.border.all(1, ft.Colors.with_opacity(0.3, ft.Colors.ORANGE_400))
                    ),

                    ft.Container(height=20),

                    # Helper buttons row
                    ft.Row([
                        default_button,
                        reset_button
                    ], spacing=15, alignment=ft.MainAxisAlignment.CENTER),

                    ft.Container(height=25),

                    # Main save button
                    ft.Container(
                        content=save_button,
                        alignment=ft.alignment.center
                    )
                ], spacing=8),
                width=750,
                padding=35,
                bgcolor=ft.Colors.with_opacity(0.03, ft.Colors.WHITE),
                border_radius=18,
                border=ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE))
            ),

            ft.Container(height=25),

            # Next steps instructions
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.INFO_OUTLINE, size=22, color=ft.Colors.GREEN_400),
                        ft.Text("📋 Sonraki Adımlar", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                    ], spacing=12),

                    ft.Container(height=10),

                    ft.Column([
                        ft.Text("1. Yukarıdaki alana öğrenmesini istediğiniz konuları yazın", size=14,
                                color=ft.Colors.WHITE),
                        ft.Text("2. 'Otonom Öğrenme Ayarlarını Kaydet' butonuna tıklayın", size=14,
                                color=ft.Colors.WHITE),
                        ft.Text("3. Eğitim paneline gidin ve 'Otonom Öğrenmeyi Başlat' butonuna basın", size=14,
                                color=ft.Colors.WHITE),
                        ft.Text("4. AI otomatik olarak kendini geliştirmeye başlayacak!", size=14,
                                color=ft.Colors.GREEN_300, weight=ft.FontWeight.BOLD)
                    ], spacing=8)
                ], spacing=5),
                padding=25,
                bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.GREEN_400),
                border_radius=12,
                border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.GREEN_400))
            ),

            ft.Container(height=30),

            # Warning/tip note
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.WARNING_AMBER, size=20, color=ft.Colors.YELLOW_600),
                    ft.Text(
                        "💡 İpucu: AI'ınız bu konularda sürekli olarak internetten yeni bilgiler öğrenecek ve kendini geliştirecektir. İlk kurulumdan sonra herhangi bir manuel işlem yapmanıza gerek kalmayacak!",
                        size=13,
                        color=ft.Colors.YELLOW_300,
                        italic=True
                    )
                ], spacing=12),
                padding=20,
                bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.YELLOW_600),
                border_radius=10,
                border=ft.border.all(1, ft.Colors.with_opacity(0.3, ft.Colors.YELLOW_600))
            )
        ], spacing=0, padding=ft.padding.all(25)),
        expand=True,
        alignment=ft.alignment.top_center
    )
