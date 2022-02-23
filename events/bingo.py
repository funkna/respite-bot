import enum

## Add this to respite_bot.py on_message event handler when you take more time to revise the code.
"""
put this outside main()
# bingo_active = False
# current_bingo = None

        global bingo_active
        global current_bingo

        auth = str(message.author)
        auth_roles = []
        cmd = message.content[1:]
        chan = message.channel

        for role in message.author.roles:
            auth_roles.append(role.name)

        # General commands for all users
        if chan.name == channels.BOT_CHANNEL:
            Logger.log(f'{auth} in #{chan.name}: {cmd}')
            if cmd.startswith(commands.HELP):
                await chan.send(messages.HELP)
            #Secret messages
            if cmd.startswith(commands.SOCIAL_CREDIT):
                await chan.send(messages.SOCIAL_CREDIT)

        if chan.name == channels.BINGO_CHANNEL:
            Logger.log(f'{auth} in #{chan.name}: {cmd}')
            if cmd.startswith(commands.BINGO_BOARD) and bingo_active == True:
                await chan.send(current_bingo.boards())

        # Commands for admins
        if chan.name == channels.ADMIN_BOT_CHANNEL:
            Logger.log(f'{auth} in #{chan.name}: {cmd}')

            if roles.verify_role(auth_roles, roles.BINGO_ADMIN) or roles.verify_role(auth_roles, roles.OWNER):
                # Bingo commands
                if cmd.startswith(commands.BINGO_START):
                    if bingo_active == False:
                        teams = cmd[len(commands.BINGO_START):].split(' ')
                        teams = [team for team in teams if team]
                        if len(teams) <= 1:
                            Logger.log(f'{auth} didn\'t specify enough teams to start a bingo.')
                            await chan.send('Failed to start bingo:  Invalid parameters.')
                        else:
                            Logger.log(f'{auth} started a bingo with {len(teams)} teams: {teams}')
                            await chan.send(f'{auth} started a bingo with {len(teams)} teams: {teams}')
                            bingo_active = True
                            current_bingo = bingo.Bingo(teams=teams)
                        return
                    else:
                        Logger.log(f'{auth} attempted to start a bingo, but one is already running.')

                elif cmd.startswith(commands.BINGO_ADD_PLAYER):
                    fields = cmd[len(commands.BINGO_ADD_PLAYER):].split(' ')
                    fields = [f for f in fields if f]
                    if len(fields) < 2:
                        Logger.log(f'{auth} Failed to add:  Invalid parameters.')
                        await chan.send('Failed to add:  Invalid parameters.')
                    team = fields[0]
                    players = fields[1:]
                    current_bingo.teams[team].add_players(players)
                    Logger.log(f'{auth} added {players} to {team}.')
                    await chan.send(f'{auth} added {players} to {team}.')

                elif cmd.startswith(commands.BINGO_REM_PLAYER):
                    fields = cmd[len(commands.BINGO_REM_PLAYER):].split(' ')
                    fields = [f for f in fields if f]
                    team = fields[0]
                    players = fields[1:]
                    if len(fields) < 2:
                        Logger.log(f'{auth} Failed to remove:  Invalid parameters.')
                        await chan.send('Failed to remove:  Invalid parameters.')
                    current_bingo.teams[team].rem_players(players)
                    Logger.log(f'{auth} removed {players} from team {team}.')
                    await chan.send(f'{auth} removed {players} from team {team}.')

                elif cmd.startswith(commands.BINGO_MARK_TILE):
                    fields = cmd[len(commands.BINGO_MARK_TILE):].split(' ')
                    fields = [f for f in fields if f]
                    team = fields[0]
                    player = fields[1]
                    row = fields[2]
                    col = fields[3]
                    if len(fields) < 3:
                        Logger.log(f'{auth} Failed to mark:  Invalid parameters.')
                        await chan.send(f'{auth} Failed to mark:  Invalid parameters.')
                    if current_bingo.teams[team].complete_tile(col, row, player):
                        Logger.log(f'{auth} marked {col}{row} for team {team} by {player}.')
                        await chan.send(f'{auth} marked {col}{row} for team {team} by {player}.')
                    else:
                        Logger.log(f'Failed to mark {col}{row} for team {team} by {player}.')
                        await chan.send(f'Failed to mark {col}{row} for team {team} by {player}.')

                elif cmd.startswith(commands.BINGO_CLEAR_TILE):
                    fields = cmd[len(commands.BINGO_CLEAR_TILE):].split(' ')
                    fields = [f for f in fields if f]
                    team = fields[0]
                    row = fields[1]
                    col = fields[2]
                    if len(fields) < 3:
                        Logger.log(f'{auth} Failed to clear:  Invalid parameters.')
                        await chan.send(f'{auth} Failed to clear:  Invalid parameters.')
                    if current_bingo.teams[team].redact_tile(col, row):
                        Logger.log(f'{auth} cleared {col}{row} for team {team}.')
                        await chan.send(f'{auth} cleared {col}{row} for team {team}.')
                    else:
                        Logger.log(f'Failed to clear {col}{row} for team {team}.')
                        await chan.send(f'Failed to clear {col}{row} for team {team}.')

                elif cmd.startswith(commands.BINGO_STATUS):
                    status_string = 'BINGO STATUS\n'
                    for team in current_bingo.teams:
                        status_string += f'Team {team}:\n{current_bingo.teams[team]}\n'
                    await chan.send(status_string)

                elif cmd.startswith(commands.BINGO_END):
                    if bingo_active == False:
                        Logger.log(f'There is no bingo active.')
                        await chan.send(f'There is no bingo active.')
                    else:
                        status_string = 'END-OF BINGO REPORT\n'
                        for team in current_bingo.teams:
                            status_string += f'Team {team}:\n{current_bingo.teams[team]}\n'
                        await chan.send(status_string)
                        Logger.log(f'{auth} ended the bingo.')
                        await chan.send(f'{auth} ended the bingo.')
                        bingo_active = False

            if cmd.startswith(commands.HELP):
                await chan.send(messages.HELP)
                await chan.send(messages.DEV_HELP)

"""


