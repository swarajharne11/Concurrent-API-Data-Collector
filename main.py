import asyncio
import random

API_DATA = {
    "users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}],
    "devices": [{"id": 101, "name": "Laptop"}, {"id": 102, "name": "Mobile"}],
    "vulnerabilities": [{"id": "V001", "severity": "High"}, {"id": "V002", "severity": "Medium"}],
    "applications": [{"id": 201, "name": "Chrome"}, {"id": 202, "name": "VS Code"}],
    "locations": [{"id": 301, "city": "Mumbai"}, {"id": 302, "city": "Pune"}],
}

ERRORS = {
    "failure": "API returned 500 Internal Server Error",
    "rate_limit": "429 Too Many Requests",
}


async def api_call(name, behavior):
    await asyncio.sleep(5 if behavior == "timeout" else random.uniform(0.5, 1.5))

    if behavior == "success":
        return {"status": "success", "data": API_DATA[name.lower()]}
    if behavior in ERRORS:
        raise Exception(ERRORS[behavior])
    return None


async def get_data(name, behavior, max_retries=2):
    for attempt in range(max_retries + 1):
        try:
            result = await asyncio.wait_for(api_call(name, behavior), timeout=3)
            return result

        except asyncio.TimeoutError:
            return {"status": "failed", "error": "Request timeout"}

        except Exception as e:
            if attempt < max_retries:
                await asyncio.sleep(1)
            else:
                return {"status": "failed", "error": str(e)}


async def collect():
    apis = {
        "Users": "success",
        "Devices": "success",
        "Vulnerabilities": "failure",
        "Applications": "rate_limit",
        "Locations": "success",
    }

    print("\n" + "=" * 60)
    print("CONCURRENT API DATA COLLECTOR")
    print("=" * 60)
    print("\nStarting API collection...\n")

    results = await asyncio.gather(*(get_data(name, behavior) for name, behavior in apis.items()))

    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)

    successful = sum(r["status"] == "success" for r in results)
    failed = len(results) - successful

    for name, result in zip(apis, results):
        print(f"\n{name}")
        print("-" * 40)
        if result["status"] == "success":
            print("Status : SUCCESS")
            print("Data   :")
            for item in result["data"]:
                print(f"         {item}")
        else:
            print("Status : FAILED")
            print(f"Error  : {result['error']}")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total APIs : {len(apis)}")
    print(f"Successful : {successful}")
    print(f"Failed     : {failed}")

    if successful and failed:
        print("Overall    : PARTIAL SUCCESS")
    elif successful == len(apis):
        print("Overall    : SUCCESS")
    else:
        print("Overall    : FAILED")


if __name__ == "__main__":
    asyncio.run(collect())
