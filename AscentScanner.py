import requests

region = "USIL"
def query(start: int, num: int) -> str: 
    return """query{
  matchRecords(season: 2024, region:""" + region + """, skip:""" + str(start) + """ , take: 50){
    count
    data{
      data{
        match{
          eventCode,
          matchNum,
          teams{
            teamNumber
          }
          scores{
          	... on MatchScores2024{
              red{
                dcPark1,
                dcPark2
              }
              blue{
                dcPark1,
                dcPark2
              }
            }
          }
        }
      }
    }
  }
}"""
def writeToFile(list: list, region: str, name: str, ext: str):
    with open(region + name + "." + ext, "w") as f:
        f.write(region + " " + name + ": " + str(len(list)) + "\n" )
        for item in list:
            f.write(str(item) + "\n")

initalQuery = "query{matchRecords(season: 2024, region: "+ region + ", skip: 0, take: 0){count}}"

url = "https://api.ftcscout.org/graphql"

r = requests.post(url, json={"query": initalQuery})
count = int(r.json()["data"]["matchRecords"]["count"] / 50) + 1
print("Requests to make: " + str(count))
none = []
l1 = []
l2 = []
l3 = []
obs = []
for i in range(count):
    call = query(i * 50, 50)
    matches = requests.post(url, json={"query": call}).json()["data"]["matchRecords"]["data"]
    for match in matches:
        got = [(none, False), (l1, False), (l2, False), (l3, False), (obs, False)]
        data = match["data"]["match"]
        teams = []
        for team in data["teams"]: 
            teams.append(team["teamNumber"])
        teams.append(data["eventCode"])
        teams.append(data["matchNum"])
        scores = data["scores"]
        parks = [scores["red"]["dcPark1"], scores["red"]["dcPark2"], scores["blue"]["dcPark1"], scores["blue"]["dcPark2"]]
        for park in parks:
            if park == "None":
                got[0] = (none, True)
            elif park == "Ascent1":
                got[1] = (l1, True)
            elif park == "Ascent2":
                got[2] = (l2, True)
            elif park == "Ascent3":
                got[3] = (l3, True)
            elif park == "ObservationZone":
                got[4] = (obs, True)
        for hangType in got:
            if hangType[1]: 
                hangType[0].append(teams)
        
    
writeToFile(none, region, "none", "txt")
writeToFile(l1, region, "l1s", "txt")
writeToFile(l2, region, "l2s", "txt")
writeToFile(l3, region, "l3s", "txt")
writeToFile(obs, region, "obses", "txt")
