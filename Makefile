build:
	@docker build -t quakelogparser .

run: build
	@docker run -it --rm quakelogparser \
		python quake_log_parser database init && \
		poetry run python quake_log_parser source add-url https://gist.githubusercontent.com/cloudwalk-tests/be1b636e58abff14088c8b5309f575d8/raw/df6ef4a9c0b326ce3760233ef24ae8bfa8e33940/qgames.log && \
		poetry run python quake_log_parser ingestion pull && \
		poetry run python quake_log_parser ingestion run && \
		poetry run python quake_log_parser report player-ranking > player-ranking-output.json

test: build
	@docker run -it --rm quakelogparser pytest .
