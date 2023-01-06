# Kid_Calculator
Embllem


Good luck kiddo


Usage: Load it into your IDE (I used Pycharm, so I will only know for sure how it works there) or install pandas manually and use IDLE or something (don't ask me how to do this, because I dont't know). I wanted to add a GUI but I couldn't be bothered, so yeah...

Run randomizer.py for randomization of any of the following games: Sacred Stones, Shadow Dragon, New Mystery, Awakening, Birthright, Conquest, Revelations and Three Houses.
3H paths are treated as different games like fates, so put in Silver Snow if you do that route etc.
An example is down in the __main__ part, just change the game name in `t = Randomizer(game_name)` and run it. Currently it uses mode 'maximal' (all characters are used if possible) but you can also set it to 'minimal' (all classes are used once) by adding 'minimal' as an argument in `result, leftover = t.randomize()`.

I've tried to add all oddities and things from all the games so it doesn't give impossible combinations, but especially fates was a pain in the ass because of the heart and friendship seals (like Jakob only being able to A+ Gunter in Conquest, not in Revelation even though you can use Gunter, or Kana F being able to A+/S support Midori or Percy unless they are their Sibling) so it might be handy to keep that in mind.



There is also a maximizer (that's why the name is Kid_calculator), which you can use by running database.py. This supports Genealogy, Awakening and Fates.
I've put a couple of examples in the comments which show what you need and how you can use the results, so just take a look there and try to change it to your game.

If you have any questions, feel free to ask, because I explained it pretty poorly.
