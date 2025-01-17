# Definition
An I/O Identity is a unique identifier for the I/O behavior of an application. It encompasses all of the information required to understand how an application does I/O, but aims to also be user-readable. Any I/O Identity can also represent the centroid of an I/O Behavior Class. It follows a schema which we define here.
## Schema
`
{
    "read_data_percent": {
        "dependencies": [],
        "include": "",
        "guard": "True",
        "expr": "self.output['read_data_percent']['val'] = self.input['total_bytes_read']['val'] / (self.input['total_bytes_read']['val'] + self.input['total_bytes_written']['val'])",
        "val": 0
    },
    "write_data_percent": {
        "dependencies": [],
        "include": "",
        "guard": "True",
        "expr": "self.output['write_data_percent']['val'] = self.input['total_bytes_written']['val'] / (self.input['total_bytes_read']['val'] + self.input['total_bytes_written']['val'])",
        "val": 0},
    "read_time_percent": {
        "dependencies": [],
        "include": "",
        "guard": "True",
        "expr": "self.output['read_time_percent']['val'] = self.input['read_time']['val'] / (self.input['read_time']['val'] + self.input['write_time']['val'])",
        "val": 0},
    "write_time_percent": {
        "dependencies": [],
        "include": "",
        "guard": "True",
        "expr": "self.output['write_time_percent']['val'] = self.input['write_time']['val'] / (self.input['read_time']['val'] + self.input['write_time']['val'])",
        "val": 0},
    "read_op_percent": {
        "dependencies": [],
        "include": "",
        "guard": "True",
        "expr": "self.output['read_op_percent']['val'] = self.input['total_reads']['val'] / (self.input['total_reads']['val'] + self.input['total_writes']['val'])",
        "val": 0},
    "write_op_percent": {
        "dependencies": [],
        "include": "",
        "guard": "True",
        "expr": "self.output['write_op_percent']['val'] = self.input['total_writes']['val'] / (self.input['total_reads']['val'] + self.input['total_writes']['val'])",
        "val": 0},
    "read_seq_percent": {
        "dependencies": [],
        "include": "",
        "guard": "self.input['total_reads']['val'] > 0",
        "expr": "self.output['read_seq_percent']['val'] = self.input['total_consec_reads']['val'] / self.input['total_reads']['val']",
        "val": 0},
    "write_seq_percent": {
        "dependencies": [],
        "include": "",
        "guard": "self.input['total_writes']['val'] > 0",
        "expr": "self.output['write_seq_percent']['val'] = self.input['total_consec_writes']['val'] / self.input['total_writes']['val']",
        "val": 0},
    "read_bw_long": {
        "dependencies": [],
        "include": "",
        "guard": "self.input['max_read_time']['val'] > 0",
        "expr": "self.output['read_bw_long']['val'] = self.input['max_read_time_size']['val'] / self.input['max_read_time']['val']",
        "val": 0},
    "write_bw_long": {
        "dependencies": [],
        "include": "",
        "guard": "self.input['max_write_time']['val'] > 0",
        "expr": "self.output['write_bw_long']['val'] = self.input['max_write_time_size']['val'] / self.input['max_write_time']['val']",
        "val": 0},
    "read_bw": {
        "dependencies": [],
        "include": "",
        "guard": "self.input['read_time']['val'] > 0",
        "expr": "self.output['read_bw']['val'] = self.input['total_bytes_read']['val'] / self.input['read_time']['val']",
        "val": 0},
    "write_bw": {
        "dependencies": [],
        "include": "",
        "guard": "self.input['write_time']['val'] > 0",
        "expr": "self.output['write_bw']['val'] = self.input['total_bytes_written']['val'] / self.input['write_time']['val']",
        "val": 0}
}
`
