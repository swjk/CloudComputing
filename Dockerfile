FROM alpine:latest
# Set the working directory to /app
RUN apk add bash
WORKDIR /wdirapp

# Copy the current directory contents into the container at /app
COPY . /wdirapp

# Install any needed packages specified in requirements.txt
RUN apk add --update python python-dev py-pip
RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install boto3
RUN pip install Pillow
# Make port 80 available to the world outside this container
EXPOSE 80
# Define environment variable
ENV NAME World
VOLUME /wdirapp/app/vol1 
# Run app.py when the container launches
CMD ["python", "-u", "setup.py"]
