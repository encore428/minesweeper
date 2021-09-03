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
 
 Unfortunately, the app does not run on Vocareum.

## Brief description of the software
Minesweeper is a populate game that was delivered together with the Windows operating system.  
This project recreates the core feature of the game, with a new intelligent feature to help player
play the game.  This feature uses the same info available to the player, and perform analysis and deductions
to help determine location of mines.

## How to use the software
See the steps at top of the readme file on how to start and run the software.  You will see this page:
![index.html page](/index.png)

Select your assistant for the game:
- Single flag: you can plant/clear flag on un-exposed slates to indicate that you think it has a mine.
- Dual flag: you can plant/clear flag on un-exposed slates to indicate that you think it has a mine.
You can also plant/clear question mark on a slate you are analysing.
- Intelligent: the computer will perform the analysis and plant flag (called Confirm flag) on 
slates that certainly have mines.  You can only plant/clear question mark (called Proposed flag) on un-exposed slates.

After you selected your preferred assistant, you can click one of the three game buttons to begin the game.  
Each game (Beginner, Intermediate, Expert) corresponds to a specific canvas size and number of mines to be planted on it.  
On clicking one of the game buttons, a game canvas of the selected size is displayed.

![game.html page](/game.png)

**Left click to expose a slate**

You start the game by left-clicking on any un-exposed slates.  When you left-click the slate, the slate becomes exposed.
- If this slate has a mine, all the mines in the canvas explode, and you lose the game.
- If this slate has no mine, it reveals a number from 0 to 8, which indicates the number of mines hidden in its 
neighboring slates.  This is called **intelligence**.  When intelligence is 0, it is simply left blank instead of 
showing the zero digit.

The goal of the game is to left-click and thus expose all the slates that have no mines.  Regardless of the game 
assistance selected, the player can left-click on any slate.

**Right click to plant a flag**

The player can right-click any un-exposed slate to cycle the flag through all valid flags applicable to the
selected game assistance mode.
<table>
<tr><th>Flag</th><th>Name</th></tr>
<tr><td>
<img src="./cFlag.png">
</td><td>Confirmed</tD></tr>
</table>

Under the Intelligent mode of the game, the computer identifies and flags all the slates that, deduced from the exposed 
intelligence, are certain to have mines.

Under the Intelligent mode of the game, a player plants Proposed flags, which is equivalent to asking the question as to
"what if these slates have mines."  The computer will then identify slates that must have been mined or safe, and 
will plant Implied flags accordingly.  From these flags, the computer further recomputes the implied intellicence, 
checks that against the exposed intelligence, and high-light any intelligence that are violated.  When intelligence are
violated, it means the Proposed flags are incorrect.  If the violation is caused by a single Proposed flag, the player 
can proceed to left-click to open the slate with the Proposed flag.


## Design of the software
**Software specifications**
The core of the application is made up of two Classes:

**Canvas**: Each game is played on a Canvas.  A canvas is a grid of width by height slates.  It also has a number that indicates
how many of those slates have a hidden mine, that if clicked open, will have the player lose the game.

**Slate**: Each instance of a Slate represents a square on the Canvas.  A slate has two statuses: 
- exposed: which is initialised to false on instantiation.  It means the slate is not exposed.  When player left-clicks on a 
slate, it become un-exposed.
- mined: this is initialised to false on instantiation, and then subsequently a specific number of slates and randomly selected
to have this attribute set to true.  If the player left-clicks on a slate where mined is true, the game ends and the player lose.

**How to verify the authenticity of the Intelligent playing mode**




 
 
 
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
<tr><td>/game</td><td>POST</td><td>
   {level: string,<br>
   &nbspassist: string<br>
   }</td>
   <td rowspan=2>
      {player_board:[],<br>
      &nbspwidth: int,<br>
      &nbspheight: int,<br>
      &nbspassist: string,<br>
      &nbspno_of_flags:int,<br>
      &nbspinitial_mines: int,<br>
      &nbspdiscovered_mines: int,<br>
      &nbsphas_won: bool,<br>
      &nbsphas_lost: bool<br>
      }</td><td>game.gen_new_game()</td>
</tr>
<tr><td>/update</td><td>POST</td><td>{cell: int,<br>&nbsptype:string<br>}</td>
   <td>if type == 'flag':<br>
      &nbsp&nbsp&nbsp&nbspgame.toggle_flag(gid, cell)<br>else:<br>&nbsp&nbsp&nbsp&nbspgame.open(gid, cell)
   </td>
</tr>
</table>

**UML diagram**

![uml diagram](/UML.png)

**Pages**

Blueprints of the pages on frontend.  Necessary files are stored in static and templates folders for it to be self-contained.

**Resources**

[Use a Flask Blueprint to Architect Your Applications](https://realpython.com/flask-blueprint/)

[Modular Applications with Blueprints](https://flask.palletsprojects.com/en/2.0.x/blueprints/)

[Flask realworld example app](https://github.com/gothinkster/flask-realworld-example-app)

## Notes

When Developing, always make sure to run on dev mode via environment variable `export FLASK_DEBUG=True`
