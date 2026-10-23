import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk

import random
import math
import dashboard_data  # Connects directly to our background calculations engine

# =====================================================
# CONFIGURATION
from project_paths import SETTINGS_FILE, LINKS_FILE, EXCEL_FILE

import os
import sys
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)




# Initialize unified global shared mailbox memory pointer
db_engine = dashboard_data.get_shared_engine()









# =========================================================================
# INTEGRATED MASTER CYBER GEOGRAPHY REGIONAL MAP COMPONENT
# =========================================================================
class PoppingMapButton(ctk.CTkFrame):
    def __init__(self, master, image_path, command=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.command = command

        # Base dimensions mapping configuration tracker
        self.base_w = 400
        self.base_h = 200

        # Load the physical file map texture layers safely
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Missing map file texture: '{image_path}'. Place your nigeria image in this folder!")

        self.raw_image = Image.open(image_path)

        # Operational state tracking variables
        self.current_w = self.base_w
        self.current_h = self.base_h
        self.target_scale_mode = "idle"  # Options: "grow", "shrink", "idle"

        # ⚡ SCAN LINE ENGINE VARIABLES
        self.scan_x = 0  # Starting position of the line
        self.scan_direction = 1  # 1 = Moving Right, -1 = Moving Left

        # 1. Main Canvas layer container definition
        self.canvas = tk.Canvas(self, width=self.base_w, height=self.base_h, bg="#070b12", highlightthickness=0)
        self.canvas.pack(expand=True, fill="both")

        # Draw the initial image on the canvas
        self.update_image_scale(self.base_w, self.base_h)

        # 2. Bind desktop pointer movement sensors directly to the canvas surface
        self.canvas.bind("<Enter>", self.on_cursor_enter)
        self.canvas.bind("<Leave>", self.on_cursor_leave)
        self.canvas.bind("<Button-1>", self.on_map_clicked)

        # 3. Kick off the scanning line animation loop immediately
        self.animate_scan_line()

    def update_image_scale(self, width, height):
        """
        🚀 STABILITY UPGRADE: Re-samples image matrices on the fly and updates
        the canvas window context securely while clearing out hidden Tkinter reference bugs!
        """
        self.canvas.config(width=int(width), height=int(height))
        resized_img = self.raw_image.resize((int(width), int(height)), Image.Resampling.LANCZOS)

        # Unpack the bitmap normally using your high-definition re-sampling process
        self.tk_bitmap = ImageTk.PhotoImage(resized_img)

        # 🛠️ FIXED: Bind the bitmap reference directly to the canvas object layer container.
        # This acts as an explicit memory anchor, preventing standard Tkinter from dropping
        # image contexts and throwing 'pyimage3 doesn't exist' layout crashes once compiled!
        self.canvas.image_cache_reference = self.tk_bitmap

        # Render image background at position (0,0)
        self.canvas.delete("map_layer")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_bitmap, tags="map_layer")
        self.canvas.tag_lower("map_layer")

    def animate_scan_line(self):
        """Calculates chronological tracking coordinates to shift the neon line across the map"""
        self.canvas.delete("scan_layer")

        line_speed = 3
        self.scan_x += line_speed * self.scan_direction

        if self.scan_x >= self.current_w:
            self.scan_direction = -1
        elif self.scan_x <= 0:
            self.scan_direction = 1

        # RENDER CYBER LOGIC PATH: Draw glowing network scan bar + soft trailing shadow line
        self.canvas.create_line(self.scan_x, 0, self.scan_x, self.current_h, fill="#0ea5e9", width=2, tags="scan_layer")

        shadow_offset = 4 * (self.scan_direction * -1)
        self.canvas.create_line(self.scan_x + shadow_offset, 0, self.scan_x + shadow_offset, self.current_h, fill="#0284c7", width=1, tags="scan_layer")

        self.after(16, self.animate_scan_line)

    def on_cursor_enter(self, event):
        """Triggers the growing pop animation state instantly on hover"""
        self.target_scale_mode = "grow"
        self.execute_pulse_animation()

    def on_cursor_leave(self, event):
        """Smoothly shrinks the container back to baseline sizes when leaving"""
        self.target_scale_mode = "shrink"
        self.execute_pulse_animation()

    def execute_pulse_animation(self):
        """Asynchronous scaling frame driver for clean frame-rate movement cycles"""
        max_pop_w = self.base_w + 24
        max_pop_h = self.base_h + 16
        step_speed = 3

        if self.target_scale_mode == "grow":
            if self.current_w < max_pop_w:
                self.current_w += step_speed
                self.current_h += (step_speed * (self.base_h / self.base_w))
                self.update_image_scale(self.current_w, self.current_h)
                self.after(15, self.execute_pulse_animation)

        elif self.target_scale_mode == "shrink":
            if self.current_w > self.base_w:
                self.current_w -= step_speed
                self.current_h -= (step_speed * (self.base_h / self.base_w))
                self.update_image_scale(self.current_w, self.current_h)
                self.after(15, self.execute_pulse_animation)

    def on_map_clicked(self, event):
        """Fires an expansive pure tkinter window centered on screen with standard window control functionality."""
        print("🌍 [NOC ROUTE PROBE] Nigeria Network Sector Base Targeted!")

        # Standard pure tk.Toplevel ensures maximum window thread stability
        popup = tk.Toplevel(self)
        popup.title("🛰️ REGIONAL INFRASTRUCTURE PROFILE: NIGERIA")

        # Get the main top-level root window frame dimensions to scale the popup larger
        root_window = self.winfo_toplevel()
        root_window.update_idletasks()

        main_w = root_window.winfo_width()
        main_h = root_window.winfo_height()
        main_x = root_window.winfo_rootx()
        main_y = root_window.winfo_rooty()

        # Forces the popup window geometry dimensions to be cleanly bigger than your master window bounds
        popup_width = main_w + 120
        popup_height = main_h + 80

        # Centering offset calculations to align it nicely on top of your main application
        center_x = main_x + (main_w // 2) - (popup_width // 2)
        center_y = main_y + (main_h // 2) - (popup_height // 2)

        # Apply geometry values strings parameters
        popup.geometry(f"{popup_width}x{popup_height}+{center_x}+{center_y}")
        popup.configure(bg="#070b12")  # Match midnight deck theme canvas background color
        popup.resizable(False, False)

        # 🛠️ REMOVED / COMMENTED OUT: Removing this line allows Minimize and Maximize to work normally!
        # popup.transient(root_window)

        # Force the frame to stay completely locked on top of the active layout view screen layers stack
        popup.attributes("-topmost", True)

        # =====================================================================
        # 🛰️ CONNECT BRIDGE ENGINE: Loads and updates the map visualization live
        # =========================================================================
        try:
            import hologram_map
            hologram_map.HologramMapTerminal(
                master_widget=self,
                popup_window=popup,
                w=popup_width,
                h=popup_height
            )
        except Exception as bridge_err:
            print("🚨 Hologram Map data routing connection failure error:", bridge_err)

        if self.command:
            self.command()


# =========================================================================
# MAIN DASHBOARD INTERFACE ORCHESTRATION PANEL
# =========================================================================
def create_dashboard_interface(parent_frame, show_page_callback):
    """
    Constructs the clean, graph-free Cyber NOC Dashboard landing workspace.
    Completely stable, lightweight, and driven by data pushed from the Monitor tab.
    """
    parent_frame.configure(fg_color="#090d16")  # Deep cyber navy background

    # -----------------------------------------------------------------
    # UPPER LAYER: 4 GLOWING NEON VITAL METRICS CARDS RIBBON
    # -----------------------------------------------------------------
    kpi_ribbon = ctk.CTkFrame(parent_frame, fg_color="transparent")
    kpi_ribbon.pack(fill="x", padx=15, pady=(15, 5), side="top")

    # Fetch initial metrics calculation numbers from the dataset manager cache registry
    stats = db_engine.generate_current_ui_matrix_payload()

    card_configs = [
        ("TOTAL LINKS:", stats["total_links"], "#0ea5e9"),  # Cyan Neon
        ("AVG UPTIME:", stats["avg_uptime"], "#10b981"),  # Green Neon
        ("CRITICAL FAULTS:", stats["critical_faults"], "#ef4444"),  # Red Neon
        ("ACCUM VOLUME:", stats["accum_volume"], "#3b82f6")  # Blue Neon
    ]

    card_labels = {}  # Memory reference cache tracking internal label strings updates

    for i, (title, val, neon_color) in enumerate(card_configs):
        kpi_ribbon.grid_columnconfigure(i, weight=1, uniform="equal")

        card_chassis = ctk.CTkFrame(
            kpi_ribbon,
            fg_color="#0b0f19",
            border_width=1,
            border_color=neon_color,
            corner_radius=10
        )
        card_chassis.grid(row=0, column=i, padx=8, pady=5, sticky="nsew")

        title_lbl = ctk.CTkLabel(card_chassis, text=title, font=("Arial", 11, "bold"), text_color="#64748B")
        title_lbl.pack(pady=(12, 2))

        val_lbl = ctk.CTkLabel(card_chassis, text=val, font=("Consolas", 24, "bold"), text_color=neon_color)
        val_lbl.pack(pady=(0, 12))
        card_labels[title] = val_lbl

        # =====================================================================
        # 🛠️ FIXED: HOOK DYNAMIC MULTI-MODULE SHORTCUT TO MONITOR LINK DOWN VIEW
        # =====================================================================
        if title == "CRITICAL FAULTS:":
            # Change mouse cursor style to a selection pointer to show it's clickable
            card_chassis.configure(cursor="hand2")
            title_lbl.configure(cursor="hand2")
            val_lbl.configure(cursor="hand2")

            # Inline callback execution logic that targets the active Monitor panel toggle hooks
            # Inline callback execution logic that targets the active Monitor panel toggle hooks
            def navigate_to_faults_view(event=None):
                print("⚡ [NOC PIPELINE] Routing to Monitor tab and opening [LINK DOWN] view console...")

                # 1. Switch sidebar screen context immediately to the target Monitor frame viewport
                show_page_callback("Monitor")

                # 2. 🛠️ TRIGGER REAL BUTTON PACK ACTION INVOKE
                try:
                    import ctk_monitor
                    if hasattr(ctk_monitor, "link_down_btn_widget") and ctk_monitor.link_down_btn_widget:
                        # 📐 Emulates a clean native widget invocation click loop to launch your popup window instantly!
                        ctk_monitor.link_down_btn_widget.invoke()
                except Exception as route_err:
                    print("⚠️ Note: Sidebar switched to Monitor, but background module function trigger errored:",
                          route_err)

            # Bind mouse clicks (<Button-1> is left click) to the chassis box AND text items
            card_chassis.bind("<Button-1>", navigate_to_faults_view)
            title_lbl.bind("<Button-1>", navigate_to_faults_view)
            val_lbl.bind("<Button-1>", navigate_to_faults_view)

    # -----------------------------------------------------------------
    # SECTION 2: MASTER BOTTOM LAYOUT SPLIT
    # -----------------------------------------------------------------
    bottom_grid = ctk.CTkFrame(parent_frame, fg_color="transparent")
    bottom_grid.pack(fill="both", expand=True, padx=15, pady=(5, 15), side="top")

    bottom_grid.grid_columnconfigure(0, weight=6, uniform="equal")  # Left content frame width
    bottom_grid.grid_columnconfigure(1, weight=4, uniform="equal")  # Right column panel width
    bottom_grid.grid_rowconfigure(0, weight=1)

    # --- LEFT COLUMN HOUSING FRAME CHASSIS (MOUNTS INTEGRATED MAP WIDGET) ---
    left_column = ctk.CTkFrame(bottom_grid, fg_color="#0b0f19", corner_radius=10, border_width=1,
                               border_color="#1e293b")
    left_column.grid(row=0, column=0, padx=8, pady=5, sticky="nsew")

    # 🛠️ FIXED: Completely removed 'from live_GUI_3 import resource_path' to break the circular import!
    # This function resolves the path independently so the app boots up perfectly without clashing.
    def get_local_resource_path(relative_path):
        import sys, os
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    resolved_map_img = get_local_resource_path("nigeria.jpeg")

    # Mount our new map item button cleanly using the resolved runtime asset path location
    map_btn = PoppingMapButton(left_column, image_path=resolved_map_img)
    map_btn.pack(expand=True, padx=20, pady=20)

    # --- RIGHT COLUMN DESIGN WRAPPER ARCHITECTURE ---
    right_column_wrapper = ctk.CTkFrame(bottom_grid, fg_color="transparent")
    right_column_wrapper.grid(row=0, column=1, padx=8, pady=5, sticky="nsew")
    right_column_wrapper.grid_columnconfigure(0, weight=1)
    right_column_wrapper.grid_rowconfigure(0, weight=5, uniform="equal")
    right_column_wrapper.grid_rowconfigure(1, weight=5, uniform="equal")

    # --- LIVE HIGH-TECH NAVIGATION CONTROL PANEL CONSOLE GRID ---
    nav_panel = ctk.CTkFrame(right_column_wrapper, fg_color="#0b0f19", corner_radius=10, border_width=1,
                             border_color="#1e293b")
    nav_panel.grid(row=0, column=0, padx=0, pady=(0, 8), sticky="nsew")

    ctk.CTkLabel(nav_panel, text="⚡ SYSTEM CORE NAVIGATION CONSOLE", font=("Arial", 12, "bold"),
                 text_color="#38BDF8").pack(anchor="w", padx=20, pady=12)

    buttons_grid = ctk.CTkFrame(nav_panel, fg_color="transparent")
    buttons_grid.pack(fill="both", expand=True, padx=20, pady=(0, 15))
    buttons_grid.grid_columnconfigure((0, 1), weight=1, uniform="equal")
    buttons_grid.grid_rowconfigure((0, 1), weight=1, uniform="equal")

    button_maps = [
        ("📊 DASHBOARD", "Dashboard", 0, 0),
        ("📡 MONITOR", "Monitor", 0, 1),
        ("📈 GRAPHS", "Graphs", 1, 0),
        ("⚡ PING DIAG", "Ping", 1, 1)
    ]

    for label_txt, target_page, row_pos, col_pos in button_maps:
        btn = ctk.CTkButton(
            buttons_grid,
            text=label_txt,
            font=("Arial", 12, "bold"),
            text_color="#FFFFFF",
            fg_color="#0F172A",
            hover_color="#1E293B",
            border_width=1,
            border_color="#334155",
            corner_radius=6,
            height=46,
            command=lambda page=target_page: show_page_callback(page)
        )
        btn.grid(row=row_pos, column=col_pos, padx=6, pady=6, sticky="nsew")

    # --- DYNAMIC PATH STABILITY RADAR GAUGE CANVAS PANEL ---
    radar_panel = ctk.CTkFrame(right_column_wrapper, fg_color="#0b0f19", corner_radius=10, border_width=1,
                               border_color="#1e293b")
    radar_panel.grid(row=1, column=0, padx=0, pady=(8, 0), sticky="nsew")
    radar_panel.grid_columnconfigure(0, weight=1)
    radar_panel.grid_rowconfigure(0, weight=0)
    radar_panel.grid_rowconfigure(1, weight=1)

    ctk.CTkLabel(radar_panel, text="🛰️ DYNAMIC PATH STABILITY RADAR GAUGE", font=("Arial", 12, "bold"),
                 text_color="#10B981").grid(row=0, column=0, sticky="w", padx=20, pady=12)

    radar_canvas = tk.Canvas(radar_panel, bg="#05070c", highlightthickness=0)
    radar_canvas.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")

    # Local variable cache state managing pulsing wave offsets smoothly
    state_tracker = {"pulse_step": 0.0}

    # =========================================================================
    # CORE INTERACTIVE GRAPHICS ENGINE (RADAR ONLY)
    # =========================================================================
    def render_pulsing_radar_matrix():
        """Generates dynamic multi-layer glowing target orbit loops mimicking professional telemetry scopes."""
        radar_canvas.delete("all")

        # Safe dimensions fallback extraction to prevent canvas boundary crashes
        rw = radar_canvas.winfo_width()
        rh = radar_canvas.winfo_height()
        if rw < 50 or rh < 50:
            rw, rh = 240, 180

        rx_center = rw // 2
        ry_center = rh // 2

        state_tracker["pulse_step"] += 0.04
        step = state_tracker["pulse_step"]
        pulse_scale = (math.sin(step) + 1) / 2

        # Compute dynamic radius bounds loop values safely within widget frames
        rad_base_1 = rw // 8 + (pulse_scale * 15)
        rad_base_2 = rw // 4 + (math.cos(step) * 10)

        # Ring A: Neon Turquoise Pulsing Wave Circle Trace
        radar_canvas.create_oval(
            rx_center - rad_base_1, ry_center - rad_base_1,
            rx_center + rad_base_1, ry_center + rad_base_1,
            outline="#2DD4BF", width=2
        )

        # Ring B: Glowing Emerald Green Dashed Orbit Circle Trace
        radar_canvas.create_oval(
            rx_center - rad_base_2, ry_center - rad_base_2,
            rx_center + rad_base_2, ry_center + rad_base_2,
            outline="#10b981", width=1, dash=(10, 8)
        )

        # Orbit Satellite Data Processing Dots
        for idx in range(3):
            dot_angle = step + (idx * (2 * math.pi / 3))
            dx = rx_center + (math.cos(dot_angle) * rad_base_2)
            dy = ry_center + (math.sin(dot_angle) * rad_base_2)
            radar_canvas.create_oval(
                dx - 3, dy - 3, dx + 3, dy + 3,
                fill="#38BDF8", outline=""
            )

        # Center Status Text
        radar_canvas.create_text(
            rx_center, rh - 20,
            text="[ Monitor Tab Core Active Engine Sync ]",
            fill="#64748B", font=("Arial", 10)
        )

    # =========================================================================
    # BACKGROUND AUTOMATED SCHEDULER SYNC PIPELINES
    # =========================================================================
    def execute_fast_graphics_loop():
        """Maintains ultra-smooth, continuous vector graphic updates (~25 FPS fluid layout tracking)."""
        if not parent_frame.winfo_exists():
            return
        try:
            render_pulsing_radar_matrix()
        except:
            pass
        parent_frame.after(40, execute_fast_graphics_loop)

    def execute_live_monitor_sync_loop():
        """Automatically polls the global shared mailbox variables populated by your Monitor tab, updating cards."""
        if not parent_frame.winfo_exists():
            return

        # Fetch fresh metrics updates from the unified mailbox engine instance
        live_stats = db_engine.generate_current_ui_matrix_payload()

        # Overwrite the upper four glowing headers text strings contents instantly
        for title, val in [("TOTAL LINKS:", live_stats["total_links"]),
                           ("AVG UPTIME:", live_stats["avg_uptime"]),
                           ("CRITICAL FAULTS:", live_stats["critical_faults"]),
                           ("ACCUM VOLUME:", live_stats["accum_volume"])]:
            if title in card_labels:
                card_labels[title].configure(text=val)

        # Triggers mailbox synchronization refresh check loop every 2 seconds
        parent_frame.after(2000, execute_live_monitor_sync_loop)

    # Launch automated loop execution cycles instantly inside window thread scope frames
    execute_fast_graphics_loop()
    execute_live_monitor_sync_loop()
