from RPS_game import play, quincy, abbey, kris, mrugesh
from RPS import player


print("vs quincy:", play(player, quincy, 1000))
print("vs abbey:", play(player, abbey, 1000))
print("vs kris:", play(player, kris, 1000))
print("vs mrugesh:", play(player, mrugesh, 1000))

# Uncomment to run tests
# import unittest
# unittest.main(module='test_module', exit=False)
