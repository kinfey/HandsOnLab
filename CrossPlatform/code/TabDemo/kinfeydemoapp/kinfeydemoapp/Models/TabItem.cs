using System;

namespace kinfeydemoapp.Models 
{
    public class TabItem
    {
        public TabItem()
        {

        }
        public TabItem(string title, string icon)
        {
            Title = title;
            Icon = icon;
        }
        public string Title { get; set; }
        public string Icon { get; set; }

        public override string ToString() => Title;
    }
}