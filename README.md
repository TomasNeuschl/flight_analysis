Flight analysis
===========
is mini application to analyze flight data of drones.
## How to run
1. Clone the repository
2. Run 'docer-compose build' in the root directory
2. Run `docker-compose up` in the root directory
3. Open `http://localhost:8000/admin` in your browser
4. login with user `User` adn password `password`
5. Run `docker-compose down` in the root directory to stop the service

Don't miss `Flight analysis` button on the flight detail page. it will redirect you to the streamlit application where you can analyze the flight data.



## Documentation
Documentation is available at `http://localhost:8000/schema/swagger-ui/` when the service is running.
table of used technologies:

| Technology     | Description |
|----------------| --- |
| Python 3.10    | Python is an interpreted, high-level and general-purpose programming language. |
| Docker         | Docker is a set of platform as a service products that use OS-level virtualization to deliver software in packages called containers. |
| Docker-compose | Compose is a tool for defining and running multi-container Docker applications. |
| poetry         | Poetry is a tool for dependency management and packaging in Python. |
| Streamlit      | Streamlit is an open-source Python library that allows users to create interactive web applications for data science and machine learning projects with ease. |
| InfluxDB       | InfluxDB is a time-series database designed to handle high volumes of timestamped data, commonly used for storing, querying, and visualizing metrics and events in real-time applications. |
| SQLite         | SQLite is a lightweight relational database designed for embedded systems and small to medium-sized applications. |

## Authors

* **Tomáš Neuschl**