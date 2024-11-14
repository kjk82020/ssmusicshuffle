from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
import json
import random

class PlaylistShufflerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.file_chooser = FileChooserListView(path='/')
        self.shuffle_button = Button(text='Shuffle Playlist', on_press=self.shuffle_playlist)
        self.result_label = Label(text='Select a .smpl file and press Shuffle')

        self.layout.add_widget(self.file_chooser)
        self.layout.add_widget(self.shuffle_button)
        self.layout.add_widget(self.result_label)

        return self.layout

    def shuffle_playlist(self, instance):
        selected_file = self.file_chooser.selection
        if not selected_file:
            self.result_label.text = 'Please select a .smpl file'
            return

        playlist_file = selected_file[0]
        if not playlist_file.endswith('.smpl'):
            self.result_label.text = 'Please select a valid .smpl file'
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

            self.result_label.text = f'Playlist shuffled and saved:\n{playlist_file}'
        except Exception as e:
            self.result_label.text = f'Error: {str(e)}'

if __name__ == '__main__':
    PlaylistShufflerApp().run()