namespace NewsPoster
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;

    class FeedItem
    {
        public FeedItem()
        {
            this.RssItems = new List<RssItem>();
        }

        public FeedItem(Uri feedUrl) : this()
        {
            this.FeedUrl = feedUrl;            
        }

        public FeedItem(Uri feedUrl, string[] specificTags) : this(feedUrl)
        {            
            this.SpecificTags = specificTags;
        }

        public Uri FeedUrl { get; set; }
        public string[] SpecificTags { get; set; }
        public List<RssItem> RssItems { get; set; }
    }
}
