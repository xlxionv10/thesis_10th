import os
import glob
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

def get_latest_metric(log_dir, tag):
    tag_dir = os.path.join(log_dir, tag)
    if not os.path.exists(tag_dir):
        subdirs = [d for d in os.listdir(log_dir) if os.path.isdir(os.path.join(log_dir, d)) and tag in d]
        if not subdirs:
            return None
        tag_dir = os.path.join(log_dir, subdirs[0])
    
    event_files = glob.glob(os.path.join(tag_dir, "events.out.tfevents.*"))
    if not event_files:
        return None
    
    latest_event_file = max(event_files, key=os.path.getmtime)
    
    ea = EventAccumulator(latest_event_file)
    ea.Reload()
    
    tags = ea.Tags()['scalars']
    if not tags:
        return None
    
    scalar_tag = tags[0]
    events = ea.Scalars(scalar_tag)
    if not events:
        return None
    
    latest_event = events[-1]
    return latest_event.value, latest_event.step

log_dir = "/Users/nhi/Desktop/on-policy-1/onpolicy/scripts/results/BOSCH/mappo/check/run99/logs"

def print_metric_group(name, tags):
    print(f"\n--- {name} ---")
    print(f"{'Metric':<30} | {'Value':<15}")
    print("-" * 50)
    for tag in tags:
        result = get_latest_metric(log_dir, tag)
        if result:
            val, step = result
            print(f"{tag:<30} | {val:<15.4f}")
        else:
            print(f"{tag:<30} | {'Not found':<15}")

# 1. Per-Line Utilization
print_metric_group("Utilization per Line", [f"util_line_{i}" for i in range(6)])

# 2. Per-Product Backlog
print_metric_group("Backlog per Product", [f"backlog_prod_{i}" for i in range(8)])

# 3. Per-Product Inventory
print_metric_group("Inventory per Product", [f"inventory_prod_{i}" for i in range(8)])

# 4. Per-Line Horizon
print_metric_group("Horizon per Line", [f"horizon_line_{i}" for i in range(6)])

# 5. Global Metrics
print_metric_group("Global Metrics", ["period_utilization", "period_backlog_qty", "period_inv_qty", "period_setup_cost", "period_queue_avg"])
