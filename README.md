## To execute (on Windows)

Open an Anaconda Prompt session, perform the following:

```
git clone https://github.com/encore428/minesweeper
cd minesweeper
python -m venv virtenv
virtenv\Scripts\activate
flask run
```

The following will be displayed on screen:
```
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 ```
 
 Access the game at this [URL](http://127.0.0.1:5000/)
 
 After testing, Press CTRL+C on Anaconda Prompt to terminate the server, exit to terminate the prompt.
 
**Api**

Blueprints of the api of the game:

- init game: to start a new game.
- update game: as initiated by player tapping on a slate, the action and location of the slate is sent to back-end, back-end performs processing, and return a copy of updated canvas which is then rendered on the browser.


**Software architecture**

![software architecture](/software-architecture.jpg)

**External game API**

<table>
<tr><th>API</th><th>METHODS</th><th>Req.body</th><th>Res.body</th><th>Direct class and methods</th>
</tr>
<tr><td>/game</td><td>POST</td><td>{level: string,<br> assist:string}</td><td rowspan=2>{grid:[],<br> width: int,<br> height: int,<br> assist: int,<br> noOfFlags:int,<br> NoOfMines: int,<br> discovered_mines: int,<br> hasWon: bool,<br> hasLost: bool}</td><td>Canvas.initGame()</td>
</tr>
<tr><td>/update</td><td>POST</td><td>{x: int,<br> y:int,<br> action:string}</td><td>Canvas.update()</td>
</tr>
</table>

![external api](/external-api-design.jpg)

**UML diagram**

![uml diagram](/uml.jpg)

**Pages**

Blueprints of the pages on frontend. We will store the static and templates here for it to be self-contained as a front-end only folder.

**Resources**

[Use a Flask Blueprint to Architect Your Applications](https://realpython.com/flask-blueprint/)

[Modular Applications with Blueprints](https://flask.palletsprojects.com/en/2.0.x/blueprints/)

[Flask realworld example app](https://github.com/gothinkster/flask-realworld-example-app)

## Notes

When Developing, always make sure to run on dev mode via environment variable `export FLASK_DEBUG=True`
