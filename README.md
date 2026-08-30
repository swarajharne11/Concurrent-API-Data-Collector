# Concurrent-API-Data-Collector
Build an application that retrieves data from multiple APIs, such as users, devices, vulnerabilities, applications, and locations, using concurrent execution.Handle timeouts, retries, API failures, partial results, rate limits, and logging. The application must return successful results even when some APIs fail
# Concurrent API Data Collector

A Python-based asynchronous application that collects data from multiple APIs concurrently while handling common real-world API problems such as timeouts, retries, failures, rate limits, logging, and partial results.

This project demonstrates how applications can continue working even when some external APIs fail.

## Features

* Concurrent API requests using `asyncio`
* Timeout handling
* Automatic retry mechanism
* API failure handling
* Rate-limit handling
* Logging for request status and errors
* Partial result support
* Summary of successful and failed API requests
* Simulated API responses for testing different scenarios

## APIs Simulated

The application simulates five different APIs:

* Users API
* Devices API
* Vulnerabilities API
* Applications API
* Locations API

Each API can be configured with one of the following behaviors:

| Behavior     | Description                                           |
| ------------ | ----------------------------------------------------- |
| `success`    | API responds successfully                             |
| `failure`    | API returns a simulated server error                  |
| `rate_limit` | API returns a simulated `429 Too Many Requests` error |
| `timeout`    | API takes longer than the allowed timeout             |

## Technologies Used

* Python 3
* `asyncio`
* `logging`
* `random`

No external Python packages are required.

## Project Structure

```text
concurrent-api-data-collector/
│
├── main.py
└── README.md
```

## How It Works

The application creates multiple API requests and executes them concurrently using Python's `asyncio`.

Instead of waiting for one API request to finish before starting another, all API requests are started almost at the same time.

For example:

```text
Users API
Devices API
Vulnerabilities API
Applications API
Locations API
```

are executed concurrently.

The concurrent execution is implemented using:

```python
results = await asyncio.gather(*tasks)
```

This improves performance when working with multiple independent network requests.

## Timeout Handling

Every API request has a maximum timeout of 3 seconds.

```python
result = await asyncio.wait_for(
    api_call(name, behavior),
    timeout=3
)
```

If an API takes longer than 3 seconds, the request is cancelled and the program returns:

```text
Request timeout
```

instead of waiting indefinitely.

## Retry Mechanism

Failed API requests are automatically retried.

```python
max_retries = 2
```

This means an API can be attempted a maximum of three times:

```text
Attempt 1
Attempt 2
Attempt 3
```

There is also a 1-second delay before retrying.

```python
await asyncio.sleep(1)
```

If all attempts fail, the API is marked as failed.

## Failure Handling

The project simulates server errors using:

```python
raise Exception("API returned 500 Internal Server Error")
```

Instead of crashing the entire application, the error is caught and returned as a failed result.

Example:

```text
Vulnerabilities
----------------------------------------
Status : FAILED
Error  : API returned 500 Internal Server Error
```

## Rate Limit Handling

APIs sometimes reject requests when too many requests are sent within a short period.

This is commonly represented by HTTP status code:

```text
429 Too Many Requests
```

The project simulates this situation using:

```python
raise Exception("429 Too Many Requests")
```

The request is retried according to the configured retry policy.

## Partial Results

One of the main goals of this project is fault tolerance.

If one or more APIs fail, successful API results are still returned.

For example:

```text
Users               SUCCESS
Devices             SUCCESS
Vulnerabilities     FAILED
Applications        FAILED
Locations           SUCCESS
```

The entire application does not fail just because one API is unavailable.

The final result becomes:

```text
Overall : PARTIAL SUCCESS
```

## Logging

Python's built-in `logging` module is used to monitor API execution.

Example logs:

```text
INFO: Users: Attempt 1
INFO: Devices: Attempt 1
INFO: Vulnerabilities: Attempt 1
INFO: Applications: Attempt 1
INFO: Locations: Attempt 1

INFO: Users: SUCCESS
INFO: Devices: SUCCESS

WARNING: Vulnerabilities: API returned 500 Internal Server Error
INFO: Vulnerabilities: Retrying...

WARNING: Applications: 429 Too Many Requests
INFO: Applications: Retrying...
```

