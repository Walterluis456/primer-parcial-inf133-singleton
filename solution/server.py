class GuessGame:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.reset()
        return cls._instance

    def reset(self):
        self.games = {}
        self.next_id = 1

    def create_game(self, player):
        game_id = self.next_id
        self.games[game_id] = {
            "player": player,
            "number": randint(1, 100),
            "attempts": [],
            "status": "En Progreso"
        }
        self.next_id += 1
        return game_id

    def get_game_by_id(self, game_id):
        return self.games.get(game_id)

    def get_games_by_player(self, player):
        return {game_id: game for game_id, game in self.games.items() if game["player"] == player}

    def update_attempts(self, game_id, attempt):
        game = self.games.get(game_id)
        if game:
            game["attempts"].append(int(attempt))
            if int(attempt) == game["number"]:
                game["status"] = "Finalizado"
                return "¡Felicitaciones! Has adivinado el número"
            elif int(attempt) < game["number"]:
                return "El número a adivinar es mayor"
            else:
                return "El número a adivinar es menor"
        return "Partida no encontrada"

    def delete_game(self, game_id):
        if game_id in self.games:
            del self.games[game_id]
            return "Partida eliminada"
        return "Partida no encontrada"

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from random import randint
import json

class APIServer(BaseHTTPRequestHandler):
    def _set_response(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_POST(self):
        if self.path == '/guess':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            player = data.get('player')
            game_id = GuessGame().create_game(player)
            response_data = GuessGame().get_game_by_id(game_id)
            self._set_response()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))

    def do_GET(self):
        if self.path == '/guess':
            response_data = GuessGame().games
            self._set_response()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        elif self.path.startswith('/guess/'):
            path_parts = self.path.split('/')
            if len(path_parts) == 3:
                game_id = int(path_parts[2])
                response_data = GuessGame().get_game_by_id(game_id)
                if response_data:
                    self._set_response()
                    self.wfile.write(json.dumps(response_data).encode('utf-8'))
                else:
                    self._set_response(404)
                    self.wfile.write("Partida no encontrada".encode('utf-8'))
            else:
                query_components = parse_qs(urlparse(self.path).query)
                player = query_components.get('player', [None])[0]
                if player:
                    response_data = GuessGame().get_games_by_player(player)
                    self._set_response()
                    self.wfile.write(json.dumps(response_data).encode('utf-8'))

    def do_PUT(self):
        if self.path.startswith('/guess/'):
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            data = json.loads(put_data)
            path_parts = self.path.split('/')
            if len(path_parts) == 3:
                game_id = int(path_parts[2])
                attempt = data.get('attempt')
                response_message = GuessGame().update_attempts(game_id, attempt)
                self._set_response()
                self.wfile.write(json.dumps({"message": response_message}).encode('utf-8'))

    def do_DELETE(self):
        if self.path.startswith('/guess/'):
            path_parts = self.path.split('/')
            if len(path_parts) == 3:
                game_id = int(path_parts[2])
                response_message = GuessGame().delete_game(game_id)
                self._set_response()
                self.wfile.write(json.dumps({"message": response_message}).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=APIServer, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
