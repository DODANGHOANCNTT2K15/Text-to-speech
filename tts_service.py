import os
import json
from gtts import gTTS

class TTSService:
    def __init__(self, config_path="config.json"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.output_dir = "audio"
        os.makedirs(self.output_dir, exist_ok=True)

    def text_to_speech(self, text, lang, voice, output_file=None):
        """
        Chuyển văn bản thành giọng nói dùng gTTS.
        :param text: Văn bản cần chuyển đổi
        :param lang: Ngôn ngữ (vi, en)
        :param voice: ID giọng nói (gTTS dùng lang làm voice)
        :param output_file: Tên file đầu ra (nếu không cung cấp, tạo tên mặc định)
        :return: Đường dẫn file âm thanh hoặc None nếu lỗi
        """
        if not output_file:
            output_file = os.path.join(self.output_dir, f"output_{lang}.mp3")

        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(output_file)
            return output_file
        except Exception as e:
            print(f"Lỗi: {e}")
            return None

    def play_audio(self, audio_file):
        """
        Phát file âm thanh.
        :param audio_file: Đường dẫn file âm thanh
        """
        try:
            if os.name == 'nt':  # Windows
                os.system(f"start {audio_file}")
            else:  # macOS/Linux
                os.system(f"mpg123 {audio_file}")
        except Exception as e:
            print(f"Lỗi khi phát âm thanh: {e}")

    def get_languages(self):
        """
        Lấy danh sách ngôn ngữ từ config.
        :return: Dict chứa thông tin ngôn ngữ
        """
        return self.config["languages"]

    def get_voices(self, lang):
        """
        Lấy danh sách giọng nói của ngôn ngữ.
        :param lang: Mã ngôn ngữ (vi, en)
        :return: List giọng nói
        """
        return self.config["languages"].get(lang, {}).get("voices", [])