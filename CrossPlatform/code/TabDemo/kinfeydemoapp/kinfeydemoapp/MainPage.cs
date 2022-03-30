namespace kinfeydemoapp;
using System.Collections.Generic;
using kinfeydemoapp.Models;
using kinfeydemoapp.Views;
public class MainPage : View
{
	List<TabItem> tabs = new List<TabItem>
	{
		new TabItem("首页","home2.png"),
		new TabItem("动态","list2.png"),
		new TabItem("直播","live2.png"),
		new TabItem("我","me2.png"),
	};

	
	View tabView() =>new TabView
			{	
				tabs.Select(item=>new HStack{
					new Text(item.Title).Color(Colors.Blue)
				}.TabIcon(item.Icon).TabText(item.Title).Color(Colors.Black))
                
			}.Title("MSReactor");

	
	// View tabView1() => new TabView
	// 		{
	// 			new HStack{
	// 				new Text("Tab 1"),
	// 			}.TabText("首页"),
	// 			new HStack
	// 			{
	// 				new Text("Tab 2"),
	// 			}.TabText("动态"),
	// 			new HStack{
	// 				new Text("Tab 1"),
	// 			}.TabText("直播"),
	// 			new HStack
	// 			{
	// 				new Text("Tab 2"),
	// 			}.TabText("我")
	// 		};




	[Body]
	View body()
		=> new NavigationView
		{ 
			tabView()
		  
		};
}


