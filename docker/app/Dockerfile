# Use Ubuntu 20.04
FROM ubuntu:20.04

# User must give the GitHub token
ARG GITHUB_TOKEN

# Update package lists and install needed software
RUN apt-get update \
    && apt-get install --no-install-recommends --yes locales python3.8 python3-pip \
    && apt-get install --no-install-recommends --yes curl lynx nano vim \
    && apt-get clean all \
    && pip3 install pipenv

# Generate and set locales
RUN locale-gen en_US.UTF-8 fi_FI.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Create directory for the project and set it as the work directory
RUN mkdir -p /webapp/eventshuffle
WORKDIR /webapp/eventshuffle

# Create eventsfl user and set permissions
# Group and user id is set to 1000, because usually that's the GID and UID
# on developers machine, too
# Home dir is created, because pipenv needs it
# --no-log-init is used to avoid adding user to the lastlog and faillog databases
RUN groupadd --gid 1000 --system eventsfl && \
    useradd --uid 1000 --no-log-init --system --home-dir /home/eventsfl --gid eventsfl eventsfl && \
    mkdir -p /home/eventsfl && \
    chown eventsfl:eventsfl /home/eventsfl && \
    chmod -R 740 /home/eventsfl && \
    chown eventsfl:eventsfl /webapp/eventshuffle && \
    chmod -R 740 /webapp/eventshuffle

USER eventsfl

# Copy project codes from GitHub and set these files to /webapp/eventshuffle
RUN curl -H "Authorization: token ${GITHUB_TOKEN}" -L https://api.github.com/repos/spexii/eventshuffle/tarball/main -o /tmp/eventshuffle.tar.gz && \
    tar -C /tmp -xf /tmp/eventshuffle.tar.gz && \
    mv /tmp/spexii-eventshuffle-*/* /webapp/eventshuffle && \
    rm /tmp/eventshuffle.tar.gz

# Copy the settings file for production with the ownership of eventsfl
# By default COPY command copies as root
COPY --chown=eventsfl:eventsfl settings.py /webapp/eventshuffle/eventshuffle/settings.py

# Install python environment
RUN pipenv install

# Switch back to user root
USER root

# Copy and run finalize-environment.sh script
COPY finalize-environment.sh /tmp
RUN chmod +x /tmp/finalize-environment.sh && \
    /tmp/finalize-environment.sh && \
    rm /tmp/finalize-environment.sh

EXPOSE 8000

CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
