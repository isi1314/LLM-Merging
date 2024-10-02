import yaml

# Load the YAML file
with open('environment.yml') as file:
    env = yaml.safe_load(file)

# Start writing pyproject.toml for Poetry
with open('pyproject.toml', 'w') as file:
    file.write('[tool.poetry]\n')
    file.write(f'name = "{env.get("name", "myenv")}"\n')
    file.write('version = "0.1.0"\n')
    file.write('description = ""\n')
    file.write('authors = ["Your Name <email@example.com>"]\n\n')

    file.write('[tool.poetry.dependencies]\n')

    # Write the python version
    for dep in env['dependencies']:
        if isinstance(dep, str) and dep.startswith('python'):
            python_version = dep.split('=')[1]
            file.write(f'python = "^{python_version}"\n')
    
    # Write the package dependencies
    for dep in env['dependencies']:
        if isinstance(dep, str) and not dep.startswith('python'):
            name, _, version = dep.partition('=')  # Use partition to split at the first '='
            if version:
                file.write(f'{name} = "{version}"\n')
            else:
                file.write(f'{name} = "*"\n')

        elif isinstance(dep, dict) and 'pip' in dep:
            for pip_dep in dep['pip']:
                file.write(f'{pip_dep} = "*"\n')

    file.write('\n[build-system]\n')
    file.write('requires = ["poetry-core>=1.0.0"]\n')
    file.write('build-backend = "poetry.core.masonry.api"\n')
