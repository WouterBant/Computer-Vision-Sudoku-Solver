<h1 align="center">Computer Vision Sudoku Solver</h1>

## TODO

- Train NN to solve puzzles --> determine the accuracy

- GUI from image as well

## About
Utilizing computer vision to get Sudoku puzzles from images/pictures.

## Structure

* The code for the Deep Neural Networks and the network themselves can be found in [/models](models)
 
  * [/digit_classifier](models/digit_classifier.ipynb): contains the code to create and train the DNN to classify digits. For this the MNIST dataset was utilized.

  * [/classes](models/solve.ipynb): TODO: will contain code to create a DNN that can solve Sudoku's.

* All other code can be found in [/src](src):

  * [/analysis_util](src/analysis_util): contains a [cycle classifier](src/analysis_util/cylcle_classifier.py) and functions used for [plotting](src/analysis_util/visualize.py) and to get the [statistics](src/analysis_util/statistics.py) presented in the paper.

  * [/classes](src/classes): contains the [Q-learning](src/classes/Qlearning.py), [DQN](src/classes/DQN.py) and [regulator](src/classes/regulator.py) agents, as well as the [economic environment](src/classes/environment.py) and the [action](src/classes/action.py) class.

  * [/runs](src/runs): contains the analysis of different runs and shows the figures presented in the paper.

  * [algorithms.py](src/algorithms.py): contains the algorithms used to simulate episodes in the different settings discussed in the paper.


## Getting started
### Requirements

Install the dependencies with the following command:

```

pip install -r requirements.txt

```

Python 3.10.6 was used.

### Usage
Run the following command to open the GUI:

```

python main.py

```

## License
MIT