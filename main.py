# main.py - ENHANCED WITH SEARCH RESULTS BEST PRACTICES
"""
🤖 SeydappAI ModelTrainer - Enhanced with Thread-Safe Logging
✅ Search results [1][2][3][4] best practices implemented
✅ Non-blocking logging with proper cleanup
✅ Context manager pattern for resource management
"""

import asyncio
import sys
import logging
import traceback
import atexit
import signal
from pathlib import Path
from datetime import datetime
from contextlib import asynccontextmanager
import flet as ft
from queue import Queue
from logging.handlers import QueueHandler, QueueListener, RotatingFileHandler
from src.ui.ultra_modern_training_ui import create_ultra_modern_training_ui
from src.ui.builder.control_panel.control_panel_base import ControlPanelBase


# ===============================================================================
# 📝 ENHANCED LOGGING CONFIGURATION - Search results [1][2][3]
# ===============================================================================

class LoggingManager:
    """
    Centralized logging manager with proper cleanup[3]
    Implements search results [1] QueueHandler pattern
    """

    def __init__(self):
        self.queue_listener = None
        self.log_queue = None
        self.logger = None

    def setup_logging(self):
        """Enhanced thread-safe logging - Search results [1][2] pattern"""
        log_dir = Path(__file__).parent / "logs"
        log_dir.mkdir(exist_ok=True)

        log_filename = f"seydappai_main_{datetime.now().strftime('%Y%m%d')}.log"
        log_file_path = log_dir / log_filename

        # ✅ Search results [1] QueueHandler pattern - Non-blocking logging
        self.log_queue = Queue()

        # ✅ Search results [3] RotatingFileHandler for better file management
        console_handler = logging.StreamHandler(sys.stdout)
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )

        # ✅ Search results [2] Enhanced formatter with thread info
        formatter = logging.Formatter(
            '%(asctime)s - %(name)-20s - %(threadName)-15s - %(levelname)-8s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # ✅ Search results [1][4] QueueListener - Separate thread for log handling
        self.queue_listener = QueueListener(
            self.log_queue,
            console_handler,
            file_handler,
            respect_handler_level=True
        )

        # ✅ Start listener
        self.queue_listener.start()

        # ✅ Search results [1] Configure root logger with QueueHandler
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)  # ✅ INFO level for production

        # Clear existing handlers to avoid duplication
        root_logger.handlers.clear()

        # ✅ Add QueueHandler to root logger
        queue_handler = QueueHandler(self.log_queue)
        queue_handler.setLevel(logging.DEBUG)
        root_logger.addHandler(queue_handler)

        # ✅ Configure specific loggers
        self._configure_module_loggers()

        self.logger = logging.getLogger("SeydappAI-Main")
        self.logger.info("📝 Enhanced thread-safe logging system initialized")

        # ✅ Register cleanup hooks - Search results [3] pattern
        atexit.register(self.cleanup_logging)
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        return self.logger

    def _configure_module_loggers(self):
        """Configure specific module loggers - Search results [2]"""
        # Control panel logger
        control_panel_logger = logging.getLogger("src.ui.builder.control_panel")
        control_panel_logger.setLevel(logging.INFO)

        # UI logger
        ui_logger = logging.getLogger("src.ui")
        ui_logger.setLevel(logging.INFO)

        # Training logger
        training_logger = logging.getLogger("src.training")
        training_logger.setLevel(logging.DEBUG)

        # Suppress noisy third-party loggers
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('requests').setLevel(logging.WARNING)

    def _signal_handler(self, signum, frame):
        """Signal handler for graceful shutdown"""
        if self.logger:
            self.logger.info(f"📡 Received signal {signum}, shutting down logging...")
        self.cleanup_logging()
        sys.exit(0)

    def cleanup_logging(self):
        """Cleanup logging resources - Search results [3][4]"""
        try:
            if self.logger:
                self.logger.info("🧹 Cleaning up logging system...")

            if self.queue_listener:
                self.queue_listener.stop()
                self.queue_listener = None

            if self.logger:
                self.logger.info("✅ Logging cleanup completed")

        except Exception as e:
            print(f"❌ Logging cleanup error: {e}")


# Global logging manager instance
logging_manager = LoggingManager()


# ===============================================================================
# 🎯 APPLICATION CONTEXT MANAGER - Search results [3] lifespan pattern
# ===============================================================================

