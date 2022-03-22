# exchange-rates Repo
Exchange rates values in USD-MXN fixes

### Requirements

- Docker
- Docker Compose

### Instalation

1.- Clonning the repo: 

```bash
$ git clone https://github.com/krsrk/exchange-rates.git
``` 

2.- Change dir to the clonning repo:

```bash
$ cd exchange-rates
``` 

3.- Build services images:

```bash
$ docker-compose build
``` 

4.- Deploy the services:

```bash
$ docker-compose up -d
``` 


### Backend

5.- Deploying the web server:

```bash
$ docker-compose exec api uvicorn main:app --reload --port 8889 --host 0.0.0.0
``` 

The option **--reload** reloads the server when any changes in the code base is saved. This option is only used in Development.

#### Database
If you need to visualize the data in your IDE, just configure this database params:
* HOST: localhost
* PORT: 8891
* USER: root
* PASS: root

### Test

If you want to run the app test, run:

```bash
$ docker-compose exec api pytest
```


