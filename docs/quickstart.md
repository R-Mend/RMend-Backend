# Quick Start

## Install MongoDB

Install MongoDB following their [documentation](https://docs.mongodb.com/manual/administration/install-community/) and verify that mongo was installed successfully.

```bash
mongo --version
```

Example Output:

```
db version v4.4.4
Build Info: {
    "version": "4.4.4",
    "gitVersion": "8db30a63db1a9d84bdcad0c83369623f708e0397",
    "modules": [],
    "allocator": "system",
    "environment": {
        "distarch": "x86_64",
        "target_arch": "x86_64"
    }
}
```

## Install Node and Node Dependencies

Install Node following their [documentation](https://nodejs.org/en/download/) and verify npm was install successfully.

```bash
npm --version
```

Example Output:
```
7.7.6
```

Install node dependencies

```bash
npm install
```

## Serving Routes

Test that all the routes are working properly with `npm run test`. The test should be successful but you may need to run `npm start` to initialize the MongoDB.

```bash
npm run test
```

Then, run the local server with `npm start`. You can then make requests to `http://localhost:3000`.

```bash
npm start
```
