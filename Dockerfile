FROM ubuntu:22.04

# Environment variables
ENV SPARK_USER_HOME=/home/sparkuser
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV HOME=/home/sparkuser

# Set to root to install packages
USER root

# Install system packages and dependencies
RUN apt-get update && \
    apt-get install -y sudo net-tools nano && \
    apt-get install -y openjdk-11-jdk && \
    update-alternatives --install /usr/bin/java java $JAVA_HOME/bin/java 100 && \
    update-alternatives --install /usr/bin/javac javac $JAVA_HOME/bin/javac 100 && \
    apt-get install -y python3 python3-pip python3-venv && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Create a user and set password
RUN useradd -m -s /bin/bash sparkuser && \
    echo "sparkuser:Arv@806" | chpasswd

# Give passwordless sudo access to the user
RUN echo 'sparkuser ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Switch to new user
USER sparkuser

# Set working directory
WORKDIR /home/sparkuser

# Create Python virtual environment
RUN python3 -m venv $SPARK_USER_HOME/venv

# Default command
CMD ["su", "-", "sparkuser"]