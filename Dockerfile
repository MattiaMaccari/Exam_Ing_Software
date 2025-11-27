FROM python
WORKDIR /home/exam
COPY dist/exam-0.0.1-py3-none-any.whl .
RUN ["python","-m","pip","install","exam-0.0.1-py3-none-any.whl"]
ENTRYPOINT ["exam"]