class Board:

    class Tile:
        class StatusEnum(enum.Enum):
            INCOMPLETE = 0
            COMPLETE = 1

        def __init__(self, status=StatusEnum.INCOMPLETE):
            self.status=status
            self.completed_by=None

        def __str__(self):
            if self.status == Board.Tile.StatusEnum.INCOMPLETE:
                return '-'
            if self.status == Board.Tile.StatusEnum.COMPLETE:
                return 'X'

    def __init__(self, dimension=5):
        self.dimension = dimension
        self.tiles = []
        self.tiles = [[self.Tile() for row in range(self.dimension)] for col in range(self.dimension)]

    def __str__(self):
        f_str = '```'
        for row in range(0,self.dimension):
            f_str += f'['
            for col in range(0,self.dimension):
                f_str += f' {self.tiles[row][col]} '
            f_str += f']\n'
        return f_str + '```'

    def set_tile_status(self, col, row, status, completed_by=None):
        self.tiles[row][col].status = status
        self.tiles[row][col].completed_by = completed_by

    def get_board_stats(self):
        tile_completion_dict = {}
        for row in range(0,self.dimension):
            for col in range(0,self.dimension):
                tile = self.tiles[row][col]
                if tile.completed_by not in tile_completion_dict.keys():
                    tile_completion_dict[tile.completed_by] = 0
                if tile.status == Board.Tile.StatusEnum.COMPLETE:
                    tile_completion_dict[tile.completed_by] += 1
        return tile_completion_dict


class Team:

    def __init__(self, name=None):
        self.players = []
        self.name = name
        self.board = Board()

    def __str__(self):
        f_str = f'Players:  '
        for player in self.players:
            f_str += f'{player}, '
        f_str = f_str[:-2] + '\n'
        f_str += f'MVP: '
        stats = self.board.get_board_stats()
        mvp_name = max(stats, key=stats.get)
        mpv_score = max(stats.values())
        f_str += f'{mvp_name} with {mpv_score}.\n'
        f_str += f'Board:\n'
        f_str += f'{self.board}'
        return f_str

    def complete_tile(self, col, row, player=None):
        if player not in self.players:
            return False
        row_num = ord(row) - ord('A')
        col_num = int(col) - 1
        if (row_num < 0 or row_num > 4) or (col_num < 0 or col_num > 4):
            return False
        self.board.set_tile_status(row_num, col_num, Board.Tile.StatusEnum.COMPLETE, completed_by=player)
        return True

    def redact_tile(self, col, row):
        row_num = ord(row) - ord('A')
        col_num = int(col) - 1
        if (row_num < 0 or row_num > 4) or (col_num < 0 or col_num > 4):
            return False
        self.board.set_tile_status(row_num, col_num, Board.Tile.StatusEnum.INCOMPLETE)
        return True

    def add_players(self, players):
        self.players.extend(players)

    def rem_players(self, players):
        for player in players:
            self.players.remove(player)



class Bingo:

    def __init__(self, teams=['1', '2']):
        self.teams = {}
        for team in teams:
            self.teams[team] = Team(name=team)

    def boards(self):
        f_str = 'BINGO BOARDS'
        for team in self.teams:
            f_str += f'\n\nTeam {self.teams[team].name}:{self.teams[team].board}'
        return f_str

