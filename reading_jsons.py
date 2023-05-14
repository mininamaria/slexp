from typing import List


def countitude(crds: List[List[int]]):
    result = crds[0][0] + crds[1][0] / 60 + crds[2][0] / (10000 * 3600)
    return round(result, 2)


def main():
    print("Hello world!")
    temporary = [[37, 0], [97, 0], [360000]]
    countitude(temporary)
    skeleton = {"type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": []
                        },
                        "properties": {
                            "name": "",
                            "tags": [],
                            "date": ""
                        }
                    }
                ]}


if __name__ == "__main__":
    main()

'''
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [20, 10]
    },
      "properties": {
        "name": "null island"
  }
}
  ]
}
'''
