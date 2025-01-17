
import unittest, pytest
from luxio.common.error_codes import *
from luxio.external_clients.serializer.serializer_factory import *
from luxio.common.enumerations import *

class TestSerializer(unittest.TestCase):
    test_dict = {
        "an_integer": 25,
        "a_float": 25.289,
        "a_string" : "I'm going to go to the only place not tainted by capatilasim....SPACE!!!",
        "a_bool": True,
        "a_dict": {
            "a_game": "Command and Conquer: Red Alert",
            "an_int": 99,
            "a_float": 53.252
        }
    }

    def test_pickle(self):
        srl = SerializerFactory.get(SerializerType.PICKLE)
        self.assertEqual(TestSerializer.test_dict, srl.deserialize(srl.serialize(TestSerializer.test_dict)))

    def test_msgpack(self):
        srl = SerializerFactory.get(SerializerType.MSGPACK)
        self.assertEqual(TestSerializer.test_dict, srl.deserialize(srl.serialize(TestSerializer.test_dict)))

if __name__ == "__main__":
    unittest.main()
