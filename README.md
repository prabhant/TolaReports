# TolaReports


Version : 0.2
This is the toldata automatic report generation app.The deployed app can be seen here : "https://tolareports.herokuapp.com/".
The app is in initial phase, to reccomend a feature please generate an issue.

## What's TolaReports
The goal of TolaReports is to reduce developers efforts in deploying a visual web application such that for a new dataset the only task required is Data wrangling and manipulation. The web app takes the input data and provides the interactive visuals to qery the data at the real time which in turn reduces developer's time required for making a new web app as well as the time required for the organisation to get the output. TolaReports is highly useful in case of rapid visualisation conditions in case of humanitarian causes.

## Features
1. Tolareports uses Dash and plotly for intective visualisations and web app deployment.
2. The current version of tolareports uses CSV file(can be replaced by JSON feed)
3. Tolareports can be deployed with 4 simple git commands

## Setup
We recommend using virtual environment for deployment
```$ git init        # initializes an empty git repo
$ virtualenv venv # creates a virtualenv called "venv"
$ source venv/bin/activate # uses the virtualenv
```

To deploy the app on heroku follow these instructions
```
$ heroku create my-dash-app # change my-dash-app to a unique name
$ git add . # add all files to git
$ git commit -m 'Initial app boilerplate'
$ git push heroku master # deploy code to heroku
$ heroku ps:scale web=1  # run the app with a 1 heroku "dyno"
```

See the detailed instructions here: https://dash.plot.ly/deployment
