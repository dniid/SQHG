FROM eclipse-temurin:17-jdk-focal

WORKDIR /code

COPY .mvn/ .mvn
COPY mvnw pom.xml ./
RUN ./mvnw dependency:go-offline

COPY src ./src

EXPOSE 8080
STOPSIGNAL SIGINT

CMD ["./mvnw", "spring-boot:run"]