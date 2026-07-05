package com.example.nowtime;

import org.junit.jupiter.api.Test;

import java.time.Instant;

import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

public class NowControllerTest {

    @Test
    void testNowEndpoint() {
        EpochClient mockClient = mock(EpochClient.class);

        when(mockClient.toEpoch(any(Instant.class)))
                .thenReturn(1234567890L);

        NowController controller = new NowController(mockClient);

        NowResponse response = controller.now();

        assertEquals("now is 1234567890", response.message());
    }
}