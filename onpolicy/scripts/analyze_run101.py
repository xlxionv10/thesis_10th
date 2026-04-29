import os
import glob
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

LOG_DIR = "/Users/nhi/Desktop/on-policy-1/onpolicy/scripts/results/BOSCH/mappo/check/run101/logs"

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

def print_metric_group(name, tags):
    print(f"\n--- {name} ---")
    print(f"{'Metric':<35} | {'Value':<15} | {'Step':<10}")
    print("-" * 65)
    for tag in tags:
        result = get_latest_metric(LOG_DIR, tag)
        if result:
            val, step = result
            print(f"{tag:<35} | {val:<15.4f} | {step:<10}")
        else:
            print(f"{tag:<35} | {'Not found':<15}")

print_metric_group("Utilization per Line", [f"util_line_{i}" for i in range(6)])
print_metric_group("Queue Avg per Line", [f"queue_avg_line_{i}" for i in range(6)])
print_metric_group("Setup Cost per Line", [f"setup_cost_line_{i}" for i in range(6)])
print_metric_group("Prod Cost per Line", [f"prod_cost_line_{i}" for i in range(6)])
print_metric_group("Horizon per Line", [f"horizon_line_{i}" for i in range(6)])
print_metric_group("Backlog per Product", [f"backlog_prod_{i}" for i in range(8)])
print_metric_group("Inventory per Product", [f"inventory_prod_{i}" for i in range(8)])
print_metric_group("Assigned Lines per Product", [
    "assigned_lines_prod_067",
    "assigned_lines_prod_072",
    "assigned_lines_prod_083",
    "assigned_lines_prod_089",
    "assigned_lines_prod_094",
    "assigned_lines_prod_097",
    "assigned_lines_prod_100",
    "assigned_lines_prod_111",
])
print_metric_group("Agent Rewards", [f"agent{i}_episode_reward_agent{i}" for i in range(7)])
print_metric_group("Global Metrics", [
    "period_utilization",
    "period_backlog_qty",
    "period_inv_qty",
    "period_setup_cost",
    "period_queue_avg",
    "period_prod_cost",
    "period_pm_cost",
    "period_cm_cost",
    "period_manager_horizon_mean",
])
