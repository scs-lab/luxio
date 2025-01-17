# Definition
An SSLO or Storage Service Level Objectives is a structure to capture the behavior of a storage service under various types of workloads. It follows a schema which we define here.
## Schema
{
    "read_heavy": {
        "dependencies": [],
        "include": "variables, weights = ['read_data_percent', 'read_time_percent', 'read_op_percent', 'read_seq_percent', 'read_bw_long', 'read_bw'], [0.3, 0.4, 0.25, 0.05, 0, 0]",
        "guard": "True",
        "expr": "self.output['read_heavy']['val'] = sum([self.input[var]['val']*weight for (var, weight, self) in zip(variables, weights, [self]*len(variables))])",
        "val": 0
    },
    "write_heavy": {
        "dependencies": [],
        "include": "variables, weights = ['write_data_percent', 'write_time_percent', 'write_op_percent', 'write_seq_percent', 'write_bw_long', 'write_bw'], [0.3, 0.4, 0.25, 0.05, 0, 0]",
        "guard": "True",
        "expr": "self.output['write_heavy']['val'] = sum([self.input[var]['val']*weight for (var, weight, self) in zip(variables, weights, [self]*len(variables))])",
        "val": 0
    }
}
