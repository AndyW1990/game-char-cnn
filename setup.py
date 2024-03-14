from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='game_char_cnn',
      version="0.0.1",
      description="CNN to detect wether video game character is protagonist or antagonist",
      license="AW Data Analytics",
      author="Andy Whitworth",
      author_email="",
      #url="https://github.com/AndyW1990/game-char-cnn,
      install_requires=requirements,
      packages=find_packages(),
      test_suite="tests",
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      zip_safe=False)