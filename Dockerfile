FROM python:3

# PYTHONUNBUFFERED disables buffering for python code
# SECRET_KEY doesn't matter since it's used only for collectstatic
ENV PYTHONUNBUFFERED=1 \
    SECRET_KEY=derpy_key

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
RUN /code/manage.py collectstatic --clear --link --no-input