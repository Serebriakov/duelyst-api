#!/usr/bin/env python3

# time python pwb.py scripts/pagefromfile.py -notitle -force -file:/home/fgombault/Sync/duelyst/duelyst-api/wiki_articles.txt

import json
import re
import sys

def getCardImageName(p):
    return getCardName(p).replace(" ", "_")


def getRace(p):
    if (p['category'] == 'unit'):
        return p['type'] # should contain "Minion", "Arcanyst", "Golem"...
    else:
        return u''


def getType(p):
    if (p['category'] == 'unit'):
        if (p['type'] == 'General'):
            return 'General'
        else:
            return 'Minion'
    return str.upper(p['category'][0]) + p['category'][1:]


def boldKeywords(str):
    output = ""
    matches = re.findall(r'<b>[^<>]*</b>', str)
    for m in matches:
        candidate = re.sub(r'<b>', '[[', re.sub(r'</b>', ']] ', m))
        if (not candidate in output):
            output = output + candidate
    words = output.split()
    return " ".join(sorted(set(words), key=words.index))


def getAbilities(p):
    if (p['category'] != 'unit'):
        return ""
    try:
        shortdesc = p['description'][0:p['description'].rindex('<br')]
    except ValueError:
        shortdesc = p['description']
    return boldKeywords(shortdesc)


def getTags(p):
    output = u"[[%s]] " % getFaction(p)
    output += u"[[%s]] " % p['rarity']
    if (p['hidden'] == True):
        output += u"[[Hidden]] "
    # Removed because sometimes keywords are not bold, so let's look for them specifically
    # output += boldKeywords(p['description'])

    # Find some keywords in the text
    for w in [u'Dispel', u'Draw', u'Replace', u'Airdrop', u'Backstab', u'Blast', u'Blood Surge', u'Bond', u'Build', u'Celerity', u'Deathwatch', u'Dying Wish', u'Flying', u'Forcefield', u'Frenzy', u'Grow', u'Infiltrate', u'Intensify', u'Invulnerable', u'Opening Gambit', u'Provoke', u'Ranged', u'Rebirth', u'Rush', u'Sentinel', u'Stun', u'Transform', u'Trial', u'Destiny', u'Zeal', u'Shadow Creep', u'Primal Flourish', u'Hallowed Ground', u'Exhuming Sand', u'Wall']:
        if (re.search(w, p['description'], re.IGNORECASE)):
            output += u' [[' + w + ']]'
    if (re.search(r'Egg', p['description'], re.IGNORECASE)):
        output += u' [[Rebirth]]'
    if (re.search(r'Summon.*Dervish', p['description'], re.IGNORECASE)):
        output += u' [[Summon Dervish]]'
    if (re.search(r'(put|add|return).*(in|to) your action bar', p['description'], re.IGNORECASE)):
        output += u' [[Draw]]'

    return output


def getCardSet(p):
    if (p['setName'] == 'Core'):
        return 'Core'
    if (p['setName'] == 'Basic'):
        return 'Core'
    if (p['setName'] == 'Ancients'):
        return 'Ancient Bonds'
    if (p['setName'] == 'ShimZar'):
        return "Denizens of Shim'Zar"
    if (p['setName'] == 'Unearthed'):
        return 'Unearthed Prophecy'
    if (p['setName'] == 'Immortal'):
        return 'Immortal Vanguard'
    if (p['setName'] == 'Mythron'):
        return 'Trials of Mythron'
    # default value
    return p['setName']


def getDescription(p):
    output = re.sub(r'<b>', "<b>[[", re.sub(r'</b>', ']]</b>', p['description']))
    return output


def getFaction(p):
    if (p['faction'] == 'Lyonar'):
        return u'Lyonar Kingdoms'
    if (p['faction'] == 'Songhai'):
        return u'Songhai Empire'
    if (p['faction'] == 'Magmar'):
        return u'Magmar Aspects'
    if (p['faction'] == 'Vetruvian'):
        return u'Vetruvian Imperium'
    if (p['faction'] == 'Abyssian'):
        return u'Abyssian Host'
    if (p['faction'] == 'Vanar'):
        return u'Vanar Kindred'
    return p['faction']


def getCategories(p):
    cats = getTags(p)
    cats = re.sub(r'\[\[', "[[Category:", cats)
    if (getType(p) != ''):
        cats += " [[Category:%s]]" % getType(p)
    if (getRace(p) != ''):
        cats += " [[Category:%s]]" % getRace(p)
    cats += " [[Category:%s]]" % getCardSet(p)
    return cats


# this is a function to suppress output of some cards we don't want to appear on the wiki
def getBlacklisted(p):
    name_bl = ['QA-IBERO', 'CALIBERO 2.0']
    name_bl += ['Abyssal Scar', 'Malice', 'Shadowspawn']
    id_bl = []
    if p['name'] in name_bl or p['id'] in id_bl:
        return True
    return False


processed_cards = []

# This is to avoid overwriting some articles for cards that have the same name
def getCardName(p):
    keepers = ['Watchful Sentinel', 'Legion', 'Bonechill Barrier', 'Gravity Well', 'Luminous Charge', 'Blazing Spines']
    if p['name'] in keepers and p['name'] in processed_cards:
        return "{0} ({1} {2})".format(p['name'], p['faction'], getType(p))
    return p['name']


output_filter = ''
if len(sys.argv) > 1:
    output_filter = sys.argv[1]


with open('cards.json', encoding='utf-8') as json_file:
    data = json.load(json_file)
    for p in data:
        if p['id'] < 1000000 and getBlacklisted(p) == False:
            output = ''
            output += u"{{-start-}}" + '\n'
            output += u"'''Data:Cards/" + getCardName(p) + u"'''" + '\n'
            output += u"This page is maintained by bots. MANUAL CHANGES '''WILL''' BE OVERWRITTEN.\n" + '\n'
            output += u"Please edit the user-facing display page:  [[{{#dplreplace:{{PAGENAME}}|Data:Cards/|}}]]" + '\n'
            output += u'<onlyinclude>' + '\n'
            output += u'{{Card Metadata' + '\n'
            output += u'| name = ' + getCardName(p) + '\n'
            output += u'| image = ' + getCardImageName(p) + '\n'
            output += u'| set = ' + getCardSet(p) + '\n'
            output += u'| faction = ' + getFaction(p) + '\n'
            output += u'| rarity = ' + p['rarity'] + '\n'
            output += u'| type = ' + getType(p) + '\n'
            output += u'| race = ' + getRace(p) + '\n'
            try:
                output += u'| cost = %d' % p['mana'] + '\n'
            except: KeyError
            try:
                output += u'| attack = %d' % p['attack'] + '\n'
                output += u'| hp = %d' % p['hp'] + '\n'
            except: KeyError
            output += u'| abilities = ' + getAbilities(p) + '\n'
            output += u'| tags = ' + getTags(p) + '\n'
            output += u'| desc = ' + getDescription(p) + '\n'
            output += u'| link = ' + '\n'
            output += u'| id = %d' % p['id'] + '\n'
            output += u'| rotation = standard' + '\n'
            output += u'| available = %s' % p['available'] + '\n'
            output += u'| hidden = %s' % p['hidden'] + '\n'
            output += u"}}" + '\n' # End of Card Metadata
            output += getCategories(p) + '\n'
            output += u'</onlyinclude>' + '\n'
            # output += u'\n{{Display Card Metadata}}' + '\n'
            output += u"{{-stop-}}" + '\n'

            if len(output_filter) == 0 or re.search(output_filter, output, re.IGNORECASE):
                print(output)

            # Mark this card as done
            processed_cards += [getCardName(p)]
