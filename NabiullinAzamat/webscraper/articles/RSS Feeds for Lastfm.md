---
title: Last.fm RSS Feeds
description: RSS Feed for your last.fm recent tracks and loved tracks. all you have to do is tell me your username and i'll give you four URLs, one for you recent tracks, one for your loved ones, one for your top tracks and one for your top artists
date: "2016-01-01"
tags: ['RSS, Last.fm, Python, RSS Feed, Recent tracks,Loved tracks']
---
# Last.fm RSS Feeds

So you we're looking for the RSS Feed of Last.fm, and then discovered they were gone!

Well, the solution is right here, all you have to do is tell me your username and i'll give you four URLs,
    one for you recent tracks, one for your loved ones, one for your top tracks and one for your top artists (the last two with an optional period, defaults to 1 month).

also new: images! if last.fm adds something other than a default image, it's large version is added as an enclosure

2025: Added support for recommended tracks. This comes bot in RSS as Soundixx-compatible JSON format.

    
    ## Example URLs (thexiffy)

     https://lfm.xiffy.nl/thexiffy
    

 https://lfm.xiffy.nl/thexiffy/loved
    

 https://lfm.xiffy.nl/thexiffy/toptracks 

    https://lfm.xiffy.nl/thexiffy/toptracks?period=6month
    

 https://lfm.xiffy.nl/thexiffy/topartists 

    https://lfm.xiffy.nl/thexiffy/topartists?period=7day
    

period can be: 7day, 1month, 3month, 6month, 12month or overall

     https://lfm.xiffy.nl/thexiffy/recommended
    

 https://lfm.xiffy.nl/thexiffy/recommended/json