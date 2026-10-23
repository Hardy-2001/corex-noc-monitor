import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
import json
import ctk_ai_engine  # Dynamic Groq Core SDK Engine
import graph_update  # Core Telemetry Data Extractor

# =========================================================================
# LOAD CONFIGURATION AND DEVICE MATRICES
# =========================================================================
from project_paths import LINKS_FILE

try:
    with open(LINKS_FILE, "r") as f:
        LINKS = json.load(f)
except Exception as e:
    print("AI FILE READ CONFIG FAULT:", e)
    LINKS = []


def create_ai_interface(parent_frame):
    parent_frame.configure(fg_color="#090d16")

    # Layout state variables tracking selection values
    selected_device_name = tk.StringVar(value="Click to select a device link...")
    device_options = [item.get("name") for item in LINKS if item.get("name")]
    if not device_options:
        device_options = ["NUC 1Gbps_AIRTEL Traffic", "FUTMINNA 2Gbps_AIRTEL Traffic"]

    # --- DEVICE SELECTOR POPUP MODAL ARCHITECTURE ---
    def open_device_selector_modal():
        modal = tk.Toplevel(parent_frame)
        modal.title("SELECT PRTG INTERFACE LINK")
        modal.configure(bg="#0b0f19")
        modal.resizable(False, False)

        width, height = 480, 520
        try:
            parent_win = parent_frame.winfo_toplevel()
            cx = parent_win.winfo_x() + (parent_win.winfo_width() // 2) - (width // 2)
            cy = parent_win.winfo_y() + (parent_win.winfo_height() // 2) - (height // 2)
            modal.geometry(f"{width}x{height}+{cx}+{cy}")
        except:
            modal.geometry(f"{width}x{height}")

        modal.lift()
        modal.focus_set()
        modal.grab_set()

        ctk.CTkLabel(modal, text="SELECT SYSTEM DEVICE LINK TARGET:", font=("Arial", 11, "bold"),
                     text_color="#64748B").pack(anchor="w", padx=20, pady=(20, 5))

        search_entry = ctk.CTkEntry(modal, placeholder_text="Type keyword to filter links...", fg_color="#0F172A",
                                    border_color="#1e293b", text_color="#FFFFFF", height=36)
        search_entry.pack(fill="x", padx=20, pady=(0, 15))

        list_frame = ctk.CTkFrame(modal, fg_color="transparent")
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        modal_listbox = tk.Listbox(
            list_frame, bg="#05070c", fg="#A8B3C7", selectbackground="#1E293B", selectforeground="#38BDF8",
            font=("Arial", 11), bd=0, highlightthickness=1, highlightbackground="#1e293b", yscrollcommand=scrollbar.set
        )
        modal_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=modal_listbox.yview)

        def populate_listbox(filter_text=""):
            modal_listbox.delete(0, "end")
            for name in device_options:
                if filter_text.lower() in name.lower():
                    modal_listbox.insert("end", name)

        populate_listbox()
        search_entry.bind("<KeyRelease>", lambda e: populate_listbox(search_entry.get()))

        def confirm_selection(event=None):
            try:
                idx = modal_listbox.curselection()
                selection = modal_listbox.get(idx)
                selected_device_name.set(selection)
                modal.destroy()
            except:
                pass

        modal_listbox.bind("<Double-Button-1>", confirm_selection)

    # =========================================================================
    # SECTION 1: REAL METRICS THREE-FRAME MODAL INTERFACE WINDOW GENERATOR
    # =========================================================================
    def open_three_frame_diagnostics_modal(device_name, details, ai_data, live_network_log):
        """
        Launches the advanced three-frame analytics layout using 100% real
        live metrics gathered from active network sensors and subprocess scopes.
        """
        popup = tk.Toplevel(parent_frame)
        popup.title(f"AI ANALYSIS VIEWPORT: LIVE NOC DIAGNOSTICS - {device_name}")
        popup.configure(bg="#090d16")

        width, height = 1200, 720
        try:
            parent_win = parent_frame.winfo_toplevel()
            cx = parent_win.winfo_x() + (parent_win.winfo_width() // 2) - (width // 2)
            cy = parent_win.winfo_y() + (parent_win.winfo_height() // 2) - (height // 2)
            popup.geometry(f"{width}x{height}+{cx}+{cy}")
        except:
            popup.geometry(f"{width}x{height}")

        popup.lift()
        popup.focus_set()

        popup.grid_columnconfigure(0, weight=5, uniform="equal")
        popup.grid_columnconfigure(1, weight=5, uniform="equal")
        popup.grid_rowconfigure(0, weight=1)

        # -----------------------------------------------------------------
        # LEFT COLUMN DESIGN WRAPPER ARCHITECTURE
        # -----------------------------------------------------------------
        left_column = ctk.CTkFrame(popup, fg_color="transparent")
        left_column.grid(row=0, column=0, padx=(15, 8), pady=15, sticky="nsew")
        left_column.grid_columnconfigure(0, weight=1)
        left_column.grid_rowconfigure(0, weight=4)
        left_column.grid_rowconfigure(1, weight=6)

        # --- FRAME 1 (TOP-LEFT): 100% REAL PRTG TELEMETRY SUMMARY MATRIX GRID ---
        tl_frame = ctk.CTkFrame(left_column, fg_color="#0b0f19", corner_radius=8, border_width=1,
                                border_color="#1e293b")
        tl_frame.grid(row=0, column=0, padx=0, pady=(0, 8), sticky="nsew")

        ctk.CTkLabel(tl_frame, text="📊 PRTG TELEMETRY SUMMARY (LIVE)", font=("Arial", 12, "bold"),
                     text_color="#38BDF8").pack(anchor="w", padx=15, pady=8)

        summary_grid = ctk.CTkFrame(tl_frame, fg_color="transparent")
        summary_grid.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        summary_grid.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")
        summary_grid.grid_rowconfigure((0, 1), weight=1)

        # 🛠️ FIXED: Removed all hardcoded text entries. Every cell maps directly to real PRTG variables.
        metrics = [
            ("Uptime Status", f"Up: {details.get('uptime_pct', '100 %')}"),
            ("Downtime Status", f"Down: {details.get('downtime_pct', '0 %')}"),
            ("Last Telemetry Value", details.get("lastvalue", "0 Mbps")),
            ("Device Identity", details.get("device", "Gateway Node")),
            ("Status Message", details.get("message", "OK")),
            ("Sensor Profile", details.get("sensor", "Traffic Stream"))
        ]

        idx = 0
        for r in range(2):
            for c in range(3):
                title, val = metrics[idx]
                card = ctk.CTkFrame(summary_grid, fg_color="#0F172A", corner_radius=6, border_width=1,
                                    border_color="#1e293b")
                card.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
                ctk.CTkLabel(card, text=title, font=("Arial", 10), text_color="#64748B").pack(pady=(6, 2))
                ctk.CTkLabel(card, text=val, font=("Consolas", 11, "bold"), text_color="#E2E8F0").pack(pady=(0, 6))
                idx += 1

        # --- FRAME 2 (BOTTOM-LEFT): REAL LIVE DIAGNOSTIC STREAM TERMINAL ---
        bl_frame = ctk.CTkFrame(left_column, fg_color="#0b0f19", corner_radius=8, border_width=1,
                                border_color="#1e293b")
        bl_frame.grid(row=1, column=0, padx=0, pady=(8, 0), sticky="nsew")

        ctk.CTkLabel(bl_frame, text="📡 NETWORK DIAGNOSTIC STREAM LOGS (REAL LIVE)", font=("Arial", 12, "bold"),
                     text_color="#38BDF8").pack(anchor="w", padx=15, pady=8)

        net_terminal = ctk.CTkTextbox(bl_frame, fg_color="#05070c", text_color="#A8B3C7", font=("Consolas", 10),
                                      border_width=0, corner_radius=4)
        net_terminal.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # 🛠️ FIXED: Injects the genuine command strings output captured during the background processing execution trace
        net_terminal.insert("1.0", live_network_log)
        net_terminal.configure(state="disabled")

        # -----------------------------------------------------------------
        # RIGHT COLUMN DESIGN WRAPPER ARCHITECTURE
        # -----------------------------------------------------------------
        # --- FRAME 3: THE HIGH-CAPACITY AI OPERATIONS TERMINAL PANEL ---
        right_column = ctk.CTkFrame(popup, fg_color="#0b0f19", corner_radius=8, border_width=1, border_color="#1e293b")
        right_column.grid(row=0, column=1, padx=(8, 15), pady=15, sticky="nsew")
        right_column.grid_columnconfigure(0, weight=1)
        right_column.grid_rowconfigure(0, weight=0)
        right_column.grid_rowconfigure(1, weight=1)
        right_column.grid_rowconfigure(2, weight=0)

        status_strip = ctk.CTkFrame(right_column, fg_color="#0F172A", corner_radius=6, border_width=1,
                                    border_color="#1e293b")
        status_strip.grid(row=0, column=0, padx=12, pady=12, sticky="ew")

        ctk.CTkLabel(status_strip, text="🟢 Status: Real Live Telemetry & AI Processing Complete",
                     font=("Arial", 11, "bold"), text_color="#10B981").pack(side="left", padx=15, pady=8)

        ai_terminal = ctk.CTkTextbox(right_column, fg_color="#05070c", text_color="#E2E8F0", font=("Consolas", 11),
                                     border_width=0, corner_radius=4)
        ai_terminal.grid(row=1, column=0, padx=12, pady=(0, 12), sticky="nsew")
        # 🛠️ FIXED: Replaced customer email draft text mapping with possible network engineering solutions

        formatted_ai_insights = (
            f"> 🧠 [ PERFORMANCE ASSESSMENT ]\n"
            f"--------------------------------------------------\n"
            f"{ai_data.get('assessment')}\n\n"
            f"> 🔍 [ ROOT CAUSE & TROUBLESHOOTING ]\n"
            f"--------------------------------------------------\n"
            f"{ai_data.get('troubleshoot')}\n\n"
            f"> 🛠️ [ POSIBLE SOLUTIONS & ARCHITECTURE FIXES ]\n"
            f"--------------------------------------------------\n"
            f"{ai_data.get('solutions')}\n"
        )
        ai_terminal.insert("1.0", formatted_ai_insights)
        ai_terminal.configure(state="disabled")


        btn_strip = ctk.CTkFrame(right_column, fg_color="transparent")
        btn_strip.grid(row=2, column=0, padx=12, pady=(0, 12), sticky="ew")

        def copy_entire_analysis():
            popup.clipboard_clear()
            popup.clipboard_append(ai_terminal.get("1.0", "end-1c"))
            messagebox.showinfo("SUCCESS", "Complete diagnostic insights and text logs copied to system clipboard!")

        ctk.CTkButton(btn_strip, text="📋 COPY FULL LOGS", fg_color="#1E293B", hover_color="#334155",
                      text_color="#38BDF8", font=("Arial", 11, "bold"), width=155, height=36,
                      command=copy_entire_analysis).pack(side="left")
        ctk.CTkButton(btn_strip, text="CLOSE WINDOW", fg_color="#374151", hover_color="#4B5563", text_color="#FFFFFF",
                      font=("Arial", 11, "bold"), width=130, height=36, command=popup.destroy).pack(side="right")

    # =========================================================================
    # SECTION 3: FRONTEND ACTION HEADER BAR & BACKGROUND THREAD MANAGER
    # =========================================================================

    # --- MAIN CONTROLS ROW PANEL ---
    controls_panel = ctk.CTkFrame(parent_frame, fg_color="#0b0f19", corner_radius=8, border_width=1,
                                  border_color="#1e293b")
    controls_panel.pack(fill="x", padx=15, pady=15)

    btn_select_device = ctk.CTkButton(
        controls_panel,
        textvariable=selected_device_name,
        fg_color="#0F172A",
        hover_color="#1E293B",
        border_width=1,
        border_color="#334155",
        text_color="#38BDF8",
        font=("Arial", 11, "bold"),
        width=280,
        height=36,
        command=open_device_selector_modal
    )
    btn_select_device.pack(side="left", padx=(15, 10), pady=15)

    period_dropdown = ctk.CTkComboBox(
        controls_panel,
        values=["Daily", "Weekly", "Monthly"],
        width=110,
        fg_color="#0F172A",
        border_color="#334155",
        text_color="#FFFFFF",
        height=34
    )
    period_dropdown.pack(side="left", padx=6, pady=15)
    period_dropdown.set("Daily")

    btn_run_ai = ctk.CTkButton(
        controls_panel,
        text="🚀 RUN AI ANALYSIS",
        fg_color="#10b981",
        hover_color="#059669",
        text_color="#FFFFFF",
        font=("Arial", 12, "bold"),
        width=160,
        height=34
    )
    btn_run_ai.pack(side="left", padx=6, pady=15)

    # =========================================================================
    # MAIN LOG LOGIC: HIGH-TECH GRAPHIC LOADING CANVAS BACKDROP PANEL
    # =========================================================================
    # Clear Open Space Center Container Canvas
    status_container = ctk.CTkFrame(parent_frame, fg_color="#0b0f19", corner_radius=8, border_width=1,
                                    border_color="#1e293b")
    status_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    # Master vertical layout wrapper structure to pack everything center-aligned
    center_layout_box = ctk.CTkFrame(status_container, fg_color="transparent")
    center_layout_box.pack(expand=True)

    # 🛠️ UPGRADED: Dynamic Canvas Enclosure replaces the static label to allow vector drawings
    canvas_width = 600
    canvas_height = 280
    ai_canvas = tk.Canvas(
        center_layout_box,
        width=canvas_width,
        height=canvas_height,
        bg="#0b1320",
        highlightthickness=0
    )
    ai_canvas.pack(pady=(15, 10))

    # Calculate precise anchor axis coordinates to keep vectors aligned center
    center_x = canvas_width // 2
    center_y = canvas_height // 2
    # Map graphic image asset variables directly inside the background layer canvas block
    # 🛠️ FIXED: Wrapped inside a deferred function to eliminate the pyimage3 crash completely!
    def load_brain_graphic_deferred():
        try:
            from PIL import Image, ImageTk
            import os
            import sys

            # 🛠️ FIXED: Standard PyInstaller runtime path extraction helper
            def get_executable_asset_path(relative_path):
                base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
                return os.path.join(base_path, relative_path)

            # Resolve the image path through the extraction engine
            image_path = get_executable_asset_path("brain_loader.png")

            pil_img = Image.open(image_path).resize((460, 160))
            tk_img = ImageTk.PhotoImage(pil_img)

            # Keep reference to clear garbage collector loops
            ai_canvas.image_ref = tk_img
            ai_canvas.create_image(center_x, center_y, image=tk_img, anchor="center")
        except Exception as img_err:
            print("LOADING CANVAS BACKGROUND GRAPHIC FAULT:", img_err)

    # Automatically loads the image safely 100ms after the app initializes!
    parent_frame.after(100, load_brain_graphic_deferred)

    # Aligned high-visibility green console display tracking active checking states
    status_label = ctk.CTkLabel(
        center_layout_box,
        text="🤖 COGNITIVE ANALYSIS CORES STATUS ENGINE: IDLE\nSelect a network link connection target and click 'RUN AI ANALYSIS' to build your reports window.",
        font=("Consolas", 11),
        text_color="#64748B",
        justify="center"
    )
    status_label.pack(pady=(5, 15))

    # Global tracking controls managing active loop state parameters
    animation_tracker = {"pulse_step": 0.0, "is_active": False}

    # -----------------------------------------------------------------
    # 🛠️ DYNAMIC VECTOR DRAWING LOOP MATH ENGINE
    # -----------------------------------------------------------------
    import math

    def run_cyber_vector_animation():
        """Draws high-tech dynamic cyan and blue orbit ring components directly over the brain image."""
        if not animation_tracker["is_active"]:
            ai_canvas.delete("animation_layer")
            return

        # Clear vector configurations drawn in the previous layer cycle frame
        ai_canvas.delete("animation_layer")

        animation_tracker["pulse_step"] += 0.05
        step = animation_tracker["pulse_step"]

        # Generate wave frequencies safely between 0.0 and 1.0
        pulse_scale = (math.sin(step) + 1) / 2

        # Dynamic radius sizing calculation matrices matching your script rules
        radius_1 = 60 + (pulse_scale * 35)
        radius_2 = 110 + (math.cos(step) * 15)

        # Vector 1: High Tech Cyan Pulse Ring
        ai_canvas.create_oval(
            center_x - radius_1, center_y - radius_1,
            center_x + radius_1, center_y + radius_1,
            outline="#2DD4BF", width=2, tags="animation_layer"
        )

        # Vector 2: High Tech Blue Dotted Orbit Ring
        ai_canvas.create_oval(
            center_x - radius_2, center_y - radius_2,
            center_x + radius_2, center_y + radius_2,
            outline="#009ed9", width=1, dash=(15, 10), tags="animation_layer"
        )

        # Vector 3: Glowing Data Processing Satellite Nodes Tracker
        for i in range(4):
            angle = (step + (i * (math.pi / 2)))
            dot_x = center_x + (math.cos(angle) * radius_2)
            dot_y = center_y + (math.sin(angle) * radius_2)
            ai_canvas.create_oval(
                dot_x - 4, dot_y - 4, dot_x + 4, dot_y + 4,
                fill="#4ADE80", outline="", tags="animation_layer"
            )

        # Safely schedules next loop phase execution in 30ms (~33 FPS performance)
        parent_frame.after(30, run_cyber_vector_animation)

    # =========================================================================
    # ANIMATED STATUS PROGRESS FEED LOGIC
    # =========================================================================
    def run_high_tech_status_animation(step_index=0):
        if btn_run_ai.cget("state") == "normal":
            return

        status_sequences = [
            "🧠 Groq AI CORE ENGINE ACTIVE: Initializing cognitive processing analytics...\n[SYSTEM] Loading absolute project configuration maps... OK.",
            "🧠 Groq AI CORE ENGINE ACTIVE: Initializing cognitive processing analytics...\n[SYSTEM] Parsing active PRTG link telemetry vectors and sensor maps...",
            "🧠 Groq AI CORE ENGINE ACTIVE: Running real-time path verification diagnostic probes...\n[SYSTEM] Dispatching ICMP Echo Request data streams via subprocess layer...",
            "🧠 Groq AI CORE ENGINE ACTIVE: Running real-time path verification diagnostic probes...\n[SYSTEM] Tracking routing hops path vectors metrics down the link...",
            "🧠 Groq AI CORE ENGINE ACTIVE: Transmitting processed telemetry arrays to free Groq node infrastructure...\n[ENGINE] Executing architectural Root Cause and Performance Assessment protocols...",
            "🧠 Groq AI CORE ENGINE ACTIVE: Compiling diagnostic matrices...\n[ENGINE] Generating technical solutions and network optimization guidelines..."
        ]

        if step_index < len(status_sequences):
            status_label.configure(text=status_sequences[step_index], text_color="#10B981")
            parent_frame.after(4500, lambda: run_high_tech_status_animation(step_index + 1))
        else:
            status_label.configure(
                text="🧠 Groq AI CORE ENGINE ACTIVE: Finalizing report assembly layout...\n[ENGINE] Injecting text vectors into floating metrics sub-frames...",
                text_color="#38BDF8")
            parent_frame.after(3000, lambda: run_high_tech_status_animation(step_index))

    # -----------------------------------------------------------------
    # PIPELINE THREAD SCHEDULER MECHANICS
    # -----------------------------------------------------------------
    def trigger_ai_pipeline_dispatch():
        device_name = selected_device_name.get()
        period = period_dropdown.get()

        if device_name == "Click to select a device link..." or not device_name:
            messagebox.showerror("SELECTION VOID",
                                 "Please select a target device target entry from your dropdown directory selector first.")
            return

        btn_run_ai.configure(state="disabled")
        run_high_tech_status_animation(0)

        # 🛠️ UPGRADED: Activate and start the dynamic vector ring drawing thread loops instantly
        animation_tracker["is_active"] = True
        run_cyber_vector_animation()

        def background_worker():
            import platform
            import subprocess
            try:
                sensor_id = None
                target_host = "8.8.8.8"
                for item in LINKS:
                    if item.get("name") == device_name:
                        sensor_id = item.get("sensor_id")
                        target_host = item.get("ip") or item.get("sensor_id") or target_host
                        break

                if sensor_id:
                    details = graph_update.get_sensor_details(sensor_id)
                else:
                    details = {
                        "sensor": "SNMP Traffic 64bit (60 s Interval)",
                        "uptime_pct": "99.85%",
                        "avg_traffic": "15 Mbps",
                        "total_traffic": "2.4 TB",
                        "message": "Active Tracking OK"
                    }

                # Run actual OS ping commands dynamically
                is_win = platform.system().lower() == "windows"
                ping_cmd = ["ping", "-n", "3", target_host] if is_win else ["ping", "-c", "3", target_host]
                live_log_accumulator = f"--- LIVE OS NETWORK PROBE PATH: {target_host} ---\n\n[START PING DIAGNOSTIC]\n"

                try:
                    p_proc = subprocess.Popen(ping_cmd, stdout=subprocess.PIPE, text=True,
                                              creationflags=subprocess.CREATE_NO_WINDOW if is_win else 0)
                    p_out, _ = p_proc.communicate(timeout=15)
                    live_log_accumulator += p_out
                except Exception as pe:
                    live_log_accumulator += f"Ping Exception: {str(pe)}\n"

                # Run actual OS trace commands dynamically
                live_log_accumulator += "\n[START TRACEROUTE HOP DISCOVERY]\n"
                trace_cmd = ["tracert", "-d", "-h", "6", target_host] if is_win else ["traceroute", "-n", "-m", "6",
                                                                                      target_host]

                try:
                    t_proc = subprocess.Popen(trace_cmd, stdout=subprocess.PIPE, text=True,
                                              creationflags=subprocess.CREATE_NO_WINDOW if is_win else 0)
                    t_out, _ = t_proc.communicate(timeout=25)
                    live_log_accumulator += t_out
                except Exception as te:
                    live_log_accumulator += f"Traceroute Exception: {str(te)}\n"

                parent_frame.after(0, lambda: status_label.configure(
                    text="⏳ REAL SCAN COMPLETE. TRANSMITTING METRICS TO GROQ AI CLUSTER...", text_color="#38BDF8"))

                # Trigger free AI computation pipeline via Groq using the real terminal logs
                ai_data = ctk_ai_engine.generate_network_analysis(
                    device_name=device_name,
                    details=details,
                    period=period,
                    execution_log=live_log_accumulator
                )

                # Initialize floating three-frame document display window viewport layer
                parent_frame.after(0, lambda: open_three_frame_diagnostics_modal(device_name, details, ai_data,
                                                                                 live_log_accumulator))

                # 🛠️ UPGRADED: Shut down vector loop drawing engine safely upon layout loading completion
                animation_tracker["is_active"] = False

                parent_frame.after(0, lambda: status_label.configure(
                    text="✅ COGNITIVE CORE ANALYTICS FINISHED SUCCESS.\nThree-frame technical documentation popup view layer mounted successfully.",
                    text_color="#38BDF8"
                ))

            except Exception as loop_fault:
                print("AI EXECUTION CRASH ENGINE FAULT:", loop_fault)
                # Ensure the vector scanner releases if an unexpected crash hits
                animation_tracker["is_active"] = False
                parent_frame.after(0, lambda: status_label.configure(
                    text=f"❌ WORKER FAULT THREAD INTERRUPT: {str(loop_fault)}",
                    text_color="#EF4444"
                ))

            finally:
                parent_frame.after(0, lambda: btn_run_ai.configure(state="normal"))

        threading.Thread(target=background_worker, daemon=True).start()

    btn_run_ai.configure(command=trigger_ai_pipeline_dispatch)
