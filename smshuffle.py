from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import json
import random

class PlaylistShufflerLayout(BoxLayout):
    def shuffle_playlist(self):
        selected_file = self.ids.filechooser.selection
        if not selected_file:
            self.ids.result_label.text = 'Please select a .smpl file'
            return

        playlist_file = selected_file[0]
        if not playlist_file.endswith('.smpl'):
            self.ids.result_label.text = 'Please select a valid .smpl file'
            return

        try:
            # 파일 읽기
            with open(playlist_file, 'r', encoding='utf-8') as file:
                playlist_data = file.read()

            # JSON 파싱
            playlist = json.loads(playlist_data)

            # order 값 섞기
            current_orders = [song['order'] for song in playlist['members']]
            shuffled_orders = list(range(1, len(current_orders) + 1))
            random.shuffle(shuffled_orders)

            # 새로운 order 값 할당
            for song, new_order in zip(playlist['members'], shuffled_orders):
                song['order'] = new_order

            # 수정된 플레이리스트를 JSON으로 변환 (줄바꿈 없이)
            shuffled_playlist = json.dumps(playlist, ensure_ascii=False, separators=(',', ':'))

            # 파일에 다시 쓰기
            with open(playlist_file, 'w', encoding='utf-8') as file:
                file.write(shuffled_playlist)

            self.ids.result_label.text = f'Playlist shuffled and saved:\n{playlist_file}'
        except Exception as e:
            self.ids.result_label.text = f'Error: {str(e)}'

class PlaylistShufflerApp(App):
    def build(self):
        return PlaylistShufflerLayout()

if __name__ == '__main__':
    Builder.load_file('smshuffle.kv')
    PlaylistShufflerApp().run()
