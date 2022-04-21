def convert_id(found):
    found = list(found)
    for i in range(len(found)):
        if "_id" in found[i]:
            found[i]["_id"] = str(found[i]["_id"])
    return found


def getTrimmedWords(word):
    texts = word.split()

    text = ""
    lastRange = min(len(texts), 20)
    for i in range(0, lastRange):
        text += texts[i] + " "

    return text


def getCategoryFilter(oldFilter, category):
    if not (category == None):
        oldFilter["category"] = category

    return oldFilter


def getTagFilter(oldFilter, tag):

    if not (tag == None):
        oldFilter["tags"] = {"$in": [tag]}

    return oldFilter
