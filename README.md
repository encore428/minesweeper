**This app has been deployed to AWS at the folowing URL**
http://18.220.32.206:5000/

I referred to this for creating EC2 instances and using Cloud9 in AWS: https://hackmd.io/@Crimsonlycans/rkhvAZHZY.
I referred to this for tips on AWS deployment https://www.twilio.com/blog/deploy-flask-python-app-aws.
These are the commands used to deploy:
```ssh
sudo apt update
sudo apt install python3 python3-pip tmux htop
git clone https://github.com/encore428/minesweeper
cd minesweeper
tmux new -s minesweeper
cd minesweeper
pip3 install -r requirements.txt
sudo apt install python3-flask
flask run --host=0.0.0.0 --port=5000
```


The following will be displayed on screen:
```
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 ```

## To execute (on Windows)

Open an Anaconda Prompt session, perform the following:

```
git clone https://github.com/encore428/minesweeper
cd minesweeper
python -m venv virtenv
virtenv\Scripts\activate
pip install -U --force-reinstall -r requirements.txt
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

This project recreates the core feature of the game.  My contribution is the function to automate the analysis 
of the game.  This feature uses the same info available to the player, and performs analysis to:

1. Identify slates that must be mined, and plant **Confirmed flags** on them.

1. In response to player's planting of **Proposed flags**, which is equivalent to asking what if this slate is mined, 
analyse and idenfity and plant **Implied flags** on slates that must be **Mined** or **Safe**.

1. From the resulting flags planted, inspect each exposed slate, and high-light those where the derived number of
neighborhood mines cannot tally with the revealed number.  This is called **Violated Intelligence**.

1. When there is **Violated Intelligence**, it implies the **Proposed flags** have been incorrectly planted.  If only
one **Proposed flag** is involved, that slate can be opened safely.

## How to use the software
See the steps at the top of this readme file on how to start and run the software.
You will see this page:

![index.html page](/index.png)

Select your assistant for the game:
- **Single flag**: Player plants/clears flag on un-exposed slates to indicate that it has a mine.
- **Dual flag**: Player plants/clears flag on un-exposed slates to indicate that it has a mine.
Player can also plant/clear **Proposed flag** on a slate being analysed.
- **Intelligent**: The computer performs the analysis and plant **Confirmed flag** on slates that certainly 
have mines.  Player only plants/clears **Proposed flag** on un-exposed slates, and the computer proceeds 
to perform further analysis.

After you selected your preferred assistant, you can click one of the three game buttons to begin the game.  Each game (Beginner, Intermediate, 
Expert) corresponds to a specific canvas size and number of mines to be planted on it.  On clicking one of the game buttons, a game canvas of 
the selected size is displayed.

![game.html page](/game.png)

**Left click to expose a slate**

Player starts the game by left-clicking on any un-exposed slates.  When player left-clicks the slate, the slate becomes exposed.
- If this slate has a mine, all the mines in the canvas explode, and player loses the game.
- If this slate has no mine, it reveals a number from 0 to 8, which indicates the number of mines hidden in its 
neighboring slates.  This is called **intelligence** of that slate.  When **intelligence** is 0, it is simply 
left blank instead of showing the zero digit.

The goal of the game is to left-click and thus expose all the slates that have no mines.  Regardless of the game 
assistant selected, the player can left-click on any slate.

**Right click to plant a flag**

The player can right-click any un-exposed slate to cycle the flag through all valid flags applicable to the
selected game assistant mode.
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

With intelligent assistant, the computer identifies and plants **Confirmed flags** on all Slates that, deduced from the exposed 
intelligence, are certain to have mines.

The player plants only **Proposed flags**, which is equivalent to asking the question "what if these 
slates have mines."  The computer will then identify slates that must have been mined or safe, and will plant 
**Implied flags** accordingly.  From these flags, the computer further recomputes the implied **intelligence**, 
checks that against the exposed **intelligence**, and high-light any **intelligence** that are violated.  
When intelligence are violated, it means the **Proposed flags** are incorrect.  If the violation is caused by a 
single **Proposed flag**, the player can proceed to left-click to open the slate with the **Proposed flag**.

Example of a **Violated Intelligence** and it's high-lighting:

![Violated intelligence](/VI.PNG)


## Design of the software
**Software specifications**

The core of the application is made up of two Classes:

**Canvas**: Each game is played on a Canvas.  A canvas is a grid of width by height slates.  It also has a number that indicates
how many of those slates have hidden mines, that if clicked open, will have the player lose the game.

**Slate**: Each instance of a Slate represents a square on the Canvas.  A slate has these critical attributeswo statuses: 
- **exposed**: which is initialised to false on instantiation.  It means the slate is not exposed.  When player left-clicks
on a slate, it become un-exposed.
- **mined**: this is initialised to false on instantiation, and then subsequently a specific number of slates are randomly 
selected to have this attribute set to true.  If the player left-clicks on a slate where mined is true, the game ends and 
the player loses.
- **intel**: as mines are planted on selected slates, the mined slate informs its neighbor that it has a bomb.  Each slate 
keeps track of the number of times it is informed, and this is the intel of the slate.  This number is fixed once the mines 
planting is completed.
- **neighborhood**: this is a list of other slates that forms the neighborhood of the slate.  All analisys are based on
neighborhood.  No index are involved, and a slate does not need to know its position on the Canvas to perform such analysis.

Object Orientated paradigm is adopted by having attributes and methods implemented to where each belong, and the two classes
are carefully isolated.

**How to verify the authenticity of the Intelligent playing mode**

When the game is played, intelligent mode helps to identify mines, and automactically flags and opens appropriate slates.  
How can one be sure that this is indeed the result of correct algorithm and analysis, and not intentional or accidental
cheating?

**Hiding of critical Slate attributes**

To ascertain that the program logic that automates the playing of the game relies only on the same info as a player does,
the `__private` attribute technique is used for the the critical attributes of the Slate class:
```python
class Slate:
    def __init__(self, idx, tools):
        self.__mined = False    # True if slate has a mine
        self.__exposed = False  # True if slate has been uncovered
        self.__intel = 0  # number of mines in the neighborhood
        self.__neighborhood = []  # points to neighborhood Slates

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

    def addNeighbor(self, another_slate):
        self.__neighborhood.append(another_slate)

    @property
    def neighborhood(self):
        return self.__neighborhood
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

