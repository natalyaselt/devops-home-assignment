package com.example.nowtime;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.Instant;

@RestController
public class NowController {

    private final EpochClient epochClient;

    public NowController(EpochClient epochClient) {
        this.epochClient = epochClient;
    }

    @GetMapping("/now")
    public NowResponse now() {
        Instant now = Instant.now();
        long epoch = epochClient.toEpoch(now);
        return new NowResponse("now is " + epoch);
    }
}
