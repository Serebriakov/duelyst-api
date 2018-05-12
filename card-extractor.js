function getCardsJSON() {

    console.log("-------------------------------")
    console.log("CARDS")

    var cards = GameDataManager.getInstance().cardsCollection.models
    var data = [];

    for (i = 0; i < cards.length; i++) {
        var attributes = cards[i].attributes

        // Skip Unavailable, Hidden, Token, Training Teacher
        if (attributes.isAvailable === false) { continue }
        if (attributes.isHiddenInCollection) { continue }
        if (attributes.rarityName === "Token") { continue }
        if (attributes.factionId === 200) { continue }

        // Card
        card = {}
        //card.animations = {}
        //card.keywords = []

        // Basic
        card.id = attributes.id
        card.name = attributes.name
        if (!attributes.isGeneral)
            card.mana = attributes.manaCost

        // Category
        if (attributes.isArtifact) { card.category = "artifact" }
        if (attributes.isSpell) { card.category = "spell" }
        if (attributes.isTile) { card.category = "tile" }
        if (attributes.isUnit) { card.category = "unit" }

        // Description
        // Note: Spells have a description, Units do not
        card.description = attributes.description

        // Faction
        //card.faction = attributes.factionName
        //card.factionId = attributes.factionId
        card.faction = attributes.factionName.split(" ")[0]

        // Keywords
        /*var keywords = attributes.keywordDescriptions
         if (keywords.length) {
             for (var ii = 0; ii < keywords.length; ii++) {
                 card.keywords[ii] = keywords[ii].name
             }
         }*/

        // Race
        //card.race = attributes.raceName
        card.setName = attributes.cardSetName
        var type = card.category == 'unit' ? '_active' : '_idle';
        card.localGif = card.id + type;
        switch (card.setName) {
            case "Core":
                card.gifUrl = "https://cards.duelyst.com/img/cards/core/" + card.id + type + ".gif";
                break;
            case "Shim'Zar":
                card.gifUrl = "https://cards.duelyst.com/img/cards/shimzar/" + card.id + type + ".gif";
                break;
            case "Bloodbound":
                card.gifUrl = "https://cards.duelyst.com/img/cards/bloodstorm/" + card.id + type + ".gif";
                break;
            case "Ancients":
                card.gifUrl = "https://cards.duelyst.com/img/cards/unity/" + card.id + type + ".gif";
                break;
            case "Unearthed":
                card.gifUrl = "https://cards.duelyst.com/img/cards/unearthed-prophecy/" + card.id + type + ".gif";
                break;
            case "Immortal":
                card.gifUrl = "https://cards.duelyst.com/img/cards/wartech/" + card.id + type + ".gif";
                break;
            case "Mythron":
                card.gifUrl = "https://cards.duelyst.com/img/cards/coreshatter/" + card.id + type + ".gif";
        }

        // Rarity
        card.rarity = attributes.rarityName
        //card.rarityId = attributes.rarityId

        // Search
        var atk = attributes.atk ? attributes.atk + 'atk ' + attributes.atk + 'attack' : ''
        var hp = attributes.hp ? attributes.hp + 'hp ' + attributes.hp + 'health' : ''
        var manaCost = attributes.manaCost ? attributes.manaCost + 'mana' : ''

        card.searchableContent = attributes.searchableContent + ' ' + atk + ' ' + hp + ' ' + manaCost

        // Type
        if (attributes.raceName) {
            card.type = attributes.raceName
        } else if (attributes.isGeneral) {
            card.type = "General"
        } else if (attributes.isArtifact) {
            card.type = "Artifact"
        } else if (attributes.isSpell) {
            card.type = "Spell"
        } else {
            card.type = "Minion"
        }

        // Unit
        if (card.category == "unit") {
            card.attack = attributes.atk
            card.hp = attributes.hp
        }

        card.isGeneral = attributes.isGeneral

        // Visibility
        //card.isHidden = attributes.isHiddenInCollection

        // Assets
        var animations = attributes.card._private.baseAnimResource
        var animationId = animations["idle"]
        var resource = RSX[animationId]
        //card.frame = resource.framePrefix
        //card.plist = resource.plist
        var sprite = resource.img

        // Slug
        if (card.isGeneral) {
            var url = sprite
            var pieces = url.split("/")
            var filename = pieces[pieces.length - 1]
            var slug = filename.split(".")[0]
            card.slug = slug
        }
        /*
        var cardTypeAttack = attributes.isArtifact || attributes.isSpell ? "_active.gif" : "_attack.gif"
        var cardTypeIdle = attributes.isArtifact || attributes.isSpell ? "_idle.png" : "_idle.gif"
 
        // Card GIF
        card.attackAnim = "icons/" + card.id + cardTypeAttack
        card.idleAnim = "icons/" + card.id + cardTypeIdle
        */
        // Save
        if (card["id"] < 1000000)
            data.push(card)

        //console.log("-------------------------------")
        //console.log(card.name + " - " + card.category + " - " + card.id)
        //console.log(cards[i])
        //console.log(card)

    }

    console.log("-------------------------------")
    console.log("TOTAL: " + Object.keys(data).length);

    return data;
}

copy(getCardsJSON());




/*console.log(Object.keys(card_list))
        card_list.forEach((key)=>{
            if(key.setName == "Immortal"){
            var link = document.createElement('a');
            link.href = key.gifUrl;
            link.download = key.localGif + '.gif';
            link.className = "link";
            link.innerHTML = key.gifUrl;
            console.log(link)
            document.body.appendChild(link);
            link.click();
            //document.body.removeChild(link);
            }
            
        })*/
