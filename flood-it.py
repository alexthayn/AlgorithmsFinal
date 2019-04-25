# Flood-It Solution algorithm for algorithms final project
# Game code from https://arvinbadiola.wordpress.com/2012/04/18/flood-it-game-in-python-2-7-with-pygame/
# pygame and networkx both need to be installed
import pygame
import random
import networkx as nx

DEFAULT_SCREEN_SIZE = [448, 64]
DEFAULT_BOARD_WIDTH = 448
DEFAULT_BOARD_HEIGHT = 64
DEFAULT_TILE_SIZE = [32, 32]
DEFAULT_STEP_SIZE = 32

# declares all global variables
board = None
watchlist = None  # list of coordinates of all "flooded" tiles
checkedlist = None  # list of coordinates of tiles already updated
tiles = None  # list of coordinates of all tiles in the game
is_done = False  # tells whether game is done
update = False  # tells whether display must update
for_restart = False  # tells whether player opted to restart
movecount = 0  # counts moves taken by the player
btncol = None  # list of control buttons

# returns a color RGB values given a number from 1-6


def _getcolor(colornum):
    if colornum == 1:
        return [255, 105, 180]  # hot pink
    elif colornum == 2:
        return [138, 43, 226]  # blue violet
    elif colornum == 3:
        return [255, 255, 0]  # yellow
    elif colornum == 4:
        return [255, 69, 0]  # orange red
    elif colornum == 5:
        return [110, 139, 61]  # dark olive green
    elif colornum == 6:
        return [0, 191, 255]  # deep skyblue

# tells whether the two colors are the same


def _issamecolor(color1, color2):
    if color1[0] == color2[0] and color1[1] == color2[1] and color1[2] == color2[2]:
        return True
    return False

# adds a tile's coordinate to list of flooded tiles


def _addtowatchlist(coord, color):
    global tiles
    global watchlist
    adjcolor = tiles[str(coord[0])+"-"+str(coord[1])]
    if _issamecolor(color, adjcolor):
        _fill([coord[0], coord[1]], color)

# updates the color of the flooded tiles to the newly selected one


def _colorwatchlist(color):
    global checkedlist
    global watchlist
    for i in range(len(watchlist)):
        screen.blit(color, watchlist[i])
        checkedlist.remove(watchlist[i])
    pygame.display.update()


def _fill(coord, color):
    global checkedlist
    global tiles
    global watchlist

    # stops updates of already checked coordinates
    if checkedlist.__contains__(coord):
        return
    else:
        checkedlist.append(coord)
        # adds coordinate to watchlist if not existing
        if not watchlist.__contains__(coord):
            watchlist.append(coord)

    tile = pygame.Surface(DEFAULT_TILE_SIZE)
    tile.fill(color)
    screen.blit(tile, coord)
    if coord[0] - DEFAULT_STEP_SIZE >= 0:
        X = coord[0] - DEFAULT_STEP_SIZE
        Y = coord[1]
        _addtowatchlist([X, Y], color)

    if coord[0] + DEFAULT_STEP_SIZE < DEFAULT_BOARD_WIDTH:
        X = coord[0] + DEFAULT_STEP_SIZE
        Y = coord[1]
        _addtowatchlist([X, Y], color)

    if coord[1] - DEFAULT_STEP_SIZE >= 0:
        X = coord[0]
        Y = coord[1] - DEFAULT_STEP_SIZE
        _addtowatchlist([X, Y], color)

    if coord[1] + DEFAULT_STEP_SIZE < DEFAULT_BOARD_HEIGHT:
        X = coord[0]
        Y = coord[1] + DEFAULT_STEP_SIZE
        _addtowatchlist([X, Y], color)


