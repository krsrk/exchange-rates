# exchange-rates Repo
Exchange rates values in USD-MXN fixes

## Requirements

- Docker
- Docker Compose

## Instalation

1.- Clonning the repo: 

```bash
$ git clone https://github.com/krsrk/exchange-rates.git
``` 

2.- Change dir to the clonning repo:

```bash
$ cd exchange-rates
``` 

3.- Make the database dir:

```bash
$ mkdir data && cd data && mkdir mariadb
```


4.- Build services images:

```bash
$ docker-compose build
``` 

5.- Deploy the services:

```bash
$ docker-compose up -d
``` 


## Backend

6.- Deploying the web server:

```bash
$ docker-compose exec api uvicorn main:app --reload --port 8889 --host 0.0.0.0
``` 

The option **--reload** reloads the server when any changes in the code base is saved. This option is only used in Development.

## Database
If you need to visualize the data in your IDE, just configure this database params:
* HOST: localhost
* PORT: 8891
* USER: root
* PASS: root

## Testing(Unit Test)

If you want to run the app tests, run:

```bash
$ docker-compose exec api pytest
```
## Workflow

- You must deploy your local environment to manual test the endpoints.
- We recomend software like: Insomnia or Postman; to test the endpoints.

1.- Register a user

```bash
http://localhost:8889/auth/register

Body JSON:
{
  username: "myusername",
  password: "mypass"
}

Method: POST
```
2.- Login

```bash
http://localhost:8889/auth/login

Body JSON:
{
  username: "myusername",
  password: "mypass"
}

Method: POST
```
3.- Copy the token from the Login request

4.- Configure the request with Header: Authroization - Bearer Token; paste the token in the value of the Bearer.

5.- Send the request:

```bash
http://localhost:8889/exchange/rates

Header authorization:
Bearer [login token]

Method: PUT
```



## Troubleshotting

### Limited base free plan on Fixer.io service
For the free plan only accepts the "EUR" base in the request, due to this issue we calculated the USD-MX fix value with these formula:

```bash
MXN EUR fix value / USD EUR fix value
```

https://github.com/krsrk/exchange-rates/blob/05ac838075685d66687b8200fd3984b73cdb10b7/src/api/services/exchange_rate_services.py#L29


### Limited free plan on Fixer.io service
The fixer.io api is has limited monthly request in free plan, due to this feature the fix will return value 0 in the fix value. If you want to test or see the real fix value, you must register a new account in the fixer.io, generate the access token and change the value in the service provider:

https://github.com/krsrk/exchange-rates/blob/05ac838075685d66687b8200fd3984b73cdb10b7/src/api/services/exchange_rate_services.py#L9