Logging makes it easier to debug API problems and understand what the application is doing.

## Running the Project

Make sure Python 3 is installed.

Clone the repository:

```bash
git clone <your-repository-url>
```

Move into the project directory:

```bash
cd concurrent-api-data-collector
```

Run the program:

```bash
python main.py
```

On some systems you may need:

```bash
python3 main.py
```

## Example Output

```text
============================================================
CONCURRENT API DATA COLLECTOR
============================================================

Starting API collection...

============================================================
FINAL RESULTS
============================================================

Users
----------------------------------------
Status : SUCCESS
Data   :
         {'id': 1, 'name': 'Alice'}
         {'id': 2, 'name': 'Bob'}

Devices
----------------------------------------
Status : SUCCESS
Data   :
         {'id': 101, 'name': 'Laptop'}
         {'id': 102, 'name': 'Mobile'}

Vulnerabilities
----------------------------------------
Status : FAILED
Error  : API returned 500 Internal Server Error

Applications
----------------------------------------
Status : FAILED
Error  : 429 Too Many Requests

Locations
----------------------------------------
Status : SUCCESS
Data   :
         {'id': 301, 'city': 'Mumbai'}
         {'id': 302, 'city': 'Pune'}

============================================================
SUMMARY
============================================================

Total APIs : 5
Successful : 3
Failed     : 2
Overall    : PARTIAL SUCCESS
```

## Changing API Behavior

You can test different scenarios by modifying the `APIs` dictionary inside the `collect()` function.

Example:

```python
APIs = {
    "Users": "success",
    "Devices": "timeout",
    "Vulnerabilities": "failure",
    "Applications": "rate_limit",
    "Locations": "success"
}
```

To make every API successful:

```python
APIs = {
    "Users": "success",
    "Devices": "success",
    "Vulnerabilities": "success",
    "Applications": "success",
    "Locations": "success"
}
```

## Concepts Demonstrated

This project demonstrates several important backend engineering concepts:

* Asynchronous programming
* Concurrent execution
* Fault tolerance
* API integration
* Exception handling
* Timeout handling
* Retry strategies
* Rate-limit handling
* Logging and monitoring
* Partial failure handling
* Resilient system design

## Why Concurrent Execution?

Without concurrency, API requests would run sequentially:

```text
API 1 → wait → API 2 → wait → API 3 → wait → API 4 → wait
```

If five APIs each take approximately one second, the total execution time could be around five seconds.

With concurrent execution:

```text
API 1 ─────┐
API 2 ─────┤
API 3 ─────┤ → Execute together
API 4 ─────┤
API 5 ─────┘
```

The total execution time is closer to the time taken by the slowest request rather than the sum of all request times.

## Future Improvements

The project can be extended by adding:

* Real REST API integration using `aiohttp` or `httpx`
* Exponential backoff for retries
* Special handling for HTTP status codes
* `Retry-After` support for rate limits
* JSON configuration files
* Environment variables
* API authentication
* Structured JSON logging
* Database storage
* Metrics and monitoring
* Unit testing
* Docker support
* FastAPI REST endpoint
* Circuit breaker pattern

## Real-World Use Cases

A similar architecture can be used in applications that collect information from multiple services such as:

* Cybersecurity dashboards
* Device management platforms
* Monitoring systems
* Cloud management applications
* SaaS dashboards
* Financial data aggregators
* E-commerce systems
* Microservice architectures

## Learning Objective

The main objective of this project is to understand how reliable backend applications communicate with multiple external services without allowing the failure of one service to crash the entire application.

It demonstrates an important principle of distributed systems:

> A failure in one external service should not necessarily cause the entire application to fail.

## Author

Built as a Python backend project to demonstrate asynchronous programming, concurrent API requests, retries, timeout handling, rate-limit handling, logging, and fault-tolerant application design.
