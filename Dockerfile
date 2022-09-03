FROM python:3.10-slim

#Set the working directory
WORKDIR /usr/src/app

#copy all the files
RUN mkdir github_notifications_cleaner
COPY github_notifications_cleaner github_notifications_cleaner
ADD pyproject.toml .

RUN python -m pip install .
RUN rm -rf /usr/src/app
#Run the command
CMD [ "github-notifications-cleaner"]