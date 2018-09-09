# duelyst-api
This API grants easy access to Duelyst data

## 1. Extracting the game's JSON data
The game should be run, and then you use the browser's console to run the code of card-extractor.js.
Your clipboard will be filled with the game's JSON card data, paste it in your favorite editor

## 2. Generating the CSV file
I don't know how to do that. This CSV file is currently out of date as a result.

## 3. Updating the Duelyst wiki articles
The python script cards2articles.py will generate a txt file ready to import using pywikibot.
todo: better describe this process

## 4. Generating animated gif files
The python script cards2gifs.py will generate animated gif files from the game's png and plist resources, and rename them correctly thanks to the mapping found in cards.json
todo: explain that better
todo: have the script gracefully handle both minion, spell and artifact animations

## Credits
[Constitute](https://github.com/Constitute/duelyst-api) for his Duelyst API code.
[mycroft92](https://github.com/mycroft92/ArchonPageBinder) for his help and previous wiki bot scripts
[mrtom31](https://github.com/mrtom31/duelgif) for his gif generator code
