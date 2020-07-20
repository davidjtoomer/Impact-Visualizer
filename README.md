# Checking Your Version of Anaconda

The first thing you're going to want to do is check your version of the Anaconda distribution. You can check this by running the following command:

~~~
conda --version
~~~

If the version is 4.6 or higher, you can move to the next section. If not, upgrade your version of Anaconda by running the following command: 

~~~
conda update conda
~~~

or, if you'd rather upgrade to that specific version:

~~~
conda upgrade anaconda=4.6
~~~

# Activating the Virtual Environment

After you have upgraded your version of Anaconda, you can activate the conda environment for this program by running the following commands (**IMPORTANT:** make sure you are in the <code>impact-visualizer</code> directory, which contains the file <code>environment.yml</code>):

~~~
conda env create -f environment.yml
conda activate impact-visualizer
~~~

At this point, you should see a prefix in your terminal that looks something like <code>(impact-visualizer) username@device %</code>. This signifies that your virtual environment is working and you are using it currently.

Activating the environment should automatically install all but one of the necessary dependencies (SK-Learn). You can download this final dependency by running the following: 

~~~
conda install scikit-learn
~~~

Now that all of the dependencies are set up, you are ready to run the program!

# Running the Program

This program runs in Python 3.6 or higher, which was installed in the conda environment. In order to run the program, simply run the following command:

~~~
python main.py
~~~

A graphics window leading you through the program should display at this point.