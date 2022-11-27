class PropertyReference:
    def __init__(self, namespace: list[str], key: str, version: str) -> None:
        self.namespace = namespace
        self.key = key
        self.version = version

    def get_namespace(self) -> list[str]:
        return self.namespace

    def get_key(self) -> str:
        return self.key

    def get_version(self) -> str:
        return self.version


class PropertyValue:
    def __init__(self, value: object, rule: str, segment: dict[str, object], id: str = None) -> None:
        self.id = id
        self.value = value
        self.rule = rule
        self.segment = segment

    def get_id(self) -> str:
        return self.id

    def get_value(self) -> object:
        return self.value

    def get_segment(self) -> dict[str,  object]:
        return self.segment

    def get_rule(self) -> str:
        return self.rule


class PropertyReferenceValuePair:
    def __init__(self, property_reference: PropertyReference, property_value: PropertyValue) -> None:
        self.property_reference = property_reference
        self.property_value = property_value

    def get_property_reference(self) -> PropertyReference:
        return self.property_reference

    def get_property_value(self) -> PropertyValue:
        return self.property_value


class PropertyReferenceValuePairs:
    def __init__(self) -> None:
        self.pairs = []

    def add(self, property_reference_value_pair: PropertyReferenceValuePair):
        self.pairs.append(property_reference_value_pair)

    def get(self) -> list[PropertyReferenceValuePair]:
        return self.pairs


class ReadPropertyRequest:
    def __init__(self, property_reference: PropertyReference, params: dict[str, object]) -> None:
        self.property_reference = property_reference
        self.params = params

    def get_property_reference(self):
        return self.property_reference

    def get_params(self):
        return self.params


class ReadPropertyRequests:
    def __init__(self) -> None:
        self.read_property_requests = []

    def add(self, read_property_request: ReadPropertyRequest):
        self.read_property_requests.append(read_property_request)

    def get(self) -> list[ReadPropertyRequest]:
        return self.read_property_requests


class ExecutionResult:
    def __init__(self, success: bool, property_value: PropertyValue) -> None:
        self.success = success
        self.property_value = property_value

    def is_successful(self) -> bool:
        return self.success

    def get_property_value(self) -> PropertyValue:
        return self.property_value


class ExecutionResults:
    def __init__(self) -> None:
        self.results = []

    def add(self, execution_result: ExecutionResult):
        self.results.append(execution_result)

    def get(self) -> list[ExecutionResult]:
        return self.results

    @staticmethod
    def __from_json(response_json) -> ExecutionResults:
        execution_results = ExecutionResults()

        execution_responses = response_json["responses"]

        for execution_response in execution_responses:
            success = False
            value_id = None
            value_rule = None
            value_segment = None
            value_data = None

            if "success" in execution_response:
                success = execution_response["success"]

            if "value" in execution_response:
                value_response = execution_response["value"]

                if "id" in value_response:
                    value_id = value_response["id"]

                if "rule" in value_response:
                    rule_response = value_response["rule"]
                    if "expression" in rule_response:
                        value_rule = rule_response["expression"]

                if "data" in value_response:
                    value_data = value_response["data"]

                if "segment" in value_response:
                    segment_response = value_response["segment"]
                    if "path" in segment_response:
                        segment_path = segment_response["path"]
                        value_segment = {}
                        for segment_path_component in segment_path:
                            if "name" in segment_path_component and "value" in segment_path_component:
                                value_segment[segment_path_component["name"]
                                              ] = segment_path_component["value"]

            value = PropertyValue(value_data, value_rule,
                                  value_segment, value_id)

            execution_results.add(ExecutionResult(success, value))

        return execution_results
