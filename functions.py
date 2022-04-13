def convert_id(found):
  found = list(found)
  for i in range(len(found)):
      if "_id" in found[i]:
          found[i]["_id"] = str(found[i]["_id"])
  return found