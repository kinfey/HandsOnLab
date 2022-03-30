namespace listviewapp;
using System;
using System.Collections.Generic;
using listViewapp.Models;
using listViewapp.Views;
public class MainPage : View
{

	[State]
	readonly CometRide comet = new();


		List<Video> Videos = new List<Video> {
			new Video {
				Title = "MAUI 介绍 1",
				Author = "主讲： Kinfey Lo",
				Date = "2022-03-30",
				Cover = "cover.png"
			},
			new Video {
				Title = "MAUI 介绍 2",
				Author = "主讲： Kinfey Lo",
				Date = "2022-03-30",
				Cover = "cover.png"
			},
			new Video {
				Title = "MAUI 介绍 3",
				Author = "主讲： Kinfey Lo",
				Date = "2022-03-30",
				Cover = "cover.png"
			},
			new Video {
				Title = "MAUI 介绍 4",
				Author = "主讲： Kinfey Lo",
				Date = "2022-03-30",
				Cover = "cover.png"
			},
			new Video {
				Title = "MAUI 介绍 5",
				Author = "主讲： Kinfey Lo",
				Date = "2022-03-30",
				Cover = "cover.png"
			},
			new Video {
				Title = "MAUI 介绍 6",
				Author = "主讲： Kinfey Lo",
				Date = "2022-03-30",
				Cover = "cover.png"
			},
			new Video {
				Title = "MAUI 介绍 7",
				Author = "主讲： Kinfey Lo",
				Date = "2022-03-30",
				Cover = "cover.png"
			},
			new Video {
				Title = "MAUI 介绍 8",
				Author = "主讲： Kinfey Lo",
				Date = "2022-03-30",
				Cover = "cover.png"
			}
		};


    View ProfileView() => new HStack
    {
        new Image(()=>"logo.jpeg")
		    .Frame(height: 60, width: 66)
            .ClipShape(new Ellipse()),
        new VStack(LayoutAlignment.Start) {
            new Text(()=> "Reactor上海")
                .FontSize(18)
                .FontWeight(FontWeight.Bold),
            new Text(()=> "我们一起来学习")
                .FontSize(14),
        }
        .Margin(left: 12),
        new Spacer(),

    }.FitVertical();


		View listview() => new ListView<Video>(Videos)
		{
			ViewFor = (video) => new HStack
			{
				new Image (video.Cover).Frame(160, 90).Margin(4),
				new VStack(LayoutAlignment.Start, spacing:2)
				{
					new Text (video.Title).FontSize(18),
					new Text (video.Author).Color(Colors.Grey),
					new Text (video.Date).Color(Colors.Grey),
				}.FontSize(12)
			}.Frame(height: 110).Alignment(Alignment.Leading),
		}.OnSelectedNavigate((video) => new VideoDetails().SetEnvironment("video",video));

	[Body]
	View body() 
		=> 
			new VStack {
			  ProfileView(),
			  listview()
		    };

	public class CometRide : BindingObject
	{
		public int Rides
		{
			get => GetProperty<int>();
			set => SetProperty(value);
		}

		public string CometTrain
		{
			get
			{
				return "☄️".Repeat(Rides);
			}
		}
	}
}


