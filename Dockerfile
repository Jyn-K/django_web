FROM public.ecr.aws/docker/library/python:3.9-slim
RUN apt-get update \
	&& apt-get install -y \
    	default-libmysqlclient-dev \
   		build-essential \
    	pkg-config \
    && rm -rf /var/lib/apt/lists/* \
	&& python -m pip install --upgrade pip
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
WORKDIR /app/mysite
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
