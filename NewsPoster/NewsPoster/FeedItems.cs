using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace NewsPoster
{
    class FeedItems : List<FeedItem>
    {
        public FeedItems()
        {       
            string[] englandTags = { "England", "The FA" };
            this.Add(new FeedItem(new Uri("http://www.thefa.com/rss/england/rss.xml"), englandTags));
            string[] goal442Tags = { "Goal442" };
            this.Add(new FeedItem(new Uri("http://www.goal442.com/feed/"),goal442Tags));
            string[] clubcallTags = { "Club Call" };
            this.Add(new FeedItem(new Uri("http://www.clubcall.com/rss-football.xml"), clubcallTags));
            string[] teletextTags = { "Teletext" };
            this.Add(new FeedItem(new Uri("http://feeds.teletext.co.uk/sport/football/scores/"), teletextTags));
            string[] echo1Tags = { "Liverpool", "Liverpool Echo" };
            this.Add(new FeedItem(new Uri("http://www.liverpoolecho.co.uk/liverpool-fc/liverpool-fc-news/rss.xml"), echo1Tags));
            string[] echo2Tags = { "Everton","Liverpool Echo" };
            this.Add(new FeedItem(new Uri("http://www.liverpoolecho.co.uk/everton-fc/everton-fc-news/rss.xml"), echo2Tags));
            string[] manEveTags = { "Man Utd", "Manchester Evening News" };
            this.Add(new FeedItem(new Uri("http://www.manchestereveningnews.co.uk/sport/football/manchester_united/rss.xml"), manEveTags));
            string[] manEve1Tags = { "Manchester City","Manchester Evening News" };
            this.Add(new FeedItem(new Uri("http://www.manchestereveningnews.co.uk/sport/football/manchester_city/rss.xml"), manEve1Tags));
            string[] fourfourtwoTags = { "FourFourTwo" };
            this.Add(new FeedItem(new Uri("http://fourfourtwo.com/rss/"), fourfourtwoTags));
            //uses other teletextTags            
            this.Add(new FeedItem(new Uri("http://feeds.teletext.co.uk/sport/football/stories"), teletextTags));
            string[] guardianTags = { "The Guardian" };
            this.Add(new FeedItem(new Uri("http://www.guardian.co.uk/football/rss"), guardianTags));
            string[] telegraphTags = { "The Telegraph" };
            this.Add(new FeedItem(new Uri("http://www.telegraph.co.uk/newsfeed/rss/sport_football.xml"), telegraphTags));
            string[] sportinglifeTags = { "Sportinglife" };
            this.Add(new FeedItem(new Uri("http://www.sportinglife.com/rss/football.xml"), sportinglifeTags));
            string[] reutersTags = { "Reuters" };
            this.Add(new FeedItem(new Uri("http://feeds.reuters.com/reuters/UKFootballNews"), reutersTags));
            string[] teamTalkTags = { "TeamTalk" };
            this.Add(new FeedItem(new Uri("http://www.teamtalk.com/rss/0,16039,2483,00.xml"), teamTalkTags));
            string[] sunTags = { "The Sun" };
            this.Add(new FeedItem(new Uri("http://www.thesun.co.uk/sol/homepage/feeds/rss/article247739.ece"), sunTags));
            string[] mirrorTags = { "The Mirror" };
            this.Add(new FeedItem(new Uri("http://www.mirror.co.uk/sport/football/rss.xml"), mirrorTags));
            string[] bbcTags = { "BBC Sport" };
            this.Add(new FeedItem(new Uri("http://newsrss.bbc.co.uk/rss/sportonline_uk_edition/football/rss.xml"),bbcTags));
            string[] skyTags = { "Sky Sports" };
            this.Add(new FeedItem(new Uri("http://www.skysports.com/rss/0,20514,11095,00.xml"),skyTags));
        }
    }
}
