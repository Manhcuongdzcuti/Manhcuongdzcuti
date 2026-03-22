import asyncio
import aiohttp
import argparse
import time
from typing import Optional

class LoadTester:
    def __init__(self, url: str, concurrency: int, total_requests: Optional[int] = None, duration: Optional[int] = None):
        self.url = url
        self.concurrency = concurrency
        self.total_requests = total_requests
        self.duration = duration
        self.requests_sent = 0
        self.requests_succeeded = 0
        self.requests_failed = 0
        self.start_time = None
        
    async def send_request(self, session: aiohttp.ClientSession):
        try:
            async with session.get(self.url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                status = response.status
                if 200 <= status < 400:
                    self.requests_succeeded += 1
                else:
                    self.requests_failed += 1
        except Exception:
            self.requests_failed += 1
        finally:
            self.requests_sent += 1
    
    async def worker(self, session: aiohttp.ClientSession, stop_event: asyncio.Event):
        while not stop_event.is_set():
            await self.send_request(session)
            if self.total_requests and self.requests_sent >= self.total_requests:
                stop_event.set()
                break
    
    async def run(self):
        self.start_time = time.time()
        stop_event = asyncio.Event()
        
        connector = aiohttp.TCPConnector(limit=self.concurrency, limit_per_host=self.concurrency)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [asyncio.create_task(self.worker(session, stop_event)) for _ in range(self.concurrency)]
            
            if self.duration:
                await asyncio.sleep(self.duration)
                stop_event.set()
            
            await asyncio.gather(*tasks, return_exceptions=True)
        
        elapsed = time.time() - self.start_time
        print(f"\n--- Results ---")
        print(f"URL: {self.url}")
        print(f"Time: {elapsed:.2f} seconds")
        print(f"Requests sent: {self.requests_sent}")
        print(f"Succeeded: {self.requests_succeeded}")
        print(f"Failed: {self.requests_failed}")
        print(f"Requests/sec: {self.requests_sent / elapsed:.2f}")

def main():
    parser = argparse.ArgumentParser(description="HTTP Load Tester for authorized anti-DDoS testing")
    parser.add_argument("url", help="Target URL (only test your own servers)")
    parser.add_argument("-c", "--concurrency", type=int, default=100, help="Number of concurrent connections")
    parser.add_argument("-n", "--num-requests", type=int, help="Total number of requests to send")
    parser.add_argument("-t", "--duration", type=int, help="Duration in seconds to run the test")
    
    args = parser.parse_args()
    
    if not args.num_requests and not args.duration:
        parser.error("Specify either --num-requests or --duration")
    
    # Warning banner
    print("=" * 60)
    print("WARNING: Use this tool ONLY on systems you own or have explicit")
    print("written permission to test. Unauthorized testing is illegal.")
    print("=" * 60)
    confirm = input("Do you have authorization? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Exiting.")
        return
    
    tester = LoadTester(
        url=args.url,
        concurrency=args.concurrency,
        total_requests=args.num_requests,
        duration=args.duration
    )
    
    asyncio.run(tester.run())

if __name__ == "__main__":
    main()
