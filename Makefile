FILE=requirements.txt
WITHOUT_DOCKER=docker-compose-without.yml
ONLY_DATABASE=docker-compose-database.yml

without-docker:
	apt-get install --reinstall libpq-dev;
	python3 -m venv env_project;
	env_project/bin/pip install -r $(FILE);

	docker-compose -f $(WITHOUT_DOCKER) up -d;

only-database:
	docker-compose -f $(ONLY_DATABASE) up -d;
