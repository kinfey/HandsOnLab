using System;
namespace listViewapp.Models
{
	public class Video : BindingObject
	{
		public string Cover
		{
			get => GetProperty<string>();
			set => SetProperty(value);
		}

		public string Title
		{
			get => GetProperty<string>();
			set => SetProperty(value);
		}

		public string Author
		{
			get => GetProperty<string>();
			set => SetProperty(value);
		}

		public string Date
		{
			get => GetProperty<string>();
			set => SetProperty(value);
		}
    }
}