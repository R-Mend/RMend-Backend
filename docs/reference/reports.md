# Reports

## List all reports

Lists all the reports currently in the database. Anyone can access this route.

`GET` /reports

#### Parameters

| Name        | Type   | In   | Description  |
| ----------- | -----  | ---  | ------------ |
| none        |        |      |              |


## Get a single report

Gets the data for a single report. Anyone can access this route.

`GET` /reports/:reportId

#### Parameters

| Name        | Type   | In   | Description  |
| ----------- | -----  | ---  | ------------ |
| reportId    | string | url  | unique identifier for the report |


## Create a new report

Creates a new report to the store. Anyone can access this route.

`POST` /reports/new

#### Parameters

| Name        | Type   | In   | Description  |
| ----------- | -----  | ---  | ------------ |
| title       | string | body | indicator for the reports general-purpose |
| details     | string | body | a detailed description of the report |


## Update a report

Updates a report's fields. Only authenticated users can access this route and only the reports creator can update it.

`PUT` /reports/:reportId

#### Parameters

| Name        | Type   | In   | Description  |
| ----------- | -----  | ---  | ------------ |
| reportId    | string | url  | unique identifier for the report |
| title       | string | body | indicator for the reports general-purpose |
| details     | string | body | a detailed description of the report |


## Delete a single report

Deletes a specific report based on the given report id. Only authenticated users can access this route and only a report's creators can delete it.

`DELETE` /reports/:reportId

#### Parameters

| Name        | Type   | In   | Description  |
| ----------- | -----  | ---  | ------------ |
| reportId    | string | url  | unique identifier for the report |