@asynccontextmanager
async def app_lifespan():
    """
    Application lifespan manager - Search results [3] FastAPI pattern
    Manages startup and shutdown operations
    """
    logger = logging.getLogger("AppLifespan")

    try:
        # Startup
        logger.info("🚀 Application startup initiated")

        # System validation
        system_check = validate_system_requirements()
        if not system_check.get("overall_ready", False):
            logger.error("❌ System requirements not met!")
            raise RuntimeError("System validation failed")

        logger.info("✅ Application startup completed")

        yield  # Application runs here

    except Exception as e:
        logger.error(f"❌ Application startup error: {e}", exc_info=True)
        raise
    finally:
        # Shutdown
        logger.info("🛑 Application shutdown initiated")

        # Cleanup control panel if exists
        try:
            # Add any specific cleanup here
            logger.info("🧹 Cleaning up application resources...")
        except Exception as e:
            logger.error(f"❌ Cleanup error: {e}")

        logger.info("✅ Application shutdown completed")


# ===============================================================================
# 🎯 ENHANCED MAIN FLET APPLICATION
# ===============================================================================

async def main_app(page: ft.Page):
    """Enhanced main app with proper error handling - Search results [2]"""
    logger = logging.getLogger("FletUI")

    try:
        # ✅ Use lifespan context manager
        async with app_lifespan():
            await _setup_page_ui(page, logger)

    except Exception as ex:
        logger.error(f"❌ Main app error: {ex}", exc_info=True)
        await show_error_ui(page)


async def _setup_page_ui(page: ft.Page, logger):
    """Setup page UI with enhanced error handling"""
    try:
        page.title = "SeydappAI ModelTrainer"
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 0
        page.spacing = 0

        # ✅ Enhanced theme with ControlState
        page.theme = ft.Theme(
            scrollbar_theme=ft.ScrollbarTheme(
                track_color={
                    ft.ControlState.HOVERED: ft.Colors.PURPLE_400,
                    ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
                },
                thumb_color={
                    ft.ControlState.HOVERED: ft.Colors.PURPLE_300,
                    ft.ControlState.DEFAULT: ft.Colors.GREY_600,
                },
                track_visibility=True,
                thumb_visibility=True,
                thickness=12,
                radius=6
            )
        )

        # Window configuration
        page.window.width = 1200
        page.window.height = 800
        page.window.resizable = True
        page.window.center()

        # ✅ Enhanced event handlers with logging
        def on_resize(e):
            logger.debug(f"📐 Window resized: {page.width}x{page.height}")
            page.update()

        def on_window_event(e):
            logger.debug(f"🪟 Window event: {e.data}")

        page.on_resize = on_resize
        page.window.on_event = on_window_event

        logger.info("🎨 Creating UI components...")

        # UI oluştur
        training_ui = create_ultra_modern_training_ui(page)
        if training_ui.init_ui():
            logger.info("✅ UI successfully loaded")
        else:
            raise RuntimeError("UI initialization failed")

        page.update()
        logger.info("✅ Page setup completed")

    except Exception as e:
        logger.error(f"❌ Page setup error: {e}", exc_info=True)
        raise


