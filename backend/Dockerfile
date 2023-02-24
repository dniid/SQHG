FROM eclipse-temurin:17-jdk-focal

WORKDIR /code

COPY . /code

RUN chmod +x mvnw && ./mvnw dependency:go-offline

EXPOSE 8080
STOPSIGNAL SIGINT

CMD ["./mvnw", "spring-boot:run"]
