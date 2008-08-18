using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Web;
using System.Net;
using System.Collections.Specialized;
using System.ServiceModel.Syndication;
using System.Xml;
using System.Collections;
using System.Xml.Linq;
using System.Globalization;

namespace NewsPoster
{
    class Program
    {
        static string FILE_LOCATION = System.IO.Directory.GetCurrentDirectory() + "\\processed.txt";
        const int retry = 600000 * 6; //10mins = 600000 milli
        static string target = string.Empty;
        static void Main(string[] args)
        {
            if (args.Length > 0)
            {
                target = args[0] + "/item";
            }
            else
            {
                Console.WriteLine("no target specified. Please restart with the target passed in e.g http://localhost. Press enter to continue.");
                Console.ReadLine();
                return;
            }
            
            
            Process();
            System.Timers.Timer t = new System.Timers.Timer(retry);
            t.Elapsed += new System.Timers.ElapsedEventHandler(t_Elapsed);
            Console.WriteLine("Starting timer");
            t.Start();
            Console.ReadLine();
        }

        static void t_Elapsed(object sender, System.Timers.ElapsedEventArgs e)
        {
            Console.WriteLine("timer fired");
            Process();
        }

        private static void Process()
        {
            Console.WriteLine("Fetching RSS Feeds for " + target + " @" + DateTime.Now.ToString());
            CreateRSS();
            Console.WriteLine("Completed Fetching RSS Feeds @" + DateTime.Now.ToString());
        }

       
        private static void CreateRSS()
        {
            FeedItems feeds = new FeedItems();                      
            foreach (var feed in feeds)
            {
                try
                {
                    XDocument rssFeed = XDocument.Load(feed.FeedUrl.ToString());
                    var posts = from item in rssFeed.Descendants("item")
                                select new RssItem
                                    {
                                        Title = item.Element("title").Value,                                       
                                        PublishDate = ParseDate(item.Element("pubDate").Value),
                                        Url = item.Element("link").Value,
                                        Id = item.Element("guid").Value,
                                        Description = item.Element("description").Value,
                                        SourceFeed = feed.FeedUrl.ToString()
                                    };

                    feed.RssItems.AddRange(posts.ToList());
                }
                catch (Exception e)
                {
                    Console.WriteLine("Feed:{0} failed with error message: {1}", feed.FeedUrl.ToString(), e.Message);
                }
            }
                        
            StreamReader sr = new StreamReader(FILE_LOCATION);
            string sLine = "";
            ArrayList arrText = new ArrayList();

            while (sLine != null)
            {
                sLine = sr.ReadLine();
                if (sLine != null)
                    arrText.Add(sLine);
            }
            sr.Close();

            
            int alreadyAdded = 0;
            int processCount = 0;
            FileStream fs = new FileStream(FILE_LOCATION,FileMode.Append, FileAccess.Write,FileShare.None);
            using(StreamWriter sw = new StreamWriter(fs))
            {
                foreach (var feed in feeds)
                {
                    feed.RssItems.ForEach(delegate(RssItem ri)
                                    {
                                        if (!arrText.Contains(ri.Id))
                                        {
                                            CreatePost(ri, feed.SpecificTags);
                                            sw.WriteLine(ri.Id);
                                        }
                                        else
                                        {
                                            alreadyAdded++;
                                        }
                                        processCount++;
                                    }
                                    );
                }
            }

            Console.WriteLine(processCount.ToString() + " items processed," + alreadyAdded.ToString() + " already processed.");
        }

