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
    public ResponseEntity<NowResponse> now() {
        try {
            Instant now = Instant.now();
            long epoch = epochClient.toEpoch(now);
            return ResponseEntity.ok(new NowResponse("now is " + epoch));
        } catch (Exception e) {
            return ResponseEntity.status(503)
                    .body(new NowResponse("epoch service unavailable"));
        }
    }
}
