# fetch-sre-take-home-assessment
A program to load a configuration file, perform health checks, monitor endpoints, and log cumulative availability percentages

If in IDE open this as "Preview" or in whatever view will allow for markdown.


<h2>Description</h2>
This python script loads a yaml configuration file, runs a health check on the endpoints passed to it, and returns the percentage of
service uptime.

<h2>Prerequisites</h2>
You can run this service on your machine or in a python venv, the prerequisite packages are in the requirements.txt file.


<h3>Python venv</h3>
Start a python virtual environment and use the requirements.txt to install necessary packages.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```





<h3>On Machine</h2>

```bash
pip install pyyaml requests
```

OR

```bash
pip install -r requirements.txt
```



<h2>Getting Started</h2>
To start the script, run the program with the configuration file name: 

```bash
python3 main.py config.yaml
```

You should see the log results printed within the terminal.


<h2>To exit the script </h2>
Press Ctrl^ C

<h2>Recent changes</h2>
<ul>
<li>Adding requirements.txt file.</li>
This was done to make installing additional packages necessary easier.
<li>Adding regexs' sub function to ensure port numbers are removed.</li>
This was done in accordance to the ask of ignoring port numbers when determining domain.
<li>Adding new function for validation of yaml file</li>
I added this because I noticed I was having trouble running the yaml file successfully because it was passing a string instead of an object.
The troubles were the necessary method and url in the request method and the lack of correct formats of requests in the yaml file.
<li>Adding additional check for elapsed time.</li>
This was done to account for endpoints responding in 500ms or less
</ul>

<h2>Resources Used</h2>
<ul>
<li>Python documentation</li>
<li>Yaml documentation</li>
<li>A few stackoverflow references</li>
<li>W3schools.com</li>
</ul>
