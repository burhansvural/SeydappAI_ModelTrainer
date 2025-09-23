# src/ui/builder/control_panel/__init__.py
"""
Control Panel Package - Clean Namespace with Proper State Management
Search results[1][3]: Correct event handling with state attributes
"""

# Essential imports only[1][2] - avoid side effects
from .control_panel_base import ControlPanelBase
from .autonomous_manager import AutonomousLearningManager
from .event_handlers import EventHandlers
from .progress_monitor import ProgressMonitor
from .training_coordinator import TrainingCoordinator
from .ui_components import UIComponentsManager
from .ui_helpers import UIHelpers, UIAnimations

import logging

logger = logging.getLogger(__name__)

# Package metadata
__version__ = "1.0.0"
__author__ = "SeydappAI Team"


class ControlPanel:
    """
    Clean main interface with proper state management[1][3]
    Event handlers require state attributes to be accessible
    """

    def __init__(self, log_system=None, dashboard_cards=None, config=None):
        """Constructor with proper state initialization[1][3]"""
        logger.info("🎮 Initializing ControlPanel with state management")

        # Store dependencies
        self.log_system = log_system
        self.dashboard_cards = dashboard_cards
        self.config = config or {}

        # ✅ State attributes required by event handlers[1][3]
        self.autonomous_running = False
        self.research_running = False
        self.page = None

        # ✅ Thread management attributes[3]
        self.active_threads = []

        # ✅ UI state attributes needed by components
        self.status_text = None
        self.progress_bar = None
        self.controls_container = None

        # Initialize components
        self._init_components()

        logger.info("✅ ControlPanel initialized with proper state")

    def _init_components(self):
        """Initialize components with consistent constructor pattern"""
        # Base component - delegate state management
        self.base = ControlPanelBase(
            log_system=self.log_system,
            dashboard_cards=self.dashboard_cards,
            config=self.config
        )

        # Copy base state to main instance for event handlers[1][3]
        self.autonomous_running = self.base.autonomous_running
        self.research_running = self.base.research_running
        self.active_threads = self.base.active_threads
        self.page = self.base.page

        # UI components manager
        self.ui_manager = UIComponentsManager()

        # Components that need control_panel reference[1]
        self.event_handlers = EventHandlers(control_panel_instance=self)
        self.autonomous_manager = AutonomousLearningManager(control_panel_instance=self)
        self.progress_monitor = ProgressMonitor(control_panel_instance=self)
        self.training_coordinator = TrainingCoordinator(control_panel_instance=self)

        # Static helpers
        self.helpers = UIHelpers
        self.animations = UIAnimations

        logger.debug("✅ All components initialized with proper references")

    def create_controls(self, page):
        """Create controls with proper page reference[1][4]"""
        # Store page reference for event handlers[1]
        self.page = page
        self.base.page = page

        # Create UI with event handlers[1][3]
        self.controls_container = self.ui_manager.create_control_panel(
            page=page,
            event_handler=self.event_handlers,
            config=self.config
        )

        # Store UI references for updates[3]
        self._extract_ui_references()

        logger.info("✅ Controls created with event handlers connected")

    def _extract_ui_references(self):
        """Extract UI references for state updates[3]"""
        try:
            # This will be populated by UI components when they create widgets
            # For now, we'll set up placeholders that components can fill
            pass
        except Exception as e:
            logger.debug(f"UI reference extraction: {e}")

    def get_controls(self):
        """Simple getter[2]"""
        return self.controls_container

    def safe_page_update(self):
        """Safe page update method needed by event handlers[1][3]"""
        try:
            if self.page and hasattr(self.page, 'update'):
                self.page.update()
                logger.debug("✅ Page updated successfully")
        except Exception as e:
            logger.debug(f"Page update error: {e}")

    def cleanup_threads(self):
        """Thread cleanup method needed by components[3]"""
        try:
            if hasattr(self.base, 'cleanup_threads'):
                self.base.cleanup_threads()
                # Sync thread list
                self.active_threads = self.base.active_threads
        except Exception as e:
            logger.debug(f"Thread cleanup error: {e}")

    def cleanup(self):
        """Simple cleanup delegation"""
        if hasattr(self.base, 'cleanup'):
            self.base.cleanup()


# Factory function for external use
def create_control_panel(log_system=None, dashboard_cards=None, config=None):
    """Simple factory function[2]"""
    return ControlPanel(log_system, dashboard_cards, config)


# Clean public API
__all__ = [
    'ControlPanel',
    'create_control_panel',
    'ControlPanelBase',
    'AutonomousLearningManager',
    'EventHandlers',
    'ProgressMonitor',
    'TrainingCoordinator',
    'UIComponentsManager',
    'UIHelpers',
    'UIAnimations'
]
