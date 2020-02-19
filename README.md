# mobile_coverage


1. Start the dev server for local development:
```bash
docker-compose up
```

2. Load data to from CSV file to postgres (can take few seconds)

```bash
docker exec -it mobile_coverage_web_1 python manage.py save_network_cov 
```

3. Go to browser and make some searches

Example request:
```
http://0.0.0.0:8000/api/v1/search?address=Paris
```

Enjoy!
