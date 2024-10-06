
# LABELS
LABEL maintainer="Vitor Campos <vitorh45@gmail.com>"
LABEL application="wishlist"
LABEL repository="wishilist.git"

# Copy project main folder
COPY src/app src/app
COPY src/migrations src/migrations
COPY src/wsgi.py src/wsgi.py

# Testing stage
FROM base AS testing

# Install testing packages (customize according to this application)
# Note: Do not put any lib here except for testing.
#       These libs will only be installed in the test container
RUN pip install coverage freezegun mock pytest pytest-cov pytest-mock requests-mock mixer moto==4.1.9 --no-cache-dir

# Run tests
COPY src/tests src/tests
COPY src/migrations migrations

ENV WISHLIST_DEPLOY_ENV='Testing'

RUN coverage run -m pytest src/tests/ -vvs --junitxml=/report.xml
RUN coverage xml -o /coverage.xml -i

# Final stage
FROM base AS final

RUN mv src/app app
RUN mv src/migrations migrations
RUN mv src/wsgi.py wsgi.py

COPY --from=testing /coverage.xml /
COPY --from=testing /report.xml /

RUN mkdir -p app

## insert custom codes from application here

EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]
