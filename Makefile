IMAGE_NAME=buoy_boat_detector

install:
	pip install -r requirements.txt

run:
	python src/predict.py

build:
	docker build -t $(IMAGE_NAME) .


docker-run:
	xhost +local:docker
	docker run -it --rm \
		--device /dev/video0 \
		-e DISPLAY=$(DISPLAY) \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		$(IMAGE_NAME)

deploy: build docker-run

start: install run deploy