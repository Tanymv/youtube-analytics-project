from src.apimixin import APIMixin
import datetime
import isodate


class PlayList(APIMixin):
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist_info = self.get_service().playlists().list(id=playlist_id, part='snippet,contentDetails',
                                                                 maxResults=50).execute()
        self.playlist_videos = self.get_service().playlistItems().list(playlistId=playlist_id,
                                                                       part='contentDetails, snippet',
                                                                       maxResults=50, ).execute()
        self.title = self.playlist_info['items'][0]['snippet']['title']
        self.url = "https://www.youtube.com/playlist?list=" + playlist_id
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                               id=','.join(self.video_ids)).execute()

    @property
    def total_duration(self):
        """возвращает объект класса datetime.timedelta с суммарной длительностью плейлиста """
        total = datetime.timedelta(0)

        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration
        return total

    def show_best_video(self):
        """возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""

        best_video = max(self.video_response['items'], key=lambda d: int(d['statistics']['likeCount']))
        return "https://youtu.be/" + best_video['id']
