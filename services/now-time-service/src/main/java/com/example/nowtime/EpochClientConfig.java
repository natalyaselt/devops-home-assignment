package com.example.nowtime;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.web.client.RestClient;

@Configuration
public class EpochClientConfig {

    /**
     * RestClient pointed at the external epoch service.
     * The base URL comes from the {@code epoch.base-url} property
     * (overridable with the EPOCH_BASEURL environment variable).
     */
    @Bean
    public RestClient epochRestClient(@Value("${epoch.base-url}") String baseUrl) {
        var factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(5000);
        factory.setReadTimeout(5000);
        // Buffer the body so a Content-Length header is sent instead of chunked
        // streaming; many servers (and our mock) expect Content-Length.
        factory.setOutputStreaming(false);

        return RestClient.builder()
                .baseUrl(baseUrl)
                .requestFactory(factory)
                .build();
    }
}
