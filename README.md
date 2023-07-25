# Synthetic Traffic Demand Generation Model

This repository contains the code to create a synthetic population for a theoretical city. The code takes in configurations about zones and other city parameters to produce nodes, links, as well as a synthetic population. The final output of the code is in MATSIM configuration formatting of network and agent data to run a traffic simulation on.

#### Table of Contents
1. [ Install ](#install)
2. [ Usage ](#usage)
3. [ Conclusion ](#conclusion)
4. [ License ](#license)

## Install

Clone the repository into your computer with the following command:

```bash
git clone https://codeberg.org/Inventor853/synthetic-traffic-generation.git --depth 1
```

After creating the folder you `synthetic-traffic-generation` you will want to go into the repository to complete the installation:

```bash
cd synthetic-traffic-generation
```

Create a virtual environment for your working directory.

If not done so already, install `venv` with the package manager [ pip ](https://pypi.org/project/pip/).

```bash
pip install virtualenv
```

Use `venv` to create a virtual environment in the folder `venv`.

```bash
python -m venv venv
```

Source into your virtual environment with the following command; it may be different for different shells.

```bash
source venv/bin/activate
```

Use the package manager `pip` to install the required libraries.

```bash
pip install -r requirements.txt
```

Now, we need to install the MATSIM simulator. Follow the steps on [the example repository](https://github.com/matsim-org/matsim-example-project) to build the MATSIM executable file.

Once you have built the .jar file move the file to repository of the synthetic traffic generation model. Finally, rename the file to `matsim.jar`. If you cloned the matsim example project inside this repository, you can just use the following command to do this step:

```bash
mv matsim-example-project-0.0.1-SNAPSHOT.jar ../matsim.jar
```

## Usage

Before the code can be used, the configuration file `config.json` should be modified to your preferences.

#### City

The city is defined as a rectangular grid of zones containing nodes for buildings. You can define it with the base level key `city` in the json file with the following attributes:

* `xLength` defines the dimension of the city in the x direction; **integer**
* `yLength` defines the dimension of the city in the y direction; **integer**
* `pctWorkFromHome` defines the percentage of people that work from home; **float**

#### Zones 

The zones are defined in the json file under the base level key `zones` and each zone is keyed by it's name. Under each zone are the following attributes:

* `area` defines the average area of a single building in this zone; **integer**
* `landAreaPct` is a percentage of the total city's area that this zone takes up; all the percentages must add up to 100%; **float**
* `minBuildings` represents the minimum number of buildings in each area that is of the type of this zone; **integer**
* `color` is the color of the zone in the plotting of city at the end of the generation; **string**
* `type` is a list containing all the types of activities that can take place in this zone. This allows for hierarchical zoning by adding multiple types. These types include `housing`, `work`, and `leisure`; **string**
* `numWorkers` is the number of workers in each building of type 'working' or type 'leisure' zones; **integer**

#### Run Simulation

After configuring the json file, the code can now be run with the following command from the directory of this repository:

```bash
python createCity.py
```

## Conclusion

The `createCity.py` script also executes the matsim simulation with the output data. All of the results of the simulation can be found in the `outputs/` directory. With all of this information, a wrapper script could theoretically be made that configures the `config.json` file and analyzes the differences in results. Furthermore, a genetic algorithm or some other machine learning model can be used to find a more optimal zoning structure for existing cities.

## License
This project uses a GNU General Public License v3. For more information, please look at the LICENSE file in this repository.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

___

![Neovim](https://img.shields.io/badge/NeoVim-%2357A143.svg?&style=for-the-badge&logo=neovim&logoColor=white)
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![JSON](https://img.shields.io/badge/json-5E5C5C?style=for-the-badge&logo=json&logoColor=white)
![Notion](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white)
![Arch](https://img.shields.io/badge/Arch%20Linux-1793D1?logo=arch-linux&logoColor=fff&style=for-the-badge)