def _render_controls():
    # button initialization
    global btncol
    btncol = [dict(), dict(), dict(), dict(), dict(), dict()]

    # button color initialization
    btncol[0]['color'] = _getcolor(1)
    btncol[1]['color'] = _getcolor(2)
    btncol[2]['color'] = _getcolor(3)
    btncol[3]['color'] = _getcolor(4)
    btncol[4]['color'] = _getcolor(5)
    btncol[5]['color'] = _getcolor(6)

    # button position initialization
    btncol[0]['position'] = [512, 21]
    btncol[1]['position'] = [512, 95]
    btncol[2]['position'] = [512, 169]
    btncol[3]['position'] = [512, 243]
    btncol[4]['position'] = [512, 317]
    btncol[5]['position'] = [512, 391]

    # button bounds initialization
    btncol[0]['bounds'] = pygame.Rect(512, 21, 32, 32)
    btncol[1]['bounds'] = pygame.Rect(512, 95, 32, 32)
    btncol[2]['bounds'] = pygame.Rect(512, 169, 32, 32)
    btncol[3]['bounds'] = pygame.Rect(512, 243, 32, 32)
    btncol[4]['bounds'] = pygame.Rect(512, 317, 32, 32)
    btncol[5]['bounds'] = pygame.Rect(512, 391, 32, 32)

    for i in range(len(btncol)):
        pygame.draw.circle(screen, btncol[i]['color'], [
                           btncol[i]['position'][0]+16, btncol[i]['position'][1]+16], 16)

    pygame.display.update()


def _gameover():
    shade = pygame.Surface(DEFAULT_SCREEN_SIZE)
    shade.fill([0, 0, 0])
    shade.set_alpha(200)
    screen.blit(shade, [0, 0])

    # imggameover = pygame.image.load('gameover.png')
    tilenum = random.randint(1, 4)
    rectangle = None
    if tilenum == 1:
        rectangle = pygame.Rect(0, 0, 320, 240)
    elif tilenum == 2:
        rectangle = pygame.Rect(320, 0, 320, 240)
    elif tilenum == 3:
        rectangle = pygame.Rect(0, 240, 320, 240)
    elif tilenum == 4:
        rectangle = pygame.Rect(320, 240, 320, 240)

    # screen.blit(imggameover, [64, 104], rectangle)

    pygame.display.update()


def _success():
    shade = pygame.Surface(DEFAULT_SCREEN_SIZE)
    shade.fill([0, 0, 0])
    shade.set_alpha(200)
    screen.blit(shade, [0, 0])

    # imgwin = pygame.image.load('win.png')
    tilenum = random.randint(1, 4)
    rectangle = None
    if tilenum == 1:
        rectangle = pygame.Rect(0, 0, 320, 240)
    elif tilenum == 2:
        rectangle = pygame.Rect(320, 0, 320, 240)
    elif tilenum == 3:
        rectangle = pygame.Rect(0, 240, 320, 240)
    elif tilenum == 4:
        rectangle = pygame.Rect(320, 240, 320, 240)

    # screen.blit(imgwin, [64, 104], rectangle)

    pygame.display.update()


def _init():
    global checkedlist
    global watchlist
    global tiles
    global movecount
    global for_restart
    board = dict()
    checkedlist = list()
    watchlist = list()
    tiles = dict()
    movecount = 0
    for_restart = False

    screen.fill(0)  # color screen black

    # fills the grid with randomly colored tiles
    for i in range(14):
        for j in range(2):
            # sets coordinates
            X = DEFAULT_STEP_SIZE*i
            Y = DEFAULT_STEP_SIZE*j
            # gets random tile
            colornum = random.randint(1, 6)
            board[i, j] = colornum
            tile = pygame.Surface(DEFAULT_TILE_SIZE)
            color = _getcolor(colornum)
            tile.fill(color)
            tiles[str(X)+"-"+str(Y)] = color
            screen.blit(tile, [X, Y])

    # adds starting tile to watch list
    _fill([0, 0], tiles['0-0'])

    # initializes first time coloring of watch list
    tile = pygame.Surface(DEFAULT_TILE_SIZE)
    tile.fill(tiles['0-0'])
    _colorwatchlist(tile)

    # renders the controls
    _render_controls()

    print(solution(board))


###########################################################
# MY SOLUTION CODE
###########################################################
def solution(board):
    markedTiles = findMarkedTiles(board)

    for t in markedTiles:
        convertedLocation = [32*x for x in t]
        # check if this tile is in flooded region
        if convertedLocation not in watchlist:
            executeShortestPath(convertedLocation)

