This API contains a few endpoints:
- /get_word - returns one random word, no parameters could be specified.
- /get_wiki/<word> - returns summary of Wikipedia page for given <word>. If no word is specified. It will get one using previous endpoint internally.
- /get_words/<word>/<n> - both <word> and <n> in optional. Returns fequency of <n> most used words in Wikipedia summary for given <word>. If on word is specified, it will get one from /get_word; <n> by default is equal to five.
- /get_joke?firstName=&lastName= - returns random joke about Chuck Norris. If you specify first and last name, if will substitute Chuck Norris into given identity.