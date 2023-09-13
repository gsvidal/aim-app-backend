<p align="center">
  <a href="https://www.gonzalovidal.dev/aim-app" rel="noopener">
    <img width=200px height=200px src="https://i.postimg.cc/ncFbrPCD/aim-logo-trans.png" alt="Aim App">
  </a>
</p>

<h1 align="center">Aim App</h1>
<a href="https://www.gonzalovidal.dev/aim-app">
  <img src="https://i.postimg.cc/zXdy7sHM/aim-app.gif" width="700">
</a> 
<h3>Live at: https://www.gonzalovidal.dev/aim-app</h3>

---

<h3 align="left">Description:</h3>
<p align="left"> With Aim App you will improve your FPS(First Person Shooter) games skills (Counter Strike, Valorant, Call of Duty, etc...)
</p>

## Tech Stack:

<img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/html5/html5-original-wordmark.svg" alt="html5 Logo" width="50" height="50"/><img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/css3/css3-original-wordmark.svg" alt="css3 Logo" width="50" height="50"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/javascript/javascript-original.svg" alt="Javascript Logo" width="50" height="50"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/typescript/typescript-original.svg" alt="Typescript Logo" width="50" height="50"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/react/react-original-wordmark.svg" alt="react Logo" width="50" height="50"/>
<img src="https://vitejs.dev/logo.svg" alt="Vite Logo" width="50" height="50"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/sass/sass-original.svg" alt="Sass Logo" width="50" height="50"/>
<img src="https://reactrouter.com/_brand/react-router-stacked-color.png" alt="react router Logo" width="90" height="50"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/python/python-original-wordmark.svg" alt="Python Logo" width="50" height="50"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/flask/flask-original-wordmark.svg" alt="Flask Logo" width="50" height="50"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/postgresql/postgresql-original-wordmark.svg" alt="Python Logo" width="50" height="50"/>
<img src="https://devopedia.org/images/article/152/3612.1549627952.png" alt="BEM Logo" width="50" height="50" />

## 📝 Table of Contents

- [About](#about)
- [Design Process](#design_process)
- [Video Demo](#video_demo)
- [Getting Started](#getting_started)
- [Installing](#installing)
- [Deployment](#deployment)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

This project is a fullstack React (TypeScript) - Flask (Python) application with a SQL (Postgres) database.
Users have to login and then can play 2 games: reaction time and aiming
They'll have a score and it will be saved.
Finally they can watch a positions table with players ranked depending on their scores.

## 💡 Design Process <a name = "design_process"></a>

My thought process started with:

Backend, I used Flask (Python). I used werkzeug library for password hash generation and flask_jwt_extended for token related matters, flask route decorators to handle the get and post HTTP requests for the diferent api routes.

For Databases I used sqlite3 in local, but for production I have to migrate to PosgreSql, for being a more reliable and robust option. Since both are relational Database Management Systems the migration was not that complicated.

Then for the Frontend part I picked the React library (for building the user interface) with TypeScript (for static typing) and Vite , Along with that I used React router for handling client side routing, adapters to connect back and front with models for data, custom hooks for forms, Sass for styling, semantic HTML and BEM Nomenclature.

## 🎥 Video demo <a name = "video_demo"></a>

The Aim App is pretty straightforward, but if you want to watch how it works you can find this [video demo](https://youtu.be/u3DSFnG-oLk)

## 🏁 Getting Started <a name = "getting_started"></a>

The project is currently live (to 12/09/23) you can find it [here](https://www.gonzalovidal.dev/aim-app)

But if you want to wan it local, these instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

## 💻 Installing <a name = "installing"></a>

A step by step series of examples that tell you how to get a development env running.

#### Prerequisites

Having installed:

- [Python](https://www.python.org/downloads/)

- [Postgres](https://www.postgresql.org/download/)

- Configure their environment variables in PATH

- An IDE (eg. [Visual Studio Code](https://code.visualstudio.com/))

### Requisites

Git clone the repo with:
HTTPS
https://github.com/gsvidal/aim-app-finalproject.git

or

SSH
git@github.com:gsvidal/aim-app-finalproject.git

### BACKEND:

Activate virtual environment for backend in:
./backend
then
`python -m venv .venv`
after that go to root directory
./backend/aim-server/app
and

run `pip install requirements.txt` to install all the libraries used in the project.

### DATABASE:

In: # Configure CS50 Library to use PostgreSQL database:
Replace db = SQL(f"postgresql://{db_username}:{db_password}@{db_host}/{db_name}")
with your database data
You have to have installed postgres

In the same directory run `flask run --reload` to start the development sever (similar to http://localhost:5000/)

### FRONTEND:

cd ./frontend
run `npm install`
then
run `npm run dev` to start the development server (similar to http://localhost:5173/aim-app/)

Change VITE_API_URL value to your backend development server url (after you flask run --reload it above)

## 🚀 Deployment <a name = "deployment"></a>

### BACKEND:

At render.com (As a web service)

### DATABASE:

At render.com (As a web PostgreSql DB)

### FRONTEND:

At github.com (As a github page: gh-pages)

## ✍️ Authors <a name = "authors"></a>

- [@gsvidal](https://github.com/gsvidal) - 3D (Design, Development and Deployment).

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- [Inspiration #1](https://humanbenchmark.com/)
- [Inspiration #2](https://aimlab.gg/)
