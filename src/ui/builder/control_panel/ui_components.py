# src/ui/builder/control_panel/ui_components.py
"""
🎨 UI Components Factory - Modern Factory Pattern Implementation
Search results[1][2][4]: Creational design pattern for flexible UI component creation
"""

import flet as ft
import logging
from typing import Callable, Optional, Dict, Any
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


# Step 1: Common Interface[2][4] - All UI components follow same interface
class UIComponent(ABC):
    """Abstract base class for all UI components[2][4]"""

    @abstractmethod
    def create(self, **kwargs) -> ft.Control:
        """Create and return the UI component"""
        pass

    @abstractmethod
    def get_style_config(self) -> Dict[str, Any]:
        """Get component styling configuration"""
        pass


# Step 2: Concrete Product Classes[3][5] - Specific button implementations
class AutonomousButtonComponent(UIComponent):
    """Autonomous learning button component[3]"""

    def create(self, on_click: Callable = None, **kwargs) -> ft.Container:
        """Create autonomous button with factory pattern[1]"""
        style = self.get_style_config()

        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.AUTO_AWESOME, size=28, color=ft.Colors.WHITE),
                ft.Column([
                    ft.Text(
                        "🤖 Start Autonomous Training",
                        size=17,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "AI will learn automatically",
                        size=12,
                        color=ft.Colors.WHITE70
                    )
                ], spacing=3)
            ], spacing=15, alignment=ft.MainAxisAlignment.START),

            # Apply factory-generated styling[1]
            **style,
            on_click=on_click or self._default_click_handler,
            ink=True,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT)
        )

    def get_style_config(self) -> Dict[str, Any]:
        """Get autonomous button styling[4]"""
        return {
            'padding': ft.padding.symmetric(horizontal=25, vertical=20),
            'width': 350,
            'height': 80,
            'gradient': ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.PURPLE_500, ft.Colors.PURPLE_700, ft.Colors.INDIGO_900]
            ),
            'border_radius': 20,
            'shadow': ft.BoxShadow(
                spread_radius=0,
                blur_radius=25,
                color=ft.Colors.with_opacity(0.4, ft.Colors.PURPLE_400),
                offset=ft.Offset(0, 8)
            )
        }

    def _default_click_handler(self, e):
        """Default click handler if none provided[3]"""
        logger.info("🤖 Autonomous training button clicked - no handler provided")


class ResearchButtonComponent(UIComponent):
    """Research button component[3]"""

    def create(self, on_click: Callable = None, **kwargs) -> ft.Container:
        """Create research button using factory pattern[2]"""
        style = self.get_style_config()

        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.SEARCH, size=24, color=ft.Colors.WHITE),
                ft.Text(
                    "🔍 Quick Research",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE
                )
            ], spacing=12, alignment=ft.MainAxisAlignment.CENTER),

            **style,
            on_click=on_click or self._default_click_handler,
            ink=True,
            animate=ft.Animation(200)
        )

    def get_style_config(self) -> Dict[str, Any]:
        """Get research button styling[4]"""
        return {
            'padding': 20,
            'width': 250,
            'height': 60,
            'gradient': ft.LinearGradient(
                colors=[ft.Colors.CYAN_500, ft.Colors.CYAN_700, ft.Colors.BLUE_900]
            ),
            'border_radius': 15,
            'shadow': ft.BoxShadow(
                spread_radius=0,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.3, ft.Colors.CYAN_400),
                offset=ft.Offset(0, 5)
            )
        }

    def _default_click_handler(self, e):
        """Default research click handler[3]"""
        logger.info("🔍 Research button clicked - no handler provided")


