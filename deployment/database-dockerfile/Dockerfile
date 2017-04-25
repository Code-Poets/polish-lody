FROM postgres:9.6.2

#Install Cron
RUN apt-get update
RUN apt-get -y install cron
RUN apt-get -y install nano

# Add crontab file in the cron directory
ADD simple-cron /etc/cron.d/
RUN crontab /etc/cron.d/simple-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/simple-cron

ADD backup_daily.sh /
RUN chmod +x /backup_daily.sh

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

VOLUME /backups

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log