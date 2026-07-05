package com.example.nowtime;

import org.junit.jupiter.api.Test;

import java.time.Instant;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class NowControllerTest {

    @Test
    void testNowController() {
        EpochClient mockClient = instant -> 1234567890L;

        NowController controller = new NowController(mockClient);

        NowResponse response = controller.now();

        assertTrue(response.message().startsWith("now is "));
    }
}