class StopButtonComponent(UIComponent):
    """Stop button component[3]"""

    def create(self, on_click: Callable = None, **kwargs) -> ft.Container:
        """Create stop button using factory pattern[2]"""
        style = self.get_style_config()

        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.STOP_CIRCLE, size=24, color=ft.Colors.WHITE),
                ft.Text(
                    "⏹️ Stop All",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE
                )
            ], spacing=12, alignment=ft.MainAxisAlignment.CENTER),

            **style,
            on_click=on_click or self._default_click_handler,
            disabled=kwargs.get('disabled', True),  # Initially disabled
            ink=True,
            animate=ft.Animation(200)
        )

    def get_style_config(self) -> Dict[str, Any]:
        """Get stop button styling[4]"""
        return {
            'padding': 20,
            'width': 250,
            'height': 60,
            'gradient': ft.LinearGradient(
                colors=[ft.Colors.RED_500, ft.Colors.RED_700, ft.Colors.RED_900]
            ),
            'border_radius': 15
        }

    def _default_click_handler(self, e):
        """Default stop click handler[3]"""
        logger.info("⏹️ Stop button clicked - no handler provided")


class ModelSelectorComponent(UIComponent):
    """Model selection dropdown component"""

    def create(self, on_change: Callable = None, **kwargs) -> ft.Container:
        """Create model selector dropdown"""
        # Available models from config
        models = [
            "bigcode/starcoder2-3b",
            "bigcode/starcoder2-7b",
            "microsoft/CodeBERT-base",
            "microsoft/codebert-base-mlm",
            "huggingface/CodeBERTa-small-v1"
        ]
        
        style = self.get_style_config()
        
        dropdown = ft.Dropdown(
            label="🤖 Select Model",
            hint_text="Choose a model for training",
            options=[
                ft.dropdown.Option(key=model, text=model.split('/')[-1]) 
                for model in models
            ],
            value="bigcode/starcoder2-3b",  # Default selection
            on_change=on_change or self._default_change_handler,
            width=350,
            text_style=ft.TextStyle(color=ft.Colors.WHITE, size=14),
            label_style=ft.TextStyle(color=ft.Colors.BLUE_300, size=12),
            border_color=ft.Colors.BLUE_400,
            focused_border_color=ft.Colors.BLUE_300,
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_900),
            border_radius=10
        )

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.PSYCHOLOGY, size=20, color=ft.Colors.BLUE_400),
                    ft.Text("Model Selection", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                ], spacing=8),
                dropdown
            ], spacing=8),
            **style
        )

    def get_style_config(self) -> Dict[str, Any]:
        """Get model selector styling"""
        return {
            'padding': ft.padding.all(15),
            'width': 380,
            'bgcolor': ft.Colors.with_opacity(0.05, ft.Colors.BLUE_900),
            'border_radius': 12,
            'border': ft.border.all(1, ft.Colors.with_opacity(0.3, ft.Colors.BLUE_400))
        }

    def _default_change_handler(self, e):
        """Default model change handler"""
        logger.info(f"🤖 Model selected: {e.control.value}")


