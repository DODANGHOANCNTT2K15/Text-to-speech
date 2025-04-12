import tkinter as tk
from tkinter import messagebox
from tts_service import TTSService

class TTSGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Text to Speech App")
        self.root.geometry("500x400")
        self.tts_service = TTSService()

        self.current_audio_file = None  # Lưu đường dẫn file âm thanh hiện tại
        self.play_button = None  # Lưu tham chiếu đến nút Phát
        self.setup_gui()

    def setup_gui(self):
        # Frame cho ô nhập văn bản
        text_frame = tk.Frame(self.root)
        text_frame.pack(pady=10)
        tk.Label(text_frame, text="Nhập văn bản:").pack()
        self.text_entry = tk.Text(text_frame, height=5, width=50)
        self.text_entry.pack()

        # Frame cho lựa chọn ngôn ngữ
        lang_frame = tk.Frame(self.root)
        lang_frame.pack(pady=10)
        tk.Label(lang_frame, text="Chọn ngôn ngữ:").pack()
        self.lang_var = tk.StringVar(value="vi")
        languages = self.tts_service.get_languages()
        for lang_code, lang_info in languages.items():
            tk.Radiobutton(
                lang_frame,
                text=lang_info["name"],
                variable=self.lang_var,
                value=lang_code,
                command=self.update_voices
            ).pack(anchor="w")

        # Frame cho lựa chọn giọng nói
        self.voice_frame = tk.Frame(self.root)
        self.voice_frame.pack(pady=10)
        tk.Label(self.voice_frame, text="Chọn giọng nói:").pack()
        self.voice_var = tk.StringVar()
        self.voice_radios = []
        self.update_voices()  # Khởi tạo giọng nói ban đầu

        # Frame cho các nút
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Chuyển đổi", command=self.convert_text).pack(side=tk.LEFT, padx=10)
        self.play_button = tk.Button(button_frame, text="Phát", command=self.play_audio, state=tk.DISABLED)
        self.play_button.pack(side=tk.LEFT, padx=10)

    def update_voices(self):
        """
        Cập nhật danh sách giọng nói dựa trên ngôn ngữ được chọn.
        """
        # Xóa các radio button giọng nói cũ
        for radio in self.voice_radios:
            radio.destroy()
        self.voice_radios.clear()

        # Lấy danh sách giọng nói mới
        lang = self.lang_var.get()
        voices = self.tts_service.get_voices(lang)
        if voices:
            self.voice_var.set(voices[0]["id"])  # Chọn giọng đầu tiên làm mặc định
            for voice in voices:
                radio = tk.Radiobutton(
                    self.voice_frame,
                    text=voice["name"],
                    variable=self.voice_var,
                    value=voice["id"]
                )
                radio.pack(anchor="w")
                self.voice_radios.append(radio)

    def convert_text(self):
        """
        Chuyển văn bản thành giọng nói.
        """
        text = self.text_entry.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập văn bản!")
            return

        lang = self.lang_var.get()
        voice = self.voice_var.get()

        self.current_audio_file = self.tts_service.text_to_speech(text, lang, voice)
        if self.current_audio_file:
            messagebox.showinfo("Thành công", f"Đã tạo file âm thanh tại: {self.current_audio_file}")
            # Kích hoạt nút Phát
            self.play_button.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Lỗi", "Không thể chuyển đổi văn bản thành giọng nói.")

    def play_audio(self):
        """
        Phát file âm thanh hiện tại.
        """
        if self.current_audio_file:
            self.tts_service.play_audio(self.current_audio_file)
        else:
            messagebox.showwarning("Cảnh báo", "Chưa có file âm thanh để phát!")