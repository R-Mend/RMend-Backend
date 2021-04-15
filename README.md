# RMend-Backend
> RMend backend it the manager for sending data to both the RMend website and mobile app.

RMend-Backend is the backend API for the RMend SaaS. Its goal is to be able to manage reports for multiple county road departments/goverment counsels that come in from citizens and employess of the county.


## Usage example

A typical example for how the RMend backend works involves...
1. Getting a requrest from either the mobile or web application for local reports
2. Searching the database using a geospacial query with the given lattidude and longittude
3. Respond to the request with the reports locaed 5 miles away from the requested user.

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
