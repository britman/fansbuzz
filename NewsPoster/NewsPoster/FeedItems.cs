﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace NewsPoster
{
    class FeedItems : List<FeedItem>
    {
        public FeedItems()
        {
            this.Add(new FeedItem(new Uri("http://newsrss.bbc.co.uk/rss/sportonline_uk_edition/football/rss.xml")));
            this.Add(new FeedItem(new Uri("http://www.skysports.com/rss/0,20514,11095,00.xml")));
            this.Add(new FeedItem(new Uri("http://www.guardian.co.uk/football/rss")));
            this.Add(new FeedItem(new Uri("http://www.teamtalk.com/rss/0,16039,2483,00.xml")));
            this.Add(new FeedItem(new Uri("http://www.thesun.co.uk/sol/homepage/feeds/rss/article247739.ece")));
            this.Add(new FeedItem(new Uri("http://www.mirror.co.uk/sport/football/rss.xml")));            
            this.Add(new FeedItem(new Uri("http://www.telegraph.co.uk/newsfeed/rss/sport_football.xml")));
            this.Add(new FeedItem(new Uri("http://www.sportinglife.com/rss/football.xml")));
            this.Add(new FeedItem(new Uri("http://feeds.reuters.com/reuters/UKFootballNews")));
            string[] englandTags = {"England"};
            this.Add(new FeedItem(new Uri("http://www.thefa.com/rss/england/rss.xml"),englandTags));  
            this.Add(new FeedItem(new Uri("http://www.goal442.com/feed/")));            
            this.Add(new FeedItem(new Uri("http://www.clubcall.com/rss.xml")));
            this.Add(new FeedItem(new Uri("http://downloads.bbc.co.uk/podcasts/fivelive/5lfd/rss.xml")));           
        }
    }
}
