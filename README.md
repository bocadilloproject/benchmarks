# Benchmarks

This repo provides a benchmark for various Python web frameworks against [Bocadillo].

## Disclaimer

A few things to keep in mind:

- This benchmark was created to get a sense for how Bocadillo compares in terms of performance. Ideally, you should run this on your machine, compare with other benchmarks, or — even better — do your own benchmark.
- Benchmarking is hard, because frameworks all have special ways in which they can be tweaked to optimize their performance. We're trying our best to configure all frameworks correctly, but it cannot be perfect. Consider [opening an issue](https://github.com/bocadilloproject/benchmarks/issues/new) if you want to help.
- There are many more aspects to consider outside performance when choosing a framework: ease of use, community, documentation, features, etc.
- Async frameworks naturally do better in high-concurrency settings. We have included both low, medium and high concurrency in this benchmark to give every framework a chance to shine.

## Running the benchmark

1. Install [Docker]
2. Clone the repo
3. Build the image: `docker build . -t bocadillo-benchmarks`
4. Run the container: `docker run bocadillo-benchmarks`

The benchmark can be configured via `config.json`.

## Results

> TODO

[Docker]: https://docs.docker.com/install/
[Bocadillo]: https://github.com/bocadilloproject/bocadillo
