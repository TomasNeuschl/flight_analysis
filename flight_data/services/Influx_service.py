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

    def retrieve_data(self, measurement, tag_key, tag_value):
        query = f'SELECT * FROM "{measurement}" WHERE "{tag_key}"=\'{tag_value}\''

        result = self.client.query(query)

        # Extracting the measurements
        return result.raw.get('series')[0]

    def delete_data(self, measurement, tag_key, tag_value):
        query = f'DELETE FROM "{measurement}" WHERE "{tag_key}"=\'{tag_value}\''
        self.client.query(query)

    def close(self):
        self.client.close()
