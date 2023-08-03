# Synthetic Traffic Demand Generation Model

This repository contains the code to create a synthetic population for a theoretical city. The code takes in configurations about zones and other city parameters to produce nodes, links, as well as a synthetic population. The final output of the code is in MATSIM configuration formatting of network and agent data to run a traffic simulation on.

#### Table of Contents
1. [ Install ](#install)
2. [ Introduction ](#introduction)
3. [ Usage ](#usage)
4. [ Conclusion ](#conclusion)
5. [ License ](#license)

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

## Introduction

Before one starts experimenting and analyzing the cities generated from this simulation, it is important to understand how and why the program works. To assist with this, the related paper of this research and the related presentation can be built with Latex. To complete the following steps, you must first insure that [LaTeX](https://www.latex-project.org/) is installed on your computer. Also confirm that you have [latexmk](https://mg.readthedocs.io/latexmk.html) installed to make the presentation.

#### Paper 

To build the paper first change directories into the `paper/` folder 

```bash
cd paper/
```

Next, you can make the paper with a simple command:

```bash
pdflatex paper.tex
```

#### Presentation 

To build the presentation, change directories into the `presentation/` folder from your original repository 

```bash
cd presentation/
```

Next, you can make the presentation and clean your repository with the following commands:

```bash
latexmk -xelatex presentation.tex
latexmk -c
```

## Usage

Before the code can be used, the configuration file `config.json` should be modified to your preferences.

#### Important Terms

The following configurations will use some terms that are defined below:

* `home` represents one housing entity, such as a room in an apartment or one residential house defined by the characteristics in the configuration file
* `houseEquivalence` is the number of homes that exist within one building of a zone
* `timeList` is a **list of floats** with the first float as the start time and the second float is the end time both in 24 hours format

#### Seeds

The seeds part of the configuration file is there to allow the user to make reproducable results. Everytime the program is run, the utilized seeds are outputted, so if a user had not set the seeds, then they can copy the printed numbers into the config file to get the same results again. The following seeds can be changed:

* `zones` defines the seed for the zoning layout
* `nodes` defines the seed for the network and building layout within the zones
* `agents` defines the seed for the agent schedules and household structures within a city

#### City

The city is defined as a rectangular grid of zones containing nodes for buildings. You can define it with the base level key `city` in the json file with the following attributes:

* `xLength` defines the dimension of the city in the x direction; **integer**
* `yLength` defines the dimension of the city in the y direction; **integer**
* `workFromHomeRatio` defines the ratio of people that work from home compared to all people in the city; **float**
* `workFromZoneRatio` defines the ratio of people that work from the same zone they live in compared to all people in the city; **float**
* `homesWithCarsRatio` defines the ratio of homes that have atleast one car compared to all homes in the city; **float**
* `numCarsInHome` defines the range of cars in homes with cars as a uniform distribution; **list of integers**
* `workFromHomeTiming` defines the start and end timings of an individual that work from home in a 24 hour format; **timeList**

#### Links 

The links are the attributes of the road network in the city. You can define them with the base level key `links` in the json file with the following attributes:

* `numCentralHubs` defines the range of number of central hubs within a district as a uniform distribution; **list of integers**
* `meshingRatio` defines the number of extra roads to the road network ontop of the minimum spanning tree as the product of the meshingRatio and the number of existing roads; **float**
* `highways` defines the attributes of highways in the city; **dictionary**
    * `numLanes` is the uniform distribution of the number of lanes in highways; **list of integers**
    * `speedLimit` is the uniform distribution of the speed limits in highways; **list of integers**
    * `capactiy` is the uniform distribution of the estimated capacity of highways in vehicles per hour; **list of integers**
* `districtRoads` defines the attributes of district roads in the city with the same dictionary attributes as highways; **dictionary**

#### Zones

The zones are defined in the json file under the base level key `zones` and each zone is keyed by it's name. Under each zone are the following attributes:

* `buildingArea` is the average area that one building in the zone takes up; **float**
* `landAreaRatio` is the ratio of the total land that is used up by this zone. All ratios must add up to 1; **float**
* `buildingTypes` is a list of types of activities that occur in the buildings of this zone. These can include `housing`, `work`, and `leisure`; **list of strings**
* `subZones` is a list of subzones defined above in this top level zone; **list of strings**
* `maxBuildings` is the maximum number of buildings of a top level zone that can fit in one district; **integer**
* `maxWorkers` is a distribution of the maximum number of workers in the buildings of the city if `buildingTypes` includes `work`; **list of integers**
* `numResidents` is a distribution of the number of residents in one unit of `houseEquivalence`; **list of integers**
* `houseEquivalence` is the number of home units that fit in one building in this zone; **integer**
* `timings` is a dictionary of dictionaries that defines the timings for the different activities in the zone; **dictionary**
    * `work` or `leisure` can be the key to a sub-dictionary of `timings`; **string**
        * `time` is the standard timing of the activity in the zone; **timeList**
        * `peopleVariation` is the variation in hours amongst people to come to activity in a defined building; **float**
        * `normalTimeDistribution` is the standard deviation of buildings in the region from the standard `time` defined above; **float**
        * `averageDuration` is the average duration of a person in a `leisure` activity

#### Subzones 

The subzones are definition of non top level zones in the city that can be referenced later. They are defined under the top level key `subZones` as a dictionary. The subzones are defined similar to the zones with all of the values above with the following exceptions:

* `landAreaRatio` is not a property of subZones as it is used to determine the sizing of top level zones
* `subZones` is not a property of subZones, as the model only supports one level of hierarchy
* `maxBuildings` is not supported for subZones, as the property is only used to determine the size of districts

#### Run Simulation

After configuring the json file, the code can now be run with the following command from the directory of this repository:

```bash
python createCity.py
```

## Conclusion

The `createCity.py` script also executes the matsim simulation with the output data. All of the results of the simulation can be found in the `outputs/` directory. It is recommended to copy this output along with its configuration file into another folder with all prior tests. With all of this information, a wrapper script could theoretically be made that configures the `config.json` file and analyzes the differences in results. Furthermore, a genetic algorithm or some other machine learning model can be used to find a more optimal zoning structure for existing cities.

## License
This project uses a GNU General Public License v3. For more information, please look at the LICENSE file in this repository.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

___

![Neovim](https://img.shields.io/badge/NeoVim-%2357A143.svg?&style=for-the-badge&logo=neovim&logoColor=white)
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![JSON](https://img.shields.io/badge/json-5E5C5C?style=for-the-badge&logo=json&logoColor=white)
![Notion](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white)
[![Arch](https://img.shields.io/badge/Arch%20Linux-1793D1?logo=arch-linux&logoColor=fff&style=for-the-badge)](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

