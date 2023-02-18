# Testing CassandraDB Module

Testing CassandraDB module requires spinning up a docker container with Cassandra server, so later the data could be written to the database.

_Note: it is assumed that you operate in the module's root directory._

**1. Build weeve CassandraDB module docker image.**

Build the module's image by running:

```shell
docker build -t weevenetwork/cassandradb:latest . -f docker/Dockerfile
```

**2. Build setup docker image for CassandraDB server.**

This docker image will run shortly to initialize and setup CassandraDB server.

```shell
docker build -t cassandra-setup:latest . -f test/cassandra-setup/Dockerfile
```

**3. Terminal 1: Run `docker-compose.yaml`**

Open the first terminal window and run the `docker-compose.yml` file and give it 1-2 minutes to set up everything.

```shell
cd test && docker compose up && cd ../..
```

Docker compose script will create a docker network `manual-test` with CassandraDB server image, setup script image and weeve CassandraDB module image.

It will pull `cassandra:latest` docker image that will serve as CassandraDB server. It will be run with host `cassandra` and port `9042`.

Later, it will run our setup image with the script that will create keyspace `testing` and table `temp_data` in Cassandra database with columns: `measurement_id int PRIMARY KEY`, `temperature double`, `location text`. Finally, it will insert three sample data rows:

| measurement_id | temperature | location  |
| -------------- | ----------- | --------- |
| 0              | 2.4         | Frankfurt |
| 1              | 3.7         | Frankfurt |
| 2              | 1.0         | Frankfurt |

Lastly, it will start the module image.

_IMPORTANT!!!_
_If at any point `cassandra-setup` or `weeve-cassandradb` containers don't run or crash (`Excited with code 1`), then wait a bit and restart the containers manually as probably Cassandra server container needed a little bit more time to spin._

**4. Terminal 2: Access Cassandra server database.**

Open the second terminal window and run the following command to open an extra panel to access Cassandra:

```shell
docker run --rm -it --network test_default nuvo/docker-cqlsh cqlsh cassandra 9042 --cqlversion='3.4.6'
```

You can view the above initially inserted sample data by running:

```shell
SELECT * FROM testing.temp_data;
```

**5. Terminal 3: Test weeve CassandraDB module by sending sample data.**

With this setup, the module will expect data in the format similar to:

```json
{
    "measurement_id": 3,
    "filterTemp": 3.6,
    "sensorLocation": "Berlin"
}
```

The module runs on `http://0.0.0.0:80/` and you can send data from the terminal:

```shell
curl -X POST http://0.0.0.0:80/ \
   -H 'Content-Type: application/json' \
   -d '{"measurement_id":3,"filterTemp":3.6,"sensorLocation":"Berlin"}'
```

You should see a response `OK - data accepted`.

After you look up the status of Cassandra server (`SELECT * FROM testing.temp_data;`), you should see the data:

| measurement_id | temperature | location  |
| -------------- | ----------- | --------- |
| 0              | 2.4         | Frankfurt |
| 1              | 3.7         | Frankfurt |
| 2              | 1.0         | Frankfurt |
| 3              | 3.6         | Berlin    |

**6. Sending a bunch of data.**

The module also works with a list of json data like:

```json
[
    {
        "measurement_id": 3,
        "filterTemp": 3.6,
        "sensorLocation": "Berlin"
    },
    {
        "measurement_id": 4,
        "filterTemp": 3.4,
        "sensorLocation": "Berlin"
    },
    {
        "measurement_id": 5,
        "filterTemp": 4.1,
        "sensorLocation": "Berlin"
    }
]
```

