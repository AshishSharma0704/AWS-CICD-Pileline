from lambdas.earthquake.parser import parse


def test_parse_earthquake():

    feature = {
        "id": "eq001",
        "properties": {
            "mag": 5.4,
            "place": "California",
            "time": 1746057600000
        },
        "geometry": {
            "coordinates": [-118.25, 34.05, 10.5]
        }
    }

    item = parse(feature)

    assert item["event_id"] == "eq001"
    assert item["place"] == "California"
    assert float(item["magnitude"]) == 5.4
    assert float(item["latitude"]) == 34.05
    assert float(item["longitude"]) == -118.25
    assert float(item["depth"]) == 10.5
    assert item["severity"] == "Moderate"
