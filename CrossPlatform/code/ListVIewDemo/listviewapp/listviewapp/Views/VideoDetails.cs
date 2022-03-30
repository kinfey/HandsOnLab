using System;
using listViewapp.Models;

namespace listViewapp.Views
{
	public class VideoDetails : View
	{
		[Environment]
		readonly Video video;

		public VideoDetails()
		{
			Body = () => new VStack {
				new Image(() => video.Cover).Frame(160, 90),
				new Text(() => video.Title),
				new Text(() => video.Author),
				new Text(() => video.Date),
			}.Background(Colors.White);
		}
	}
}