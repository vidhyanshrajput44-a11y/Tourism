import requests

def run_test():
    print("--- UI 8 Heritage Rewards Test ---")
    progress = requests.get("http://127.0.0.1:8000/rewards/progress-overview/test_user").json()
    
    print("\nGlobal Progress:")
    print(f"Total Monuments: {progress['global_progress']['total_monuments']}")
    print(f"Captured: {progress['global_progress']['captured_monuments']}")
    
    print("\nPer-Destination Monument Check:")
    for dest in progress['destinations']:
        dest_id = dest['destination_id']
        print(f"\n--- {dest_id} ---")
        monuments = requests.get(f"http://127.0.0.1:8000/rewards/monuments/{dest_id}").json()
        for m in monuments:
            print(f"- {m['name']} ({m['points_value']} pts): {m['description']}")

if __name__ == '__main__':
    run_test()
