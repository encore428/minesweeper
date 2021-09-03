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
Minesweeper is a popular game that was delivered together with the Windows operating system.  

This project recreates the core feature of the game, with an additonal function to automate the analysis 
of the game.  This feature uses the same info available to the player, and performs analysis to:

1 Identify slates that must be mined, and plant confirm flags on them.

1 In response to player's planting of proposed flags, which is equivalent to asking what if this slate is mined, 
analyse and idenfity and plant Implied flags on slates that must be mined or safe.

1 From the resulting flags planted, inspect each exposed slate, and high-light those when the derived number of
neighborhood mines cannot tally with the revealed number.  This is called violated intelligence.

1 When there is violated intelligence, it implies the Proposed flags have been incorrectly planted.  If only
one Proposed flag has planted, that slate can be opened safely.

## How to use the software
See the steps at the top of this readme file on how to start and run the software.
You will see this page:

![index.html page](/index.png)

Select your assistant for the game:
- Single flag: you can plant/clear flag on un-exposed slates to indicate that you think it has a mine.
- Dual flag: you can plant/clear flag on un-exposed slates to indicate that you think it has a mine.
You can also plant/clear question mark on a slate you are analysing.
- Intelligent: the computer will perform the analysis and plant flag (called Confirmed flag) on 
slates that certainly have mines.  You can only plant/clear question mark (called Proposed flag) on un-exposed slates, 
and the computer proceeds to perform further analysis.

After you selected your preferred assistant, you can click one of the three game buttons to begin the game.  
Each game (Beginner, Intermediate, Expert) corresponds to a specific canvas size and number of mines to be planted on it.  
On clicking one of the game buttons, a game canvas of the selected size is displayed.

![game.html page](/game.png)

**Left click to expose a slate**

You start the game by left-clicking on any un-exposed slates.  When you left-click the slate, the slate becomes exposed.
- If this slate has a mine, all the mines in the canvas explode, and you lose the game.
- If this slate has no mine, it reveals a number from 0 to 8, which indicates the number of mines hidden in its 
neighboring slates.  This is called **intelligence** of that slate.  When intelligence is 0, it is simply left blank instead of 
showing the zero digit.

The goal of the game is to left-click and thus expose all the slates that have no mines.  Regardless of the game 
assistance selected, the player can left-click on any slate.

**Right click to plant a flag**

The player can right-click any un-exposed slate to cycle the flag through all valid flags applicable to the
selected game assistance mode.
<table>
<tr><th colspan=3>Flag</th><th colspan=3>Applicable to</th></tr>
   <tr><th>picture</th><th>name</th><th>meaning</th><th>Single Flag</th><th>Dual flag</th><th>Intelligent</th></tr>
   <tr><td><img src="./nFlag.PNG"></td><td>nil</td><td>No flag planted</td><td>yes</td><td>yes</td><td>yes</td></tr>
<tr><td><img src="./cFlag.PNG"></td><td>Confirmed</td><td>slate is believed to be mined</td><td>yes</td><td>yes</td><td>auto</td></tr>
<tr><td><img src="./pFlag.PNG"></td><td>Proposed</td><td>player is asking what if this is mined</td><td></td><td>yes</td><td>yes</td></tr>
<tr><td><img src="./mFlag.PNG"></td><td>Implied mined</td><td>base on planted Confirmed and Proposed flags, this slate must be mined</td><td></td><td></td><td>auto</td></tr>
<tr><td><img src="./sFlag.PNG"></td><td>Implied safe</td><td>base on planted Confirmed and Proposed flags, this slate must be safe</td><td></td><td></td><td>auto</td></tr>
</table>

**Intelligent assistant**

With intelligent assistant, the computer identifies and flags all the slates that, deduced from the exposed intelligence, are certain to have mines.

A player thus plants only Proposed flags, which is equivalent to asking the question as to "what if these slates have mines."  The computer will then identify 
slates that must have been mined or safe, and will plant Implied flags accordingly.  From these flags, the computer further recomputes the implied intellicence, 
checks that against the exposed intelligence, and high-light any intelligence that are violated.  When intelligence are violated, it means the Proposed flags
are incorrect.  If the violation is caused by a single Proposed flag, the player  can proceed to left-click to open the slate with the Proposed flag.

Example of a violated intelligence and it's high-lighting:

![Violated intelligence](/VI.PNG)


## Design of the software
**Software specifications**

The core of the application is made up of two Classes:

**Canvas**: Each game is played on a Canvas.  A canvas is a grid of width by height slates.  It also has a number that indicates
how many of those slates have a hidden mine, that if clicked open, will have the player lose the game.

**Slate**: Each instance of a Slate represents a square on the Canvas.  A slate has two statuses: 
- **exposed**: which is initialised to false on instantiation.  It means the slate is not exposed.  When player left-clicks on a 
slate, it become un-exposed.
- **mined**: this is initialised to false on instantiation, and then subsequently a specific number of slates are randomly selected
to have this attribute set to true.  If the player left-clicks on a slate where mined is true, the game ends and the player lose.
- **intel**: as mines are planted on selected slates, the mined slate informs its neighbor that it has a bomb.  Each slate 
keeps track of the number of times it is informed, and this is the intel of the slate.  This number is fixed once the mines 
planting is completed.

**How to verify the authenticity of the Intelligent playing mode**

When the game is played, intelligent mode helps to identify mines, and automactically flags and opens correct slates.  
How can one be sure that this is indeed the result of correct algorithm and analysis, and not intentional or accidental
cheating?

To ascertain that the program logic that automates the playing of the game relies only on the same info as a player does,
the `__private` attribute technique is used for the most important attributes of the Slate class:
```python
class Slate:
    def __init__(self, idx, tools):
        self.__mined = False    # True if slate has a mine
        self.__exposed = False  # True if slate has been uncovered
        self.__intel = 0  # number of mines in the neighborhood
```
 To find out the intelligence of, or determine if a slate is minded, one must go through the property methods:
```python
    @property
    def mined(self):
        if self.exposed:
            return self.__mined

    @property
    def intel(self):
        if self.exposed:
            return self.__intel
```
Here, the value is returned only if the slate is exposed.  As such, no one from outside of Slate class can obtained the 
value without first opening the slate.  To open a slate, one can only do it via the Slate method crack():
```python
    ## For unexposed slates, player can tap to crack it open.  Each cracking tap is handled by this method
    ## the method returns true if a mine has gone off
    def crack(self):
        ...	
        self.__exposed = True
        # if this Slate has a mine, it explodes and game is over
        if self.mined:
            return True
        ...	
```
This is the only place `__exposed` is set to True, and it causes the game to be lost if the slate exposed is mined.

Finally, by inspecting the proper access to `__mined` and `__intel` within the Slate class, one can be assured that 
any analysis are based on valid known facts form the Canvas.

Another mechanism that prevents the location of mined slates from being known to outside of Slate class is that, 
when a request is made from Canvas to plant a mine on a designated slate, the Slate method will perform random 
walks in the neighborhood network to arrive at another slate to actually plant the mine.
```python
    def plant_mine(self, cap):
        sub_neighbor_steps = random.randint(0,int(math.sqrt(cap))) + 3
        curSlate = self
        for i in range(sub_neighbor_steps):
            curSlate = curSlate.neighborhood[random.randint(0,len(curSlate.neighborhood)-1)]
        while curSlate.__mined:
            curSlate = curSlate.neighborhood[random.randint(0,len(curSlate.neighborhood)-1)]
        curSlate.__mined = True
        for each_slate in curSlate.neighborhood:
            each_slate.intelInc()
```
 
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
