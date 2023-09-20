import subprocess
def push_repository(repo_name_create, org_name_migrate, clone_directory):
    print(f"Repository  '{repo_name_create}'")
    repo_path = f"{clone_directory}/{repo_name_create}"

    # Remove the old 'origin' remote and add a new 'origin' remote
    subprocess.run(['git', 'remote', 'remove', 'origin'], cwd=repo_path, check=True)
    subprocess.run(['git', 'remote', 'add', 'origin', f'git@github.com:{org_name_migrate}/{repo_name_create}.git'], cwd=repo_path, check=True)

    # Add lines to config file
    config_file_path = f"{clone_directory}/{repo_name_create}/config"

    # Define the lines to insert
    lines_to_insert = [
        '\tpush = +refs/heads/*:refs/heads/*',
        '\tpush = +refs/tags/*:refs/tags/*',
        '\tpush = +refs/change/*:refs/change/*',
    ]

    # Read the existing config file
    with open(config_file_path, 'r') as file:
        config_lines = file.readlines()

    # Find the index where to insert the lines
    insert_index = 0
    for i, line in enumerate(config_lines):
        if line.strip() == '[remote "origin"]':
            insert_index = i + 1
            break

    # Insert the lines
    config_lines[insert_index:insert_index] = [f"{line}\n" for line in lines_to_insert]

    # Write the updated config file
    with open(config_file_path, 'w') as file:
        file.writelines(config_lines)

    # Git push
    try:
        # Push with --mirror to push all refs, including tags and branches
        subprocess.run(['git', 'push', '--mirror', 'origin'], cwd=repo_path, check=True)
        print("Added a new remote and pushed with --mirror successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error adding a new remote and pushing with --mirror: {e}")
        return False