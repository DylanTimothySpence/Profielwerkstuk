import asyncio
import time

async def test_task(n):
    """Simuleert een asynchrone taak met een vertraging."""
    print(f"Task {n} started")
    await asyncio.sleep(60)  # Simuleert een vertraging van x seconden
    print(f"Task {n} finished")

async def stress_test(max_tasks):
    """Voert een stress-test uit door taken te starten."""
    tasks = []
    start_time = time.time()

    for n in range(1, max_tasks + 1):
        task = asyncio.create_task(test_task(n))
        tasks.append(task)

        # Print aantal actieve taken
        if n % 100 == 0 or n == max_tasks:
            print(f"{n} tasks started...")

    await asyncio.gather(*tasks)  # Wacht tot alle taken klaar zijn
    end_time = time.time()
    print(f"Completed {max_tasks} tasks in {end_time - start_time:.2f} seconds.")

# Voer de test uit
asyncio.run(stress_test(1000))  # Pas het getal hier aan om meer taken te proberen
