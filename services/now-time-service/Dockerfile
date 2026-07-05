# -------- Build stage --------
FROM gradle:8.14.3-jdk21 AS builder

WORKDIR /app

# Copy everything
COPY . .

# Build Spring Boot jar
RUN gradle clean bootJar -x test

# -------- Runtime stage --------
FROM eclipse-temurin:21-jre

WORKDIR /app

# Copy built jar from builder stage
COPY --from=builder /app/build/libs/*.jar app.jar

EXPOSE 8080

# Run application
CMD ["java", "-jar", "app.jar"]