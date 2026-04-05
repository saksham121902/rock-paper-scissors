import unittest
from RPS_game import play, quincy, abbey, kris, mrugesh
from RPS import player


class UnitTests(unittest.TestCase):
    def test_player_vs_quincy(self):
        self.assertGreater(play(player, quincy, 1000), 60)

    def test_player_vs_abbey(self):
        self.assertGreater(play(player, abbey, 1000), 60)

    def test_player_vs_kris(self):
        self.assertGreater(play(player, kris, 1000), 60)

    def test_player_vs_mrugesh(self):
        self.assertGreater(play(player, mrugesh, 1000), 60)


if __name__ == "__main__":
    unittest.main()
