# src/ui/ui_factory.py - DO NOT CALL IMMEDIATELY
from .ultra_modern_training_ui import UltraModernTrainingUI

def create_ultra_modern_training_ui(page: ft.Page) -> UltraModernTrainingUI:
    """✅ FACTORY METHOD WITH LAZY INIT"""
    ui = UltraModernTrainingUI(page)
    ui.init_components()  # Initialize backend ONLY
    return ui
