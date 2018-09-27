# Design

* [CLI](#cli)
* [Web App](#webapp)

### CLI

The TestConfig class will hold the configurations for the tests and benchmarks. These will be executed separately. The tests will be ran in parallel while the benchmarks will be ran in serial. To achieve this parallelism, the multiprocessing library will be used.

![Sequence Diagram](./imgs/cli_sequence.png)

### Web App
TODO
