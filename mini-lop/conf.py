import toml
import os
import shutil


def parse_config(config_file, overwrite_output=True):
    with open(config_file) as f:
        conf_dict = toml.load(f)

        for key in ['seeds_folder', 'output_folder', 'target', 'target_args']:
            if key not in conf_dict:
                print(f'Error: {key} is missing in the config file')
                return False, conf_dict

        if not os.path.exists(conf_dict['seeds_folder']):
            print("Seeds folder does not exist")
            return False, conf_dict

        if len(os.listdir(conf_dict['seeds_folder'])) == 0:
            print("Seeds folder is empty")
            return False, conf_dict

        if not os.path.exists(conf_dict['target']):
            print("Target does not exist")
            return False, conf_dict

        conf_dict['queue_folder'] = os.path.join(conf_dict['output_folder'], 'queue')
        conf_dict['crashes_folder'] = os.path.join(conf_dict['output_folder'], 'crashes')

        if overwrite_output and os.path.exists(conf_dict['output_folder']):
            print("Output folder already exists, overwriting it")
            shutil.rmtree(conf_dict['output_folder'])

        if not os.path.exists(conf_dict['output_folder']):
            print("Output folder does not exist, creating it")
            # queue folder is created during the dry run
            os.makedirs(conf_dict['output_folder'])
            os.makedirs(conf_dict['crashes_folder'])

        conf_dict['current_input'] = os.path.join(conf_dict['output_folder'], '.cur_input')
        shutil.copyfile(os.path.join(conf_dict['seeds_folder'], os.listdir(conf_dict['seeds_folder'])[0]),
                        conf_dict['current_input'])
        conf_dict['raw_target_args'] = conf_dict['target_args']
        conf_dict['target_args'] = [conf_dict['current_input'] if x == '@@' else x for x in conf_dict['target_args']]

        return True, conf_dict
