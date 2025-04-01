from collections import deque
import math

class GameQueue:
    def __init__(self, k, alpha=1.0, p=2, q=2):
        self.k = k
        self.queue = deque()
        self.alpha = alpha
        self.p = p
        self.q = q

    def insert(self, id_player, rating, timestamp):
        self.queue.append({"id": id_player, "rating": rating, "timestamp": timestamp})

    def delete(self, id_player):
        self.queue = deque(player for player in self.queue if player["id"] != id_player)

    def best_game(self):
        if len(self.queue) < 2 * self.k:
            return None, None

        selected_players = [self.queue.popleft() for _ in range(2 * self.k)]
        player_ids = [player["id"] for player in selected_players]
        ratings = [player["rating"] for player in selected_players]

        team1 = ratings[:self.k]
        team2 = ratings[self.k:]

        imbalance = self.calculate_imbalance(team1, team2)
        return player_ids, imbalance

    def calculate_imbalance(self, team1, team2):
        # p-fairness
        p = self.p
        q = self.q
        alpha = self.alpha

        sp1 = sum(r ** p for r in team1) ** (1 / p)
        sp2 = sum(r ** p for r in team2) ** (1 / p)
        dp = abs(sp1 - sp2)

        # q-uniformity
        all_players = team1 + team2
        mean = sum(all_players) / len(all_players)
        vq = (sum(abs(r - mean) ** q for r in all_players) / len(all_players)) ** (1 / q)

        return alpha * dp + vq


def main():
    k = 3
    game_queue = GameQueue(k)

    events = [
        ("enqueue", 2400, "12:54:33.567"),
        ("enqueue", 2200, "12:54:34.567"),
        ("enqueue", 2100, "12:54:35.567"),
        ("enqueue", 2300, "12:54:36.567"),
        ("enqueue", 2500, "12:54:37.567"),
        ("enqueue", 2000, "12:54:38.567"),
        ("Make_game", "12:55:00.000")
    ]

    current_id = 0
    for event in events:
        if event[0] == "enqueue":
            _, rating, timestamp = event
            game_queue.insert(current_id, rating, timestamp)
            current_id += 1
        elif event[0] == "Make_game":
            _, timestamp = event
            players, imbalance = game_queue.best_game()
            if players is not None:
                print("PLAYERS:")
                print(" ".join(map(str, players)))
                print(f"IMBALANCE: {imbalance:.2f}")
            else:
                print(f"[!] Not enough players to create a game at {timestamp}.")


if __name__ == "__main__":
    main()