# find the marked tiles on the board


def findMarkedTiles(board):
    # There is a marked tile for each color on the board
    markedTiles = dict()

    for i in range(14):
        for j in range(2):
            curColor = board[i, j]
            markedTiles[curColor] = [i, j]

    # order the tiles from righmost located to leftmost located
    orderedTiles = []
    for t in markedTiles.values():
        orderedTiles.append(t)
    return sorted(orderedTiles)

# execute the flood fill algorithm on the shortest path


def executeShortestPath(location):
    # get the cost matrix
    costMatrix = createPathCostMatrix(watchlist[len(watchlist)-1]
                                      if len(watchlist) > 0 else [0, 0], location)
    graph = createGraph(costMatrix)
    source = ""
    if len(watchlist) == 0:
        source = "0-0"
    else:
        source = str(watchlist[len(watchlist)-1][0])+"-"+str(watchlist[len(watchlist)-1][1])
    target = str(location[0])+"-"+str(location[1])
    path = nx.shortest_path(graph, source=source,
                            target=target, method='dijkstra')
    prevNode = None
    for node in path:
        if prevNode != None and tiles[prevNode] != tiles[node]:
            print(node)
            setTile(tiles[node])
        prevNode = node


def setTile(color):
    global movecount
    global for_restart
    if color != None and movecount < 25:
        if not for_restart:
            movecount += 1
            tile = pygame.Surface(DEFAULT_TILE_SIZE)
            tile.fill(color)
            for i in range(len(watchlist)):
                _fill(watchlist[i], color)
            _colorwatchlist(tile)
            pygame.display.set_caption('Flood-it! '+str(movecount)+'/25')

        if len(watchlist) == 196:
            if not for_restart:
                _success()
                for_restart = True
            pygame.display.set_caption('Flood-it! Congratulations. You won!')

        if movecount == 25 and len(watchlist) != 196:
            if not for_restart:
                _gameover()
                for_restart = True
            pygame.display.set_caption('Flood-it! GAME OVER!')
    pygame.time.wait(500)


def ycolorLocation(color):
    if color == [255, 105, 180]:
        return 21+15
    if color == [138, 43, 226]:
        return 95+15
    if color == [255, 255, 0]:
        return 169+15
    if color == [255, 69, 0]:
        return 243+15
    if color == [110, 139, 61]:
        return 317+15
    if color == [0, 191, 255]:
        return 391+15

# create  a graph given a matrix of costs


def createGraph(costs):
    g = nx.DiGraph()
    # create all the nodes
    for i in range(14):
        for j in range(2):
            g.add_node(str(i*32)+"-"+str(j*32))

    # add weighted edges
    j = 0
    for i in range(14):
        source = str(i*32)+"-"+str(j*32)
        if(i < 13):
            # add right edge
            right = str((i+1)*32)+"-"+str(j*32)
            g.add_edge(source, right, weight=costs[j][i+1])

        # add down edge
        down = str(i*32)+"-"+str((j+1)*32)
        g.add_edge(source, down, weight=costs[j+1][i])

    j = 1
    for i in range(14):
        source = str(i*32)+"-"+str(j*32)
        if(i < 13):
            # add right edge
            right = str((i+1)*32)+"-"+str(j*32)
            g.add_edge(source, right, weight=costs[j][i+1])

        # add up edge
        up = str(i*32)+"-"+str((j-1)*32)
        g.add_edge(source, up, weigth=costs[j][i-1])
    return g


