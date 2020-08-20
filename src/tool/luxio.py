from io_requirement_extractor.io_requirement_extractor import IORequirementExtractor
from storage_configurator.storage_configurator_factory import *
from storage_requirement_builder.storage_requirement_builder import *
from external_clients.json_client import *

class LUXIO:
    def __init__(self):
        pass

    def _initialize(self) -> None:
        pass

    def run(self) -> dict:
        self._initialize()
        # run io requirement extractor
        extractor = IORequirementExtractor()
        io_requirement = extractor.run()
        JSONClient().dumps(io_requirement)
        #
        builder = StorageRequirementBuilder()
        storage_requirement = builder.run(io_requirement)
        JSONClient().dumps(storage_requirement)
        #
        conf = ConfigurationManager.get_instance()
        configurator = StorageConfiguratorFactory.get(conf.storage_configurator_type)
        configuration = configurator.run(storage_requirement)
        self._finalize()
        return configuration

    def _finalize(self) -> None:
        pass


if __name__ == '__main__':
    """
    The main method to start the benchmark runtime.
    """
    tool = LUXIO()
    tool.run()
    exit(0)