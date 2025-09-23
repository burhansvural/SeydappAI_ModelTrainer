# src/ui/ultra_modern_training_ui.py
"""
🎨 Ultra-Modern Training Interface - Enhanced Modular Architecture
Search results [1][3][5] implementation: Reusable components with configuration support
✅ UI Abstraction and State Management [1][5]
✅ Composability and Reusability [3]
✅ Clean Code Structure [4]
"""

import flet as ft
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

# Import modular components - Search results [3] reusable UI components pattern
from .builder.log_system import LogSystem
from .builder.dashboard_cards import DashboardCards
from .builder.control_panel import ControlPanel
from .builder.responsive_sidebar import ResponsiveSidebar
from .builder.main_content import MainContent


class UltraModernTrainingUI:
    """
    Enhanced modular component manager with configuration support
    Search results [1][3][5] pattern: UI abstraction, reusable components, best practices
    """

    def __init__(self, page: ft.Page, app_config=None):
        """
        Initialize with enhanced configuration support
        Search results [1] UI Abstraction and [3] composability pattern
        """
        self.page = page
        self.current_view = "training"
        self.ui_ready = False

        # Enhanced configuration - Search results [4] clean code structure
        self.app_config = app_config or self._get_default_configuration()

        # Component references - Search results [3] reusable UI components
        self.log_system = None
        self.dashboard_cards = None
        self.control_panel = None
        self.sidebar = None
        self.main_content = None

        # UI state management - Search results [1][5] state management
        self.initialization_time = None
        self.component_count = 0

        logger.info("🔍 UltraModernTrainingUI instance created", extra={
            "config_provided": bool(app_config),
            "max_cycles": self.app_config.get('control_panel', {}).get('max_cycles', 10)
        })

    def _get_default_configuration(self) -> dict:
        """
        Get default application configuration
        Search results [4] Python best practices for sensible defaults
        """
        return {
            'control_panel': {
                'max_cycles': 10,
                'cycle_duration_seconds': 60,
                'research_depth': 'detailed',
                'auto_stop_enabled': True,
                'progress_tracking': True,
                'websites_per_topic': 5,
                'enable_real_scraping': False,
                'save_research_data': True
            },
            'dashboard': {
                'update_interval_ms': 500,
                'show_detailed_stats': True,
                'enable_animations': True,
                'card_count': 4
            },
            'ui': {
                'theme_mode': 'dark',
                'enable_responsive': True,
                'animation_duration_ms': 300,
                'sidebar_width': 280
            },
            'logging': {
                'console_level': 'INFO',
                'file_level': 'DEBUG',
                'max_log_entries': 1000,
                'enable_file_logging': True
            }
        }

    def init_ui(self) -> bool:
        """
        Enhanced UI initialization with proper component management
        Search results [1] UI Abstraction and [5] UI best practices
        """
        try:
            self.initialization_time = datetime.now()
            logger.info("🔧 Starting enhanced UI component initialization sequence")

            # 1. Initialize Log System (CORE) - Search results [1] state management
            self._initialize_log_system()

            # 2. Initialize Dashboard Cards (MIDDLEWARE) - Search results [3] composability
            self._initialize_dashboard_cards()

            # 3. Initialize Control Panel (MIDDLEWARE) - Search results [1] event handling
            self._initialize_control_panel()

            # 4. Initialize Sidebar (UI) - Search results [3] reusable components
            self._initialize_sidebar()

            # 5. Initialize Main Content (UI) - Search results [5] UI best practices
            self._initialize_main_content()

            # 6. Create and setup main layout - Search results [1][5] UI abstraction
            self._create_main_layout()

            # 7. Finalize initialization - Search results [4] clean structure
            self._finalize_initialization()

            return True

        except Exception as e:
            logger.error(f"❌ UI initialization error: {e}", exc_info=True)
            self._handle_initialization_error(e)
            return False

    def _initialize_log_system(self):
        """Initialize logging system - Search results [1] state management"""
        logger.debug("🔧 Initializing LogSystem component")

        log_config = self.app_config.get('logging', {})
        self.log_system = LogSystem(self.page)
        self.component_count += 1

        logger.debug("✅ LogSystem component initialized")

    def _initialize_dashboard_cards(self):
        """Initialize dashboard cards - Search results [3] reusable UI components"""
        logger.debug("🔧 Initializing DashboardCards component")

        dashboard_config = self.app_config.get('dashboard', {})
        self.dashboard_cards = DashboardCards(self.log_system)
        self.dashboard_cards.create_cards(self.page)
        self.component_count += 1

        logger.debug("✅ DashboardCards component initialized")

    def _initialize_control_panel(self):
        """Initialize control panel with proper configuration - Search results [1] event handling"""
        logger.debug("🔧 Initializing ControlPanel component")

        # ✅ Enhanced ControlPanel initialization with config - Search results [4] best practices
        control_panel_config = self.app_config.get('control_panel', {})

        logger.info("🎮 Creating ControlPanel with configuration", extra={
            "max_cycles": control_panel_config.get('max_cycles', 10),
            "research_depth": control_panel_config.get('research_depth', 'detailed'),
            "auto_stop": control_panel_config.get('auto_stop_enabled', True)
        })

        self.control_panel = ControlPanel(
            self.log_system,
            self.dashboard_cards,
            config=control_panel_config  # ✅ Proper config dictionary
        )
        self.control_panel.create_controls(self.page)
        self.component_count += 1

        logger.debug("✅ ControlPanel component initialized")

    def _initialize_sidebar(self):
        """Initialize responsive sidebar - Search results [3] composability"""
        logger.debug("🔧 Initializing ResponsiveSidebar component")

        ui_config = self.app_config.get('ui', {})
        self.sidebar = ResponsiveSidebar(
            self.page,
            self.log_system,
            self.handle_view_change
        )
        self.sidebar.create_sidebar()
        self.component_count += 1

        logger.debug("✅ ResponsiveSidebar component initialized")

    def _initialize_main_content(self):
        """Initialize main content area - Search results [5] UI best practices"""
        logger.debug("🔧 Initializing MainContent component")

        self.main_content = MainContent(
            self.page,
            self.log_system,
            self.dashboard_cards,
            self.control_panel,
            self.sidebar
        )
        self.main_content.create_content()
        self.component_count += 1

        logger.debug("✅ MainContent component initialized")

    def _create_main_layout(self):
        """Create main application layout - Search results [1][5] UI abstraction"""
        logger.debug("🔧 Creating main application layout")

        # Enhanced layout with theme support - Search results [5] UI best practices
        ui_config = self.app_config.get('ui', {})

        main_layout = ft.Row(
            controls=[
                self.sidebar.get_sidebar(),
                self.main_content.get_content()
            ],
            spacing=0,
            expand=True
        )

        # Enhanced background with configuration - Search results [1] UI abstraction
        background_gradient = self._create_themed_background(ui_config.get('theme_mode', 'dark'))

        # Add to page with proper structure - Search results [4] clean structure
        self.page.add(ft.Container(
            content=ft.Stack([
                background_gradient,
                main_layout
            ]),
            expand=True
        ))

        # Update page to establish hierarchy - Search results [1] state management
        self.page.update()

        logger.debug("✅ Main layout created and added to page")

    def _create_themed_background(self, theme_mode: str) -> ft.Container:
        """Create themed background - Search results [5] UI best practices"""
        if theme_mode == 'light':
            colors = [ft.Colors.GREY_50, ft.Colors.GREY_100, ft.Colors.GREY_200]
        else:
            colors = [ft.Colors.GREY_900, ft.Colors.BLACK87, ft.Colors.BLACK]

        return ft.Container(
            gradient=ft.RadialGradient(
                center=ft.alignment.center,
                radius=1.2,
                colors=colors
            ),
            expand=True
        )

    def _finalize_initialization(self):
        """Finalize UI initialization - Search results [1] state management"""
        logger.debug("🔧 Finalizing UI initialization")

        # Attach log system after page hierarchy is established
        self.log_system.attach_to_page(self.page)

        # Setup welcome logs
        self.log_system.setup_welcome_logs()

        # Calculate initialization time
        init_duration = (datetime.now() - self.initialization_time).total_seconds()

        # Update UI state
        self.ui_ready = True

        # Success logging with metrics - Search results [4] clean structure
        logger.info("✅ UI initialization completed successfully", extra={
            "components_initialized": self.component_count,
            "initialization_duration_seconds": round(init_duration, 3),
            "ui_ready": True
        })

    def _handle_initialization_error(self, error: Exception):
        """Handle initialization errors - Search results [1] event handling"""
        logger.error("❌ UI initialization failed", extra={
            "error_type": type(error).__name__,
            "components_initialized": self.component_count
        })

        # Create error UI if possible
        if hasattr(self, 'page') and self.page:
            error_ui = self._create_error_ui(str(error))
            try:
                self.page.add(error_ui)
                self.page.update()
            except Exception as page_error:
                logger.error(f"❌ Failed to show error UI: {page_error}")

    def build_ui(self) -> ft.Container:
        """
        Build UI container - Search results [3] reusable components pattern
        This method maintains compatibility with existing code
        """
        if not self.ui_ready:
            return ft.Container(
                content=ft.Column([
                    ft.ProgressRing(width=40, height=40, color=ft.Colors.PURPLE_400),
                    ft.Text("🔧 UI initializing...", size=16, color=ft.Colors.WHITE),
                    ft.Text(f"Components: {self.component_count}/5", size=12, color=ft.Colors.GREY_400)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                alignment=ft.alignment.center,
                expand=True
            )

        # Return minimal container - UI already added in init_ui
        return ft.Container(expand=True)

    def handle_view_change(self, view_key: str):
        """
        Enhanced view change handler
        Search results [1] event handling and [3] reusable component pattern
        """
        if not self.ui_ready:
            logger.warning("⚠️ View change requested before UI ready", extra={
                "requested_view": view_key,
                "ui_ready": False
            })
            return

        try:
            logger.info(f"🔄 Processing view change request: {view_key}", extra={
                "previous_view": self.current_view,
                "new_view": view_key
            })

            # Update current view
            self.current_view = view_key

            # Notify main content - Search results [1] state management
            self.main_content.update_view(view_key)

            # Log successful change - Search results [4] clean logging
            self.log_system.add_event_log(f"📱 View switched to: {view_key}", "UI")

            logger.info("✅ View change completed successfully", extra={
                "current_view": self.current_view
            })

        except Exception as e:
            logger.error(f"❌ View change error: {e}", extra={
                "requested_view": view_key,
                "current_view": self.current_view
            }, exc_info=True)
            self.log_system.add_event_log(f"❌ View change error: {str(e)}", "ERROR")

    def _create_error_ui(self, message: str) -> ft.Container:
        """
        Enhanced error UI - Search results [4] clean structure and [5] UI best practices
        """
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.ERROR_OUTLINE, size=72, color=ft.Colors.RED_400),
                ft.Text("UI Initialization Error", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_400),
                ft.Container(height=20),
                ft.Text("Details:", size=16, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
                ft.Container(
                    content=ft.Text(message, size=14, color=ft.Colors.GREY_300, text_align=ft.TextAlign.CENTER),
                    width=600,
                    padding=20,
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.RED_400),
                    border_radius=10
                ),
                ft.Container(height=30),
                ft.Row([
                    ft.ElevatedButton(
                        "🔄 Restart Application",
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE,
                        on_click=lambda _: self.page.go("/")
                    ),
                    ft.ElevatedButton(
                        "📝 View Logs",
                        bgcolor=ft.Colors.ORANGE_600,
                        color=ft.Colors.WHITE,
                        on_click=self._show_error_logs
                    )
                ], spacing=15, alignment=ft.MainAxisAlignment.CENTER)
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            expand=True,
            padding=40
        )

    def _show_error_logs(self, e):
        """Show error logs in dialog - Search results [1] event handling"""
        try:
            if self.log_system:
                # Implementation would show log dialog
                logger.info("📝 Error logs dialog requested")
        except Exception as ex:
            logger.error(f"❌ Failed to show error logs: {ex}")

    def get_configuration(self) -> dict:
        """Get current configuration - Search results [4] clean structure"""
        return self.app_config.copy()

    def update_configuration(self, new_config: dict):
        """Update application configuration - Search results [1] state management"""
        logger.info("🔧 Updating application configuration", extra={
            "config_keys": list(new_config.keys())
        })

        self.app_config.update(new_config)

        # Notify components of configuration change if needed
        if self.ui_ready:
            logger.info("✅ Configuration updated successfully")


# Enhanced factory function - Search results [1][3][5] reusable component pattern
def create_ultra_modern_training_ui(page: ft.Page, config_path=None) -> UltraModernTrainingUI:
    """
    Enhanced factory function with configuration support
    Search results [1][3][5] pattern: Reusable component creation with best practices
    """
    config = None

    # Load configuration from file if provided - Search results [4] best practices
    if config_path:
        try:
            import json
            config_file = Path(config_path)
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                logger.info(f"📁 Configuration loaded from {config_file}")
            else:
                logger.warning(f"⚠️ Configuration file not found: {config_file}")
        except Exception as ex:
            logger.error(f"❌ Failed to load configuration: {ex}", exc_info=True)

    # Create UI instance - Search results [3] reusable UI components
    ui = UltraModernTrainingUI(page, config)

    logger.info("✅ UltraModernTrainingUI factory completed", extra={
        "config_provided": bool(config),
        "config_source": config_path or "default"
    })

    return ui
