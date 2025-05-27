import json
import requests
import time


class EverAITTS:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url_base = 'https://www.everai.vn/api/v1/tts'

    def generate_voice(self, text, voice_code, audio_type='mp3',
                       bitrate=128, speed_rate=1.0, pitch_rate=1.0,
                       volume=None, callback_url=None):
        '''
        Gửi yêu cầu tạo giọng nói đến EverAI và trả về request_id.
        '''

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        body = {
            'response_type': 'indirect',
            'input_text': text,
            'voice_id': voice_code,
            'audio_type': audio_type,
            'bitrate': bitrate,
            'speed_rate': speed_rate,
            'pitch_rate': pitch_rate,
        }

        if callback_url:
            body['callback_url'] = callback_url
        if volume is not None:
            body['volume'] = volume

        response = requests.post(self.url_base, headers=headers, json=body)

        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code} - {response.text}")

        result = response.json().get('result')
        if not result:
            raise Exception(f"Invalid response: {response.text}")

        request_id = result['request_id']
        print(f"🕒 Đã gửi request (ID: {request_id})")
        return request_id

    def get_request_status(self, request_id):
        '''
        Kiểm tra trạng thái xử lý của request và trả về đường link audio nếu đã hoàn tất.
        '''

        url = f"{self.url_base}/{request_id}"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"GET request failed: {response.status_code} - {response.text}")

        result = response.json().get('result')
        if not result:
            raise Exception("No result returned in response.")

        status = result.get('status')
        progress = result.get('progress', 0)
        audio_link = result.get('audio_link')

        print(f"📊 Trạng thái: {status}, Tiến độ: {progress}%")

        if status == 'done' and audio_link:
            return audio_link
        elif status == 'failure':
            raise Exception("❌ Request failed.")
        else:
            return None  # Chưa xong

    def wait_and_download(self, request_id, filename, check_interval=3, timeout=60):
        '''
        Đợi cho tới khi audio hoàn tất, sau đó tải file về.
        '''

        start_time = time.time()
        while time.time() - start_time < timeout:
            audio_link = self.get_request_status(request_id)
            if audio_link:
                print(f"✅ Hoàn tất. Tải từ: {audio_link}")
                audio_data = requests.get(audio_link)
                with open(filename, 'wb') as f:
                    f.write(audio_data.content)
                print(f"💾 File đã lưu tại: {filename}")
                return filename
            time.sleep(check_interval)

        raise TimeoutError("⏰ Quá thời gian chờ xử lý audio.")
    
# if __name__ == "__main__":
#     # Example
#     api_key = "ztrinQTPSlB5NZz8vmAHZE4iaMNLLyCzm"
#     tts = EverAITTS(api_key)

#     # Bước 1: Gửi yêu cầu tạo giọng nói
#     request_id = tts.generate_voice(
#         text="Sự thật thú vị mà có lẽ bạn đéo biết",
#         voice_code="vi_male_onyx_default"
#     )

#     # Bước 2: Đợi và tải về file âm thanh
#     tts.wait_and_download(request_id, filename='everai_output.mp3')