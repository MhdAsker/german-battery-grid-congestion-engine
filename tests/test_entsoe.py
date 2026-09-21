from gridflex.ingestion.entsoe import parse_timeseries_xml


def test_parse_entsoe_points():
    payload = b'''<Publication_MarketDocument xmlns="urn:test"><TimeSeries><Period>
    <timeInterval><start>2025-01-01T00:00Z</start></timeInterval><resolution>PT15M</resolution>
    <Point><position>1</position><quantity>10</quantity></Point>
    <Point><position>2</position><quantity>12</quantity></Point>
    </Period></TimeSeries></Publication_MarketDocument>'''
    frame = parse_timeseries_xml(payload)
    assert frame.value.tolist() == [10.0, 12.0]
    assert (frame.index[1] - frame.index[0]).seconds == 900

