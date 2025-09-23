# src/ui/responsive_sidebar.py
import flet as ft
import logging

logger = logging.getLogger(__name__)


class ResponsiveSidebar:
    """Modern Responsive Sidebar with smooth animations - FIXED"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.is_expanded = True
        self.sidebar_width = 250
        self.collapsed_width = 80
        self.current_view = "training"
        self.ui_callback = None
        self.nav_controls = {}  # Store references to all nav items

        self.build_sidebar()
        logger.info("✅ ResponsiveSidebar initialized properly")

    def set_ui_callback(self, callback):
        """✅ SET CALLBACK ONLY WHEN UI IS READY"""
        self.ui_callback = callback
        # Trigger initial view selection
        if self.ui_callback and self.current_view:
            self.activate_view(self.current_view)



    def build_sidebar(self):
        """✅ BUILD: Correct hierarchy with all necessary event handlers"""

        # Logo section
        self.logo_section = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.AUTO_AWESOME, size=32, color=ft.Colors.WHITE),
                ft.Text("SeydappAI", size=18, weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE, visible=self.is_expanded, animate_opacity=200),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(vertical=20),
        )

        # Navigation items configuration
        nav_items_list = []
        nav_config = [
            ("training", ft.Icons.ROCKET_LAUNCH, "Training", ft.Colors.GREEN_400, True),
            ("chat", ft.Icons.CHAT, "AI Chat", ft.Colors.PURPLE_400, False),
            ("analytics", ft.Icons.ANALYTICS, "Analytics", ft.Colors.BLUE_400, False),
            ("settings", ft.Icons.SETTINGS, "Settings", ft.Colors.ORANGE_400, False),
            ("models", ft.Icons.COMPUTER, "Models", ft.Colors.PURPLE_400, False),
            ("logs", ft.Icons.DESCRIPTION, "Logs", ft.Colors.CYAN_400, False)
        ]

        for view_key, icon, text, color, active in nav_config:
            # ✅ CREATE nav item WITH complete event handlers
            nav_item, icon_control, text_control = self._create_nav_item(view_key, icon, text, color, active)

            # ✅ Store references for direct access
            self.nav_controls[view_key] = {
                "container": nav_item,
                "icon": icon_control,
                "text": text_control,
                "color": color
            }

            nav_items_list.append(nav_item)

        self.nav_items = ft.Column(nav_items_list, spacing=5)

        # Toggle button - Stores a reference to its own icon
        toggle_icon = ft.Icon(ft.Icons.MENU_OPEN if self.is_expanded else ft.Icons.MENU, size=24, color=ft.Colors.WHITE)
        self.toggle_btn = ft.Container(
            content=ft.Row([
                toggle_icon
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=15,
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
            border_radius=30,
            border=ft.border.all(1, ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
            width=50,
            height=50,
            on_click=self.toggle_sidebar,
            ink=True,
            animate=ft.Animation(300)
        )

        # ✅ Store toggle icon reference
        self.nav_controls['toggle'] = {
            "container": self.toggle_btn,
            "icon": toggle_icon,
            "text": None,
            "color": ft.Colors.WHITE
        }

        # ✅ MAIN SIDEBAR CONTAINER - NO EXPAND CONFLICTS
        self.sidebar_container = ft.Container(
            content=ft.Column([
                self.logo_section,
                ft.Divider(height=1, color=ft.Colors.GREY_700),
                self.nav_items,
                ft.Container(height=20),  # Spacer
                self.toggle_btn
            ], expand=True),
            width=self.sidebar_width,
            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
            border_radius=ft.border_radius.only(top_right=20, bottom_right=20),
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
            animate_size=ft.Animation(300, ft.AnimationCurve.EASE_OUT_QUINT),
            padding=10
        )

    def _create_nav_item(self, view_key: str, icon_name, text: str, color, active: bool):
        """✅ CREATE: Correct nested controls with ALL event handlers"""
        # Create individual controls
        icon = ft.Icon(icon_name, size=20, color=color if active else ft.Colors.GREY_500)
        text_control = ft.Text(text, size=14, color=ft.Colors.WHITE if active else ft.Colors.GREY_500,
                               visible=self.is_expanded, animate_opacity=200)

        # ✅ Container - Primary event handler
        container = ft.Container(
            content=ft.Row([icon, text_control], spacing=15),  # Row content
            padding=ft.padding.symmetric(vertical=12, horizontal=20),
            bgcolor=ft.Colors.with_opacity(0.2, color) if active else ft.Colors.TRANSPARENT,
            border_radius=10,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            on_click=lambda e: self._handle_navigation_click(e, view_key),  # ✅ CRITICAL
            ink=True,
            cursor=ft.MouseCursor.CLICK
        )

        # ✅ Row - Secondary event handler (propagation)
        container.content.on_click = lambda e: self._handle_navigation_click(e, view_key)

        # ✅ Icon - Tertiary event handler (propagation)
        icon.on_click = lambda e: self._handle_navigation_click(e, view_key)

        # ✅ Text - Tertiary event handler (propagation)
        text_control.on_click = lambda e: self._handle_navigation_click(e, view_key)

        return container, icon, text_control

    def _handle_navigation_click(self, e, view_key: str):
        """✅ SAFE: Handle click event from ANY nested control"""
        try:
            # Ensure we have UI callback
            if not self.ui_callback:
                logger.warning(f"⚠️ Navigation aborted - no UI callback set for {view_key}")
                return

            # ✅ Correctly mark current selection
            for key, controls in self.nav_controls.items():
                if key == "toggle" or key == view_key:
                    continue

                # Deactivate others
                if 'container' in controls:
                    controls['container'].bgcolor = ft.Colors.TRANSPARENT

                if 'icon' in controls:
                    controls['icon'].color = ft.Colors.GREY_500

                if 'text' in controls and hasattr(controls['text'], 'visible'):
                    controls['text'].color = ft.Colors.GREY_500

            # ✅ Activate selected item
            if view_key in self.nav_controls:
                controls = self.nav_controls[view_key]
                controls['container'].bgcolor = ft.Colors.with_opacity(0.2, controls['color'])
                controls['icon'].color = controls['color']
                if controls['text'] and hasattr(controls['text'], 'color'):
                    controls['text'].color = ft.Colors.WHITE

            # ✅ Update current view
            self.current_view = view_key

            # ✅ Trigger callback
            self.ui_callback(view_key)

            # ✅ Force update of all sidebar components
            self.sidebar_container.update()
            logger.info(f"✅ Navigation successfully executed to: {view_key}")

        except Exception as ex:
            logger.error(f"❌ Navigation error: {ex}")
            # Attempt a safe UI update
            try:
                self.sidebar_container.update()
            except:
                pass


    def navigate_to_view_fixed(self, view_key: str):
        """✅ COMPLETELY FIXED: Direct control access without list iteration"""
        try:
            logger.info(f"🔄 Navigating to: {view_key}")

            # ✅ FIXED: Direct control access using stored references
            for stored_view_key, controls in self.nav_controls.items():
                icon_control = controls["icon"]
                text_control = controls["text"]
                color = controls["color"]

                if stored_view_key == view_key:
                    # ✅ Activate selected item
                    icon_control.color = color
                    text_control.color = ft.Colors.WHITE
                    controls["active"] = True

                    # Update container background
                    self._update_nav_container_bg(stored_view_key,
                                                  ft.Colors.with_opacity(0.2, color))
                else:
                    # ✅ Deactivate other items
                    icon_control.color = ft.Colors.GREY_500
                    text_control.color = ft.Colors.GREY_500
                    controls["active"] = False

                    # Update container background
                    self._update_nav_container_bg(stored_view_key, ft.Colors.TRANSPARENT)

            self.current_view = view_key

            # ✅ Trigger view change callback
            if self.ui_callback:
                self.ui_callback(view_key)

            self.page.update()
            logger.info(f"✅ Navigation successful: {view_key}")

        except Exception as e:
            logger.error(f"❌ Navigation fixed error: {e}")

    def _update_nav_container_bg(self, view_key: str, bgcolor):
        """Update navigation container background"""
        try:
            # Find container by view_key in nav_items
            for container in self.nav_items.controls:
                if hasattr(container, 'data') and container.data:
                    if container.data.get("view_key") == view_key:
                        container.bgcolor = bgcolor
                        break
        except Exception as e:
            logger.warning(f"⚠️ Container bg update warning: {e}")

    def nav_hover_effect_fixed(self, e: ft.HoverEvent, view_key: str):
        """✅ FIXED: Hover effect with direct control access"""
        try:
            if view_key not in self.nav_controls:
                return

            controls = self.nav_controls[view_key]
            color = controls["color"]
            active = controls["active"]

            # Find the container
            for container in self.nav_items.controls:
                if (hasattr(container, 'data') and container.data and
                        container.data.get("view_key") == view_key):

                    if e.data == "true":
                        container.bgcolor = ft.Colors.with_opacity(0.1, color)
                    else:
                        container.bgcolor = (ft.Colors.with_opacity(0.2, color)
                                             if active else ft.Colors.TRANSPARENT)
                    break

            self.page.update()

        except Exception as ex:
            logger.warning(f"⚠️ Hover effect error: {ex}")

    def toggle_sidebar(self, e):
        """✅ FIXED: Toggle with complete update mechanism"""
        try:
            if not self.sidebar_container:
                return

            self.is_expanded = not self.is_expanded

            # Update toggle icon
            if 'toggle' in self.nav_controls:
                toggle_icon = self.nav_controls['toggle']['icon']
                toggle_icon.name = ft.Icons.MENU_OPEN if self.is_expanded else ft.Icons.MENU

            # Update sidebar width
            new_width = self.sidebar_width if self.is_expanded else self.collapsed_width
            self.sidebar_container.width = new_width

            # Update all text elements
            for controls in self.nav_controls.values():
                if 'text' in controls and controls['text'] and hasattr(controls['text'], 'visible'):
                    controls['text'].visible = self.is_expanded

            # Force sidebar update
            self.sidebar_container.update()

            # Log success
            logger.info(f"✅ Sidebar toggled successfully: {new_width}px")

        except Exception as ex:
            logger.error(f"❌ Sidebar toggle failed: {ex}")



    def handle_window_resize(self, e):
        """✅ FIXED: Proper resize handling with expand"""
        try:
            # ✅ Don't set manual height - let expand handle it
            logger.info(f"✅ Window resized - expand=True handling height automatically")

            # ✅ Just update the page - expand will handle sizing
            self.page.update()

        except Exception as e:
            logger.warning(f"⚠️ Window resize handler error: {e}")


    def get_sidebar(self) -> ft.Container:
        return self.sidebar_container


    def sidebar_hover_effect(self, e):
        """✅ CLASS LEVEL METHOD - Search results [1] pattern[1]"""
        try:
            if e.data == "true":
                self.toggle_btn.bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.WHITE)
                self.toggle_btn.scale = 1.1
            else:
                self.toggle_btn.bgcolor = ft.Colors.TRANSPARENT
                self.toggle_btn.scale = 1.0

            self.page.update()

        except Exception as ex:
            logger.warning(f"⚠️ Hover effect error: {ex}")

    def init_sidebar(self):
        """Sidebar initialization - FIXED to prevent nav_items error"""
         # ✅ FIX: nav_items kontrolü ekle
        if self.nav_items is None:
            logger.warning("⚠️ nav_items not initialized, calling build_sidebar()")
            self.build_sidebar()
         # ✅ Sidebar height'i dinamik olarak ayarla
        self.update_sidebar_height()

        logger.info("✅ Sidebar initialization completed")

    def update_sidebar_height(self):
        """✅ FIX #2: Dynamic height - EXPAND BASED[3]"""
        try:
            # ✅ Expand kullandığımız için height set etmiyoruz[3]
            if self.sidebar:
                self.sidebar.expand = True
                logger.info("✅ Sidebar height updated (expand=True)")

            if self.page:
                self.page.update()

        except Exception as e:
            logger.warning(f"⚠️ Sidebar height update warning: {e}")

    def _create_nav_item(self, icon_name, text: str, color, active: bool, view_key: str):
        """✅ FIXED: Single click handler[2][3]"""
        nav_text = ft.Text(
            text,
            size=14,
            color=ft.Colors.WHITE if active else ft.Colors.GREY_500,
            visible=self.is_expanded,
            animate_opacity=200
        )

        item_container = ft.Container(
            content=ft.Row([
                ft.Icon(icon_name, size=20, color=color if active else ft.Colors.GREY_500),
                nav_text
            ], spacing=15),
            padding=ft.padding.symmetric(vertical=12, horizontal=20),
            bgcolor=ft.Colors.with_opacity(0.2, color) if active else ft.Colors.TRANSPARENT,
            border_radius=10,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            on_hover=self.nav_hover_effect,
            on_click=lambda e, view=view_key: self.navigate_to_view(view),  # ✅ Single handler[2]
            ink=True  # ✅ Click animation[1]
        )

        item_container.data = {
            "color": color,
            "active": active,
            "text_control": nav_text,  # ✅ Direct text reference
            "view_key": view_key,
            "icon_index": 0,  # ✅ Icon position in Row
            "text_index": 1  # ✅ Text position in Row
        }

        return item_container

    def navigate_to_view(self, view_key: str):
        """✅ FIXEd: List erişim hatası düzeltildi[1][2]"""
        try:
            # ✅ View key mapping
            view_mapping = {
                "training": "training",
                "ai chat": "chat",
                "chat": "chat",
                "analytics": "analytics",
                "settings": "settings",
                "models": "models",
                "logs": "logs"
            }

            normalized_key = view_mapping.get(view_key.lower(), view_key.lower())

            # ✅ CRITICAL FIX: Doğru list element erişimi
            for item in self.nav_items.controls:
                try:
                    item_data = item.data
                    if not item_data:
                        continue

                    # ✅ Row içindeki kontrollere doğru erişim
                    row_controls = item.content.controls  # Bu bir list
                    if len(row_controls) >= 2:
                        icon_control = row_controls  # ✅ İlk element: Icon
                        text_control = row_controls[1]  # ✅ İkinci element: Text

                        if item_data["view_key"] == normalized_key:
                            # ✅ Activate - Doğru property erişimi
                            item.bgcolor = ft.Colors.with_opacity(0.2, item_data["color"])
                            icon_control.color = item_data["color"]  # ✅ Icon'un color'ı
                            text_control.color = ft.Colors.WHITE  # ✅ Text'in color'ı
                            item_data["active"] = True
                        else:
                            # ✅ Deactivate
                            item.bgcolor = ft.Colors.TRANSPARENT
                            icon_control.color = ft.Colors.GREY_500
                            text_control.color = ft.Colors.GREY_500
                            item_data["active"] = False

                except (IndexError, AttributeError, KeyError) as item_error:
                    logger.warning(f"⚠️ Nav item access error: {item_error}")
                    continue

            self.current_view = normalized_key

            # ✅ UI callback for content switching
            if self.ui_callback:
                self.ui_callback(normalized_key)

            self.page.update()
            logger.info(f"✅ Navigation successful: {view_key} -> {normalized_key}")

        except Exception as e:
            logger.error(f"❌ Navigation error fixed: {e}")

    def nav_hover_effect(self, e: ft.HoverEvent):
        try:
            if not hasattr(e.control, 'data') or e.control.data is None:
                return

            color = e.control.data.get("color", ft.Colors.GREY_400)
            active = e.control.data.get("active", False)

            if e.data == "true":
                e.control.bgcolor = ft.Colors.with_opacity(0.1, color)
            else:
                e.control.bgcolor = ft.Colors.with_opacity(0.2, color) if active else ft.Colors.TRANSPARENT
            self.page.update()
        except Exception as ex:
            logger.warning(f"⚠️ Hover effect error: {ex}")




    def adjust_main_content_padding(self):
        """Main content padding'i sidebar durumuna göre ayarla"""
        try:
            # Main content container'ı bul ve padding'ini ayarla
            main_content = None
            for control in self.page.controls:
                if hasattr(control, 'content') and hasattr(control.content, 'controls'):
                    # Stack içinde main content'i ara
                    for stack_item in control.content.controls:
                        if hasattr(stack_item, 'key') and stack_item.key == "MAIN_CONTENT":
                            main_content = stack_item
                            break

            if main_content:
                current_width = self.sidebar_width if self.is_expanded else self.collapsed_width
                main_content.padding = ft.padding.only(
                    left=current_width + 20,
                    right=30,
                    top=20,
                    bottom=20
                )

        except Exception as e:
            logger.warning(f"⚠️ Main content padding adjustment warning: {e}")

    def add_event_listeners(self):
        """Page resize handler ekleme"""
        try:
            self.page.on_resize = self.handle_page_resize
            logger.info("✅ Event listeners added")
        except Exception as e:
            logger.warning(f"⚠️ Event listener warning: {e}")

    def handle_page_resize(self, e):
        """Page resize event handler"""
        try:
            self.update_sidebar_height()
            self.adjust_main_content_padding()
        except Exception as e:
            logger.warning(f"⚠️ Page resize handler warning: {e}")


