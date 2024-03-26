from influxdb import InfluxDBClient


class InfluxService:
    def __init__(self, host, port, database):
        self.host = host
        self.port = port
        self.database = database
        self.client = InfluxDBClient(host=host, port=port, database=database)

    def write_data(self, measurement, tags, data):
        influx_data = []
        for data_point in data:
            time = data_point.pop("time")
            json_data = {
                "measurement": measurement,
                "tags": tags,
                "time": time,
                "fields": data_point
            }
            influx_data.append(json_data)
        self.client.write_points(influx_data)

    def query_data(self, query):
        return self.client.query(query)

    def delete_data(self, tag_key, tag_value):
        query = f"SHOW MEASUREMENTS WHERE \"{tag_key}\" = '{tag_value}'"
        result = self.client.query(query)

        # Extracting the measurements
        measurements = [measurement['name'] for measurement in result.get_points()]

        # Deleting each measurement
        for measurement in measurements:
            self.client.query(f"DROP MEASUREMENT {measurement}")

    def close(self):
        self.client.close()