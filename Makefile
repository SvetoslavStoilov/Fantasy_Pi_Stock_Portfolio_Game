build:
	sudo rm -rf data
	mkdir data
	sudo rm -rf data_jenkins
	mkdir data_jenkins
	sudo chown 1000 data_jenkins
	docker stop fantasy_pi_db_c1 || true
	docker rm fantasy_pi_db_c1 || true
	docker rmi fantasy_pi_db || true
	docker stop fantasy_pi_jenkins_c1 || true
	docker rm fantasy_pi_jenkins_c1 || true
	docker rmi fantasy_pi_jenkins || true
	docker stop fantasy_pi_app_c1 || true
	docker rm fantasy_pi_app_c1 || true
	docker rmi fantasy_pi_app || true
	docker-compose up
	sleep 2

up:
	docker stop fantasy_pi_db_c1 || true
	docker stop fantasy_pi_jenkins_c1 || true
	docker stop fantasy_pi_app_c1 || true
	docker-compose up
	sleep 2



.PHONY: build up 
