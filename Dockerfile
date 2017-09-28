FROM python:3
COPY . /app
WORKDIR /app/src
RUN pip install -r requirements.txt \
  && ../patch_bootstrap3_datetime.sh
EXPOSE 8000
CMD ["gunicorn", "-b :8000", "Activities.wsgi"]