        private static void CreatePost(RssItem ri, string[] specificTags)
        {
            string[] tags = {"England", "Scotland", "Wales", "N.Ireland", "Rep of Ireland", "Italy", "Spain", "Holland", "Brazil", "Portugal", "Arsenal", "Aston Villa", "Barnsley", "Blackburn", "Blackpool", "Bolton", "Bristol City", "Burnley", "Cardiff","Celtic", "Charlton", "Chelsea", "Colchester", "Coventry", "Crystal Palace","Derby", "Everton","Fulham", "Hull", "Ipswich", "Leicester", "Liverpool", "Manchester City", "Man Utd", "Middlesbrough ", "Newcastle", "Norwich", "Plymouth", "Portsmouth", "Preston", "QPR", "Scunthorpe", "Sheffield Utd", "Sheff Wed", "Southampton", "Stoke", "Sunderland", "Tottenham", "Watford", "West Brom", "West Ham", "Wigan", "Wolverhampton", "Swansea", "Nottm Forest", "Doncaster", "Carlisle", "Leeds", "Southend", "Brighton", "Oldham", "Northampton", "Huddersfield", "Tranmere", "Walsall", "Swindon", "Leyton Orient", "Hartlepool", "Bristol Rovers", "Millwall", "Yeovil", "Cheltenham", "Crewe", "Bournemouth", "Gillingham", "Port Vale", "Luton", "Milton Keynes Dons", "Peterborough", "Hereford", "Stockport","Rangers", "Rochdale", "Darlington", "Wycombe", "Chesterfield", "Rotherham", "Bradford", "Morecambe", "Barnet", "Bury", "Brentford", "Lincoln City", "Grimsby", "Accrington Stanley", "Shrewsbury", "Macclesfield", "Dag & Red", "Notts County", "Chester", "Mansfield", "Wrexham" };
            
            Console.WriteLine("beginning post:" + ri.Title);
            try
            {
                PostSubmitter post = new PostSubmitter();
                post.Url = target;
                post.PostItems.Add("Title", ri.Title);
                post.PostItems.Add("Url", ri.Url);
                post.PostItems.Add("Description", ri.Description);
                post.PostItems.Add("Pub", ri.PublishDate.ToString("R"));

                bool isTagged = false;

                //specific tagging first
                if (specificTags != null && specificTags.Length > 0)
                {
                    foreach (var tag in specificTags)
                    {
                        post.PostItems.Add("Tags", tag);
                        isTagged = true;
                    }
                } 

                //then general tagging
                foreach (var t in tags)
                {
                    //need check to see if the tag has already been used.                   
                    if (post.PostItems["Tags"] == null || !post.PostItems["Tags"].Contains(t))
                    {
                        //check title
                        if(ri.Title.Contains(t))
                        {
                            post.PostItems.Add("Tags", t);
                            isTagged = true;
                        }//then check body
                        else if (ri.Description.Contains(t))
                        {
                            post.PostItems.Add("Tags", t);
                            isTagged = true;
                        }
                    }
                }             

                if (!isTagged)
                {
                    post.PostItems.Add("Tags", "General");
                }

                //add football tag
                post.PostItems.Add("Tags", "Football");
                post.PostItems.Add("Auth", "britman@gmail.com");
                post.Type = PostSubmitter.PostTypeEnum.Post;
                string result = post.Post();
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }

            //Console.WriteLine(result);
        }

        private static DateTime ParseDate(string date)
        {
            DateTime d;
            if (DateTime.TryParse(date, out d))
            {
                return d.ToUniversalTime();
            }
            if (date.Contains("BST"))
            {
                try
                {
                    d = DateTime.ParseExact(date, "dd MMM yyyy HH:mm:ss BST", CultureInfo.InvariantCulture);
                    return d.ToUniversalTime();
                }
                catch (FormatException fe)
                {
                    try
                    {
                        d = DateTime.ParseExact(date, "ddd, dd MMM yyyy HH:mm:ss BST", CultureInfo.InvariantCulture);
                        return d.ToUniversalTime();
                    }
                    catch (FormatException fex)
                    {
                        Console.WriteLine("Item with pubDate of:{0} failed due to date parse error. Error msg: {1}", date, fex.Message);
                    }
                }
            }
            return DateTime.Now.ToUniversalTime().Subtract(new TimeSpan(1,0,0)); 
        }

       
    }

    public class RssItem
    {
        public string Title { get; set; }
        public DateTime PublishDate { get; set; }
        public string Url { get; set; }
        public string Id { get; set; }
        public string Description { get; set; }
        public string SourceFeed { get; set; }
    }

}

