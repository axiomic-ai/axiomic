
import axiomic
import axiomic.core.checks as checks

class EnforceJsonSchema:
    def __init__(self, schema):
        self.schema = schema
        self.checked_schema = axiomic.Text(self.schema).check(checks.CheckJsonSyntax())

    def infer(self, json_str):
        w = axiomic.Text(json_str)
        return w.checkpoint(checks.CheckJsonSyntax()).check(self.checked_schema)
    