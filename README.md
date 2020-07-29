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

Now that all of the dependencies are set up, you are ready to run the program!

# Running the Program

This program runs in Python 3.6 or higher, which was installed in the conda environment. In order to run the program, simply execute the following command:

~~~
python app.py
~~~

After loading, your command line should display information that reads something like the following:

~~~
Dash is running on http://127.0.0.1:8050/

  Warning: This is a development server. Do not use app.run_server
  in production, use a production WSGI server like gunicorn instead.

  * Serving Flask app "app" (lazy loading)
  * Environment: production
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
  * Debug mode: on
~~~

This shows that the program is up and running on your computer. To see it in action, simply copy and paste the link in the first line (http://127.0.0.1:8050) into your favorite browser.

# Exiting the Program

Once you're done using the program, you can exit out of the app by first closing the browser tab. However, this won't fully turn off the server. To do this, go to your terminal, and type *Ctrl + c*, and you will have successfully ended the program. After this, you can run the following to deactivate the virtual environment:

~~~
conda deactivate
~~~