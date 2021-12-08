# DESIGN: BENJY AND WILL LISTEN TO YOUR MUSIC by Benjy Wall-Feng and Will Hahn
## CS50 final project // 7 December 2021

### Introduction
Our goal with this project was to provide a concise, entertaining mini-analysis of a user's Spotify data. Importantly, by using the Spotify API we were able to access data (specifically user_top_tracks) that users cannot normally see, so the content provided here is novel.

In broad terms, our project reads the user's top tracks and generates a series of comments "written by Benjy and Will" that praise or criticize the user's music.

### Python, part 1
Our project makes use of a module which builds into Spotify’s API: Spotipy. There are a few moving parts to properly implementing Spotipy, which we will outline and go into greater detail about: authorization and retrieving data. Firstly, there is authorization, which entails providing the client_id and secret for a Spotify Developer App. Once those variables have been set, and a specific Spotify user has been added to the Developer Dashboard, as outlined in our README.md, the user can then be prompted to log in through the util.prompt_for_user_token function. This redirects, if the user is not already logged in or does not have the .cache file set, the user to log into Spotify in their browser. Once done so, the .cache file will be set. This contains a temporary access key which is what further allows Spotify’s information to be accessed without repeatedly prompting a log-in. Once there, the user’s token is set and sp.current_user_top_tracks retrieves their top tracks.

This information is then processed into a json file, from which it is processed and parsed into various arrays within the program. These arrays, when combined with information retrieved from test.db via SQl commands through a combination of splicing and appending, become the comments which are then passed into Flask to be displayed on the website.

### SQL
The various possible comments are stored in the SQL database "test.db". This file is not modified by running app.py. We first created a collaborative Google Sheets document in order to write comments more easily, then downloaded each sheet as a .csv file and read those files into test.db using sqlite3 .import; while this could have been accomplished similarly using Python arrays, we felt that SQL provided a cleaner workflow.

### Python, part 2
We will take a moment to explain the particular way in which "comments" are generated. We used three tables: artcoms, popcoms, and rancoms, for artist, popularity, and random comments respectively.

Artcoms has prewritten comments for several hundred of Spotify's most popular artists; if any of these are among a user's top artists, the associated comments will be passed. 

Tracks have "popularity" data (an int between 1 and 100) associated with them. Popcoms takes the mean of these popularities and associates each range of mean popularities with a prewritten comment. For example, if a user's top tracks' mean popularity is 63, the comments from "Benjy" and "Will" associated with 55-65 range (perhaps something like "Your taste in music is pretty underground") will be passed.

Lastly, a number of random comments are passed. Some of these are generic comments that could apply to anyone ("I like your music"). Others contain the placeholder ARTISTNAME, for which Python substitute's one of the user's actual artist names before passing. For example, a random comment might be "My mom loves ARTISTNAME"; a user who listens to Billie Eilish might see "My mom loves Billie Eilish".

### Flask
The website part of the implementation is fairly straightforward. We used Flask to manage the different parts, and ultimately there are just two pages to render, index.html and results.html. When the user has successfully connected their Spotify account and the Python script has generated "comments" as detailed above, Flask passes those comments (as *vals*) into results.html, which uses Jinja syntax to render them as a list.

### HTML/CSS
Aesthetically, our intent was to combine a basic but nice-looking website design with some more dynamic elements. This is the reason for the image of the two of us that bounces around the homepage (using the <marquee> tag, which is deprecated but still a lot of fun for our purposes) and the admittedly dopey-looking avatars of our faces that precede the comments on the results pages (achieved with the CSS :before selector). The rest of the CSS is fairly straightforward, with the notable inclusion of the @media rule to make some elements more mobile-friendly.

### JavaScript
JavaScript is used on the homepage to disable the main button after it is clicked, and to change its inner text to a loading message so that the user knows the program is working. A more complicated use of JavaScript is on the results page. We wanted a way to pass a comment (e.g., "Benjy: I love Adele" if "Adele" is in the user's top artists) from Python to HTML given that 1) the object passed should not be any more complex than a string and 2) the HTML should format the comment nicely. In this case we introduced some language markers of our own. In Python, the comment is created as "@#Benjy: #@ I love !@Adele@!", which is a string. The JavaScript on the results page iterates through these comments and replaces @# #@ with <span class="benjy"> </span> and !@ @! with <span class="highlight"> </span>. This results in "Benjy: " being bolded and preceded by an image of Benjy's face, and "Adele" being bolded and pink.
