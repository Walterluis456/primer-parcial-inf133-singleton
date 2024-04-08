import requests

class GuessGameClient:
    base_url = 'http://localhost:8000'

    @classmethod
    def create_game(cls, player):
        url = f'{cls.base_url}/guess'
        response = requests.post(url, json={"player": player})
        return response.json()

    @classmethod
    def list_games(cls):
        url = f'{cls.base_url}/guess'
        response = requests.get(url)
        return response.json()

    @classmethod
    def get_game_by_id(cls, game_id):
        url = f'{cls.base_url}/guess/{game_id}'
        response = requests.get(url)
        return response.json()

    @classmethod
    def get_games_by_player(cls, player):
        url = f'{cls.base_url}/guess/?player={player}'
        response = requests.get(url)
        return response.json()

    @classmethod
    def make_attempt(cls, game_id, attempt):
        url = f'{cls.base_url}/guess/{game_id}'
        response = requests.put(url, json={"attempt": attempt})
        return response.json()

    @classmethod
    def delete_game(cls, game_id):
        url = f'{cls.base_url}/guess/{game_id}'
        response = requests.delete(url)
        return response.json()

if __name__ == "__main__":

    game_id = GuessGameClient.create_game("Julian")["1"]
    print(f"Game created with ID: {game_id}")

    games = GuessGameClient.list_games()
    print("List of games:", games)

    game = GuessGameClient.get_game_by_id(game_id)
    print("Game details:", game)

    games_by_player = GuessGameClient.get_games_by_player("Julian")
    print("Games by player Julian:", games_by_player)

    print(GuessGameClient.make_attempt(game_id, 25))

    game = GuessGameClient.get_game_by_id(game_id)
    print("Game details")
