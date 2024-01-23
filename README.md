# Benchmarks

This repository contains the code required to reproduce the benchmarks presented in Section IV.A. of the [qibolab paper](https://arxiv.org/abs/2308.06313).

## Required libraries

Executing the benchmarks on instruments requires installing the [qibolab](https://qibo.science/qibolab/stable/getting-started/installation.html)
and [qibocal](https://qibo.science/qibocal/stable/getting-started/installation.html) libraries, as well as instrument specific dependencies.

The following versions were used to perform the benchmarks presented in the paper:

Library | Version
-- | --
`qibolab` | 0.1.0
`qibocal` | 0.0.3
`qblox-instruments` | 0.9.0
`qm-qua` | 1.1.1
`laboneq` | 2.7.0
`qick` | 0.2.135
`qibosoq` | 0.0.3

Different versions of these libraries may not support the platforms and runcards provided here.

## Setup

The `platforms` directory provides the platform runcards for the different instruments provided, particularly:
* zurich for Zurich instruments,
* qm for Quantum Machines,
* qblox for Qblox instruments,
* rfsoc for the RFSoC 4x2 controlled using QICK.

Using these platforms in a self-hosted lab that has access to any of these instruments may require changing some of the setup parameters, such as instrument IP addresses.

The `runcards` directory provides the qibocal runcards for executing the calibration routines that were benchmarked.

Before executing any routines or programs, qibolab should be configured to read the platform runcards from the correct directory.
This can be done by setting the following environment variable:
```sh
export QIBOLAB_PLATFORMS=./platforms
```
If this is run from a different location than this README, the directory should be modified accordingly.

## Execution

Benchmarks can be executed using the `qq` command provided by qibocal, for example:
```sh
qq auto runcards/routines_benchmarks.yml --no-update
```
will execute the benchmarks presented in Fig. 6 of the paper.

Note that running the benchmark on different instruments requires changing the `platform` key in the qibocal runcards to the corresponding platform name.

## Data

Succesful execution of the `qq` command will create a new folder in the current directory.
Note that the name of this folder can be controlled with the `-o` option in `qq`.

This folder contains the data acquired for each executed routine as well as a `meta.json` file
with metadata related to the execution. Acquisition, fit and total runtimes for each executed
routine can be found in `meta.json`.
