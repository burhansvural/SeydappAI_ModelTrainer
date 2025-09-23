# src/ui/builder/responsive_sidebar.py

import flet as ft
import logging

logger = logging.getLogger(__name__)


class ResponsiveSidebar:
    """Responsive sidebar bileşeni - Log sistemi mevcut olmalı"""

    def __init__(self, page, log_system, view_change_callback):
        """✅ INIT: View değiştirme callback'i alınır - UI oluşturulmaz"""
        self.page = page
        self.log_system = log_system
        self.view_change_callback = view_change_callback
        self.current_view = "training"
        self.sidebar_container = None
        self.nav_controls = {}  # Gezinti kontrollerini sakla
        self.is_expanded = True
        self.sidebar_width = 250
        self.collapsed_width = 80

        self.logo_text = None
        self.toggle_icon = None
        self.logo_section = None

    def create_sidebar(self):
        """✅ UI OLUŞTUR: Direct references ile - Search results [1][2] hierarchy[1][2]"""
        logger.info("🔧 Creating sidebar UI components")

        # ✅ Logo text - DIRECT REFERENCE[1][2]
        self.logo_text = ft.Text(
            "SeydappAI",
            key="logo_text",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE
        )

        # ✅ Logo section - Search results [2] control nesting pattern[2]
        self.logo_section = ft.Container(
            key="logo_section",
            content=ft.Column([
                ft.Icon(name=ft.Icons.AUTO_AWESOME, size=32, color=ft.Colors.WHITE),
                self.logo_text  # ✅ Direct reference[1][2]
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(vertical=20),
        )

        # Gezinti elemanlarını oluştur
        nav_items = [
            self._create_nav_item("training", ft.Icons.ROCKET_LAUNCH, "Training", ft.Colors.GREEN_400, True),
            self._create_nav_item("chat", ft.Icons.CHAT, "AI Chat", ft.Colors.PURPLE_400, False),
            self._create_nav_item("analytics", ft.Icons.ANALYTICS, "Analytics", ft.Colors.BLUE_400, False),
            self._create_nav_item("settings", ft.Icons.SETTINGS, "Settings", ft.Colors.ORANGE_400, False),
            self._create_nav_item("models", ft.Icons.COMPUTER, "Models", ft.Colors.PURPLE_400, False),
            self._create_nav_item("logs", ft.Icons.DESCRIPTION, "Logs", ft.Colors.CYAN_400, False),
        ]

        # ✅ Toggle icon - DIRECT REFERENCE[1][2]
        self.toggle_icon = ft.Icon(
            key="toggle_icon",
            name=ft.Icons.MENU_OPEN,
            size=24,
            color=ft.Colors.WHITE
        )

        # ✅ Toggle button - Search results [2] control structure[2]
        toggle_btn = ft.Container(
            key="toggle_btn",
            content=ft.Row([self.toggle_icon], alignment=ft.MainAxisAlignment.CENTER),  # ✅ Direct reference[1][2]
            width=35,
            height=35,
            on_click=self.toggle_sidebar,
            ink=True,
            animate=ft.Animation(300)
        )

        # ✅ Sidebar container - Search results [1][2] control tree[1][2]
        self.sidebar_container = ft.Container(
            key="sidebar_container",
            content=ft.Column([
                self.logo_section,  # ✅ Direct reference[1][2]
                ft.Divider(height=1, color=ft.Colors.GREY_700),
                ft.Column(key="nav_items", controls=nav_items, spacing=5),
                ft.Container(key="spacer", height=20),
                ft.Divider(),
                toggle_btn  # ✅ Direct reference[1][2]
            ], expand=True, alignment=ft.MainAxisAlignment.SPACE_AROUND),
            width=self.sidebar_width,
            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
            border_radius=ft.border_radius.only(top_right=20, bottom_right=20),
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
            animate_size=ft.Animation(300, ft.AnimationCurve.EASE_OUT_QUINT),
            padding=10
        )

        self.log_system.add_event_log("🖥️ Sidebar initialized", "SYSTEM")
        logger.info("✅ Sidebar UI components created")

    def _create_nav_item(self, view_key, icon_name, text, color, active):
        """✅ FIXED: Navigation item creation - Search results [1][2] pattern[1][2]"""
        # ✅ Direct control creation - Search results [1][2] approach[1][2]
        icon_control = ft.Icon(
            key=f"icon_{view_key}",
            name=icon_name,
            size=20,
            color=color if active else ft.Colors.GREY_500
        )

        text_control = ft.Text(
            key=f"text_{view_key}",
            value=text,
            size=14,
            color=ft.Colors.WHITE if active else ft.Colors.GREY_500
        )

        # Gezinti elemanını saracak konteyner
        item_container = ft.Container(
            key=f"nav_{view_key}",
            content=ft.Row([icon_control, text_control], spacing=15),
            padding=ft.padding.symmetric(vertical=12, horizontal=20),
            bgcolor=ft.Colors.with_opacity(0.2, color) if active else ft.Colors.TRANSPARENT,
            border_radius=10,
            on_click=lambda e: self._on_nav_click(view_key),
            ink=True
        )

        # ✅ Direct references sakla - Search results [1][2] clean management[1][2]
        self.nav_controls[view_key] = {
            "container": item_container,
            "icon": icon_control,
            "text": text_control,
            "color": color,
            "active": active
        }

        if active:
            self.current_view = view_key

        return item_container

    def _on_nav_click(self, view_key):
        """Gezinti butonuna tıklandığında"""
        # Mevcut aktif olanı kaldır
        if self.current_view in self.nav_controls:
            controls = self.nav_controls[self.current_view]
            controls["container"].bgcolor = ft.Colors.TRANSPARENT
            controls["icon"].color = ft.Colors.GREY_500
            controls["text"].color = ft.Colors.GREY_500
            controls["active"] = False

        # Yeni aktif olanı ayarla
        if view_key in self.nav_controls:
            controls = self.nav_controls[view_key]
            controls["container"].bgcolor = ft.Colors.with_opacity(0.2, controls["color"])
            controls["icon"].color = controls["color"]
            controls["text"].color = ft.Colors.WHITE
            controls["active"] = True
            self.current_view = view_key

        # UI'yi güncelle
        self.sidebar_container.update()

        # Log event
        self.log_system.add_event_log(f"View changed to: {view_key}", "UI")

        # View değişikliği için callback çağır
        self.view_change_callback(view_key)

    def toggle_sidebar(self, e):
        """✅ FIXED: Direct references kullan - Search results [1][2] clean approach[1][2]"""
        logger.info(f"🔘 Sidebar toggle requested ({self.is_expanded})")

        try:
            # Durumu tersine çevir
            self.is_expanded = not self.is_expanded
            new_width = self.sidebar_width if self.is_expanded else self.collapsed_width

            # ✅ Sidebar genişliğini güncelle
            self.sidebar_container.width = new_width

            # ✅ FIXED: Direct reference kullan - NO HIERARCHY TRAVERSAL[1][2]
            if self.logo_text:
                self.logo_text.visible = self.is_expanded

            # ✅ FIXED: Direct reference kullan - NO HIERARCHY TRAVERSAL[1][2]
            if self.toggle_icon:
                self.toggle_icon.name = ft.Icons.MENU_OPEN if self.is_expanded else ft.Icons.MENU

            # Nav item metinlerini gizle/göster - Direct references[1][2]
            for controls in self.nav_controls.values():
                try:
                    controls["text"].visible = self.is_expanded
                except:
                    pass

            # Log event
            action = "expanded" if self.is_expanded else "collapsed"
            self.log_system.add_event_log(f"🔘 Sidebar {action} ({new_width}px)", "UI")

            # ✅ UI güncelle - Search results [2] update pattern[2]
            self.sidebar_container.update()

            logger.info(f"✅ Sidebar toggle completed: {action}")

        except Exception as ex:
            logger.error(f"❌ Sidebar toggle error: {ex}")
            self.log_system.add_event_log(f"❌ Sidebar toggle failed: {str(ex)}", "ERROR")

    def update_active_item(self, view_key):
        """Dışarıdan görünüm değişikliği olduğunda"""
        if view_key == self.current_view:
            return

        # Mevcut aktif olanı kaldır
        if self.current_view in self.nav_controls:
            controls = self.nav_controls[self.current_view]
            controls["container"].bgcolor = ft.Colors.TRANSPARENT
            controls["icon"].color = ft.Colors.GREY_500
            controls["text"].color = ft.Colors.GREY_500
            controls["active"] = False

        # Yeni aktif olanı ayarla
        if view_key in self.nav_controls:
            controls = self.nav_controls[view_key]
            controls["container"].bgcolor = ft.Colors.with_opacity(0.2, controls["color"])
            controls["icon"].color = controls["color"]
            controls["text"].color = ft.Colors.WHITE
            controls["active"] = True
            self.current_view = view_key

        # UI'yi güncelle
        self.sidebar_container.update()

    def get_sidebar(self) -> ft.Container:
        """Sidebar bileşenini döndürür"""
        return self.sidebar_container


    def _get_keys(self):
        """Available keys for the sidebar content"""
        if self.sidebar_container and hasattr(self.sidebar_container, 'content') and \
                hasattr(self.sidebar_container.content, 'controls'):
            return [control.key for control in self.sidebar_container.content.controls if hasattr(control, 'key')]
        return []
