# README: BENJY AND WILL LISTEN TO YOUR MUSIC by Benjy Wall-Feng and Will Hahn
## CS50 final project // 7 December 2021

### Introduction
Our project, "Benjy and Will Listen to Your Music" (stylized in all lowercase), is a web-based application utilizing the Spotify API. (Spotify is a popular music streaming service.) The user is prompted to connect their Spotify account to the website and upon doing so sees a list of comments from "Benjy and Will" analyzing their music taste. The project uses Python, Flask, HTML, CSS, SQL, and JavaScript.

Note that to use this program as intended, the user must have a Spotify account.

### Video
The presentation video for our project is hosted at https://bit.ly/bawltymvideo.

### Installing the project
The project files are hosted in a repository on GitHub at the following link: https://bit.ly/bawltym-code. The most recent version of the project can be downloaded by clicking **Code** -> **Download ZIP**.

We used the desktop edition of Visual Studio Code and recommend that staff do as well. To open the project in VS Code, navigate in the "Explorer" tab to the location on the user's computer of the unzipped file. The user should have a Python interpreter as well as the "numpy", "spotipy", and "flask" libraries installed. To install these libraries, run

**pip3 install numpy**
**pip3 install spotipy**
**pip3 install flask**

in the command line. (The other libraries used, namely "sqlite", "random", "os", and "json", should come pre-installed in Python, but may be installed via the command line using a similar method if they are not.)

### Authorizing user in Spotify
Spotify's developer tools come with some restrictions. In particular, the Spotify account used to login for the app must be *authorized* in the app's Developer Dashboard in able to access some of the data pulled. This restriction is in place because the app is in "developer mode" (i.e., not public), so the user will have to be authorized manually.

To do this, visit https://developer.spotify.com/dashboard/ and click "Log In". Input the following credentials:

*username*: bawltymcs50@gmail.com
*password*: devdevdev

Click on the app called "Benjy and Will Listen to Your Music". Click on "Users and Access", then "Add New User", then input the name and email address associated with the user's Spotify account. (The name field can be anything.) The user should now be authorized, although it may take several minutes to update. If the user is not correctly authorized (or it has not yet updated), running the code as described below may prompt an error.

### Running the project
Run the Python file "app.py". With our Python interpreter, this requires executing "python3 app.py" or "python app.py" in the command line, but implementations may vary depending on the user's setup of VS Code. Upon successful execution a website will open. If the user has previously used the server to log in, the website that opens will be the server homepage (called "Benjy and Will Listen to Your Music"). Otherwise, the website that opens will be a Spotify page prompting the user to log in. In this case, log in using the email that was authorized in the previous step, and click "Agree" when prompted to allow the app to access user data. The website will then redirect to the server homepage.

### Using the project
The user may read the content of the main webpage. The hyperlinks are interesting but ancillary to the focus of the project. To proceed, the user should click the rectangular pink button that says "I badly want this." After between 15 and 30 seconds, the website will redirect to a new page that reads "Here's what we thought," followed by a list of comments. This concludes the primary function of the website. Repeating this process will yield a different list of comments, since they are randomly pulled from a predetermined database.
