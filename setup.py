#!/usr/bin/env python3
import os
from setuptools import setup

# Skill info
SKILL_AUTHOR = "mmalpartida"
SKILL_NAME = "chicken-assistant"
SKILL_PKG = "chicken_assistant_skill"
SKILL_CLAZZ = "ChickenAssistant"

# Plugin entry point for OVOS
PLUGIN_ENTRY_POINT = f"{SKILL_NAME}.{SKILL_AUTHOR}={SKILL_PKG}:{SKILL_CLAZZ}"

# Get version from version.py
def get_version():
    """Read version from version.py"""
    version_file = os.path.join(os.path.dirname(__file__), 'version.py')
    version_dict = {}
    with open(version_file) as f:
        exec(f.read(), version_dict)

    version = (
        f"{version_dict['VERSION_MAJOR']}."
        f"{version_dict['VERSION_MINOR']}."
        f"{version_dict['VERSION_BUILD']}"
    )
    if version_dict.get('VERSION_ALPHA', 0) != 0:
        version += f"a{version_dict['VERSION_ALPHA']}"

    return version


def find_resource_files():
    """Find all locale files, audio files, and other resources"""
    resource_files = []
    base_dir = os.path.join(os.path.dirname(__file__), SKILL_PKG)

    for root, dirs, files in os.walk(base_dir):
        # Get relative path from package directory
        rel_dir = os.path.relpath(root, base_dir)

        # Find locale files (intent, dialog, vocab, etc.)
        if 'locale' in root:
            for file in files:
                if rel_dir == '.':
                    resource_files.append(file)
                else:
                    resource_files.append(os.path.join(rel_dir, file))

        # Find audio files
        for file in files:
            if file.endswith(('.mp3', '.wav', '.ogg')):
                if rel_dir == '.':
                    resource_files.append(file)
                else:
                    resource_files.append(os.path.join(rel_dir, file))

    return resource_files


# Read requirements
with open("requirements.txt", "r") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]


setup(
    name=f"ovos-skill-{SKILL_NAME}",
    version=get_version(),
    description="HeiHei Chicken voice assistant skill for OVOS - controls servo-based animatronic chicken",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url=f"https://github.com/{SKILL_AUTHOR}/{SKILL_NAME}-skill",
    author="Mitchell Malpartida",
    author_email="",
    license="Apache-2.0",
    packages=[SKILL_PKG],
    package_data={
        SKILL_PKG: find_resource_files()
    },
    include_package_data=True,
    install_requires=requirements,
    keywords="ovos skill mycroft voice assistant chicken robot animatronic",
    entry_points={
        "ovos.plugin.skill": PLUGIN_ENTRY_POINT
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Home Automation",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
)
