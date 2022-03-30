using System;
using System.Collections.Generic;

namespace kinfeydemoapp.Views
{
	public class ImageViews : View
	{
        [Body]
		View ImageView() => new HStack()
		{
			new Image(()=>"dotnet_bot.png")
				.ClipShape(new Ellipse())
				.Alignment(Alignment.Center),
		};
	}

}