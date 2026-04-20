import requests
from app.settings import get_settings

class AuthService:
    _instance = None
    
    @classmethod
    def depends_init(cls):
        if cls._instance is None:
            cls._instance = cls(settings=get_settings())
        return cls._instance

    def __init__(self, settings):
        self.settings = settings

    def fetch_map_data(self):
        response = requests.get(self.settings.MC_VERIFY_URL)
        return response.json()

    def is_on_coordinates(self, x, y, z):
        target_coords = tuple(map(int, self.settings.MC_COORDINATES.split(",")))
        player_coords = (int(x), int(y), int(z))
        print(f"Checking coordinates: {player_coords} against target {target_coords}")
        return player_coords == target_coords

    def verify_minecraft_user(self, mc_username: str):
        map_data = self.fetch_map_data()
        players = map_data.get("players", [])
        for player in players:
            print(f"Checking player: {player.get('name')}")
            if player.get("name") == mc_username:
                print(f"Found player {mc_username} in map data.")
                position = player.get("position", {})
                if self.is_on_coordinates(position.get("x"), position.get("y"), position.get("z")):
                    return True
        return False