# README: BENJY AND WILL LISTEN TO YOUR MUSIC by Benjy Wall-Feng and Will Hahn
## CS50 final project // 7 December 2021

### Introduction
Our project, "Benjy and Will Listen to Your Music" (stylized in all lowercase), is a web-based application utilizing the Spotify API. (Spotify is a popular music streaming service.) The user is prompted to connect their Spotify account to the website and upon doing so sees a list of comments from "Benjy and Will" analyzing their music taste. The project uses Python, Flask, HTML, CSS, SQL, and JavaScript.

### Video
The presentation video for our project is hosted at https://bit.ly/bawltym-video.

### Installing the project
The project files are hosted in a repository on GitHub at the following link: https://bit.ly/bawltym-code. The most recent version of the project can be downloaded by clicking **Code** -> **Download ZIP**.

We used the desktop edition of Visual Studio Code and recommend that staff do as well. To open the project in VS Code, navigate in the "Explorer" tab to the location on the user's computer of the unzipped file. The user should have a Python interpreter as well as the "numpy", "spotipy", and "flask" libraries installed. To install these libraries, run

**pip3 install numpy**
**pip3 install spotipy**
**pip3 install flask**

in the command line. (The other libraries used, namely "sqlite", "random", "os", and "json", should come pre-installed in Python, but may be installed via the command line using a similar method if they are not.)

### Running the project
Run the Python file "app.py". With our Python interpreter, this requires executing "python3 app.py" or "python app.py" in the command line, but implementations may vary depending on the user's setup of VS Code. The terminal should ouput something like:

> Serving Flask app 'app' (lazy loading)
> Environment: production
> WARNING: This is a development server. Do not use it in a production deployment.
> Use a production WSGI server instead.
> Debug mode: on
> Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
> Restarting with stat
> Debugger is active!
> Debugger PIN: XXX-XXX-XXX

and  server should be a website titled "Benjy and Will Listen to Your Music".

### Using the project
The user may read the content of the main webpage. The hyperlinks are interesting but ancillary to the focus of the project. To proceed, the user should click the rectangular pink button that says "I badly want this." They will be prompted to log in with their Spotify username and password. Click the "Agree" button to allow the app to access the user's top artists. Then the user will be redirected back to the main webpage, and after between 15 and 30 seconds, to a new page that reads "Here's what we thought," followed by a list of comments. This concludes the primary function of the website. Repeating this process will yield a different list of comments, since they are randomly pulled from a predetermined database.