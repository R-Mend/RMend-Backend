# RMend-Backend
> RMend backend is the manager for sending data to both the RMend website and mobile app.

RMend-Backend is the backend API for the RMend SaaS. Its goal is to be able to manage reports for multiple county road departments/government counsels that come in from citizens and employees of the county.


## Usage example

A typical example of how the RMend backend works involves...
1. Getting a request from either the mobile or web application for local reports
2. Searching the database using a geospatial query with the given latitude and longitude
3. Respond to the request with the reports located 5 miles away from the requested user.

## Development setup

```sh
docker-compose up
docker exec -it <container_id> python manage.py test
```

## Meta

Tanner York

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/R-Mend](https://github.com/R-Mend)

## Contributing

1. Fork it (https://github.com/R-Mend/RMend-Backend)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