**Hiding of Slate and Mine Positions**

Slates do not know it's exact positon on the Canvas.  To perform analysis, each relies on the intel from its neighborhood.

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
Note that the neighbor notified of addition of mines in its neighborhood, does not know which of its neighbors actually 
is informing it.

## Use of Graph Based algorithms

**Recursion to implement propagation**

When a Slate is cracked open, and if it has no mine, it reveals its intel.  The pogram analyse the intel, and may 
proceed to crack open some of its neighborhood Slates.  This process can propagate. 

```python
    ## For unexposed slates, player can tap to crack it open.  Each cracking tap is handled by this method
    ## the method returns true if a mine has gone off
    def crack(self):
	    ...
        # now expose this Slate
        self.__exposed = True
        # if this Slate has a mine, it explodes and game is over
        if self.mined:
            return True
        pass
        # now that this Slate is exposed, if its intel is = 0, all its neigborhood slates can be cracked open
        if self.intel == 0:
            for neighbor in self.neighborhood:
                if not neighbor.exposed:
                    print(f"    Crack slate[{neighbor.__idx}] because slate[{self.__idx}]intel=0")
                    neighbor.crack()
        # That's all for opening the Slate
        if self.tools != 2:
            return False
        pass
        ### The following is for games in Auto mode
        # Check if neighborhood unexposed Slates count matches Intel, and
        # flag all exposed slate with Confirm flag
        self.seek2Confirm()
        # For each Slate in the neighborhood
        # Check if its neighborhood unexposed Slates count matches Intel, and
        # flag all exposed slate with Confirm flag
        for neighbor in self.neighborhood:
            neighbor.seek2Confirm()
        # Check if neighborhood Confirmed flag count matches Intel,
        # and crack open all unflagged slates
        if (self.intel > 0) and (self.intel == self.flagCIntel):
            for neighbor in self.neighborhood:
                if (not neighbor.exposed) and (flag_symbols[neighbor.flag][1] != 'confirmed'):
                    print(f"    Crack neighbor slate[{neighbor.__idx}] because slate[{self.__idx}] flag count = Intel")
                    neighbor.crack()
        # Repeat for each neighborhood Slate
        for neighbor in self.neighborhood:
            if (neighbor.exposed) and (neighbor.intel > 0) and (neighbor.intel == neighbor.flagCIntel):
                for sub_neighbor in neighbor.neighborhood:
                    if (not sub_neighbor.exposed) and (flag_symbols[sub_neighbor.flag][1] != 'confirmed'):
                        print(f"    Crack sub-neighborSlate[{sub_neighbor.__idx}] of slate[{neighbor.__idx}] with flag count = intel")
                        sub_neighbor.crack()
        return False
```

**BFS to implement What-if Analysis**

