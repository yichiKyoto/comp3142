import argparse
import os
import subprocess
from conf import *


def sorted_directory_listing_by_creation_time_with_os_listdir(directory):
    def get_creation_time(item):
        item_path = os.path.join(directory, item)
        return os.path.getctime(item_path)

    items = os.listdir(directory)
    sorted_items = sorted(items, key=get_creation_time)
    return sorted_items

def main():

    print("====== Welcome to use Mini-Lop's Seed Inspector ======")

    parser = argparse.ArgumentParser(description='the seed inspector utility for Mini-Lop')

    parser.add_argument('--config', '-c', required=True, help='Path to config file', type=str)

    args = parser.parse_args()

    config_path = os.path.abspath(args.config)

    config_valid, conf = parse_config(config_path, overwrite_output=False)

    if not config_valid:
        print("Config file is not valid")
        return

    afl_showmap_path = '/usr/local/bin/afl-showmap'

    if not os.path.exists(afl_showmap_path):
        print("afl-showmap not found, please make sure AFL is installed")
        return

    all_edges = set()

    # keep track of the initial seeds
    initial_seeds = set()

    # get the edge coverage of the initial seeds
    for seed in os.listdir(conf['seeds_folder']):
        initial_seeds.add(seed)
        seed_path = os.path.join(conf['seeds_folder'], seed)
        args = [seed_path if x == '@@' else x for x in conf['raw_target_args']]
        output_path = f'/tmp/{seed}.txt'
        showmap_args = [afl_showmap_path, '-m', 'none', '-o', output_path, conf["target"]] + args
        os.system(' '.join(showmap_args) + ' > /dev/null 2>&1')
        with open(output_path) as f:
            for line in f:
                edge = int(line.strip().split(':')[0])
                all_edges.add(edge)

    print(f'Initial seeds cover {len(all_edges)} edges')

    # get the edge coverage of the initial seeds

    for seed in sorted_directory_listing_by_creation_time_with_os_listdir(conf['queue_folder']):
        if seed not in initial_seeds:
            seed_path = os.path.join(conf['queue_folder'], seed)
            args = [seed_path if x == '@@' else x for x in conf['raw_target_args']]
            output_path = f'/tmp/{seed}.txt'
            showmap_args = [afl_showmap_path, '-m', 'none', '-o', output_path, conf["target"]] + args
            os.system(' '.join(showmap_args) + ' > /dev/null 2>&1')
            edges_before = len(all_edges)
            with open(output_path) as f:
                for line in f:
                    edge = int(line.strip().split(':')[0])
                    all_edges.add(edge)
            edges_after = len(all_edges)
            print(f'Seed: {seed_path} covers {edges_after - edges_before} new edges')


if __name__ == '__main__':
    main()