class ProfileSelectorComponent(UIComponent):
    """Training profile selection component"""

    def create(self, on_change: Callable = None, **kwargs) -> ft.Container:
        """Create profile selector dropdown"""
        # Training profiles from config
        profiles = {
            "micro_test": "5-Minute Test - Hızlı test için minimal ayarlar",
            "rtx3060_optimized": "RTX 3060 Optimized - RTX 3060 için optimize edilmiş",
            "production": "Production Training - Tam kapsamlı production training"
        }
        
        style = self.get_style_config()
        
        # Profile description text (will be updated dynamically)
        self.profile_description_text = ft.Text(
            "RTX 3060 için optimize edilmiş ayarlar",
            size=11,
            color=ft.Colors.GREEN_200,
            italic=True
        )
        
        def handle_profile_change(e):
            """Handle profile change and update description"""
            try:
                selected_profile = e.control.value
                description = profiles.get(selected_profile, "").split(' - ')[-1]
                self.profile_description_text.value = description
                self.profile_description_text.update()
                
                # Call original handler if provided
                if on_change:
                    on_change(e)
                else:
                    self._default_change_handler(e)
                    
            except Exception as ex:
                logger.error(f"Profile change handler error: {ex}")
        
        dropdown = ft.Dropdown(
            label="⚙️ Training Profile",
            hint_text="Choose training configuration",
            options=[
                ft.dropdown.Option(key=key, text=desc.split(' - ')[0]) 
                for key, desc in profiles.items()
            ],
            value="rtx3060_optimized",  # Default selection
            on_change=handle_profile_change,
            width=350,
            text_style=ft.TextStyle(color=ft.Colors.WHITE, size=14),
            label_style=ft.TextStyle(color=ft.Colors.GREEN_300, size=12),
            border_color=ft.Colors.GREEN_400,
            focused_border_color=ft.Colors.GREEN_300,
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN_900),
            border_radius=10
        )

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.SETTINGS, size=20, color=ft.Colors.GREEN_400),
                    ft.Text("Training Profile", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                ], spacing=8),
                dropdown,
                # Profile description (dynamic)
                ft.Container(
                    content=self.profile_description_text,
                    padding=ft.padding.only(top=5)
                )
            ], spacing=8),
            **style
        )

    def get_style_config(self) -> Dict[str, Any]:
        """Get profile selector styling"""
        return {
            'padding': ft.padding.all(15),
            'width': 380,
            'bgcolor': ft.Colors.with_opacity(0.05, ft.Colors.GREEN_900),
            'border_radius': 12,
            'border': ft.border.all(1, ft.Colors.with_opacity(0.3, ft.Colors.GREEN_400))
        }

    def _default_change_handler(self, e):
        """Default profile change handler"""
        logger.info(f"⚙️ Profile selected: {e.control.value}")


class StartTrainingButtonComponent(UIComponent):
    """Start training button component"""

    def create(self, on_click: Callable = None, **kwargs) -> ft.Container:
        """Create start training button"""
        style = self.get_style_config()

        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.PLAY_ARROW, size=28, color=ft.Colors.WHITE),
                ft.Column([
                    ft.Text(
                        "🚀 Start Training",
                        size=17,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "Begin model training",
                        size=12,
                        color=ft.Colors.WHITE70
                    )
                ], spacing=3)
            ], spacing=15, alignment=ft.MainAxisAlignment.START),

            **style,
            on_click=on_click or self._default_click_handler,
            ink=True,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT)
        )

    def get_style_config(self) -> Dict[str, Any]:
        """Get start training button styling"""
        return {
            'padding': ft.padding.symmetric(horizontal=25, vertical=20),
            'width': 350,
            'height': 80,
            'gradient': ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.ORANGE_500, ft.Colors.ORANGE_700, ft.Colors.RED_900]
            ),
            'border_radius': 20,
            'shadow': ft.BoxShadow(
                spread_radius=0,
                blur_radius=25,
                color=ft.Colors.with_opacity(0.4, ft.Colors.ORANGE_400),
                offset=ft.Offset(0, 8)
            )
        }

    def _default_click_handler(self, e):
        """Default start training click handler"""
        logger.info("🚀 Start training button clicked - no handler provided")


# Step 3: Factory Creator Class[1][2] - Main factory for component creation
class UIComponentFactory:
    """
    Factory class for creating UI components[1][2][4]
    Implements Factory Method pattern for flexible component creation
    """

    # Component registry[1] - separates object creation from main application
    _components = {
        'autonomous_button': AutonomousButtonComponent,
        'research_button': ResearchButtonComponent,
        'stop_button': StopButtonComponent,
        'model_selector': ModelSelectorComponent,
        'profile_selector': ProfileSelectorComponent,
        'start_training_button': StartTrainingButtonComponent
    }

    @classmethod
    def create_component(cls, component_type: str, **kwargs) -> ft.Control:
        """
        Factory method for creating components[2][4]
        Eliminates complex if/elif/else conditionals

        Args:
            component_type: Type of component to create
            **kwargs: Component-specific parameters

        Returns:
            ft.Control: Created UI component

        Raises:
            ValueError: If component type not found
        """
        logger.debug(f"🏭 Creating component: {component_type}")

        if component_type not in cls._components:
            available = ', '.join(cls._components.keys())
            raise ValueError(f"Unknown component type: {component_type}. Available: {available}")

        # Create component instance and call its factory method[2]
        component_class = cls._components[component_type]
        component_instance = component_class()

        return component_instance.create(**kwargs)

    @classmethod
    def register_component(cls, component_type: str, component_class: type):
        """
        Register new component type[1][4]
        Allows extending factory without modifying existing code
        """
        logger.info(f"📝 Registering new component type: {component_type}")
        cls._components[component_type] = component_class

    @classmethod
    def get_available_components(cls) -> list:
        """Get list of available component types[4]"""
        return list(cls._components.keys())


