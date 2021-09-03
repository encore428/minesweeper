from datetime import datetime
import random
from .Slate import Slate



def cycle_slate_idx(cap, start, step=1):
    # warps the index as it moves up and down the slates array
    result = start + step
    if result >= cap:
        result = result - cap
    elif result < 0:
        result = result + cap
    return result



class Canvas:
    def __init__(self, width, height, mines, tools, seed=None):
        self.__width = width
        self.__height = height
        self.__mines = mines
        self.__tools = tools          # 0=Confirm flag only, 1=has Proposed flag, 2=only Proposed flag
        ######## tools  is a Canvas attribute. But is's value affects the behaviour of some of the 
        ######## Slate methods.  It is therefore replicated to Slate class and present i nall Slate instances.
        self.__start = None       # game start date time stamp
        self.__slates = []
        self.__queueProposed = [] # to keep track of Proposed flags for Intelligent game mode.

        self.__hasWon = False # game is won when all safe slates are opened
        self.__hasLost = False # game is lost when a mine is opened

        cap = self.__width * self.__height
        # instantiate required Slates for the canvas and place into array
        for i in range(cap):
            self.__slates.append(Slate(i, self.__tools))
        # set up neighborhood for each Slate
        for i in range(cap):
            my_row = i // self.__width
            my_col = i % self.__width
            # add top neighbors
            if my_row > 0:
                if my_col > 0:
                    self.__slates[i].addNeighbor(self.__slates[i-self.__width-1]) # top left neighbor
                self.__slates[i].addNeighbor(self.__slates[i-self.__width])       # top neighbor
                if my_col < self.__width -1:
                    self.__slates[i].addNeighbor(self.__slates[i-self.__width+1]) # top right neighbor
            # add side neighbors
            if my_col > 0:
                self.__slates[i].addNeighbor(self.__slates[i-1]) # left neighbor
            if my_col < self.__width -1:
                self.__slates[i].addNeighbor(self.__slates[i+1]) # right neighbor
            # add bot neighbors
            if my_row < self.__height - 1:
                if my_col > 0:
                    self.__slates[i].addNeighbor(self.__slates[i+self.__width-1]) # bot left neighbor
                self.__slates[i].addNeighbor(self.__slates[i+self.__width])       # bot neighbor
                if my_col < self.__width -1:
                    self.__slates[i].addNeighbor(self.__slates[i+self.__width+1]) # bot right neighbor
        # plant secret mines on random Slates
        random.seed(seed)   # seed can be specified when instantiating, or passed in as None
        dig_into = 0
        for i in range(self.__mines):  # to plant mine {mines} times.
            dig_into = cycle_slate_idx(cap, dig_into, random.randint(1,cap))
            self.__slates[dig_into].plant_mine(cap)



    @property
    def slates(self):
        return self.__slates

    @property
    def tools(self):
        return self.__tools

    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width

    @property
    def mines(self):
        return self.__mines

    @property
    # number of exposed slates
    def discovery(self):
        return sum(map(lambda slate: slate.exposed, self.__slates))

    @property
    # number of confirmed flags on canvas
    def cFlagCount(self):
        return sum(map(lambda slate: slate.flag == 1, self.__slates))

    @property
    # number of confirmed flags on canvas
    def pFlagCount(self):
        return sum(map(lambda slate: slate.flag == 2, self.__slates))

    @property
    # number of confirmed flags on canvas
    def mFlagCount(self):
        return sum(map(lambda slate: slate.flag == 3, self.__slates))

    @property
    # number of confirmed flags on canvas
    def sFlagCount(self):
        return sum(map(lambda slate: slate.flag == 4, self.__slates))

    @property
    def hasWon(self):
        return self.__hasWon

    @property
    def hasLost(self):
        return self.__hasLost

    @property
    def queueProposed(self):
        return self.__queueProposed

    @property
    def showGrid(self):
        retu_grid = [[' ' for row in range(self.width)] for column in range(self.height)]
        for slate in self.slates:
            retu_grid[slate.idx // self.width][slate.idx % self.width] = slate.slateSymbol[0]

        return {
            "grid": retu_grid,
            "width": self.width,
            "height": self.height,
            "noOfFlags": self.discovery,
            "noOfMines": self.mines,
            "hasWon": self.hasWon,
            "hasLost": self.hasLost
        }

    def clearImpliedFlags(self):
        for slate in self.slates:
            if (slate.flag == 3) or (slate.flag == 4):
                slate.flagClear()


    def playCrack(self, idx):
        print(f"Crack slate[{idx}] user initiated")
        if self.hasWon or self.hasLost:
            print(f"Game was {'won' if self.hasWon else 'lost'}, please start a new game")
            return self.showGrid

        self.clearImpliedFlags()
        if self.slates[idx].crack():
            # when this returns true, a mine has exploded
            print(f"game is lost, slate[{idx}] is has bomb")
            for slate in self.slates:
                slate.lit()
            self.__hasLost = True
        else:
            if self.tools == 2:
                self.reAnalysis(self.slates[idx])

            ## I want these to be updated inside Slate class, what is the best approach to doing that?
            if (self.discovery + self.mines == self.width * self.height):
                if self.cFlagCount == self.mines:
                    print(f"game is finished, all mines flagged and all safe slates creaked open")
                else:
                    print(f"game is finished, all safe slates creaked open, proceeding to plant confirm flag on all un-exposed slates.")
                    for slate in self.slates:
                        if not slate.exposed and slate.flag != 1:
                            slate.flag = 1
                self.__hasWon = True
            else:
                if (self.tools == 2) and (self.cFlagCount == self.mines):
                    for slate in self.slates:
                        if not slate.exposed and slate.flag != 1:
                            print(f"    Crack slate[{idx}] victory run")
                            slate.crack()
                    print(f"game is finished, all mines flagged")
                    self.__hasWon = True

        return self.showGrid


    def playFlag(self, idx):
        print(f"User cycles flag for slate[{idx}]")
        if self.hasWon or self.hasLost:
            print(f"Game was {'won' if self.hasWon else 'lost'}, please start a new game")
            return self.showGrid
        self.clearImpliedFlags()
        flagWas = self.slates[idx].flag
        if (self.slates[idx].cycleFlag()):
            ## the above returns Ture if there has been changes
            ## if so, check if game is played under auto-mode
            if self.tools == 2:
                ## if a proposd flag has been planted/cleared, add/remove it from the queue
                if self.slates[idx].flag == 2:
                    self.__queueProposed.append(self.slates[idx])
                if flagWas == 2:
                    self.__queueProposed.remove(self.slates[idx])
                self.reAnalysis(self.slates[idx])
        return self.showGrid


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
        for slate in self.slates:
            if slate.exposed:
                if slate.intel == slate.flagCIntel:
                    for neighbor in slate.neighborhood:
                        if not neighbor.exposed and neighbor.flag != 1:
                            print(f"    Crack slate[{neighbor.idx}] because slate[{slate.idx}] has cFlatCount=intel")
                            neighbor.crack()
        for slate in self.slates:
            if slate.exposed:
                if slate.intel == slate.unexposedIntel:
                    for neighbor in slate.neighborhood:
                        if not neighbor.exposed and neighbor.flag != 1:
                            print(f"    Plant confirm flag on slate[{neighbor.idx}] because slate[{slate.idx}] has unexposed=intel")
                            neighbor.flagConfirm()
                            workQueue.append(neighbor)

        ## if all mines have been flagged, it implies all the other unexposed slates are safe
        if self.mines == self.cFlagCount + self.pFlagCount + self.mFlagCount:
            for slate in self.slates:
                if (not slate.exposed) and (slate.flag == 0):
                    slate.flagImpliedSafe()
                    workQueue.append(slate)
        ## if un-exposed slates count minues those flagged safe, matches Canvas mines count
        ## it implies are remaining un-exposed un-flagged slates are mined
        if self.width * self.height - self.discovery - self.sFlagCount == self.mines:
            for slate in self.slates:
                if (not slate.exposed) and (slate.flag == 0):
                    slate.flagImpliedMine()
                    workQueue.append(slate)

    def board(self):
        ## This is to dump details of the canvas and slates for progem debugging process
        result  = f"\n{self.__height} rows and {self.__width} columns and {self.mines} mines and {self.tools} tools\n"
        for r in range(self.__height):
            result = result + "["
            for c in range(self.__width):
                symbol, comment = self.slates[r*self.width+c].slateSymbol
                result = result + symbol
            result = result + "]\n"
        result = result + f"{self.cFlagCount} flags, {self.discovery} slates exposed, game is "
        result = result + f"{'won' if self.hasWon else ('lost' if self.hasLost else 'on-going')}."
        return result

    def __str__(self):
        result = f"{self.__height} rows and {self.__width} columns and {self.mines} mines and {self.tools} tools\n"
        for i in range(self.__height * self.__width):
            result = result + f"slate[{i}]: {self.__slates[i]} "
            result = result + "\n"
        return result


