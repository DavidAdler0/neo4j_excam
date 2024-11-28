


class ConversationRepository:
    def __init__(self, driver):
        self._driver = driver

    def create_device(self, device_data):
        with self._driver.session() as session:
            query = """
                MERGE (device:Device {device_id: $id, 
                                        name: $name,
                                        brand: $brand,
                                        model: $model,
                                        os: $os
                                    })
                RETURN device.device_id
                """
            result = session.run(query, device_data)
            record = result.single()
            return dict(record)["device.device_id"]

    def create_connected_relationship(self, relation_data):
        with self._driver.session() as session:
            query = """
                MATCH (device1:Device{device_id: $from_device})
                MATCH (device2:Device{device_id: $to_device})
                CREATE (device1)-[:CONNECTED {from_device: $from_device,
                                                to_device: $to_device,
                                                method: $method,
                                                bluetooth_version: $bluetooth_version,
                                                signal_strength_dbm: $signal_strength_dbm,
                                                distance_meters: $distance_meters,
                                                duration_seconds: $duration_seconds,
                                                timestamp: $timestamp
                                            }]->(device2)
                """
            result = session.run(query, relation_data)
            record = result.single()
            return dict(record)

    def find_strong_signal(self):
        with self._driver.session() as session:
            query = """
                    match (d1:Device)-[c:CONNECTED]-(d2:Device)
                    where c.signal_strength_dbm > -60
                    return d1, d2
                    """
            result = session.run(query)
            return list(result)

    def count_connections_of_device(self, device_id):
        with self._driver.session() as session:
            query = """
                    match (node1:Device) -[rel:CONNECTED]- (:Device)
                    where node1.device_id = $device_id
                    return count(node1)
            """
            result = session.run(query, device_id=device_id)
            return result.single()