# Step 4: High-level Manager[1] - Simplified interface for package users
class UIComponentsManager:
    """
    High-level manager for UI components[1]
    Provides simplified, coherent namespace for external use
    """

    def __init__(self):
        self.factory = UIComponentFactory()
        # ✅ Store UI references for event handlers[4]
        self.status_text_ref = None
        self.progress_bar_ref = None

    def create_control_panel(self, page, event_handler, config: Dict[str, Any] = None) -> ft.Container:
        """
        Create complete control panel using factory pattern[1][4]
        Main interface method that external code should use
        """
        logger.info("🎨 Creating control panel with factory components")
        config = config or {}

        try:
            # ✅ Proper event handler method mapping[1][4]
            autonomous_callback = None
            research_callback = None
            stop_callback = None
            model_change_callback = None
            profile_change_callback = None
            start_training_callback = None

            if event_handler:
                # Check if methods exist before assigning[4]
                if hasattr(event_handler, 'toggle_autonomous_learning'):
                    autonomous_callback = event_handler.toggle_autonomous_learning
                    logger.debug("✅ Autonomous event handler mapped")

                if hasattr(event_handler, 'start_quick_research'):
                    research_callback = event_handler.start_quick_research
                    logger.debug("✅ Research event handler mapped")

                if hasattr(event_handler, 'stop_all_processes'):
                    stop_callback = event_handler.stop_all_processes
                    logger.debug("✅ Stop event handler mapped")
                
                if hasattr(event_handler, 'on_model_change'):
                    model_change_callback = event_handler.on_model_change
                    logger.debug("✅ Model change event handler mapped")
                
                if hasattr(event_handler, 'on_profile_change'):
                    profile_change_callback = event_handler.on_profile_change
                    logger.debug("✅ Profile change event handler mapped")
                
                if hasattr(event_handler, 'start_training'):
                    start_training_callback = event_handler.start_training
                    logger.debug("✅ Start training event handler mapped")

            # Create selection components
            model_selector = self.factory.create_component(
                'model_selector',
                on_change=model_change_callback
            )

            profile_selector = self.factory.create_component(
                'profile_selector',
                on_change=profile_change_callback
            )

            # Create training button
            start_training_btn = self.factory.create_component(
                'start_training_button',
                on_click=start_training_callback
            )

            # Create other components using factory method[2][4]
            autonomous_btn = self.factory.create_component(
                'autonomous_button',
                on_click=autonomous_callback
            )

            research_btn = self.factory.create_component(
                'research_button',
                on_click=research_callback
            )

            stop_btn = self.factory.create_component(
                'stop_button',
                on_click=stop_callback,
                disabled=True
            )

            # Create additional components with references[4]
            status_display = self._create_status_section()
            progress_section = self._create_progress_section()

            # ✅ Store UI references for event handlers to access[4]
            if event_handler and hasattr(event_handler, 'control_panel'):
                try:
                    event_handler.control_panel.status_text = self.status_text_ref
                    event_handler.control_panel.progress_bar = self.progress_bar_ref
                    logger.debug("✅ UI references stored in control panel")
                except Exception as ref_error:
                    logger.debug(f"UI reference storage: {ref_error}")

            # Assemble final control panel
            control_panel = ft.Container(
                content=ft.Column([
                    self._create_header(),
                    ft.Divider(height=1, color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),

                    # ✅ Model and Profile Selection Section
                    ft.Container(
                        content=ft.Column([
                            ft.Text("🎯 Training Configuration", 
                                   size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Container(height=10),
                            ft.Row([
                                model_selector,
                                profile_selector
                            ], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
                            ft.Container(height=15),
                            start_training_btn
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=15,
                        bgcolor=ft.Colors.with_opacity(0.03, ft.Colors.WHITE),
                        border_radius=12,
                        border=ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE))
                    ),

                    ft.Divider(height=1, color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),

                    # ✅ Autonomous and Research Section
                    ft.Container(
                        content=ft.Column([
                            ft.Text("🤖 Advanced Features", 
                                   size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Container(height=10),
                            autonomous_btn,
                            ft.Container(height=15),
                            ft.Row([research_btn, stop_btn],
                                   spacing=20,
                                   alignment=ft.MainAxisAlignment.CENTER)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=15,
                        bgcolor=ft.Colors.with_opacity(0.03, ft.Colors.PURPLE_900),
                        border_radius=12,
                        border=ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.PURPLE_400))
                    ),

                    ft.Divider(height=1, color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
                    status_display,
                    progress_section

                ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
                border_radius=15,
                border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.PURPLE_400))
            )

            logger.info("✅ Control panel created with event handlers connected")
            return control_panel

        except Exception as e:
            logger.error(f"❌ Control panel creation failed: {e}")
            return self._create_fallback_panel()

    def _create_header(self) -> ft.Container:
        """Create header section"""
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.PSYCHOLOGY, size=36, color=ft.Colors.PURPLE_400),
                ft.Text("🎮 Control Panel",
                        size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Icon(ft.Icons.FACTORY, size=24, color=ft.Colors.GREEN_400)
            ], spacing=15, alignment=ft.MainAxisAlignment.CENTER),
            padding=10
        )

    def _create_status_section(self) -> ft.Container:
        """Create status display section with stored reference[4]"""
        # ✅ Create status text with reference storage
        self.status_text_ref = ft.Text(
            "Status: Factory-Ready ✨",
            size=14,
            color=ft.Colors.GREEN_400,
            text_align=ft.TextAlign.CENTER
        )

        return ft.Container(
            content=self.status_text_ref,
            padding=15
        )

    def _create_progress_section(self) -> ft.Container:
        """Create progress bar section with stored reference[4]"""
        # ✅ Create progress bar with reference storage
        self.progress_bar_ref = ft.ProgressBar(
            width=400, height=6,
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
            color=ft.Colors.PURPLE_400,
            value=0.0
        )

        return ft.Container(
            content=ft.Column([
                ft.Text("Training Progress", size=16, weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER),
                self.progress_bar_ref
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            padding=15
        )

    def _create_fallback_panel(self) -> ft.Container:
        """Create fallback UI if factory fails[1]"""
        logger.warning("⚠️ Using fallback UI - Factory creation failed")

        return ft.Container(
            content=ft.Column([
                ft.Text("🏭 Factory Error - Safe Mode",
                        size=18, color=ft.Colors.ORANGE_400),
                ft.Text("UI components could not be created",
                        size=12, color=ft.Colors.GREY_400),
                ft.ElevatedButton(
                    "🔄 Retry",
                    bgcolor=ft.Colors.BLUE_600,
                    width=200,
                    on_click=lambda e: logger.info("🔄 Retry requested")
                )
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.ORANGE_400),
            border_radius=15
        )


# Factory convenience functions[1][4] - Additional factory utilities
def create_button_component(button_type: str, on_click: Callable = None, **kwargs) -> ft.Control:
    """
    Convenience function for creating button components[4]
    Simplified interface for external use
    """
    return UIComponentFactory.create_component(f"{button_type}_button", on_click=on_click, **kwargs)


def create_control_panel_manager(config: Dict[str, Any] = None) -> UIComponentsManager:
    """
    Factory function for creating UIComponentsManager[1]
    Follows search results[1] factory pattern for manager creation
    """
    logger.info("🏭 Creating UIComponentsManager via factory")
    return UIComponentsManager()


# Public API - what external code should use[1]
__all__ = [
    'UIComponentsManager',
    'UIComponentFactory',
    'create_button_component',
    'create_control_panel_manager'
]
