from collections import deque

class GameQueue:
    def __init__(self, k):
        self.k = k
        self.queue = deque()

    def insert(self, id_player, rating, timestamp):
        self.queue.append({"id": id_player, "rating": rating, "timestamp": timestamp})

    def delete(self, id_player):
        self.queue = deque(player for player in self.queue if player["id"] != id_player)

    def best_game(self):
        if len(self.queue) < 2 * self.k:
            return None, None

        # Za zdaj vzamemo prvih 2k igralcev
        selected_players = [self.queue.popleft() for _ in range(2 * self.k)]
        player_ids = [player["id"] for player in selected_players]

        # Placeholder imbalance vrednost (fiksno)
        imbalance = 0

        return player_ids, imbalance

