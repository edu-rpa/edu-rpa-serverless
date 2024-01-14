FROM public.ecr.aws/lambda/python:3.9-rapid-x86_64

COPY requirements.txt ./
RUN python3.9 -m pip install -r requirements.txt -t .

RUN yum -y install mesa-libGL.x86_64

COPY . ./

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.upload_sample_document"]