When the player plants a Proposed flag, the program will analyse the Slates, and when sufficient assumption is made, it
will proceed to plant Implied flags.  Such flags will require further analysis.  So these flags are added to a queue
as and when they are planted, so that they can be analysed subsequenly.  As the program analyses all the neighbors of
a Slate before proceeding to take out another Slate from the queue, this is a BFS search.

```python
    def reAnalysis(self, triggerSlate):
        workQueue = self.__queueProposed.copy()
        if triggerSlate != None and triggerSlate.flag == 1:
            workQueue.insert(0,triggerSlate)
        ## perform the analysis for each slate in queue
        workQueue = self.__queueProposed.copy()
        while len(workQueue) > 0:
            thisSlate = workQueue.pop(0)
            print(f"         analysing exposed neighborhood of slate[{thisSlate.idx}] for implied mines")
            ## From this queue which starts with slates with proposed flags, derive implied flags.
            ## As Implied flags are planted, each slate with new flag is added to the queue for similar analysis.
            ## This goes on until the queue is cleared.
            for neighbor in thisSlate.neighborhood:
                # print(f"        analysis of mines for neignbor slate[{neighbor.idx}]")
                # check Intel of its exposed neighbors, if it's intel matches un-exposed slates in its neighborhood,
                # plant implied mine flags.
                if neighbor.exposed and (neighbor.intel == neighbor.unexposedIntel - neighbor.flagSIntel):
                    print(f"             analysing un-exposed sub_neighborhood of neighborSlate[{neighbor.idx}]")
                    for sub_neighbor in neighbor.neighborhood:
                        # print(f"            analysis of sub-neignbor slate[{sub_neighbor.idx}]")
                        if not sub_neighbor.exposed and (sub_neighbor.flag == 0):
                            print(f"                 sub_neighborSlate[{sub_neighbor.idx}] has implid mine")
                            sub_neighbor.flagImpliedMine()
                            workQueue.append(sub_neighbor)
            print(f"         analysing exposed neighborhood of slate[{thisSlate.idx}] for implied safe slates")
            for neighbor in thisSlate.neighborhood:
                # print(f"        analysis of safe for neignbor slate[{neighbor.idx}] having {neighbor.exposed} {neighbor.intel} {neighbor.flagCIntel+neighbor.flagPIntel+neighbor.flagMIntel}")
                # check Intel of my exposed neighbors, if its intel matches flag count,
                # plant implied safe flags to the remaining unexposed neighbors.
                if neighbor.exposed and (
                        neighbor.intel == neighbor.flagCIntel + neighbor.flagPIntel + neighbor.flagMIntel):
                    print(f"             analysing un-exposed sub_neighborhood of neighborSlate[{neighbor.idx}]")
                    for sub_neighbor in neighbor.neighborhood:
                        # print(f"            analysis of sub-neignbor slate[{sub_neighbor.idx}]")
                        if (not sub_neighbor.exposed) and (sub_neighbor.flag == 0):
                            print(f"                 sub_neighborSlate[{sub_neighbor.idx}] implid safe")
                            sub_neighbor.flagImpliedSafe()
                            workQueue.append(sub_neighbor)
```

## Documentation

Program code uses intuitive class, attribute/property, and method names.

There are in-program comments to explain key segments of program logic.

The idx attribute for each Slate is for printing tracing statements for debugging purpose only.  The index is not used otherwise.

The tracing print statements clearly denote what the analyis it is performing.  Those output can be used to animate the progress of the 
analysis, flag planting, and slate opening process if interface to front-end.

## Further enhancement

Program can be further enhanced to perform iterative what-if analysis to safely open more slates.

Beyond logical analysis that returns results with certainty, the program can also be enhanced to, when there is no clue to flag or open further slates,
compute the possibilty of having mine for each un-exposed slate, and to pick the one with the lowest probability to open.

Eventually, the human player can be eliminated.


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

Note that the is a `idx` attribute for Slate class.  This attribute uniquely identifies the slate instance.  It does not
participate in the core logic of the Slate class methods.  It is here only for printing tracing messages for 
debugging purpose.


**Pages**

Blueprints of the pages on frontend.  Necessary files are stored in static and templates folders for it to be self-contained.

**Resources**

[Use a Flask Blueprint to Architect Your Applications](https://realpython.com/flask-blueprint/)

[Modular Applications with Blueprints](https://flask.palletsprojects.com/en/2.0.x/blueprints/)

[Flask realworld example app](https://github.com/gothinkster/flask-realworld-example-app)

## Notes

When Developing, always make sure to run on dev mode via environment variable `export FLASK_DEBUG=True`
