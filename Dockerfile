FROM python:3.11-slim
WORKDIR /exam
#COPY dist/exam-0.0.1-py3-none-any.whl .
COPY . .
#RUN ["python","-m","pip","install","exam-0.0.1-py3-none-any.whl"]
RUN ["python","-m","pip","install","."]
ENTRYPOINT ["exam"]
