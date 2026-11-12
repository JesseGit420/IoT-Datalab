# Wat deed de stekker het laatste uur?
import os
from influxdb_client import InfluxDBClient

client = InfluxDBClient(url="http://influxdb:8086", org="iot",
                        token=os.environ["INFLUXDB_TOKEN"])
vraag = '''
from(bucket: "energie")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "meting" and r._field == "vermogen")
'''
metingen = []
for tabel in client.query_api().query(vraag):
    for rij in tabel.records:
        metingen.append(rij.get_value())

print(len(metingen), "metingen")
print("gemiddeld:", round(sum(metingen) / len(metingen)), "W")
