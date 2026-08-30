import asyncio
import logging
import random

# LOGGING

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


# API DATA


API_DATA = {
    "users": {
        "data": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
        ]
    },

    "devices": {
        "data": [
            {"id": 101, "name": "Laptop"},
            {"id": 102, "name": "Mobile"},
        ]
    },

    "vulnerabilities": {
        "data": [
            {"id": "V001", "severity": "High"},
            {"id": "V002", "severity": "Medium"},
        ]
    },

    "applications": {
        "data": [
            {"id": 201, "name": "Chrome"},
            {"id": 202, "name": "VS Code"},
        ]
    },

    "locations": {
        "data": [
            {"id": 301, "city": "Mumbai"},
            {"id": 302, "city": "Pune"},
        ]
    },
}


# FAKE API

async def api_call(name, behavior):

    logging.info(f"{name}: Request started")

    # Simulate network delay
    if behavior == "timeout":
        await asyncio.sleep(5)
    else:
        await asyncio.sleep(random.uniform(0.5, 1.5))

    # ---------------- SUCCESS ----------------

    if behavior == "success":

        return {
            "status": "success",
            "data": API_DATA[name.lower()]["data"]
        }

    # ---------------- FAILURE ----------------

    if behavior == "failure":

        raise Exception("API returned 500 Internal Server Error")

    # ---------------- RATE LIMIT ----------------

    if behavior == "rate_limit":

        raise Exception("429 Too Many Requests")

    return None


# API REQUEST WITH TIMEOUT + RETRY

async def get_data(name, behavior):

    max_retries = 2

    for attempt in range(max_retries + 1):

        try:

            logging.info(
                f"{name}: Attempt {attempt + 1}"
            )

            # TIMEOUT HANDLING

            result = await asyncio.wait_for(
                api_call(name, behavior),
                timeout=3
            )

            logging.info(
                f"{name}: SUCCESS"
            )

            return result

        except asyncio.TimeoutError:

            logging.error(
                f"{name}: TIMEOUT after 3 seconds"
            )

            return {
                "status": "failed",
                "error": "Request timeout"
            }

        except Exception as e:

            logging.warning(
                f"{name}: {e}"
            )


            # RETRY HANDLING

            if attempt < max_retries:

                logging.info(
                    f"{name}: Retrying..."
                )

                await asyncio.sleep(1)

            else:

                logging.error(
                    f"{name}: FAILED after retries"
                )

                return {
                    "status": "failed",
                    "error": str(e)
                }


# CONCURRENT API COLLECTOR

async def collect():

    # Each API has a behavior.
    #
    # success     → API works normally
    # failure     → API returns an error
    # rate_limit  → API returns 429
    # timeout     → API takes too long

    APIs = {
        "Users": "success",
        "Devices": "success",
        "Vulnerabilities": "failure",
        "Applications": "rate_limit",
        "Locations": "success"
    }

    print("\n")
    print("=" * 60)
    print("CONCURRENT API DATA COLLECTOR")
    print("=" * 60)

    print("\nStarting API collection...\n")

    # CONCURRENT EXECUTION

    tasks = [
        get_data(name, behavior)
        for name, behavior in APIs.items()
    ]

    # All APIs execute concurrently
    results = await asyncio.gather(*tasks)

    # DISPLAY RESULTS

    print("\n")
    print("=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)

    successful = 0
    failed = 0

    for name, result in zip(APIs.keys(), results):

        print(f"\n{name}")
        print("-" * 40)

        if result["status"] == "success":

            print("Status : SUCCESS")
            print("Data   :")

            for item in result["data"]:
                print(f"         {item}")

            successful += 1

        else:

            print("Status : FAILED")
            print(f"Error  : {result['error']}")

            failed += 1

    # PARTIAL RESULTS

    print("\n")
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    print(f"Total APIs : {len(APIs)}")
    print(f"Successful : {successful}")
    print(f"Failed     : {failed}")

    if successful > 0 and failed > 0:

        print("Overall    : PARTIAL SUCCESS")

    elif successful == len(APIs):

        print("Overall    : SUCCESS")

    else:

        print("Overall    : FAILED")


# START PROGRAM

if __name__ == "__main__":

    asyncio.run(collect())