def createPathCostMatrix(start, end):
    costMatrix = [[1 for x in range(14)]
                  for y in range(2)]
    i = start[0]
    while i <= end[0]:
        for j in range(2):
            if j == 0:
                # check if left tile is same color
                if(i-32 >= 0):
                    if tiles[str(i-32)+"-"+str(j)] == tiles[str(i)+"-"+str(j)]:
                        costMatrix[j][i // 32] = 0

                    if tiles[str(i)+"-"+str(j+32)] == tiles[str(i)+"-"+str(j)] and tiles[str(i-32)+"-"+str(j+32)] == tiles[str(i)+"-"+str(j)]:
                        costMatrix[j][i // 32] = 0

            if j == 1:
                j = 32
                if(i-32 >= 0):
                    if tiles[str(i-32)+"-"+str(j)] == tiles[str(i)+"-"+str(j)]:
                        costMatrix[j//32][i // 32] = 0
                    up = costMatrix[0][i // 32]
                    if up == 0 and tiles[str(i-32)+"-"+str(j-32)] == tiles[str(i)+"-"+str(j)]:
                        costMatrix[j//32][i // 32] = 0
        i += 32
    return costMatrix



###########################################################
# GAME LOOP
###########################################################
if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode(DEFAULT_SCREEN_SIZE)
    pygame.display.set_caption('Flood-it!')

    _init()

    while is_done == False:
        # checks for changes in direction and validates it
        for e in pygame.event.get():
            color = None

            if e.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(btncol)):
                    if btncol[i]['bounds'].collidepoint(e.pos):
                        color = _getcolor(i+1)
            elif e.type == pygame.QUIT:
                is_done = True
            elif e.type == pygame.KEYUP:
                update = True
                if e.key == pygame.K_ESCAPE:
                    is_done = True
                elif e.key == pygame.K_r:
                    _init()
                elif e.key == pygame.K_a:
                    color = _getcolor(1)
                elif e.key == pygame.K_s:
                    color = _getcolor(2)
                elif e.key == pygame.K_d:
                    color = _getcolor(3)
                elif e.key == pygame.K_z:
                    color = _getcolor(4)
                elif e.key == pygame.K_x:
                    color = _getcolor(5)
                elif e.key == pygame.K_c:
                    color = _getcolor(6)

            if color != None and movecount < 25:
                if not for_restart:
                    movecount += 1
                    tile = pygame.Surface(DEFAULT_TILE_SIZE)
                    tile.fill(color)
                    for i in range(len(watchlist)):
                        _fill(watchlist[i], color)
                    _colorwatchlist(tile)
                    pygame.display.set_caption(
                        'Flood-it! '+str(movecount)+'/25')

            if len(watchlist) == 196:
                if not for_restart:
                    _success()
                    for_restart = True
                pygame.display.set_caption(
                    'Flood-it! Congratulations. You won!')

            if movecount == 25 and len(watchlist) != 196:
                if not for_restart:
                    _gameover()
                    for_restart = True
                pygame.display.set_caption('Flood-it! GAME OVER!')
        if update == True:
            # TODO: call update function
            update = False


#############################################
# TESTS
#############################################
def test_findMarkedTiles():
    # create test board
    board = dict()
    for i in range(14):
        for j in range(2):
            board[i, j] = 2

    markedTilesSet = findMarkedTiles(board)
    assert len(markedTilesSet) == 1
    assert markedTilesSet[0] == [13, 1]

    # insert two more marked tiles
    board[5, 0] = 0
    board[5, 1] = 4
    markedTilesSet = findMarkedTiles(board)
    assert len(markedTilesSet) == 3
    assert markedTilesSet[0] == [5, 0]
    assert markedTilesSet[1] == [5, 1]
    assert markedTilesSet[2] == [13, 1]


def test_createGraph():
    # create a cost matrix to base the graph from
    pass


def test_createCostMatrix():
    # create a test board
    global tiles
    tiles = dict()
    for i in range(14):
        for j in range(2):
            tiles[str(i*32)+"-"+str(j*32)] = _getcolor(2)
    tiles["0-0"] = _getcolor(1)
    tiles["32-0"] = _getcolor(1)
    tiles["64-0"] = _getcolor(1)
    print(tiles)
    matrix = createPathCostMatrix([0,0],[416,32])
    print(matrix)
    expectedMatrix = [[1,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    assert expectedMatrix == matrix

    # change board tiles
    tiles["96-32"] = _getcolor(1)
    matrix = createPathCostMatrix([0,0],[416,32])
    expectedMatrix = [[1,0,0,1,0,0,0,0,0,0,0,0,0,0],[1,0,0,1,0,0,0,0,0,0,0,0,0,0]]
    assert expectedMatrix == matrix