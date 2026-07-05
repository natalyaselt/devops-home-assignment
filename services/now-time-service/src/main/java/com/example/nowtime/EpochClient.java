    package com.example.nowtime;

    import org.springframework.http.MediaType;
    import org.springframework.stereotype.Component;
    import org.springframework.web.client.RestClient;

    import java.time.Instant;

    @Component
    public class EpochClient {

        private final RestClient restClient;

        public EpochClient(RestClient epochRestClient) {
            this.restClient = epochRestClient;
        }

        /**
         * Calls POST /epoch with the given instant and returns the epoch seconds
         * reported by the external service.
         */
        public long toEpoch(Instant instant) {
            EpochResponse response = restClient.post()
                    .uri("/epoch")
                    .contentType(MediaType.APPLICATION_JSON)
                    .body(new EpochRequest(instant.toString()))
                    .retrieve()
                    .body(EpochResponse.class);

            if (response == null) {
                throw new IllegalStateException("Empty response from epoch service");
            }
            return response.epoch();
        }
    }
