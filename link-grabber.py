import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import requests
import re
import time

APP_ICON = "icon.ico"  # Global icon for window and messageboxes

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, bg_color, fg_color="white", btn_width=150):
        tk.Canvas.__init__(self, parent, height=45, width=btn_width, bg=parent['bg'], highlightthickness=0)
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.btn_width = btn_width

        # Draw rounded rectangle
        self.rounded_rect = self.create_rounded_rectangle(5, 5, btn_width-5, 40, radius=22, fill=bg_color, outline="")
        self.text_id = self.create_text(btn_width/2, 22, text=text, fill=fg_color, font=("Segoe UI", 10, "bold"))

        self.bind("<Button-1>", lambda e: self.command())
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, x2, y1+radius,
                  x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2,
                  x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius,
                  x1, y1+radius, x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)

    def on_enter(self, e):
        self.config(cursor="hand2")

    def on_leave(self, e):
        self.config(cursor="")

    def configure_state(self, state):
        if state == "disabled":
            self.itemconfig(self.rounded_rect, fill="#cccccc")
            self.unbind("<Button-1>")
        else:
            self.itemconfig(self.rounded_rect, fill=self.bg_color)
            self.bind("<Button-1>", lambda e: self.command())


class LinkGrabberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Link Grabber")
        self.root.geometry("900x700")
        self.root.configure(bg="#1e1e1e")
        self.root.minsize(700, 500)

        # ---- Set main window icon ----
        try:
            self.root.iconbitmap(APP_ICON)
        except:
            pass

        # ---- Make messagebox dialogs use same icon ----
        self.msgbox_root = tk.Toplevel()
        self.msgbox_root.withdraw()
        try:
            self.msgbox_root.iconbitmap(APP_ICON)
        except:
            pass

        self.is_running = False
        self.extracted_links = []

        self.setup_ui()

    def setup_ui(self):
        container = tk.Frame(self.root, bg="#1e1e1e")
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Logo placeholder
        logo_frame = tk.Frame(container, bg="#1e1e1e")
        logo_frame.pack(pady=(0, 8))
        logo_canvas = tk.Canvas(logo_frame, width=50, height=50, bg="#1e1e1e", highlightthickness=0)
        logo_canvas.pack()
        logo_canvas.create_oval(5, 5, 45, 45, fill="#3498db", outline="")
        logo_canvas.create_polygon([25, 13, 21, 26, 27, 26, 23, 39, 31, 24, 25, 24], fill="#ffffff", outline="")

        tk.Label(container, text="Link Grabber", font=("Segoe UI", 22, "bold"),
                 bg="#1e1e1e", fg="#ffffff").pack(pady=(0, 3))
        tk.Label(container, text="Extract fuckingfast.co download links", font=("Segoe UI", 9),
                 bg="#1e1e1e", fg="#b0b0b0").pack(pady=(0, 15))

        # Input area
        input_frame = tk.Frame(container, bg="#2d2d2d", highlightthickness=1, 
                               highlightbackground="#3d3d3d", highlightcolor="#3d3d3d")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        tk.Label(input_frame, text="Paste URLs Here", font=("Segoe UI", 9, "bold"),
                 bg="#2d2d2d", fg="#ffffff").pack(anchor=tk.W, padx=12, pady=(8, 5))
        self.input_text = tk.Text(input_frame, font=("Consolas", 9), bg="#252525", fg="#e0e0e0",
                                  relief=tk.FLAT, padx=12, pady=8, wrap=tk.WORD,
                                  insertbackground="#3498db", selectbackground="#3d5875",
                                  selectforeground="#ffffff")
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        # Buttons
        btn_frame = tk.Frame(container, bg="#1e1e1e")
        btn_frame.pack(pady=(0, 12))
        self.start_btn = RoundedButton(btn_frame, "Start", self.start_extraction, "#3498db", btn_width=160)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn = RoundedButton(btn_frame, "Stop", self.stop_extraction, "#e74c3c", btn_width=160)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn.configure_state("disabled")
        self.save_btn = RoundedButton(btn_frame, "Save", self.save_links, "#27ae60", btn_width=160)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        self.save_btn.configure_state("disabled")

        # Status
        self.status_label = tk.Label(container, text="Ready", font=("Segoe UI", 8),
                                     bg="#1e1e1e", fg="#b0b0b0")
        self.status_label.pack(pady=(0, 8))

        # Progress bar
        self.progress_canvas = tk.Canvas(container, bg="#1e1e1e", highlightthickness=0, height=12)
        self.progress_canvas.pack(fill=tk.X, pady=(0, 15))
        self.progress_value = 0
        self.progress_max = 100
        self.progress_canvas.bind("<Configure>", lambda e: self.update_progress_bar())

        # Log area
        log_frame = tk.Frame(container, bg="#2d2d2d", highlightthickness=1,
                             highlightbackground="#3d3d3d", highlightcolor="#3d3d3d")
        log_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(log_frame, text="Activity Log", font=("Segoe UI", 9, "bold"),
                 bg="#2d2d2d", fg="#ffffff").pack(anchor=tk.W, padx=12, pady=(8, 5))
        self.log_text = tk.Text(log_frame, font=("Consolas", 8), bg="#252525", fg="#e0e0e0",
                                relief=tk.FLAT, state=tk.DISABLED, padx=12, pady=8, wrap=tk.WORD,
                                selectbackground="#3d5875", selectforeground="#ffffff")
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))
        self.log_text.tag_config("success", foreground="#27ae60")
        self.log_text.tag_config("error", foreground="#e74c3c")
        self.log_text.tag_config("info", foreground="#3498db")

    def update_progress_bar(self):
        canvas = self.progress_canvas
        canvas.delete("all")
        width = canvas.winfo_width()
        if width < 2: return
        self.create_rounded_rect(canvas, 0, 0, width, 12, 6, "#2d2d2d")
        progress_width = (self.progress_value / self.progress_max) * width
        if progress_width > 0:
            self.create_rounded_rect(canvas, 0, 0, progress_width, 12, 6, "#3498db")

    def create_rounded_rect(self, canvas, x1, y1, x2, y2, r, color):
        points = [x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r,
                  x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2,
                  x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r,
                  x1, y1+r, x1, y1]
        canvas.create_polygon(points, fill=color, outline="", smooth=True)

    def log(self, message, tag="normal"):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n", tag)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def extract_download_link(self, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                return None, f"HTTP {response.status_code}"
            pattern = r'window\.open\("(https://fuckingfast\.co/dl/[^"]+)"\)'
            match = re.search(pattern, response.text)
            if match:
                return match.group(1), None
            return None, "Link not found"
        except Exception:
            return None, "Connection error"

    def start_extraction(self):
        urls_text = self.input_text.get("1.0", tk.END).strip()
        if not urls_text:
            messagebox.showwarning("Empty", "Please paste URLs first!", parent=self.msgbox_root)
            return

        urls = []
        for line in urls_text.split("\n"):
            line = line.strip()
            if line.startswith("- ") or line.startswith("* "):
                line = line[2:].strip()
            if "fuckingfast.co" in line:
                urls.append(line)

        if not urls:
            messagebox.showwarning("Invalid", "No valid URLs found!", parent=self.msgbox_root)
            return

        self.is_running = True
        self.start_btn.configure_state("disabled")
        self.stop_btn.configure_state("normal")
        self.save_btn.configure_state("disabled")
        self.extracted_links = []
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state=tk.DISABLED)

        threading.Thread(target=self.extract_links, args=(urls,), daemon=True).start()

    def extract_links(self, urls):
        total = len(urls)
        self.progress_max = total
        self.progress_value = 0
        self.update_progress_bar()
        self.log(f"Processing {total} URLs...\n", "info")
        success = 0
        failed = 0

        for i, url in enumerate(urls, 1):
            if not self.is_running:
                self.log("\nStopped", "error")
                break

            self.status_label.config(text=f"Processing {i}/{total}")
            self.progress_value = i
            self.update_progress_bar()

            filename = url.split("#")[-1] if "#" in url else f"file_{i}"
            link, error = self.extract_download_link(url)
            if link:
                self.log(f"✓ [{i}/{total}] {filename[:50]}", "success")
                self.extracted_links.append(link)
                success += 1
            else:
                self.log(f"✗ [{i}/{total}] {filename[:50]}", "error")
                failed += 1

            time.sleep(0.5)

        self.log(f"\nComplete: {success} success, {failed} failed", "info")
        self.is_running = False
        self.start_btn.configure_state("normal")
        self.stop_btn.configure_state("disabled")
        if self.extracted_links:
            self.save_btn.configure_state("normal")
        self.status_label.config(text=f"Done - {success} links extracted")

        if success > 0:
            messagebox.showinfo("Success", f"Extracted {success} links!", parent=self.msgbox_root)

    def stop_extraction(self):
        self.is_running = False
        self.stop_btn.configure_state("disabled")
        self.status_label.config(text="Stopping...")

    def save_links(self):
        if not self.extracted_links:
            messagebox.showwarning("No Links", "No links to save!", parent=self.msgbox_root)
            return

        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                                                initialfile="download_links.txt")
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    for link in self.extracted_links:
                        f.write(link + "\n")
                messagebox.showinfo("Saved",
                                    f"Saved {len(self.extracted_links)} links!\n\n"
                                    "Import to IDM:\nTasks → Import → Import from text file",
                                    parent=self.msgbox_root)
                self.log(f"\nSaved: {filename}", "success")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save:\n{str(e)}", parent=self.msgbox_root)


def main():
    root = tk.Tk()
    app = LinkGrabberApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