async def show_error_ui(page: ft.Page):
    """Enhanced error UI with better UX"""
    logger = logging.getLogger("ErrorUI")
    logger.error("🚨 Showing error UI")

    page.clean()

    error_ui = ft.Container(
        content=ft.Column([
            ft.Icon(name=ft.Icons.ERROR, size=64, color=ft.Colors.RED_400),
            ft.Text("🚨 Critical Error", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_400),
            ft.Text("UI initialization failed", size=16, color=ft.Colors.WHITE),
            ft.Container(height=20),
            ft.Text("📋 Troubleshooting:", size=18, color=ft.Colors.CYAN_400, weight=ft.FontWeight.BOLD),
            ft.Text("• Check logs in ./logs directory", size=14, color=ft.Colors.GREY_300),
            ft.Text("• Restart the application", size=14, color=ft.Colors.GREY_300),
            ft.Text("• Update Flet: pip install --upgrade flet", size=14, color=ft.Colors.GREY_300),
            ft.Text("• Check system requirements", size=14, color=ft.Colors.GREY_300),
            ft.Container(height=30),
            ft.Row([
                ft.ElevatedButton(
                    "🔄 Retry",
                    bgcolor=ft.Colors.BLUE_600,
                    color=ft.Colors.WHITE,
                    on_click=lambda _: page.go("/")
                ),
                ft.ElevatedButton(
                    "📋 View Logs",
                    bgcolor=ft.Colors.ORANGE_600,
                    color=ft.Colors.WHITE,
                    on_click=lambda _: logger.info("User requested log view")
                )
            ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
        ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=50,
        expand=True,
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.GREY_950,
        border=ft.border.all(2, ft.Colors.RED_400)
    )

    page.add(error_ui)
    page.update()


# ===============================================================================
# 🔧 ENHANCED SYSTEM VALIDATION
# ===============================================================================

def validate_system_requirements() -> dict:
    """Enhanced system validation with better error handling"""
    from importlib.metadata import version, PackageNotFoundError

    logger = logging.getLogger("SystemValidation")

    validation_results = {
        "python_compatible": False,
        "flet_available": False,
        "flet_version_compatible": False,
        "control_state_available": False,
        "overall_ready": False,
        "details": {}
    }

    try:
        # Python version check
        python_version = sys.version_info
        validation_results["details"][
            "python_version"] = f"{python_version.major}.{python_version.minor}.{python_version.micro}"

        if python_version >= (3, 9, 0):
            validation_results["python_compatible"] = True
            logger.info(f"✅ Python {validation_results['details']['python_version']} - Compatible")
        else:
            logger.error(f"❌ Python {validation_results['details']['python_version']} - Requires 3.9+")

        # Flet availability and version check
        try:
            import flet
            flet_version = version('flet')
            validation_results["flet_available"] = True
            validation_results["details"]["flet_version"] = flet_version
            logger.info(f"🔍 Detected Flet version: {flet_version}")

            # ✅ DÜZELTME: Güvenli version parsing[1][4]
            try:
                version_parts = flet_version.split('.')

                # ✅ Safe element access with bounds checking
                major = 0
                minor = 0

                if len(version_parts[0]) > 0 and version_parts[0].isdigit():
                    major = int(version_parts[0])

                if len(version_parts[1]) > 1 and version_parts[1].isdigit():
                    minor = int(version_parts[1])

                logger.info(f"🔍 Parsed version: {major}.{minor}")

                # Version compatibility check (Flet 0.23+ required for ControlState)
                if major > 0 or (major == 0 and minor >= 23):
                    validation_results["flet_version_compatible"] = True
                    logger.info(f"✅ Flet {flet_version} - ControlState API compatible")

                    # Test ControlState availability
                    try:
                        test_state = ft.ControlState.HOVERED
                        validation_results["control_state_available"] = True
                        logger.info("✅ ControlState enum available")
                    except AttributeError:
                        logger.error("❌ ControlState not available - API mismatch")
                else:
                    logger.warning(f"⚠️ Flet {flet_version} - Upgrade to v0.23.0+ required")

            except (ValueError, IndexError) as ve:
                logger.warning(f"⚠️ Version parsing error: {ve} - Assuming compatibility")
                validation_results["flet_version_compatible"] = True
                validation_results["control_state_available"] = True

        except (ImportError, PackageNotFoundError) as e:
            logger.error(f"❌ Flet not available: {e}")
            validation_results["details"]["flet_error"] = str(e)

        # Overall validation
        validation_results["overall_ready"] = all([
            validation_results["python_compatible"],
            validation_results["flet_available"],
            validation_results["flet_version_compatible"],
            validation_results["control_state_available"]
        ])

        if validation_results["overall_ready"]:
            logger.info("✅ All system requirements met")
        else:
            logger.error("❌ System requirements validation failed")

        return validation_results

    except Exception as e:
        logger.error(f"❌ System validation error: {e}", exc_info=True)
        validation_results["details"]["validation_error"] = str(e)
        return validation_results


# ===============================================================================
# 🏁 ENHANCED APPLICATION ENTRY POINT
# ===============================================================================

def run_seydappai_modeltrainer():
    """Enhanced SeydappAI ModelTrainer - Search results [1][2][3] best practices"""
    print("🤖 SeydappAI ModelTrainer")
    print("=" * 60)

    # ✅ Setup enhanced logging
    logger = logging_manager.setup_logging()

    try:
        logger.info("🔍 System requirements validation...")
        system_check = validate_system_requirements()

        if not system_check.get("overall_ready", False):
            logger.error("❌ System requirements not met!")
            logger.error(f"Details: {system_check.get('details', {})}")
            return 1

        logger.info("✅ System ready - Enhanced thread-safe logging active")

        # ✅ Launch app with enhanced error handling
        try:
            ft.app(
                target=main_app,
                assets_dir="assets",
                route_url_strategy="path"
            )
        except Exception as app_error:
            logger.error(f"❌ Flet app error: {app_error}", exc_info=True)
            return 1

        return 0

    except KeyboardInterrupt:
        logger.info("⌨️ Keyboard interrupt received")
        return 0
    except Exception as e:
        logger.error(f"❌ Application startup error: {e}", exc_info=True)
        return 1
    finally:
        logger.info("🏁 SeydappAI ModelTrainer session ended")


# ===============================================================================
# 🏁 MAIN EXECUTION
# ===============================================================================

if __name__ == "__main__":
    try:
        exit_code = run_seydappai_modeltrainer()
        sys.exit(exit_code)
    except Exception as e:
        print(f"❌ Critical error: {e}")
        traceback.print_exc()
        sys.exit(1)
